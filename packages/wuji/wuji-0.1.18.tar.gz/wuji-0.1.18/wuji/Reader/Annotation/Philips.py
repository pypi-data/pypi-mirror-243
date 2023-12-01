#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   Phillip
@Time        :   2023/9/14 15:40
@Author      :   Xuesong Chen
@Description :
"""

import os
import glob
import time
import random

from wuji.Reader.utils import get_equal_duration_and_labeled_chunks
from wuji.Reader.Annotation.Base import Base
import pandas as pd
import xmltodict
from datetime import datetime


from wuji.Reader.utils import get_equal_duration_and_labeled_chunks
from wuji.Reader.Annotation.Base import Base
import pandas as pd
import xmltodict
from datetime import datetime

class PhilipsAnnotationReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)

    def _parse_file(self, file_path):
        f = open(file_path, encoding='utf-8')
        self.info_dict = xmltodict.parse(f.read())
        start_time_str = self.info_dict['PatientStudy']['Acquisition']['Sessions']['Session'][
            'RecordingStart']
        self.recording_start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
        self.duration = int(self.info_dict['PatientStudy']['Acquisition']['Sessions']['Session']['Duration'])

    def get_standard_sleep_stages(self, drop_not_scored=False, **kwargs):
        stages = self.get_sleep_stages()
        self.sleep_stages = get_equal_duration_and_labeled_chunks(stages, **kwargs)
        if drop_not_scored:
            self.sleep_stages = self.sleep_stages[self.sleep_stages['Type'].isin(['Wake', 'N1', 'N2', 'N3', 'REM'])]
        return self.sleep_stages

    def get_sleep_stages(self):
        stage_list = self.info_dict['PatientStudy']['ScoringData']['StagingData'][
            'UserStaging']['NeuroAdultAASMStaging']['Stage']
        stage_dic = {
            'Start': [int(i['@Start']) for i in stage_list],
            'Type': [i['@Type'] for i in stage_list],
        }
        stages = pd.DataFrame.from_dict(stage_dic)
        stages['Duration'] = stages['Start'].shift(-1) - stages['Start']
        stages.at[stages.index[-1], 'Duration'] = self.duration - stages['Start'].iloc[-1]
        map_dic = {
            'Wake': 'Wake', 'NonREM1': 'N1', 'NonREM2': 'N2',
            'NonREM3': 'N3', 'NonREM4': 'N3', 'REM': 'REM',
            'NotScored': 'NotScored'
        }
        stages.loc[:, 'Type'] = stages['Type'].map(map_dic)
        return stages

    def get_standard_AH_events(self):
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        resp_events_list = [i for i in events_list if i['@Family'] == 'Respiratory']
        # print('resp_events_list: ', resp_events_list)
        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'MixedApnea': 'Apnea',
            'CentralApnea': 'Apnea',
            'ObstructiveApnea': 'Apnea',
            'Hypopnea': 'Hypopnea',
        }
        for e in resp_events_list:
            if 10 <= float(e['@Duration']) <= 120:
                if e['@Type'] in ['PeriodicRespiration']:
                    continue
                type_list.append(map_dic[e['@Type']])
                start_list.append(float(e['@Start']))
                duration_list.append(float(e['@Duration']))
        respiratory_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }
        respiratory_events = pd.DataFrame.from_dict(respiratory_events_dic)
        self.respiratory_events = respiratory_events
        return respiratory_events

    # 返回 10 < float(e['@Duration']) < 120 的 所有Apnea, 和 只有'Machine' == 'true 的Hypopnea
    def get_standard_AH_events_H_with_machine(self):
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        resp_events_list = [i for i in events_list if i['@Family'] == 'Respiratory']

        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'MixedApnea': 'Apnea',
            'CentralApnea': 'Apnea',
            'ObstructiveApnea': 'Apnea',
            'Hypopnea': 'Hypopnea',
        }

        for e in resp_events_list:
            if 10 <= float(e['@Duration']) <= 120:
                if e['@Type'] in ['PeriodicRespiration']:
                    continue
                if e['@Type'] == 'Hypopnea' and e.get('@Machine') == 'true':
                    type_list.append(map_dic[e['@Type']])
                    start_list.append(float(e['@Start']))
                    duration_list.append(float(e['@Duration']))
                elif e['@Type'] in ['MixedApnea', 'CentralApnea', 'ObstructiveApnea']:
                    type_list.append(map_dic[e['@Type']])
                    start_list.append(float(e['@Start']))
                    duration_list.append(float(e['@Duration']))

        respiratory_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }

        respiratory_events = pd.DataFrame.from_dict(respiratory_events_dic)
        self.respiratory_events = respiratory_events
        return respiratory_events

    # 只返回 是Hypopnea 且 不是机器标注的数据
    def get_standard_AH_events_H_with_no_machine(self):
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        resp_events_list = [i for i in events_list if i['@Family'] == 'Respiratory']

        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'MixedApnea': 'Apnea',
            'CentralApnea': 'Apnea',
            'ObstructiveApnea': 'Apnea',
            'Hypopnea': 'Hypopnea',
        }

        for e in resp_events_list:
            if 10 <= float(e['@Duration']) <= 120:
                if e['@Type'] == 'Hypopnea' and e.get('@Machine') != 'true':
                    type_list.append(map_dic[e['@Type']])
                    start_list.append(float(e['@Start']))
                    duration_list.append(float(e['@Duration']))

        respiratory_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }

        respiratory_events = pd.DataFrame.from_dict(respiratory_events_dic)
        self.respiratory_events = respiratory_events
        return respiratory_events


    def get_OD_events(self, type='AHI3'): # 3 for 1A and 4 for 1B
        if type=='AHI3':
            threshold = 3
        elif type=='AHI4':
            threshold = 4
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        OD_events_list = [i for i in events_list if i['@Family'] == 'SpO2']
        # print('OD_events_list', OD_events_list)
        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'RelativeDesaturation': 'Desaturation',
            'AbsoluteDesaturation': 'Desaturation',
        }
        for e in OD_events_list:
            ODBefore = int(e.get('O2Before', 0))
            ODMin = int(e.get('O2Min', 0))

            # Add the condition: ODBefore minus ODMin should be greater than or equal to 4
            if ODBefore - ODMin >= threshold:
                type_list.append(map_dic[e['@Type']])
                start_list.append(float(e['@Start']))
                duration_list.append(float(e['@Duration']))

        OD_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }
        OD_events = pd.DataFrame.from_dict(OD_events_dic)
        self.OD_events = OD_events
        return OD_events

    # def get_O2_events(self):
    #     events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
    #     O2_events_list = [i for i in events_list if i['@Family'] == 'SpO2']
    #     print('O2_events_list', O2_events_list)
    #     type_list = []
    #     start_list = []
    #     duration_list = []
    #     map_dic = {
    #         'RelativeDesaturation': 'Desaturation',
    #         'AbsoluteDesaturation': 'Desaturation',
    #     }
    #     for e in O2_events_list:
    #         type_list.append(map_dic[e['@Type']])
    #         start_list.append(float(e['@Start']))
    #         duration_list.append(float(e['@Duration']))
    #     O2_events_dic = {
    #         'Type': type_list,
    #         'Start': start_list,
    #         'Duration': duration_list,
    #     }
    #     O2_events = pd.DataFrame.from_dict(O2_events_dic)
    #     self.O2_events = O2_events
    #     return O2_events

    def get_arousal_events(self):
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        Neuro_events_list = [i for i in events_list if i['@Family'] == 'Neuro']
        # print('Neuro_events_list', Neuro_events_list)
        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'Arousal': 'Arousal',
        }


        for e in Neuro_events_list:
            event_type = e['@Type']

            # Skip events with type 'REMSleepBehaviorDisorder'
            if event_type == 'REMSleepBehaviorDisorder':
                continue

            # Only include events with type 'Arousal'
            if event_type == 'Arousal':
                type_list.append(map_dic[event_type])
                start_list.append(float(e['@Start']))
                duration_list.append(float(e['@Duration']))

        Neuro_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }
        Neuro_events = pd.DataFrame.from_dict(Neuro_events_dic)
        self.Neuro_events = Neuro_events
        return Neuro_events

    def get_possible_machine_values(self):
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        resp_events_list = [i for i in events_list if i['@Family'] == 'Respiratory']

        machine_values = set()

        for e in resp_events_list:
            machine_value = e.get('@Machine')
            machine_values.add(machine_value)

        return machine_values

if __name__ == '__main__':
    fp = '/Volumes/Extreme SSD/parallel_data/00000720-LEBS21876_2621497/00000720-LEBS21876_2621497.rml'
    anno = PhilipsAnnotationReader(fp)
    res = anno.get_standard_sleep_stages()
    res = anno.get_standard_respiration_events()
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    anno.plot_sleep_stage(ax=ax)
    plt.show()
