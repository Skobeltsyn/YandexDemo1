import sys
import csv
from PyQt5 import QtWidgets, uic, Qt, QtGui
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter

from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QPushButton
from PyQt5.QtChart import QChart, QChartView, QLineSeries

class YandexApp(QtWidgets.QMainWindow):
    def __init__(self):
        self.my_csv_path = ""
        self.csv_reader = None
        self.csv_data = None
        self.csv_data_buttons = []
        self.chosenColumn = None
        self.csv_data = []
        super().__init__()
        uic.loadUi("design.ui", self)
        self.setup_ui()

    def setup_ui(self):
        self.trigger_stage_1()
        pass

    def trigger_stage_1(self):
        self.content_1.setVisible(True)
        self.content_2.setVisible(False)
        self.content_3.setVisible(False)
        self.content_4.setVisible(False)
        self.openFileBtn.clicked.connect(self.get_csv)
        self.openFileBtn.setStyleSheet("background: #c3fb12; font-size: 20px; padding: 9px; border-radius: 10px;")
        self.progressBar.setValue(0)
        self.csv_file_path.setText(self.my_csv_path)
        self.stage_1.setChecked(True)
        self.stage_1.setEnabled(True)
        self.stage_2.setChecked(False)
        self.stage_2.setEnabled(False)
        self.stage_3.setChecked(False)
        self.stage_3.setEnabled(False)
        self.stage_4.setChecked(False)
        self.stage_4.setEnabled(False)
        self.chooseDataRows.setStyleSheet("color: #000; border: 1px solid #000;")
        self.chooseDataRows.setEnabled(False)
        self.update()

    def trigger_stage_2(self):
        # self.content_1.hide()
        self.open_csv()
        self.content_1.setVisible(False)
        self.content_2.setVisible(True)
        self.content_3.setVisible(False)
        self.content_4.setVisible(False)
        self.stage_1.setChecked(False)
        self.stage_1.setEnabled(False)
        self.stage_2.setChecked(True)
        self.stage_2.setEnabled(True)
        self.stage_3.setChecked(False)
        self.stage_3.setEnabled(False)
        self.stage_4.setChecked(False)
        self.stage_4.setEnabled(False)
        self.progressBar.setValue(30)

    def trigger_stage_3(self):
        self.get_column_data()
        self.content_1.setVisible(False)
        self.content_2.setVisible(False)
        self.content_3.setVisible(True)
        self.content_4.setVisible(False)
        self.progressBar.setValue(59)
        self.stage_1.setChecked(False)
        self.stage_1.setEnabled(False)
        self.stage_2.setChecked(False)
        self.stage_2.setEnabled(False)
        self.stage_3.setChecked(True)
        self.stage_3.setEnabled(True)
        self.stage_4.setChecked(False)
        self.stage_4.setEnabled(False)
        self.chooseDataRepresentation_2.clicked.connect(self.trigger_stage_4)

    def trigger_stage_4(self):
        # self.get_column_data()
        self.content_1.setVisible(False)
        self.content_2.setVisible(False)
        self.content_3.setVisible(False)
        self.content_4.setVisible(True)
        self.progressBar.setValue(99)
        self.stage_1.setChecked(False)
        self.stage_1.setEnabled(False)
        self.stage_2.setChecked(False)
        self.stage_2.setEnabled(False)
        self.stage_3.setChecked(False)
        self.stage_3.setEnabled(False)
        self.stage_4.setChecked(True)
        self.stage_4.setEnabled(True)

        series = QLineSeries(self)
        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)
        series << QPointF(11, 1) << QPointF(13, 3) << QPointF(17, 6) << QPointF(18, 3) << QPointF(20, 2)
        chart = QChart()
        #
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(self.chosenColumn[0])
        #
        chart.legend().setVisible(True)


        # chart.legend().setAlignment(Qt.AlignBottom)
        #
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.content_4.layout = QtWidgets.QVBoxLayout(self)
        self.content_4.layout.addWidget(chartview)

        # layout = QtGui.QVBoxLayout()
        # layout.addWidget(self.content_4)
        # self.setLayout(layout)

        self.setCentralWidget(chartview)
        # self.content_4.se

    def get_csv(self):
        self.my_csv_path = QFileDialog.getOpenFileName(self, 'Выбрать файл с данными', '')[0]
        self.csv_file_path.setText(self.my_csv_path)
        self.chooseDataRows.setStyleSheet("background: #c3fb12; font-size: 20px; padding: 9px; border-radius: 10px; "
                                          "color: #000000;")
        self.chooseDataRows.setEnabled(True)
        self.openFileBtn.setStyleSheet("background: transparent; color: #c3fb12; border: 1px solid #c3fb12; "
                                       "font-size: 20px; padding: 9px; border-radius: 10px;")
        self.chooseDataRows.clicked.connect(self.trigger_stage_2)

    def open_csv(self):
        # csv_file = open(self.my_csv_path, "r")
        with open(self.my_csv_path, newline='') as f:
            self.csv_reader = csv.reader(f, delimiter=',')
            self.csv_data = list(self.csv_reader)
            # object =
            # self.vbox.addWidget(object)
        print(self.csv_data[0])
        data_layout = Qt.QVBoxLayout()
        self.csv_data_buttons.clear()
        column_id = 0
        for x in self.csv_data[0]:
            column_label = QPushButton(x)
            self.csv_data_buttons.append(column_label)
            column_label.clicked.connect(lambda: self.choose_data_row())
            data_layout.addWidget(column_label)
            column_id += 1

        w = Qt.QWidget()
        w.setLayout(data_layout)
        self.data_columns_area.setWidget(w)

    def choose_data_row(self):
        chosen_column_index = 0
        for x in self.csv_data_buttons:
            # print(x)
            x.setStyleSheet("background: #000;")
            if x == self.sender():
                self.chosenColumn = [x.text(), chosen_column_index]
                # print(self.chosenColumn)
            chosen_column_index += 1
        self.sender().setStyleSheet("background: #FFFFFF; color: #000;")
        self.chooseDataRepresentation.setStyleSheet("background: #c3fb12; font-size: 20px; padding: 9px; "
                                                    "border-radius: 10px; "
                                                    "color: #000000;")
        self.chooseDataRepresentation.clicked.connect(self.trigger_stage_3)

    def get_column_data(self):
        shown_data = []
        i = -1
        data_content_layout = Qt.QVBoxLayout()
        aw = Qt.QWidget()
        aw.setLayout(data_content_layout)
        self.data_area.setWidget(aw)
        # print(len(self.csv_data))
        data = []
        for row in self.csv_data:
            i += 1
            if i < 1:
                continue
            # print(row)
            # print(self.chosenColumn[1])
            value = row[self.chosenColumn[1]]
            data.append(value)
            if i > 100:
                continue
            # print(value)
            # shown_data.append(row[self.chosenColumn[1]])
            if len(value) > 0:
                row_label = QLabel(value)
                data_content_layout.addWidget(row_label)


def main(name):
    app = QtWidgets.QApplication(sys.argv)
    window = YandexApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main('YandexDemo1')
#
