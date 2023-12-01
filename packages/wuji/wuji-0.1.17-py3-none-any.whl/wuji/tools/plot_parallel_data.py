#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   plot_parallel_data 
@Time        :   2023/11/30 18:32
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib.pyplot as plt

def plot_multiple_datasets(*datasets, sampling_rates, labels):
    """
    Plots multiple datasets with different sampling rates but the same total duration.

    :param datasets: A variable number of datasets (arrays or lists of data points).
    :param sampling_rates: A list of sampling rates corresponding to each dataset.
    :param labels: A list of labels corresponding to each dataset.
    """
    # 创建一个图形和多个轴
    fig, axes = plt.subplots(len(datasets), 1, sharex=True, figsize=(10, 6))

    # 如果只有一个数据集，我们需要将axes数组化
    if len(datasets) == 1:
        axes = [axes]

    # 为每个数据集创建一个轴
    for i, data in enumerate(datasets):
        time_axis = [t / sampling_rates[i] for t in range(len(data))]
        axes[i].plot(time_axis, data)
        axes[i].set_ylabel(labels[i])

    # 设置x轴标签
    plt.xlabel('Time (s)')

    # 显示图表
    plt.show()
