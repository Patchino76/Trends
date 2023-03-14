from pathlib import Path
import sys
import numpy as np
from PySide6.QtCore import QUrl, QObject, Property, Signal, Slot, QTimer
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QmlElement, QQmlApplicationEngine
from PySide6.QtCharts import QAbstractSeries
from PySide6.QtCore import *

from data_gen import DataGenerator
from data_gen_regression import DataGenRegression
from trends_ui import TrendsUI


if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    qml_object_created = [False]

    def handle_qml_load_errors(obj, _url):
        qml_object_created[0] = obj is not None
    engine.objectCreated.connect(
        handle_qml_load_errors)  # pylint: disable=no-member
    # data_gen = DataGenerator()
    data_gen = DataGenRegression()

    trends_ui = TrendsUI(data_gen.data_trend)
    engine.rootContext().setContextProperty("trends_ui", trends_ui)
    engine.rootContext().setContextProperty("data_gen", data_gen)

    # data_gen.signal_data_changed.connect(trends_ui.update_trends_df)
    data_gen.signal_all_data_changed.connect(trends_ui.update_all_trends_df)

    qml_file = Path(__file__).parent / "main.qml"
    engine.load(QUrl.fromLocalFile(qml_file))


    if not qml_object_created[0]:
        sys.exit(1)

    app_errcode = app.exec()
    sys.exit(app_errcode)
