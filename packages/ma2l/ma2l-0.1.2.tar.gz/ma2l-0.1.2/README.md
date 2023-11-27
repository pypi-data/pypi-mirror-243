# MindSpore with Ascend on ModelArts Launcher


<p align="center">
<a href="https://pypi.python.org/pypi/ma2l">
    <img src="https://img.shields.io/pypi/v/ma2l.svg" alt="Release Status">
</a>

<a href="https://github.com/geniuspatrick/ma2l/actions/workflows/dev.yml">
    <img src="https://github.com/geniuspatrick/ma2l/actions/workflows/dev.yml/badge.svg" alt="CI Status">
</a>

<a href="https://geniuspatrick.github.io/ma2l/">
    <img src="https://img.shields.io/website/https/geniuspatrick.github.io/ma2l/index.html.svg?label=docs&down_message=unavailable&up_message=available" alt="Documentation Status">
</a>

</p>


A simple and clean launcher helps you train deep model
using MindSpore with Ascend on ModelArts(ROMA or HuaweiCould),
no bells and whistles.

> [!NOTE]
> This project is a shameless wrapper of [scripts](https://support.huaweicloud.com/bestpractice-modelarts/develop-modelarts-0120.html) from HuaweiCloud, all credit goes to them.

## Installation

```shell
pip install ma2l
```

Or, you can get pre-released version from test.pypi.org

```shell
pip install -i https://test.pypi.org/simple/ ma2l
```

## Usage

Just submit the following command to your training job on cloud:

```shell
ma2l YOUR_TRAINING_COMMAND
```

For example, `YOUR_TRAINING_COMMAND` might be like:

```shell
python your_train_script.py \
    --arg1=value1 \
    --arg2=value2 \
    ...
```

See the difference between the commands on the local machine and on the cloud:

```diff
- python your_train_script.py \
+ ma2l python your_train_script.py \
    --arg1=value1 \
    --arg2=value2 \
    ...
```

> [!IMPORTANT]
> Don't forget to pass the argument that turns on distributed training to your training script, if it requires one.

## Features

- No need to change **a single line** of the training script.
- There's no need to set any distribution-related environment variables, and we'll take care of everything for you.
- Supports a variety of hardware settings:
  - single-node, single-npu
  - single-node, multi-npus
  - multi-node, multi-npus
- Modularity. Fully decoupled from your training code/repository.

## Philosophies

So, what happens under the hood?
After you have created a training job on ModelArts, the launcher does the following:

1. Generate HCCL configuration files on each node, typically named `rank_table.json`, which is necessary for distributed training.
2. Automatically start n processes on each node for `YOUR_TRAINING_COMMAND`, based on the settings when you created the job.
3. Set the environment variables for each process on each node, such as `RANK_TABLE_FILE`, `DEVICE_ID`, `RANK_ID`, etc.

Simple and Easy, right? You don't need to change any code to adapt training scripts from your local machine to the cloud,
and you don't need to struggle with environment variable settings on the local machine. Keep it in mind.

## FAQs

### What does `ma2l` mean?

`ma2l` is the abbreviation for **M**indSpore with **A**scend on **M**odel**A**rts **L**auncher.

## Credits

- [Genius Patrick](https://github.com/geniuspatrick)
- [Huawei Cloud](https://support.huaweicloud.com/bestpractice-modelarts/develop-modelarts-0118.html)
