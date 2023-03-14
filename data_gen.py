import pandas as pd
from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer, QThread, QPointF, QDateTime, QAbstractTableModel, QModelIndex, Qt
import sqlite3 as db


class DataGenerator(QObject):

    signal_data_changed = Signal(pd.DataFrame)

    def __init__(self):
        QObject.__init__(self)
        # self.path = "C:\\MFC_Scripts\\MillingProcess\\MODELING\\SST\\db.sqlite3"
        self.df = pd.DataFrame()
        self.initialize_data()
        self.index = 0
        self._data_trend = pd.DataFrame()
        self.update_data(100)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(lambda : self.update_data(data_len = 100)) # using lambda so you can call update_data with parameters
        self.timer.start()


    def initialize_data(self):
        self.df = pd.read_csv('C:/DataSets/MFC/Features/Pulse_1T_Mill02.csv', 
                             parse_dates=True, index_col='TimeStamp')
        self.df = self.df[self.df.index > '2022-01-01 00:00:00']

        # for column in self.df.columns:
        #     self.df[column] = self.df[column].ewm(span = 150).mean()

    def get_data_trend(self):
        return self._data_trend

    def set_data_trend(self, data_trend):
        if not data_trend.equals(self.data_trend):
            self._data_trend = data_trend
            self.signal_data_changed.emit(data_trend)

    data_trend = property(get_data_trend, set_data_trend)

    def update_data(self, data_len):
        rows = self.df.iloc[self.index : self.index + data_len]
        self.index += 1
        self.data_trend = rows
        print(self.data_trend.tail(5))



