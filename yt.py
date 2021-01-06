from pytube import YouTube
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtSql, uic, QtCore
import sys, urllib, os
import webbrowser
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap, QMovie, QImage
import ffmpeg

class YtDetailThread(QThread):
    ytsgl = QtCore.pyqtSignal(str,bytes)
    ytsglException = QtCore.pyqtSignal(str)

    def __init__(self):
        super(YtDetailThread, self).__init__()
        self.yt_url = ''
        self.yt_title = ''
        self.yt_thumbnail = ''

    @pyqtSlot(str, bytes)
    def run(self):
        try:
            self.yt_title = self.getyttitle(self.yt_url)
            self.yt_thumbnail = self.getytthumbnail(self.yt_url)
            self.ytsgl.emit(self.yt_title, self.yt_thumbnail)
        except:
            self.ytsglException.emit(str(sys.exc_info()[1]))

    def getytthumbnail(self, url):
        yt = YouTube(url)
        tempurl = 'https://i.ytimg.com/vi/'+yt.video_id+'/default.jpg'
        return urllib.request.urlopen(tempurl).read()

    def getyttitle(self, url):
        yt = YouTube(url)
        return yt.title

########################################################################


class YtDownloadThread(QThread):
    ytdwldsgl = QtCore.pyqtSignal(float)
    ytDownloadException = QtCore.pyqtSignal(str)

    filesize = 0

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
        yt.register_on_progress_callback(self.progress_bar)

        try:
            if qual == "Best Available":
                stream = yt.streams.filter(progressive = True, file_extension = "mp4").first()
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif qual == "1080-Video-Only":
                itag = 137
                stream = yt.streams.get_by_itag(itag)
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif qual == "720p-Video-Only":
                itag = 136
                stream = yt.streams.get_by_itag(itag)
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif qual == "480p-Video-Only":
                itag = 135
                stream = yt.streams.get_by_itag(itag)
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif qual == "360p-Dual":
                itag = 134
                stream = yt.streams.get_by_itag(itag)
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif qual == "Audio-Only-50kbps":
                itag = 249
                stream = yt.streams.get_by_itag(itag)
                self.filesize = stream.filesize
                stream.download(self.yt_savepath)
            elif qual == "Audio-Only-Best":
                stream = yt.streams.filter(type = "audio").first()
        except:
            self.ytDownloadException.emit(str(sys.exc_info()[1]))

    def progress_bar(self, chunk, file_handle, bytes_remaining):
        remaining = (100 * bytes_remaining) / self.filesize
        step = 100 - int(remaining)
        self.ytdwldsgl.emit(step)


##################################################################

class MyWindow(QMainWindow):

    yturl = ""
    ytviews = ""
    ytlength = ""

    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('main.ui', self)
        self.temp = 0
        self.ytthread = YtDetailThread()
        self.ytthread.ytsgl.connect(self.finished)
        self.ytthread.ytsglException.connect(self.exceptionhandle)

        self.ytdwlthread = YtDownloadThread()
        self.ytdwlthread.ytdwldsgl.connect(self.processdwld)
        self.ytdwlthread.ytDownloadException.connect(self.exceptionhandle)

        self.savepath = os.path.expanduser("~\Desktop")
        self.locationpath.setText(self.savepath)
        self.dwnld.setEnabled(False)
        self.show()


    @pyqtSlot()
    def on_fetchbtn_clicked(self):
        self.temp = 0
        self.progressBar.setValue(0)
        self.ytthread.yt_url = self.urlinput.text()
        self.console.append("<span style='color:red'>Initializing links..</span>")
        movie = QMovie("icon/loading.gif")
        self.thumbnail.setMovie(movie)
        movie.start()
        self.console.append("URL " + str(self.ytthread.yt_url))
        self.console.append("Waiting for response ..........")
        self.ytthread.start()

    @pyqtSlot()
    def on_savelocationbtn_clicked(self):
        self.savepath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.locationpath.setText(self.savepath)

    @QtCore.pyqtSlot()
    def on_dwnld_clicked(self):
        self.console.append("Starting download....")
        self.console.append("<span style='color:orange'>If downloading not start in few 10 seconds try <b>Best Available</b> in Quality</span>")
        self.ytdwlthread.yt_url = self.urlinput.text()
        self.ytdwlthread.yt_savepath = self.savepath
        self.ytdwlthread.yt_quality = self.qualitycheck.itemText(self.qualitycheck.currentIndex())
        self.ytdwlthread.start()

    def finished(self, yttitle,ytthumbnail):
        self.ytitle.setText(yttitle)  # Show the output to the user
        self.console.append("Response received!")
        image = QImage()
        image.loadFromData(ytthumbnail)

        rect = QRect(0,12,120,66)
        image = image.copy(rect)

        self.thumbnail.setPixmap(QPixmap(image))
        self.dwnld.setEnabled(True)

    def processdwld(self, dwnld):
        self.progressBar.setValue(dwnld)
        if dwnld >= 100 and self.temp == 0:
            self.temp = self.temp + 1
            self.downloadcomplete()

    def exceptionhandle(self, msg):
        self.console.append("<span style='color:red'>Exception : " + msg + " </span>")
        self.thumbnail.setPixmap(QPixmap("icon/failed.jpg"))

    def downloadcomplete(self):
        self.console.append("<span style='color:green'>Downloading Complete :)</span>")
        self.dwnld.setEnabled(False)
        self.progressBar.setValue(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
