import sys,DownYouTube,glob,img_qrc
from PyQt5.QtWidgets import QMainWindow, QApplication,QFileDialog,QWidget
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtCore import QCoreApplication,QPoint,pyqtProperty
import subprocess
import shutil
import os
from os import path

#pytube module Update
try:
    from pytube import __version__
    from pytube import YouTube, Stream
    from pytube.helpers import safe_filename
    from pytube.extract import video_id as get_video_id
    import pytube.exceptions as exceptions

except:
    subprocess.check_call([sys.executable, 'pip','install','--upgrade','pip'])
    subprocess.check_call([sys.executable, 'pip','freeze','>','pip_frozen.txt'])
    subprocess.check_call([sys.executable, 'pip','install','-r','pip_frozen.txt','--upgrade'])

    from pytube import __version__
    from pytube import YouTube, Stream
    from pytube.helpers import safe_filename
    from pytube.extract import video_id as get_video_id
    import pytube.exceptions as exceptions

class MainClass(QMainWindow,QWidget,DownYouTube.Ui_MainWindow):
    global url,yt
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showNormal()
        self.btn_Down.clicked.connect(self.Choose_Option)
        #msg=QMessageBox()
        #version = __version__
        #msg_version = QMessageBox.about(msg,"Pytube Version","Version : "+version)
        
    @pyqtSlot()
    def Choose_Option(self):
        if self.combo_Choose.currentText:
           print(self.combo_Choose.currentText())
           if str(self.combo_Choose.currentText()) == "MP3":
                self.DownMP3()
           else:
                self.DownMP4()
       
    def show(self):
        super().show()

    def restartWindow(self):
        QCoreApplication.quit()
        st = QProcess.startDetached(sys.executable, sys.argv)
    
    def closeEvent(self,event):
        msg = QMessageBox()
        select=QMessageBox.question(msg,"Quit","Do you Want to Quit?",QMessageBox.Yes | QMessageBox.No)
        if select == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def ProgressBar(self,stream:Stream, chunk:bytes, bytes_remaining:int)->None:
        global yt
        scale = float(0.55)
        filesize =stream.filesize
        bytes_received = filesize - bytes_remaining
        columns = shutil.get_terminal_size().columns
        max_width = int(columns * scale)

        KB = float(1024)
        MB = float(KB ** 2)

        self.lbl_Downbytes.setText("Down bytes : "+"("+str(round((bytes_received/MB),2))+"MB"+"/"+str(round((filesize/MB),2))+"MB"+")")
        filled = int(round(max_width * bytes_received/ float(filesize)))
        remaining = max_width - filled
        percent = round(100.0 * bytes_received / float(filesize), 1)

        completed = 0
        while completed < 100:
            self.Progress.setProperty("value",int(percent))
            QApplication.processEvents()
            completed +=0.55

        QApplication.processEvents()
    
    def DownMP3(self):
        global url,yt
        url = self.tbx_URL.text()
        yt = YouTube(url)
        yt.register_on_progress_callback(self.ProgressBar)
        stream = yt.streams.first()
        yt_streams_mp3 = yt.streams.filter(only_audio=True)\
            .first()

        self.tbx_Status.setText(str(yt_streams_mp3) + " MP3 File Downloading..")

        SaveDir = QFileDialog.getExistingDirectory(self,"Save File")
        
        outMP3 = yt_streams_mp3.download(output_path=str(SaveDir))
        
        default_fileName = yt_streams_mp3.default_filename
        
        mp3_fileName = default_fileName[0:-3] + "mp3"

        default_path = os.path.join(SaveDir, default_fileName)

        subprocess.call(['ffmpeg','-y','-i',
                         os.path.join(SaveDir, default_fileName), 
                         os.path.join(SaveDir, mp3_fileName)])

        self.tbx_Status.setText("MP3 Download Success!")
        QMessageBox.information(self,"Success","File Download Success!")

        os.remove(default_path)
            
    def DownMP4_Video(self): 
        global url,yt,yt_streams_mp4,re_Video,SaveDir,base
        url = self.tbx_URL.text()
        yt = YouTube(url)
        yt.register_on_progress_callback(self.ProgressBar)

        try:
            if yt.streams.get_by_itag(137):
                QMessageBox.information(self,"Notice","1080p resolution\n continue the download?",QMessageBox.Ok)
                if QMessageBox.Ok:
                    yt_streams_mp4 = yt.streams.filter(adaptive=True,file_extension='mp4').first()

            else:
                QMessageBox.information(self,"Notice","Load Failed resolution 720p\n continue the download?",QMessageBox.Ok)
                if QMessageBox.Ok:
                    yt_streams_mp4 = yt.streams.filter(progressive=True,file_extension='mp4')\
                     .first()
        except:
            pass

        self.tbx_Status.setText(str(yt_streams_mp4) + " MP4 File Downloading..")

        SaveDir = QFileDialog.getExistingDirectory(self,"Save File")
        
        outMP4 = yt_streams_mp4.download(output_path=str(SaveDir))

        if os.path.isfile(str(outMP4)):
            base,ext = os.path.splitext(outMP4)
            re_Video = base+"_Video.mp4"
            os.rename(outMP4, re_Video)
        
        self.tbx_Status.setText("Video Download Success! \n Next Step")

        return re_Video

    def DownMP4_Audio(self): 
        global url,yt,yt_streams_audio,re_Audio,SaveDir
        url = self.tbx_URL.text()
        yt = YouTube(url)
        yt.register_on_progress_callback(self.ProgressBar)

        Dash_list = yt.streams.filter(adaptive=True)
        self.tbx_Status.setText(str(Dash_list))

        try:
            if yt.streams.get_by_itag(140):
                yt_streams_audio = yt.streams.filter(only_audio=True,abr='128kbps').first()
        except:
            pass
         
        self.tbx_Status.setText(str(yt_streams_audio) + "\n Audio File Downloading..")

        #SaveDir = QFileDialog.getExistingDirectory(self,"Save File")

        outAudio = yt_streams_audio.download(output_path=str(SaveDir))
       
        if os.path.isfile(str(outAudio)):
            base,ext = os.path.splitext(outAudio)
            re_Audio = base+"_Audio.mp4"
            os.rename(outAudio, re_Audio)

        self.tbx_Status.setText("Audio Download Success! \n Next Step")

        return re_Audio

    def DownMP4(self):
        global url,yt,re_Video,re_Audio,SaveDir,base
        self.DownMP4_Video()
        self.DownMP4_Audio()

        self.tbx_Status.setText(" MP4 File Downloading..")
        base_file = base + ".mp4"
        subprocess.call(['ffmpeg','-i',
                         os.path.join(SaveDir, re_Video),'-i',
                         os.path.join(SaveDir, re_Audio),'-c','copy',os.path.join(SaveDir, base_file)])

        if os.path.isfile(str(base_file)):
            os.remove(re_Video)
            os.remove(re_Audio)

        self.tbx_Status.setText("MP4 File Download Success!")
        QMessageBox.information(self,"Success","File Download Success!")
    
if __name__ =="__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    win = MainClass()
    win.show()
    sys.exit(app.exec_())