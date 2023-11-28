#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   NSRR 
@Time        :   2023/8/17 16:47
@Author      :   Xuesong Chen
@Description :   
"""
import os

import xmltodict
import pandas as pd

from wuji.Reader.Annotation.Base import Base
from wuji.Reader.utils import get_equal_duration_and_labeled_chunks
from datetime import datetime


class NSRRAnnotationReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)

    def _parse_file(self, file_path):
        with open(file_path, encoding='utf-8') as f:
            info_dict = xmltodict.parse(f.read())
            self.scored_events = pd.DataFrame(info_dict['PSGAnnotation']['ScoredEvents']['ScoredEvent'])
            date_string = self.scored_events.loc[0, 'ClockTime']
            fake_datetime = datetime.strptime('2000-01-01 ' + date_string.split(' ')[-1], '%Y-%m-%d %H.%M.%S')
            self.recording_start_time = fake_datetime
            self.duration = float(self.scored_events.loc[0, 'Duration'])
            self.scored_events[['Start', 'Duration']] = self.scored_events[['Start', 'Duration']].astype(float)
            self.scored_events = self.scored_events.iloc[1:]

    def get_standard_sleep_stages(self):
        stages = self.scored_events[self.scored_events['EventType'] == 'Stages|Stages'].copy()
        stages.loc[:, 'stage_num'] = stages['EventConcept'].str.split('|', expand=True)[1].astype(int)
        map_dic = {0: 'Wake', 1: 'N1', 2: 'N2', 3: 'N3', 4: 'N3', 5: 'REM'}
        stages.loc[:, 'Type'] = stages['stage_num'].map(map_dic)
        stages = stages[['Type', 'Start', 'Duration']]
        standard_stages = get_equal_duration_and_labeled_chunks(stages)
        self.sleep_stages = standard_stages
        return standard_stages

    def get_standard_AH_events(self, eps=5, type='AHI4'):
        if type == 'AHI4':
            self.get_OD_events(OD_level=4)
        elif type == 'AHI3':
            self.get_OD_events(OD_level=3)
            self.get_Arousal_events()
        if self.respiratory_events is None:
            self.get_respiratory_events()
        od_idx = 0
        self.respiratory_events['withOD'] = False
        self.respiratory_events.loc[self.respiratory_events['Type'] == 'Apnea', 'withOD'] = True
        for resp_idx, resp_row in self.respiratory_events[self.respiratory_events['Type'] == 'Hypopnea'].iterrows():
            resp_end_time = resp_row['Start'] + resp_row['Duration']
            for cur_idx, od_row in self.OD_events.loc[od_idx:].iterrows():
                od_end_time = od_row['Start'] + od_row['Duration']
                if abs(od_end_time - resp_end_time) <= eps or abs(resp_end_time - od_row['Start']) <= eps:
                    self.respiratory_events.loc[resp_idx, 'withOD'] = True
                    od_idx = cur_idx + 1
                    break
                elif od_row['Start'] > resp_end_time:
                    od_idx = cur_idx
                    break
        return self.respiratory_events[self.respiratory_events['withOD']]

    def get_respiratory_events(self):
        res = self.scored_events[(self.scored_events['EventConcept'] != 'Wake|0') &
                                 ((self.scored_events['EventConcept'].str.contains('pnea'))
                                  | (self.scored_events['EventConcept'] == 'Unsure|Unsure'))].copy()
        EventConcept_map = {
            'Hypopnea|Hypopnea': 'Hypopnea',
            'Obstructive apnea|Obstructive Apnea': 'Apnea',
            'Unsure|Unsure': 'Hyponpea',
            'Central apnea|Central Apnea': 'Apnea',
            'Mixed apnea|Mixed Apnea': 'Apnea',
        }
        res['Type'] = res['EventConcept'].map(EventConcept_map)
        assert res['Type'].isna().sum() == 0, f"存在未map的呼吸事件:{res['EventConcept'].unique()}"
        self.respiratory_events = res[['Type', 'Start', 'Duration']][(res['Duration'] >= 10) & (res['Duration'] <= 120)]
        self.respiratory_events.reset_index(drop=True, inplace=True)
        return self.respiratory_events

    def get_OD_events(self, OD_level=4):
        res = self.scored_events[(self.scored_events['EventConcept'] != 'Wake|0') &
                                 (self.scored_events['EventConcept'] == 'SpO2 desaturation|SpO2 desaturation')].copy()
        EventConcept_map = {
            'SpO2 desaturation|SpO2 desaturation': 'OD',
        }
        res['Type'] = res['EventConcept'].map(EventConcept_map)
        res['OD_level'] = res['SpO2Baseline'].astype(float) - res['SpO2Nadir'].astype(float)
        self.OD_events = res[['Type', 'Start', 'Duration', 'OD_level']][(res['OD_level'] >= OD_level)]
        self.OD_events.reset_index(drop=True, inplace=True)
        return self.OD_events

    def get_Arousal_events(self):
        res = self.scored_events[(self.scored_events['EventConcept'] != 'Wake|0') &
                                 (self.scored_events['EventConcept'] == 'Arousal|Arousal ()')].copy()
        EventConcept_map = {
            'Arousal|Arousal ()': 'Arousal',
        }
        res['Type'] = res['EventConcept'].map(EventConcept_map)
        self.Arousal_events = res[['Type', 'Start', 'Duration']]
        self.Arousal_events.reset_index(drop=True, inplace=True)
        return self.Arousal_events


if __name__ == '__main__':
    for file in os.listdir('/Users/cxs/project/OSAPillow/data/SHHS/annotations'):
        if file.endswith('.xml'):
            fp = os.path.join('/Users/cxs/project/OSAPillow/data/SHHS/annotations', file)
            reader = NSRRAnnotationReader(fp)
            # stages = reader.get_standard_sleep_stages()
            AH_events = reader.get_standard_AH_events()
            OD_events = reader.get_OD_events()
            print()
    # fp = '/Users/cxs/project/OSAPillow/data/SHHS/annotations/shhs1-200003-nsrr.xml'
    # reader = NSRRAnnotationReader(fp)
    # # stages = reader.get_standard_sleep_stages()
    # AH_events = reader.get_standard_AH_events()
    # print()
