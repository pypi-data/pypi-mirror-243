import logging
import os
import pathlib
import signal
import subprocess
import time
from contextlib import contextmanager

from .common import ModelArts, RankTableEnv

logger = logging.getLogger(__name__)


class FMK:
    def __init__(self, index, device):
        self.job_id = ModelArts.get_job_id()
        self.rank_id = device.rank_id
        self.device_id = str(index)

    def gen_env_for_fmk(self, rank_size):
        current_envs = os.environ.copy()

        current_envs["JOB_ID"] = self.job_id

        current_envs["ASCEND_DEVICE_ID"] = self.device_id
        current_envs["DEVICE_ID"] = self.device_id

        current_envs["RANK_ID"] = self.rank_id
        current_envs["RANK_SIZE"] = str(rank_size)

        FMK.set_env_if_not_exist(current_envs, RankTableEnv.HCCL_CONNECT_TIMEOUT, str(1800))

        log_dir = FMK.get_log_dir()
        process_log_path = os.path.join(log_dir, self.job_id, "ascend", "process_log", f"rank_{self.rank_id}")
        FMK.set_env_if_not_exist(current_envs, "ASCEND_PROCESS_LOG_PATH", process_log_path)
        pathlib.Path(current_envs["ASCEND_PROCESS_LOG_PATH"]).mkdir(parents=True, exist_ok=True)

        return current_envs

    @contextmanager
    def switch_directory(self, directory):
        owd = os.getcwd()
        try:
            os.chdir(directory)
            yield directory
        finally:
            os.chdir(owd)

    def get_working_dir(self):
        fmk_workspace_prefix = ModelArts.get_parent_working_dir()
        return os.path.join(os.path.normpath(fmk_workspace_prefix), f"device{self.device_id}")

    @staticmethod
    def get_log_dir():
        parent_path = os.getenv(ModelArts.MA_MOUNT_PATH_ENV)
        if parent_path:
            log_path = os.path.join(parent_path, "log")
            if os.path.exists(log_path):
                return log_path

        return ModelArts.TMP_LOG_DIR

    @staticmethod
    def set_env_if_not_exist(envs, env_name, env_value):
        if env_name in os.environ:
            logger.info(f"env already exists. env_name: {env_name}, env_value: {env_value}")
            return

        envs[env_name] = env_value

    def run(self, rank_size, command):
        envs = self.gen_env_for_fmk(rank_size)
        proc = f"proc-rank-{self.rank_id}-device-{self.device_id}"
        logger.info(f"bootstrap {proc}")

        log_dir = FMK.get_log_dir()
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = f"{self.job_id}-{proc}.txt"
        log_file_path = os.path.join(log_dir, log_file)

        # os.setsid: change the process(forked) group id to itself
        training_proc = subprocess.Popen(
            command,
            env=envs,
            preexec_fn=os.setsid,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        logger.info(f"{proc} (pid: {training_proc.pid})")
        # https://docs.python.org/3/library/subprocess.html#subprocess.Popen.wait
        subprocess.Popen(["tee", log_file_path], stdin=training_proc.stdout)

        return training_proc


class FMKManager:
    # max destroy time: ~20 (15 + 5)
    # ~ 15 (1 + 2 + 4 + 8)
    MAX_TEST_PROC_CNT = 4

    def __init__(self, instance):
        self.instance = instance
        self.fmk = []
        self.fmk_processes = []
        self.get_sigterm = False
        self.max_test_proc_cnt = FMKManager.MAX_TEST_PROC_CNT

    # break the monitor and destroy processes when get terminate signal
    def term_handle(func):
        def receive_term(signum, stack):
            logger.info(f"Received terminate signal {signum}, try to destroyed all processes")
            stack.f_locals["self"].get_sigterm = True

        def handle_func(self, *args, **kwargs):
            origin_handle = signal.getsignal(signal.SIGTERM)
            signal.signal(signal.SIGTERM, receive_term)
            res = func(self, *args, **kwargs)
            signal.signal(signal.SIGTERM, origin_handle)
            return res

        return handle_func

    def run(self, rank_size, command):
        for index, device in enumerate(self.instance.devices):
            fmk_instance = FMK(index, device)
            self.fmk.append(fmk_instance)
            self.fmk_processes.append(fmk_instance.run(rank_size, command))

    @term_handle
    def monitor(self, period=1):
        # busy waiting for all fmk processes exit by zero
        # or there is one process exit by non-zero

        fmk_cnt = len(self.fmk_processes)
        zero_ret_cnt = 0
        while zero_ret_cnt != fmk_cnt:
            zero_ret_cnt = 0
            for index in range(fmk_cnt):
                fmk = self.fmk[index]
                fmk_process = self.fmk_processes[index]
                if fmk_process.poll() is not None:
                    if fmk_process.returncode != 0:
                        proc = f"proc-rank-{fmk.rank_id}-device-{fmk.device_id} (pid: {fmk_process.pid})"
                        logger.error(f"{proc} has exited with non-zero code: {fmk_process.returncode}")
                        return fmk_process.returncode

                    zero_ret_cnt += 1
            if self.get_sigterm:
                break
            time.sleep(period)

        return 0

    def destroy(self, base_period=1):
        logger.info("Begin destroy training processes")
        self.send_sigterm_to_fmk_process()
        self.wait_fmk_process_end(base_period)
        logger.info("End destroy training processes")

    def send_sigterm_to_fmk_process(self):
        # send SIGTERM to fmk processes (and process group)
        for r_index in range(len(self.fmk_processes) - 1, -1, -1):
            fmk = self.fmk[r_index]
            fmk_process = self.fmk_processes[r_index]
            if fmk_process.poll() is not None:
                proc = f"proc-rank-{fmk.rank_id}-device-{fmk.device_id} (pid: {fmk_process.pid})"
                logger.info(f"{proc} has exited before receiving the term signal")
                del self.fmk_processes[r_index]
                del self.fmk[r_index]

            try:
                os.killpg(fmk_process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass

    def wait_fmk_process_end(self, base_period):
        test_cnt = 0
        period = base_period
        while len(self.fmk_processes) > 0 and test_cnt < self.max_test_proc_cnt:
            for r_index in range(len(self.fmk_processes) - 1, -1, -1):
                fmk = self.fmk[r_index]
                fmk_process = self.fmk_processes[r_index]
                if fmk_process.poll() is not None:
                    proc = f"proc-rank-{fmk.rank_id}-device-{fmk.device_id} (pid: {fmk_process.pid})"
                    logger.info(f"{proc} has exited")
                    del self.fmk_processes[r_index]
                    del self.fmk[r_index]
            if not self.fmk_processes:
                break

            time.sleep(period)
            period *= 2
            test_cnt += 1

        if len(self.fmk_processes) > 0:
            for r_index in range(len(self.fmk_processes) - 1, -1, -1):
                fmk = self.fmk[r_index]
                fmk_process = self.fmk_processes[r_index]
                if fmk_process.poll() is None:
                    proc = f"proc-rank-{fmk.rank_id}-device-{fmk.device_id} (pid: {fmk_process.pid})"
                    logger.warning(f"{proc} has not exited within the max waiting time, send kill signal")
                    os.killpg(fmk_process.pid, signal.SIGKILL)
