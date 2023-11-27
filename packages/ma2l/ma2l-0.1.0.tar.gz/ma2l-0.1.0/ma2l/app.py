import logging
import os
import sys

from .common import RankTableEnv, setup_logger
from .fmk import FMKManager
from .rank_table import RankTable, RankTableTemplate1, RankTableTemplate2

logger = logging.getLogger(__name__)


def app():
    if len(sys.argv) <= 1:
        logger.error("Usage: ma2l YOUR_TRAINING_COMMAND")
        sys.exit(1)

    setup_logger(__package__)
    train_command = sys.argv[1:]
    logger.info(f"training command: {' '.join(train_command)}")

    if os.environ.get(RankTableEnv.RANK_TABLE_FILE_V1) is not None:
        # new format rank table file
        rank_table_path = os.environ.get(RankTableEnv.RANK_TABLE_FILE_V1)
        RankTable.wait_for_available(rank_table_path)
        rank_table = RankTableTemplate1(rank_table_path)
    else:
        # old format rank table file
        rank_table_path_origin = RankTableEnv.get_rank_table_template2_file_path()
        RankTable.wait_for_available(rank_table_path_origin)
        rank_table = RankTableTemplate2(rank_table_path_origin)

    if rank_table.get_device_num() >= 1:
        logger.info(f"set rank table {RankTableEnv.RANK_TABLE_FILE} env to {rank_table.get_rank_table_path()}")
        RankTableEnv.set_rank_table_env(rank_table.get_rank_table_path())
    else:
        logger.info(f"device num < 1, unset rank table {RankTableEnv.RANK_TABLE_FILE} env")
        RankTableEnv.unset_rank_table_env()

    instance = rank_table.get_current_instance()
    server = rank_table.get_server(instance.server_id)
    current_instance = RankTable.convert_server_to_instance(server)

    fmk_manager = FMKManager(current_instance)
    fmk_manager.run(rank_table.get_device_num(), train_command)
    return_code = fmk_manager.monitor()

    fmk_manager.destroy()

    sys.exit(return_code)


def main():
    app()
