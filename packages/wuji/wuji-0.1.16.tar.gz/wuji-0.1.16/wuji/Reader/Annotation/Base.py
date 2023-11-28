#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   AnnotationBase 
@Time        :   2023/8/17 16:21
@Author      :   Xuesong Chen
@Description :   
"""
from abc import ABC, abstractmethod
from wuji.Reader.utils import get_irequal_duration_chunks
import pandas as pd


class AHI:
    def __init__(self, respiratory_events, sleep_stages):
        self.total_sleep_time = sleep_stages[~sleep_stages['Type'].isin(['Wake', 'NotScored'])]['Duration'].sum()
        self.total_sleep_time_in_hours = self.total_sleep_time / 3600
        self.total_sleep_time_in_hours_REM = sleep_stages[sleep_stages['Type'].isin(['REM'])]['Duration'].sum() / 3600
        self.total_sleep_time_in_hours_NREM = sleep_stages[sleep_stages['Type'].isin(['N1', 'N2', 'N3'])][
                                                  'Duration'].sum() / 3600
        self.sleep_stages = get_irequal_duration_chunks(sleep_stages)
        self.respiratory_events = respiratory_events
        self.sleep_stages['End'] = self.sleep_stages['Start'] + self.sleep_stages['Duration']
        self.respiratory_events['End'] = self.respiratory_events['Start'] + self.respiratory_events['Duration']
        self._assign_sleep_stage_label_to_respiratory_events()

    def _assign_sleep_stage_label_to_respiratory_events(self):
        if not self.respiratory_events.empty:
            for idx, row in self.sleep_stages.iterrows():
                start_time = row['Start']
                end_time = row['End']
                self.respiratory_events.loc[
                    (self.respiratory_events['Start'] >= start_time) & (self.respiratory_events['End'] <= end_time),
                    'SleepStage'] = row['Type']
            sleep_stage_idx_cache = 0
            for resp_idx, resp_row in self.respiratory_events[self.respiratory_events['SleepStage'].isna()].iterrows():
                for sleep_stage_idx, sleep_stage_row in self.sleep_stages.loc[sleep_stage_idx_cache:].iterrows():
                    if resp_row['End'] > sleep_stage_row['End'] and resp_row['Start'] < sleep_stage_row['End']:
                        overlap_on_cur_stage = sleep_stage_row['End'] - resp_row['Start']
                        overlap_on_next_stage = resp_row['End'] - sleep_stage_row['End']
                        cur_event_stage = None
                        if overlap_on_cur_stage >= overlap_on_next_stage:
                            cur_event_stage = sleep_stage_row['Type']
                        else:
                            cur_event_stage = self.sleep_stages.loc[sleep_stage_idx + 1, 'Type']
                        self.respiratory_events.loc[resp_idx, 'SleepStage'] = cur_event_stage
                        sleep_stage_idx_cache = sleep_stage_idx
                        break
            assert self.respiratory_events['SleepStage'].isna().sum() == 0, "存在未标记的呼吸事件"

    def get_AHI(self, type='Total'):

        if self.respiratory_events.empty:
            return 0

        if type == 'Total':
            ahi = self.respiratory_events['SleepStage'].isin(
                ['N1', 'N2', 'N3', 'REM']).sum() / self.total_sleep_time_in_hours
        elif type == 'REM':
            ahi = self.respiratory_events['SleepStage'].isin(['REM']).sum() / self.total_sleep_time_in_hours_REM
        elif type == 'NREM':
            ahi = self.respiratory_events['SleepStage'].isin(
                ['N1', 'N2', 'N3']).sum() / self.total_sleep_time_in_hours_NREM
        else:
            raise ValueError("Invalid type. Must be 'Total', 'REM', or 'NREM'.")

        return ahi

    def get_AH_events_in_sleep(self):
        return self.respiratory_events[self.respiratory_events['SleepStage'].isin(['N1', 'N2', 'N3', 'REM'])]


class Base(ABC):
    def __init__(self, file_path):
        self.sleep_stages = None
        self.respiratory_events = None
        self.AH_events = None
        self.OD_events = None
        self._parse_file(file_path)

    @abstractmethod
    def _parse_file(self, file_path):
        self.recording_start_time = None
        self.duration = None
        self.anno_df = None

    def get_recording_start_time(self):
        return self.recording_start_time

    def get_duration(self):
        return self.duration

    def get_sleep_onset_time(self):
        if self.sleep_stages is None:
            self.sleep_stages = self.get_standard_sleep_stages()
        onset_time = self.sleep_stages[self.sleep_stages['Type'].isin(['N1', 'N2', 'N3', 'REM'])]['Start'].values[0]
        return onset_time

    def total_sleep_time(self):
        if self.sleep_stages is None:
            self.sleep_stages = self.get_standard_sleep_stages()
        total_sleep_time = self.sleep_stages[self.sleep_stages['Type'].isin(['N1', 'N2', 'N3', 'REM'])][
            'Duration'].sum()
        return total_sleep_time

    def get_standard_sleep_stages(self):
        '''
        用于获取标准的睡眠分期标记

        | Type | Start | Duration |
        |------|-------|----------|

        Type: Wake, N1, N2, N3, REM
        Start: 从睡眠开始到当前分期的时间
        Duration: 当前分期的持续时间，统一为30s

        :return:
        上述Dataframe格式
        '''
        return None

    def get_standard_AH_events(self):
        '''
        用于获取标准的睡眠分期标记

        | Type | Start | Duration |
        |------|-------|----------|

        Type: Apnea, Hypopnea
        Start: 从睡眠开始到当前事件的开始时间
        Duration: 当前事件的持续时间

        :return:
        上述Dataframe格式
        '''
        pass

    def plot_sleep_stage(self, ax=None):
        import matplotlib.pyplot as plt
        from matplotlib.dates import DateFormatter

        # 设置开始时间
        start_time = self.recording_start_time
        sleep_stage = self.get_standard_sleep_stages() if self.sleep_stages is None else self.sleep_stages

        # 按照指定的顺序更新类型映射
        type_order = ['N3', 'N2', 'N1', 'REM', 'Wake', 'NotScored']
        type_mapping = {type: i for i, type in enumerate(type_order)}
        # 创建颜色映射，根据每个类型的实际含义选择颜色
        color_mapping = {
            "N3": "darkblue",
            "N2": "purple",
            "N1": "blue",
            "REM": "green",
            "Wake": "lightblue",
            "NotScored": "grey"
        }

        sleep_stage['Start'] = pd.to_timedelta(sleep_stage['Start'], unit='s') + start_time
        sleep_stage['End'] = sleep_stage['Start'] + pd.to_timedelta(sleep_stage['Duration'], unit='s')

        # 创建图表
        if not ax:
            fig, ax = plt.subplots(figsize=(100, 5))

        prev_end = None
        prev_type = None
        for _, row in sleep_stage.iterrows():
            ax.barh(type_mapping[row['Type']], row['End'] - row['Start'], left=row['Start'], height=0.5,
                    align='center',
                    color=color_mapping[row['Type']])
            if prev_end is not None and prev_type is not None:
                ax.plot([prev_end, row['Start']], [type_mapping[prev_type], type_mapping[row['Type']]],
                        color='lightgrey')
            prev_end = row['End']
            prev_type = row['Type']

        # 设置y轴的标签
        ax.set_yticks(range(len(type_mapping)))
        ax.set_yticklabels(list(type_mapping.keys()))

        # 设置x轴的刻度标签为实际的小时和分钟
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
        # set x limits
        start_time = sleep_stage['Start'].values[0]
        end_time = sleep_stage['End'].values[-1]
        ax.set_xlim([start_time, end_time])
