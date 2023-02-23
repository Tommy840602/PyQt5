import threading
from dash import dcc,dash_table,html,Input, Output, State,Dash,callback_context,ALL,MATCH
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,os

class MainWindow(QMainWindow):   
    closed = QtCore.pyqtSignal()
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def __init__(self):
        super().__init__()
        # setting title
        self.setWindowTitle("Calculator")
        # setting geometry
        self.setGeometry(100, 100, 360, 350)
        # calling method
        self.UiComponents()
        # showing all the widgets
        self.show()
 
        # method for widgets
    def UiComponents(self):
        # creating a label
        self.label = QLabel(self)
        # setting geometry to the label
        self.label.setGeometry(5, 5, 350, 70) 
        # creating label multi line
        self.label.setWordWrap(True)
        # setting style sheet to the label
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 1px solid black;"
                                 "background : white;"
                                "}")
 
        # setting alignment to the label
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
        # setting font
        self.label.setFont(QFont('Arial', 15))
 
        # adding number button to the screen
        # creating a push button
        push1 = QPushButton("1", self)
        # setting geometry
        push1.setGeometry(5, 150, 80, 40)
 
        # creating a push button
        push2 = QPushButton("2", self)
        # setting geometry
        push2.setGeometry(95, 150, 80, 40)
 
        # creating a push button
        push3 = QPushButton("3", self)
        # setting geometry
        push3.setGeometry(185, 150, 80, 40)
 
        # creating a push button
        push4 = QPushButton("4", self)
        # setting geometry
        push4.setGeometry(5, 200, 80, 40)
 
        # creating a push button
        push5 = QPushButton("5", self)
        # setting geometry
        push5.setGeometry(95, 200, 80, 40)
 
        # creating a push button
        push6 = QPushButton("6", self) 
        # setting geometry
        push6.setGeometry(185, 200, 80, 40)
 
        # creating a push button
        push7 = QPushButton("7", self)
        # setting geometry
        push7.setGeometry(5, 250, 80, 40)
 
        # creating a push button
        push8 = QPushButton("8", self)
        # setting geometry
        push8.setGeometry(95, 250, 80, 40)
 
        # creating a push button
        push9 = QPushButton("9", self) 
        # setting geometry
        push9.setGeometry(185, 250, 80, 40)
 
        # creating a push button
        push0 = QPushButton("0", self)
        # setting geometry
        push0.setGeometry(95, 300, 80, 40)
 
        # adding operator push button
        # creating push button
        push_equal = QPushButton("=", self)
        # setting geometry
        push_equal.setGeometry(5, 300, 80, 40)
        # adding equal button a color effect
        a_effect = QGraphicsColorizeEffect()
        a_effect.setColor(Qt.red)     
        push_equal.setGraphicsEffect(a_effect)
 
        # creating push button
        push_plus = QPushButton("+", self)
        # setting geometry
        push_plus.setGeometry(275, 150, 80, 40)
        # adding equal button a color effect
        d_effect = QGraphicsColorizeEffect()
        d_effect.setColor(Qt.blue)
        push_plus.setGraphicsEffect(d_effect)

        # creating push button
        push_minus = QPushButton("-", self)
        # setting geometry
        push_minus.setGeometry(275, 200, 80, 40)
        c_effect = QGraphicsColorizeEffect()
        c_effect.setColor(Qt.blue)
        push_minus.setGraphicsEffect(c_effect)

        # creating push button
        push_mul = QPushButton("*", self)
        # setting geometry
        push_mul.setGeometry(275, 250, 80, 40)
        d_effect = QGraphicsColorizeEffect()
        d_effect.setColor(Qt.blue)
        push_mul.setGraphicsEffect(d_effect)

 
        # creating push button
        push_div = QPushButton("/", self)
        # setting geometry
        push_div.setGeometry(275,300,80,40)
        e_effect = QGraphicsColorizeEffect()
        e_effect.setColor(Qt.blue)
        push_div.setGraphicsEffect(e_effect)

 
        # creating push button
        push_next = QPushButton("->", self)
        # setting geometry
        push_next.setGeometry(185, 300, 80, 40)
 
 
        # clear button
        push_clear = QPushButton("Clear", self)
        push_clear.setGeometry(185,100,80,40)
        f_effect = QGraphicsColorizeEffect()
        f_effect.setColor(Qt.red)
        push_clear.setGraphicsEffect(f_effect)

        # del one character button
        push_del = QPushButton("Del", self)
        push_del.setGeometry(275,100,80,40)
        g_effect = QGraphicsColorizeEffect()
        g_effect.setColor(Qt.red)
        push_del.setGraphicsEffect(g_effect)

        # creating left bracket button
        push_left_bracket=QPushButton("(", self)
        # setting geometry
        push_left_bracket.setGeometry(5,100,80,40)

        # creating right bracket button
        push_right_bracket=QPushButton(")", self)
        # setting geometry
        push_right_bracket.setGeometry(95,100,80,40)

        # adding action to each of the button
        push_minus.clicked.connect(self.action_minus)
        push_equal.clicked.connect(self.action_equal)
        push0.clicked.connect(self.action0)
        push1.clicked.connect(self.action1)
        push2.clicked.connect(self.action2)
        push3.clicked.connect(self.action3)
        push4.clicked.connect(self.action4)
        push5.clicked.connect(self.action5)
        push6.clicked.connect(self.action6)
        push7.clicked.connect(self.action7)
        push8.clicked.connect(self.action8)
        push9.clicked.connect(self.action9)
        push_div.clicked.connect(self.action_div)
        push_mul.clicked.connect(self.action_mul)
        push_plus.clicked.connect(self.action_plus)
        push_clear.clicked.connect(self.action_clear)
        push_del.clicked.connect(self.action_del)
        push_left_bracket.clicked.connect(self.action_push_left_bracket)
        push_right_bracket.clicked.connect(self.action_push_right_bracket)
        push_next.clicked.connect(self.action_push_next)


    def action_equal(self):
        # get the label text
        equation = self.label.text()
        try:
            # getting the ans
            ans = eval(equation)
            # setting text to the label
            self.label.setText(str(ans))
        except:
            # setting text to the label
            self.label.setText("Wrong Input")
 
    def action_plus(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + " + ")
 
    def action_minus(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + " - ")
 
    def action_div(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + " / ")
 
    def action_mul(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + " * ")
 
    def action_push_next(self):
        self.statusBar().showMessage("Switched to next window")
        self.cams = Window(self) 
        self.cams.show()
        self.close()
 
    def action0(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "0")
 
    def action1(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "1")
 
    def action2(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "2")
 
    def action3(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "3")
 
    def action4(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "4")
 
    def action5(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "5")
 
    def action6(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "6")
 
    def action7(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "7")
 
    def action8(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "8")
 
    def action9(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "9")
 
    def action_clear(self):
        # clearing the label text
        self.label.setText("")
 
    def action_del(self):
        # clearing a single digit
        text = self.label.text()
        print(text[:len(text)-1])
        self.label.setText(text[:len(text)-1])

    def action_push_left_bracket(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "(")

    def action_push_right_bracket(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + ")")

