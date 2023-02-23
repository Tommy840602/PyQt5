import sys
import threading

from PyQt5 import QtCore, QtGui,QtWidgets,QtWebEngineWidgets

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff


class QDash(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._app = dash.Dash()
        self.app.layout = html.Div()

    @property
    def app(self):
        return self._app

    def update_graph(self, df):
        fig = ff.create_gantt(df)
        self.app.layout = html.Div([dcc.Graph(figure=fig)])

    def run(self, **kwargs):
        threading.Thread(target=self.app.run_server, kwargs=kwargs, daemon=True).start()


class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.table = QtWidgets.QTableWidget()
        self.button = QtWidgets.QPushButton("Press me")

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QVBoxLayout(central_widget)
        lay.addWidget(self.browser, stretch=1)
        lay.addWidget(self.table, stretch=1)
        lay.addWidget(self.button)

        self.resize(640, 480)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(("X", "Y1", "Y2"))
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        self.qdask = QDash()
        self.qdask.run(debug=True, use_reloader=False)
        self.browser.load(QtCore.QUrl("http://127.0.0.1:8050"))

        self.button.clicked.connect(self.update_figure)

        current_date = QtCore.QDateTime.currentDateTime()

        for i in range(3):
            self.append_row(
                task="Task{}".format(i),
                start=current_date,
                finish=current_date.addDays(i + 1),
            )

    @QtCore.pyqtSlot()
    def update_figure(self):

        df = []

        for i in range(self.table.rowCount()):
            task = self.table.item(i, 0).data(QtCore.Qt.DisplayRole)
            start = (
                self.table.item(i, 1)
                .data(QtCore.Qt.DisplayRole)
                .toString(QtCore.Qt.ISODateWithMs)
            )
            finish = (
                self.table.item(i, 2)
                .data(QtCore.Qt.DisplayRole)
                .toString(QtCore.Qt.ISODateWithMs)
            )

            d = dict(Task=task, Start=start, Finish=finish)
            df.append(d)

        print(df)

        self.qdask.update_graph(df)
        self.browser.reload()

    def append_row(
        self,
        task="",
        start=QtCore.QDateTime.currentDateTime(),
        finish=QtCore.QDateTime.currentDateTime(),
    ):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for column, value in enumerate((task, start, finish)):
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, value)
            self.table.setItem(row, column, it)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

    w = Mainwindow()
    w.show()

    sys.exit(app.exec_())


