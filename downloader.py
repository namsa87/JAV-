# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'downloader.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
#https://javgo.to/en/v/fc2-ppv-2927929
import ffmpeg_streaming
import os
import sys
import datetime
import time
from pathlib import Path
from selenium import webdriver
from seleniumwire import webdriver as wired_webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from ffmpeg_streaming import Formats
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import  pyqtSlot, QObject, pyqtSignal, QTimer


class Ui_MainWindow(object):
    def __init__(self, parent=None):
        self.threadclass = ThreadClass()
        self._stdout = StdoutRedirect()
        self._stdout.printOccur.connect(lambda x: self._append_text(x))
        self._stdout.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(507, 320)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.URL_Input = QtWidgets.QTextEdit(self.centralwidget)
        self.URL_Input.setGeometry(QtCore.QRect(50, 10, 441, 31))
        self.URL_Input.setObjectName("URL_Input")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.Log_View = QtWidgets.QTextBrowser(self.centralwidget)
        self.Log_View.setGeometry(QtCore.QRect(10, 80, 481, 211))
        self.Log_View.setObjectName("Log_View")
        self.Download_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Download_Button.setGeometry(QtCore.QRect(10, 50, 481, 23))
        self.Download_Button.setObjectName("Download_Button")
        self.Download_Button.clicked.connect(self.thread_start)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 507, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _append_text(self, msg):
        #msg = "test"
        ui.Log_View.moveCursor(QtGui.QTextCursor.End)
        # self.textBrowser.moveCursor(QtGui.QTextCursor.End)
        # self.textBrowser.insertPlainText(msg)
        ui.Log_View.insertPlainText(msg)
        #ui.Log_View.append(msg)
        # refresh textedit show, refer) https://doc.qt.io/qt-5/qeventloop.html#ProcessEventsFlag-enum
       # QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def thread_start(self):
        self.threadclass.start()



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "JAVGO 다운로더"))
        self.label.setText(_translate("MainWindow", "URL"))
        self.Download_Button.setText(_translate("MainWindow", "다운로드"))


class StdoutRedirect(QObject):
    printOccur = pyqtSignal(str, str, name="print")


    def __init__(self, *param):
        QObject.__init__(self, None)
        self.daemon = True
        self.sysstdout = sys.stdout.write
        self.sysstderr = sys.stderr.write

    def stop(self):
        sys.stdout.write = self.sysstdout
        sys.stderr.write = self.sysstderr

    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write = lambda msg: self.write(msg, color="red")

    def write(self, s, color="black"):
        sys.stdout.flush()
        self.printOccur.emit(s, color)

class ThreadClass(QtCore.QThread):
    def __init__(self, parent = None):
        super(ThreadClass,self).__init__(parent)




    def run(self):

        def monitor(ffmpeg, duration, time_, time_left, process):
            print(duration)
            per = round(time_ / duration * 100)
            sys.stdout.write("\rTranscoding...(%s%%) %s left [%s%s]" %
            (per, datetime.timedelta(seconds=int(time_left)), '1' * per, '0' * (100 - per))
            )

            #(per))
            sys.stdout.flush()



        ui.Log_View.append("DownLoad Start!!")

        url = ui.URL_Input.toPlainText()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        driver = wired_webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.get(url)
        title = driver.title
        title = title.split(" ")
        title = title[1] + '.mp4'
        #path = os.path.join("C:", os.sep, "Users", "namsa", "OneDrive", "사진", "image", title)
        path = os.path.join(os.sep,title)
            #  path = Path(Path.cwd())
            # path = path.joinpath(path,title)
        for request in driver.requests:
            if request.response:
                # vnd.apple.mpegurl
                if request.response.headers["Content-Type"] == 'application/vnd.apple.mpegurl':
                        # print(f'{request.url}, 응답코드 {request.response.status_code}, 컨텐츠 유형: {request.response.headers["Content-Type"]}')
                        # print(f'{request.url}')
                    video_url = request.url
                    ui.Log_View.append(video_url)
                    ui.Log_View.append(path)
                    driver.quit();
                    video = ffmpeg_streaming.input(video_url)

                    stream = video.stream2file(Formats.h264())

                        # stream.output('C:\\Users\\namsa\\OneDrive\\사진\\image\\FC2-PPV-2928986.mp4', monitor=monitor)
                    #stream.output(path,monitor=monitor,encoding='utf-8')
                    #stream.output(path,monitor=monitor, encoding='utf-8')
                    stream.output(title, monitor=monitor, encoding='utf-8')
                    print("Finish!!")
                    sys.stdout.write("Finish!!")
                    sys.stdout.flush()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())







