from pathlib import Path
import sys
import numpy as np
import pandas as pd
import math

from PySide6.QtCore import QUrl, QObject, Property, Signal, Slot
from PySide6.QtCore import Qt, QPointF
from PySide6.QtCharts import QAbstractSeries
# from PySide6.QtCharts import QtCharts
from PySide6.QtCharts import QChart, QChartView, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PySide6.QtGui import QPen
from PySide6.QtCore import *

class TrendsUI(QAbstractListModel):

    name_role = Qt.UserRole + 1
    series_proc_role = Qt.UserRole + 2
    series_sim_role = Qt.UserRole + 3
    series_out_role = Qt.UserRole + 4
    color_role = Qt.UserRole + 5
    axis_min_role = Qt.UserRole + 6
    axis_max_role = Qt.UserRole + 7
    cur_val_proc_role = Qt.UserRole + 8
    cur_val_sim_role = Qt.UserRole + 9



    signal_series_changed = Signal(QSplineSeries, arguments=['series'])

    def __init__(self, df : pd.DataFrame):
        super().__init__()
        self.count = 0
        self.trend_df = df
        self.trends = []
        self.items = []
        self.tag_names = {
                        'Ore' : 'Разход на руда', 'WaterMill' : 'Вода в мелницата', 'WaterZumpf' : 'Вода в Зумпф',
                        'PressureHC' : 'Налягане на ХЦ', 'Power' : 'Мощност на електродв.','DensityHC' : 'Плътност на ХЦ',
                        'PulpHC' : 'Пулп към ХЦ', 'PumpRPM' : 'Обороти на помпа', 'MotorAmp' : 'Ток на електродв.',
                        'Grano' : 'Гранодиорити', 'Daiki' : 'Дайки', 'Shisti' : 'Шисти', 'Cidra200' : 'Сидра +200 мк.'
                        }
        self.feature_tags = [
                            'Ore', 'WaterZumpf', 'WaterMill', 'PressureHC', 'MotorAmp',
                            'DensityHC', 'PulpHC', 'PumpRPM',
                            # 'Grano', 'Daiki', 'Shisti'
                            ]
        self.target_tag = 'Cidra200'

        self.feature_tags_bg = [self.tag_names[i] for i in self.feature_tags ]
        self.target_tag_bg = self.tag_names[self.target_tag]

        # self.update_trends_df(df)
        self.init_items()

    def init_items(self):
        series_init = QSplineSeries()
        series_init.append(0, 10)
        self.items = [
            {"tag_name_bg": self.feature_tags_bg[0], "trend_proc": series_init, "trend_sim": series_init, "trend_out": series_init,
             "tag_color": "red", "axis_min" : 0, "axis_max" : 300, 'cur_val_proc' : 0, 'cur_val_sim' : 0},
            {"tag_name_bg": self.feature_tags_bg[1], "trend_proc": series_init, "trend_sim": series_init, "trend_out": series_init,
             "tag_color": "yellow", "axis_min" : 0, "axis_max" : 300, 'cur_val_proc' : 0, 'cur_val_sim' : 0},
            {"tag_name_bg": self.feature_tags_bg[2], "trend_proc": series_init, "trend_sim": series_init, "trend_out": series_init,
             "tag_color": "cyan", "axis_min" : 0, "axis_max" : 20, 'cur_val_proc' : 0, 'cur_val_sim' : 0},
            {"tag_name_bg": self.feature_tags_bg[3], "trend_proc": series_init, "trend_sim": series_init, "trend_out": series_init,
             "tag_color": "orange", "axis_min" : 0, "axis_max" : 20, 'cur_val_proc' : 0, 'cur_val_sim' : 0},
            {"tag_name_bg": self.feature_tags_bg[4], "trend_proc": series_init, "trend_sim": series_init, "trend_out": series_init,
             "tag_color": "green", "axis_min" : 0, "axis_max" : 20, 'cur_val_proc' : 0, 'cur_val_sim' : 0},
            {"tag_name_bg": self.feature_tags_bg[5], "trend_proc": series_init, "trend_sim": series_init, "trend_out": series_init,
             "tag_color": "brown", "axis_min" : 0, "axis_max" : 20, 'cur_val_proc' : 0, 'cur_val_sim' : 0},
             {"tag_name_bg": self.feature_tags_bg[6], "trend_proc": series_init, "trend_sim": series_init, "trend_out": series_init,
             "tag_color": "pink", "axis_min" : 0, "axis_max" : 20, 'cur_val_proc' : 0, 'cur_val_sim' : 0},
             {"tag_name_bg": self.feature_tags_bg[7], "trend_proc": series_init, "trend_sim": series_init, "trend_out": series_init,
             "tag_color": "blue", "axis_min" : 0, "axis_max" : 20, 'cur_val_proc' : 0, 'cur_val_sim' : 0}
        ]
    
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.items)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        row = index.row()
        if role == self.name_role:
            return self.items[row]["tag_name_bg"]
        if role == self.series_proc_role:
            return self.items[row]["trend_proc"]
        if role == self.series_sim_role:
            return self.items[row]["trend_sim"]
        if role == self.series_out_role:
            return self.items[row]["trend_out"]
        if role == self.color_role:
            return self.items[row]["tag_color"]
        if role == self.axis_min_role:
            return self.items[row]["axis_min"]
        if role == self.axis_max_role:
            return self.items[row]["axis_max"]
        if role == self.cur_val_proc_role:
            return self.items[row]["cur_val_proc"]
        if role == self.cur_val_sim_role:
            return self.items[row]["cur_val_sim"]
        

    def roleNames(self):
        return {
            self.name_role: QByteArray(b'tag_name'),
            self.series_proc_role: QByteArray(b'trend_proc'),
            self.series_sim_role: QByteArray(b'trend_sim'),
            self.series_out_role: QByteArray(b'trend_out'),
            self.color_role: QByteArray(b'tag_color'),
            self.axis_min_role: QByteArray(b'axis_min'),
            self.axis_max_role: QByteArray(b'axis_max'),
            self.cur_val_proc_role: QByteArray(b'cur_val_proc'),
            self.cur_val_sim_role: QByteArray(b'cur_val_sim')
        }

    def setData(self, index, value, role=Qt.UserRole):
        row = index.row()
        if role == self.series_proc_role:     
            self.items[row]["trend_proc"] = value  
            self.beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), index.row(), index.row())
            self.dataChanged.emit(index, index, [role])
            self.endInsertRows()
            return True
        if role == self.series_sim_role:     
            self.items[row]["trend_sim"] = value  
            self.beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), index.row(), index.row())
            self.dataChanged.emit(index, index, [role])
            self.endInsertRows()
            return True
        if role == self.series_out_role:     
            self.items[row]["trend_out"] = value  
            self.beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), index.row(), index.row())
            self.dataChanged.emit(index, index, [role])
            self.endInsertRows()
            return True
        if role == self.axis_min_role:     
            self.items[row]["axis_min"] = value
            self.beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), index.row(), index.row())
            self.dataChanged.emit(index, index, [role])
            self.endInsertRows()
            return True
        if role == self.axis_max_role:     
            self.items[row]["axis_max"] = value
            self.beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), index.row(), index.row())
            self.dataChanged.emit(index, index, [role])
            self.endInsertRows()
            return True
        if role == self.cur_val_proc_role:     
            self.items[row]["cur_val_proc"] = value
            self.beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), index.row(), index.row())
            self.dataChanged.emit(index, index, [role])
            self.endInsertRows()
            return True
        if role == self.cur_val_sim_role:     
            self.items[row]["cur_val_sim"] = value
            self.beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), index.row(), index.row())
            self.dataChanged.emit(index, index, [role])
            self.endInsertRows()
            return True

        return False

    
    def get_min_max_yaxis_values_for_trend_proc(self, min_value, max_value):

        exponent = math.floor(math.log10(min_value))
        range = range = 10**(exponent -1)
        if exponent >= 2: 
            range = 10
        remain_min = min_value % range
        remain_max = max_value % range

        min_val = int(min_value - range - remain_min)
        max_val = int(max_value + range - remain_max)

        if (min_val and max_val) < 1:
            min_val = 0.3
            max_val = 0.7
        return min_val, max_val
    
    @Slot(list)
    def update_all_trends_df(self, df_list: list): # trends is a list of 2 dataframes for the process and simulation

        concat_df = pd.concat(df_list)
        min_value = concat_df.min(axis=0)
        max_value = concat_df.max(axis=0)
        
        for ser_idx in range(2):
            feature_data = np.array(df_list[ser_idx][self.feature_tags])
            for i in range(len(self.items)): 
                points = []
                for j in range(feature_data.shape[0]):
                    points.append(QPointF(j, feature_data[j,i]))

                index = self.index(i)

                #update trends series by feature
                if ser_idx == 0:
                    self.setData(index, points, self.series_proc_role)
                else:
                    self.setData(index, points, self.series_sim_role)

                # update mix max values of trend axis by feature
                ser_min, ser_max = self.get_min_max_yaxis_values_for_trend_proc(min_value[i], max_value[i])
       

                self.setData(index, ser_min, self.axis_min_role)
                self.setData(index, ser_max, self.axis_max_role)
                if ser_idx == 0:
                    self.setData(index, points[-1].y(), self.cur_val_proc_role)
                else:
                    self.setData(index, points[-1].y(), self.cur_val_sim_role)

        self.update_anomalies(df_list[0]) # call the func with the process data

    # def update_anomalies(self, df_proc):
    #     df_outliers = pd.DataFrame(0, index=df_proc.index, columns=df_proc.columns)
    #     proc_data = np.array(df_proc[self.feature_tags])

    #     # 1D 
    #     z_scores = (proc_data[:,0] - np.mean(proc_data[:,0])) / np.std(proc_data[:,0])
    #     z_score_threshold = 2 #np.std(proc_data[:,0]) * 2
    #     outlier_mask = np.abs(z_scores) > z_score_threshold
    #     # df_outliers.loc[outlier_mask, self.feature_tags] = 1
    #     outliers = np.zeros_like(proc_data[:,0])
    #     outliers[outlier_mask] = proc_data[:,0][outlier_mask]

    #     points = []
    #     for j in range(len(outliers)):
    #         points.append(QPointF(j, outliers[j]))
        
    #     index = self.index(0)
    #     self.setData(index, points, self.series_out_role)

    def update_anomalies(self, df_proc):
        df_outliers = pd.DataFrame(0, index=df_proc.index, columns=df_proc.columns)
        proc_data = np.array(df_proc[self.feature_tags])

        # 1D 
        for i in range(proc_data.shape[1]):
            z_scores = (proc_data[:,i] - np.mean(proc_data[:,i])) / np.std(proc_data[:,i])
            z_score_threshold = 2 #np.std(proc_data[:,0]) * 2
            outlier_mask = np.abs(z_scores) > z_score_threshold
            # df_outliers.loc[outlier_mask, self.feature_tags] = 1
            outliers = np.zeros_like(proc_data[:,i])
            outliers[outlier_mask] = proc_data[:,i][outlier_mask]

            points = []
            for j in range(len(outliers)):
                points.append(QPointF(j, outliers[j]))
            
            index = self.index(i)
            self.setData(index, points, self.series_out_role)











        
