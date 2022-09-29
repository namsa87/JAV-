# -*- coding: utf-8 -*-

import datetime

# Form implementation generated from reading ui file 'downloader.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
import os
import threading
import time
import urllib.parse
import webbrowser

import ffmpeg_streaming
import requests


from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import  *
from bs4 import BeautifulSoup
from ffmpeg_streaming import Formats
from selenium import webdriver
from seleniumwire import webdriver as wired_webdriver
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

class Ui_MainWindow(object):
    def __init__(self, parent=None):
        self.threadclass = ThreadClass()
        self._stdout = StdoutRedirect()
        self._stdout.printOccur.connect(lambda x: self._append_text(x))
        self._stdout.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(507, 425)
        from PyQt5 import QtWidgets
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #self.URL_Input = QtWidgets.QTextEdit(self.centralwidget)
        self.URL_Input = QtWidgets.QLineEdit(self.centralwidget)
        self.URL_Input.setGeometry(QtCore.QRect(50, 50, 441, 31))
        self.URL_Input.setObjectName("URL_Input")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 50, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.Log_View = QtWidgets.QTextBrowser(self.centralwidget)

        self.Log_View.setGeometry(QtCore.QRect(10, 290, 481, 100))
        self.Log_View.setObjectName("Log_View")
        self.Download_Button = QtWidgets.QPushButton(self.centralwidget)
        #QRect(10, 310, 231, 31)
        self.Download_Button.setGeometry(QtCore.QRect(10, 250, 231, 31))
        self.Download_Button.setObjectName("Download_Button")
        self.Download_Button.clicked.connect(self.thread_start)

        self.Play_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Play_Button.setObjectName("Play_Button")
        self.Play_Button.setGeometry(QtCore.QRect(260,250,231,31))


        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(360, 10, 131, 31))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")
        self.searchInput = QtWidgets.QLineEdit(self.centralwidget)
        #self.searchInput = QtWidgets.QTextEdit(self.centralwidget)
        self.searchInput.setGeometry(QtCore.QRect(10, 10, 341, 31))
        self.ListView = QtWidgets.QListWidget(self.centralwidget)
        self.ListView.setGeometry(QtCore.QRect(10, 90, 481, 150))

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setGeometry(QRect(10,392,491,11))
        self.progressBar.setValue(0)


        font = QtGui.QFont()
        font.setPointSize(13)
        self.searchInput.setFont(font)
        self.searchInput.setObjectName("searchInput")
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

        self.timer = QBasicTimer()
        #self.step = 0
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

   # def timerEvent(self, e):
   #     if self.step >= 100:
   #         self.timer.stop()

            #return

        #self.step = self.step + 1
        #self.progressBar.setValue(self.step)

    #def doAction(self, v):
     #   if self.timer.isActive():
      #      self.timer.stop()

       # else:
        #    self.timer.start(v, self)


    def _append_text(self, msg):
        QApplication.processEvents()
        ui.Log_View.moveCursor(QtGui.QTextCursor.End)

        ui.Log_View.insertPlainText(msg)
            # ui.Log_View.append(msg)
            # refresh textedit show, refer) https://doc.qt.io/qt-5/qeventloop.html#ProcessEventsFlag-enum
        QApplication.processEvents()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "딸딸머신"))
        self.label.setText(_translate("MainWindow", "URL"))
        self.Download_Button.setText(_translate("MainWindow", "다운로드"))
        self.searchButton.setText(_translate("MainWindow", "검색"))
        self.Play_Button.setText(_translate("MainWindow","▶"))

    def Play(self):
        Html = """
        <!doctype html>
<html lang="en">
 <head>
 
  <body>
    <!-- The element where the player will be placed -->
    <div id="player-wrapper"></div>

    <!-- Eyevinn HTML Player Javascript -->
    <script src="https://player.eyevinn.technology/v0.4.2/build/eyevinn-html-player.js" type="text/javascript"></script>

    <!-- Initiate the player and auto-play with audio muted -->
    <script>
      document.addEventListener('DOMContentLoaded', function(event) {
        
        """
        f = open("index.html", 'w')
        f.write(Html)
        # os.system("ffplay -i http://d3rlna7iyyu8wu.cloudfront.net/skip_armstrong/skip_armstrong_multichannel_subs.m3u8")
        url = ui.URL_Input.text()
        print(url)
        if url != '':

            QApplication.processEvents()

            chrome_options = webdriver.ChromeOptions()
           # chrome_options = {'ca_cert': './seleniumwire_ssl/ca.crt',
            #                  'ca_key': './seleniumwire_ssl/ca.key'
             #                 }
            #chrome_options.headless = dict['state']
            chrome_options.headless = True
            driver = wired_webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            driver.get(url)


            QApplication.processEvents()
            for request in driver.requests:
                QApplication.processEvents()
                if request.response:
                        # vnd.apple.mpegurl
                    if request.response.headers["Content-Type"] == 'application/vnd.apple.mpegurl':
                            # print(f'{request.url}, 응답코드 {request.response.status_code}, 컨텐츠 유형: {request.response.headers["Content-Type"]}')
                            # print(f'{request.url}')
                         video_url = request.url
                         print(video_url)
                        #webbrowser.open(self.video_url)
                         Html = "setupEyevinnPlayer('player-wrapper','"+video_url+"').then(function(player) {"
                         f = open("index.html", 'a')
                         f.write(Html)
                         print(video_url)

            Html = """
            
          var muteOnStart = true;
          player.play(muteOnStart);
        });
      });
    </script>
  </body>
  
 </body>
</html>
"""

        f = open("index.html",'a')
        f.write(Html)
        f.close()
        time.sleep(0.5)

        webbrowser.open_new('index.html',new=1)
    def search(self):


        self.ListView.clear()

        try:
             keyword = ui.searchInput.text()
             #keyword = ui.searchInput.toPlainText()
             if keyword != '':
                 keyword = urllib.parse.quote_plus(keyword)

                 url = 'https://javgo.to/ko/search?keyword='+keyword
                 ui.Log_View.append(url)
                 page_num = self.request_page(url)
                 #self.timer.start(int(page_num), self)
                 #self.progressBar.setRange(int(page_num),int(page_num))

                 page = int(page_num)
                 for x in range(page):
                     x +=1
                     percent = x * 100 / page


                     self.progressBar.setValue(percent)
                     QApplication.processEvents()


                     url = 'https://javgo.to/ko/search?keyword='+keyword+"&page="+str(x)
                     #url = 'https://javgo.to/ko/search?keyword=' + keyword
                     r = self.request_soup(url)

                     soup = BeautifulSoup(r.text, 'html.parser')

                        #ui.ListView.addItem("test")
                     titles = soup.find('div', 'box-item-list').find_all('div', 'title')
                     codes = soup.find('div', 'box-item-list').find_all('div', 'code')

                     value = []
                        # print(codes)

                     for title, code in zip(titles, codes):

                         QApplication.processEvents()


                            #self.ListView.addItem(code.txt)
                         self.listAddItem('['+code.text + '] ' + title.text)
                         QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
                        #    print(code.text)

        except Exception as e:
                print("")
    def listAddItem(self,item):

        self.ListView.addItem(item)

    def request_page(self,url):

      #  url = 'https://javgo.to/ko/search?keyword=' + keyword

        session = requests.session()
        r = session.get(url)

        soup = BeautifulSoup(r.text,'html.parser')

        page = soup.find('span', 'form-control-text')
        if page == None:
            page = 2
        else:
            page = page.getText()
            page = page.replace(' / ', '')


        return page

    def request_soup(self, url):
        #  url = 'https://javgo.to/ko/search?keyword=' + keyword

        session = requests.session()
        r = session.get(url)

        #soup = BeautifulSoup(r.text, 'html.parser')

        # print(code.text + '\n')
        # print(title.text)
        # x +=1
        return r

    def Rename(url):

        originNM = url.split('/')
        renameFile = originNM[len(originNM) - 1]
        return renameFile

    def selectItem(self):
        item = self.ListView.currentItem().text()


        item = item.split(" ")
        #item = item.replace("[","")
        #item = item.replace("]", "")
        item = item[0].replace('[', '')
        item = item.replace(']', '')
        url = 'https://javgo.to/ko/v/'+item
        ui.URL_Input.setText(url)
        #print(item)

    def thread_start(self):
        self.threadclass.start()

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

            per = round(time_ / duration * 100)
            sys.stdout.write("\rTranscoding...(%s%%) %s left [%s%s]" %
                             (per, datetime.timedelta(seconds=int(time_left)), '1' * per, '0' * (100 - per))
                             )

            # (per))
            sys.stdout.flush()



        def Rename(url):

            originNM = url.split('/')
            renameFile = originNM[len(originNM) - 1]
            return renameFile

        url = ui.URL_Input.text()
        if url != '':
            ui.Log_View.append("DownLoad Start!!")

            chrome_options = webdriver.ChromeOptions()
            chrome_options.headless = True
            driver = wired_webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            driver.get(url)
            title = Rename(url)
            title = title + '.mp4'

            # title = driver.title
            # title = title.split(" ")
            # title = title[1] + '.mp4'
            # path = os.path.join("C:", os.sep, "Users", "namsa", "OneDrive", "사진", "image", title)
            path = os.path.join(os.sep, title)
            #  path = Path(Path.cwd())
            # path = path.joinpath(path,title)
            while True:
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
                            # stream.output(path,monitor=monitor,encoding='utf-8')
                            # stream.output(path,monitor=monitor, encoding='utf-8')
                            stream.output(title, monitor=monitor, encoding='utf-8')
                            print("Finish!!")
                            sys.stdout.write("Finish!!")
                            sys.stdout.flush()

        else:
            None

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.searchButton.clicked.connect(ui.search)
    #ui.searchButton.clicked.connect(ui.doAction)
    ui.ListView.itemClicked.connect(ui.selectItem)
    ui.Play_Button.clicked.connect(ui.Play)

    MainWindow.show()
    sys.exit(app.exec_())
