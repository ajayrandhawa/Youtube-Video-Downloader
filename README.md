# Blackcat Youtube Downloader

Blackcat Youtube Downloader is Open Source GUI tool to download Youtube video. It is Developed with Python, Qt, and Pytube Library. It is Multi-thread Application. Best Available Option download video in highly available Quality . Download Videos in 720p, 480p,  360p etc. 

## Features

1. Graphical User Interface.
2. Multi-Threaded.
3. Fetch Title & Thumbnail.
4. High Quality Video Download.
5. Playlist Download (Soon...)

| Wireframe | Screenshot |
| --------------------- | -------------------- |
| <img src="mock.png"> | <img src="logo.png"> |

### Code

```
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtSql, uic, QtCore
import sys, urllib, os
import webbrowser
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap, QMovie, QImage
from pytube import YouTube

class YtDetailThread(QThread):
    ytsgl = QtCore.pyqtSignal(str,bytes)

    def __init__(self):
        super(YtDetailThread, self).__init__()
        self.yt_url = ""
        self.yt_title = ""
        self.yt_thumbnail = ""


    @pyqtSlot(str,bytes)
    def run(self):
        self.getytdetails(self.yt_url)
        yttitle = self.yt_title
        ytthumbnail = self.yt_thumbnail
        self.ytsgl.emit(yttitle,ytthumbnail)


    def getytdetails(self, url):

        yt = YouTube(url)
        self.yt_title = yt.title

        yturl = yt.thumbnail_url
        self.yt_thumbnail = urllib.request.urlopen(yturl).read()

########################################################################

class YtDownloadThread(QThread):
    ytdwldsgl = QtCore.pyqtSignal(str)

    def __init__(self):
        super(YtDownloadThread, self).__init__()
        self.yt_url = ""
        self.yt_savepath = ""
        self.yt_quality = ""

    @pyqtSlot(str)
    def run(self):
        self.downloadyt(self.yt_url,self.yt_savepath, self.yt_quality)

    def downloadyt(self, url, pth, qual):

        yt = YouTube(url)

        if(qual == "Best Available"):
            stream = yt.streams.filter(progressive = True, file_extension = "mp4").first()
            stream.download()
            print("Downloaded")
        elif(qual == "720p"):
            itag = 22
        elif (qual == "360p"):
            itag = 18
        elif (qual == "Audio Only"):
            stream = yt.streams.filter(only_audio=True).first()
            stream.download()
            print("Downloaded")


##################################################################

class MyWindow(QMainWindow):

    yturl = ""
    ytviews = ""
    ytlength = ""

    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('main.ui', self)
        self.ytthread = YtDetailThread()
        self.ytthread.ytsgl.connect(self.finished)

        self.ytdwlthread = YtDownloadThread()
        self.ytdwlthread.ytdwldsgl.connect(self.processdwld)

        self.savepath = os.path.expanduser("~/Desktop")
        self.locationpath.setText(self.savepath)
        self.dwnld.setEnabled(False)
        self.show()

    @pyqtSlot()
    def on_gitbtn_clicked(self):
        webbrowser.open('https://github.com/ajayrandhawa')

    @pyqtSlot()
    def on_ytbtn_clicked(self):
        webbrowser.open('https://www.youtube.com/channel/UCn8h0PL1p8gGPYUwKpx49YQ')

    @pyqtSlot()
    def on_linkedbtn_clicked(self):
        webbrowser.open('https://www.linkedin.com/in/ajaypalsinghrandhawa')

    @pyqtSlot()
    def on_fetchbtn_clicked(self):
        self.ytthread.yt_url = self.urlinput.text()
        self.console.append("Initializing Links..")
        movie = QMovie("icon/loading.gif")
        self.thumbnail.setMovie(movie)
        movie.start()
        self.console.append("URL " + str(self.ytthread.yt_url))
        self.console.append("Waiting For Response ..........")
        self.ytthread.start()


    @pyqtSlot()
    def on_saveLocationbtn_clicked(self):
        self.savepath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.locationpath.setText(self.savepath);

    @QtCore.pyqtSlot()
    def on_dwnld_clicked(self):
        self.ytdwlthread.yt_url = self.urlinput.text()
        self.ytdwlthread.yt_savepath = self.savepath
        self.ytdwlthread.yt_quality = self.qualitycheck.itemText(self.qualitycheck.currentIndex())

        self.ytdwlthread.start()

    def finished(self, yttitle,ytthumbnail):
        self.ytitle.setText(yttitle)  # Show the output to the user
        self.console.append("Response Received!")
        image = QImage()
        image.loadFromData(ytthumbnail)

        rect = QRect(0,12,120,66)
        image = image.copy(rect)

        self.thumbnail.setPixmap(QPixmap(image))

        self.dwnld.setEnabled(True)

    def processdwld(self, dwnld):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())

```

### Under Development :)
#### Happy Open Source......
