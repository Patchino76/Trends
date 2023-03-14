import pandas as pd
from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer, QThread, QPointF, QDateTime, QAbstractTableModel, QModelIndex, Qt
import numpy as np
import math


class DataGenRegression(QObject):

    signal_data_changed = Signal(pd.DataFrame)
    signal_sp_cidra_proc_changed = Signal(float)
    signal_sp_cidra_sim_changed = Signal(float)
    signal_all_data_changed = Signal(list)

    def __init__(self):
        QObject.__init__(self)
        # self.df_reg =  pd.read_csv("C:/MFC_Scripts/MillingProcess/MODELING/Mills_Data/reg_coefs.csv")
        self.df_reg =  pd.read_csv("C:/MFC_Scripts/MillingProcess/MODELING/Mills_Data/reg_poly_coefs.csv")
        self._data_trend = pd.DataFrame()
        self.data_trends = []

        self._sp_cidra_proc = 23.0
        self._sp_cidra_sim = 23.0
        self.sp_cidra_std = 0.5

        self.do_sp_cidra_sim_to_proc = False

        self.feature_tags = [
                            'Ore', 'WaterZumpf', 'WaterMill', 'PressureHC', 'MotorAmp',
                            'DensityHC', 'PulpHC', 'PumpRPM',
                            # 'Grano', 'Daiki', 'Shisti'
                            ]
        self.target_tag = 'Cidra200'
        self.all_tags = self.feature_tags.copy()
        self.all_tags.append(self.target_tag)

        self.initialize_data(self.sp_cidra_proc, self.sp_cidra_std)
        self.initialize_data(self.sp_cidra_sim)
        # self.data_trends.append(pd.DataFrame(np.zeros((100, len(self.df_reg)+1)), columns=self.all_tags)) # the alarms dataframe
        self.signal_all_data_changed.emit(self.data_trends)
        
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(lambda : self.update_data(self.sp_cidra_proc, sp_cidra_std = 0.2, index = 0)) # using lambda so you can call update_data with parameters
        self.timer.timeout.connect(lambda : self.update_data(self.sp_cidra_sim, index = 1)) # using lambda so you can call update_data with parameters
        self.timer.timeout.connect(lambda : self.gradualy_move_sp_cidra_sim_to_proc())
        self.timer.start()

    def get_data_trend(self):
        return self._data_trend

    def set_data_trend(self, data_trend):
        if not data_trend.equals(self.data_trend):
            self._data_trend = data_trend
            self.signal_data_changed.emit(data_trend)

    data_trend = property(get_data_trend, set_data_trend)

# Set Point - Cidra - Process
    @Property(float, notify=signal_sp_cidra_proc_changed)
    def sp_cidra_proc(self):
        return self._sp_cidra_proc

    @sp_cidra_proc.setter
    def sp_cidra_proc(self, value):
        if self._sp_cidra_proc != value:
            self._sp_cidra_proc = value
            self.signal_sp_cidra_proc_changed.emit(value)
    
# Set Point - Cidra - Simulation
    @Property(float, notify=signal_sp_cidra_sim_changed)
    def sp_cidra_sim(self):
        return self._sp_cidra_sim

    @sp_cidra_sim.setter
    def sp_cidra_sim(self, value):
        if self._sp_cidra_sim != value:
            self._sp_cidra_sim = value
            self.signal_sp_cidra_sim_changed.emit(value)
    

    def initialize_data(self, sp_cidra, sp_cidra_std=0.01,  n_samples = 100):
        cidra_mu, cidra_s = sp_cidra, sp_cidra_std
        noise_mu, noise_s = 0, 0.05
        cidra = np.random.normal(cidra_mu, cidra_s, n_samples).reshape(-1, 1)
        print(cidra.shape)

        trends = np.empty((n_samples, len(self.df_reg)))

        for i in range(len(self.df_reg)):
            bias = float(self.df_reg.iloc[i]['Bias'])
            slope1 = self.df_reg.iloc[i]['Slope1']
            slope2 = self.df_reg.iloc[i]['Slope2']

            noise = np.random.normal(noise_mu, noise_s, 1)
            tag_vals = bias + slope1*cidra + slope2*cidra**2 + noise
            trends[:,i] = tag_vals.squeeze()
        
        trends = np.hstack((trends, cidra.reshape(-1,1)))
        self.data_trends.append(pd.DataFrame(trends, columns=self.all_tags)) # list of 2 full dataframes for process and simulation!!!
        


    def update_data(self, sp_cidra, sp_cidra_std = 0.01, index = 0):
        cidra_mu, cidra_s = sp_cidra, sp_cidra_std
        
        
        cidra = np.random.normal(cidra_mu, cidra_s, 1)
        trends = np.empty((1, len(self.df_reg)))
        trends_df = self.data_trends[index].copy()

        for i in range(len(self.df_reg)):
            bias = float(self.df_reg.iloc[i]['Bias'])
            slope1 = self.df_reg.iloc[i]['Slope1']
            slope2 = self.df_reg.iloc[i]['Slope2']

 

            tag_vals = bias + slope1*cidra + slope2*cidra**2 #+ noise
            # Noise management
            if index == 0:
                exponent = math.floor(math.log10(tag_vals))
                if exponent >= 3:
                    noise_std = 10**exponent * 0.01 / 5 # for density HC
                else:
                    noise_std = 10**exponent *  np.random.rand() / 10.0 #0.01
                noise = np.random.normal(0, noise_std, 1)
                tag_vals += noise


            trends[:,i] = tag_vals.squeeze()

        trends = np.hstack((trends, cidra.reshape(-1,1)))
        trends_tmp_df = pd.DataFrame(trends, columns=self.all_tags)
     
        trends_df = pd.concat([trends_df, trends_tmp_df], ignore_index=True)
        trends_df = trends_df.shift(-1)
        trends_df = trends_df.drop(trends_df.index[-1])
        self.data_trends[index] = trends_df

        if index == 1: #means that both series are processed
            self.signal_all_data_changed.emit(self.data_trends)

    @Slot(bool)
    def save_sp_cidra_sim_to_proc(self, state):
        # self.sp_cidra_proc = self.sp_cidra_sim
        self.do_sp_cidra_sim_to_proc = state

    def gradualy_move_sp_cidra_sim_to_proc(self):

        if self.do_sp_cidra_sim_to_proc:
            diff = self.sp_cidra_sim - self.sp_cidra_proc
            self.sp_cidra_proc = self.sp_cidra_proc +  (diff / 15.0)



        