class Window(QMainWindow):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Next Window')
        self.setGeometry(100,100,360,350)
        
    def __init__(self, value, parent=None):
        super().__init__(parent)
        # setting title
        self.setWindowTitle("Calculator")
        # setting geometry
        self.setGeometry(100, 100, 360, 350)
        # calling method
        self.UiComponents()
        # showing all the widgets
        self.show()
 
        # method for widgets
    def UiComponents(self):
        # creating a label
        self.label = QLabel(self)
        # setting geometry to the label
        self.label.setGeometry(5, 5, 350, 70) 
        # creating label multi line
        self.label.setWordWrap(True)
        # setting style sheet to the label
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 1px solid black;"
                                 "background : white;"
                                 "}")
 
        # setting alignment to the label
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
        # setting font
        self.label.setFont(QFont('Arial', 15))
 
        # adding number button to the screen
        # creating a push button
        # creating push button
        push_last = QPushButton("<-", self)
        # setting geometry
        push_last.setGeometry(185, 300, 80, 40)

        # adding action to each of the button
        push_last.clicked.connect(self.goMainWindow)

    def goMainWindow(self):
        self.cams = MainWindow()
        self.cams.show()
        self.close() 

class Manager(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._view = None

    @property
    def view(self):
        return self._view

    def init_gui(self):
        self._view = MainWindow()

    @QtCore.pyqtSlot()
    def show_popup(self):
        if self.view is not None:
            self.view.show()

qt_manager = Manager()

app = dash.Dash()

data={"A":[5.9,2.4],"B":[8.7,9.5]}

app.layout = html.Div([
        html.H1('TEST'),
        html.Button("show calculator", id="button"),
        html.Div(children=[],id="result")]     
)

@app.callback(
    Output("result","children"),
    [Input("button","n_clicks")]
)

def pop(n_clicks):
    if not n_clicks:
        return dash.exceptions.PreventUpdate
    loop = QtCore.QEventLoop()
    qt_manager.view.closed.connect(loop.quit)
    QtCore.QMetaObject.invokeMethod(qt_manager,"show_popup", QtCore.Qt.QueuedConnection)
    loop.exec_()
    return "Calculator" 


def main():
    qt_app = QApplication.instance()
    if qt_app is None:
       qt_app = QApplication([os.getcwd()])
    qt_app.setQuitOnLastWindowClosed(False)
    qt_manager.init_gui()
    threading.Thread(target=app.run_server, kwargs=dict(debug=False), daemon=True).start()
    return qt_app.exec_()


if __name__ == "__main__":
    main()