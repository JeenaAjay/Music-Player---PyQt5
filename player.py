import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QTimer
import random, time
from pygame import mixer
from mutagen.mp3 import MP3
import style

musicList = []
mixer.init()
muted = False
count = 0
songLength = 0
index = 0


class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(550, 150, 480, 700)
        self.setWindowTitle("Music Player")
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ########################Top Layer Widgets##############################
        self.progressBar = QProgressBar()
        self.progressBar.setStyleSheet(style.progressBarStyle())
        self.progressBar.setTextVisible(False)
        self.songTimerLabel = QLabel("0:00")
        self.songLengthLabel = QLabel("/ 0:00")
        #####################Middle layer widgets##############################
        self.addBtn = QToolButton()
        self.addBtn.setIcon(QIcon("icons/add.png"))
        self.addBtn.setIconSize(QSize(48, 48))
        self.addBtn.setToolTip("Add a song")
        self.addBtn.clicked.connect(self.addSound)

        self.shuffleBtn = QToolButton()
        self.shuffleBtn.setIcon(QIcon("icons/shuffle.png"))
        self.shuffleBtn.setIconSize(QSize(48, 48))
        self.shuffleBtn.setToolTip("Shuffle the list")
        self.shuffleBtn.clicked.connect(self.shuffleSound)

        self.prevBtn = QToolButton()
        self.prevBtn.setIcon(QIcon("icons/previous.png"))
        self.prevBtn.setIconSize(QSize(48, 48))
        self.prevBtn.setToolTip("Play previous")
        self.prevBtn.clicked.connect(self.playPrevious)

        self.playBtn = QToolButton()
        self.playBtn.setIcon(QIcon("icons/play.png"))
        self.playBtn.setIconSize(QSize(64, 64))
        self.playBtn.setToolTip("Play")
        self.playBtn.clicked.connect(self.playSound)

        self.nextBtn = QToolButton()
        self.nextBtn.setIcon(QIcon("icons/next.png"))
        self.nextBtn.setIconSize(QSize(48, 48))
        self.nextBtn.setToolTip("Play next")
        self.nextBtn.clicked.connect(self.playNext)

        self.muteBtn = QToolButton()
        self.muteBtn.setIcon(QIcon("icons/mute.png"))
        self.muteBtn.setIconSize(QSize(24, 24))
        self.muteBtn.setToolTip("Mute")
        self.muteBtn.clicked.connect(self.muteSound)

        self.volSlider = QSlider(Qt.Horizontal)
        self.volSlider.setToolTip("Volume")
        self.volSlider.setValue(70)
        self.volSlider.setMinimum(0)
        self.volSlider.setMaximum(100)
        mixer.music.set_volume(0.7)             # because range of vol in mixer is 0 to 1
        self.volSlider.valueChanged.connect(self.setVolume)

        ############################Bottom layer widgets#######################
        self.playList = QListWidget()
        self.playList.doubleClicked.connect(self.playSound)
        self.playList.setStyleSheet(style.playListStyle())

        #################################Timer#################################
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateProgressbar)


    def addSound(self):
        directory = QFileDialog.getOpenFileName(self, "Add Sound", "", "Sound Files (*.mp3 *.ogg *.wav")
        self.filename = os.path.basename(directory[0])
        self.playList.addItem(self.filename)
        musicList.append(directory[0])

    def shuffleSound(self):
        random.shuffle(musicList)
        self.playList.clear()
        for song in musicList:
            filename = os.path.basename(song)
            self.playList.addItem(filename)

    def playSound(self):
        global index
        global songLength
        global count
        count = 0
        index = self.playList.currentRow()
        # print(musicList[index])
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            name = str(musicList[index])
            sound = MP3(name)
            songLength = sound.info.length
            songLength = round(songLength)
            print(songLength)
            # self.progressBar.setMaximum(4)
            min,sec = divmod(songLength,60)                             # converts seconds into min & sec

            self.songLengthLabel.setText("/ "+str(min)+":"+str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)

        except:
            pass

    def playPrevious(self):
        global index
        global songLength
        global count
        count = 0
        items = self.playList.count()

        if index == 0:
            index = items

        index -= 1

        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            name = str(musicList[index])
            sound = MP3(name)
            songLength = sound.info.length
            songLength = round(songLength)
            print(songLength)
            # self.progressBar.setMaximum(4)
            min, sec = divmod(songLength, 60)

            self.songLengthLabel.setText("/ " + str(min) + ":" + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)

        except:
            pass

    def playNext(self):
        global index
        global songLength
        global count
        count = 0
        items = self.playList.count()
        index += 1

        if index == items:
            index = 0

        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            name = str(musicList[index])
            sound = MP3(name)
            songLength = sound.info.length
            songLength = round(songLength)
            print(songLength)
            # self.progressBar.setMaximum(4)
            min, sec = divmod(songLength, 60)

            self.songLengthLabel.setText("/ " + str(min) + ":" + str(sec))
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)

        except:
            pass

    def setVolume(self):
        self.volume = self.volSlider.value()
        # print(self.volume)
        mixer.music.set_volume(self.volume/100)

    def muteSound(self):
        global muted
        if muted == False:
            self.newvolume = self.volSlider.value()
            mixer.music.set_volume(0.0)
            self.volSlider.setValue(0)
            self.muteBtn.setIcon(QIcon("icons/unmuted.png"))
            self.muteBtn.setToolTip("Unmute")
            muted = True

        else:
            mixer.music.set_volume(self.newvolume/100)
            self.volSlider.setValue(self.newvolume)
            self.muteBtn.setIcon(QIcon("icons/mute.png"))
            self.muteBtn.setToolTip("Mute")
            muted = False

    def updateProgressbar(self):
        global count
        global songLength
        count += 1
        self.progressBar.setValue(count)
        self.songTimerLabel.setText(time.strftime("%M:%S",time.gmtime(count)))
        if count == songLength:
            self.timer.stop()

    def layouts(self):
        ################################Layouts#################################
        self.mainLayout = QVBoxLayout()
        self.topMainLayout = QVBoxLayout()
        self.topGroupBox = QGroupBox("Music Player")
        self.topGroupBox.setStyleSheet(style.GroupBoxStyle())            # Calling a function outside our class

        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()

        self.topMainLayout.addLayout(self.topLayout)
        self.topMainLayout.addLayout(self.middleLayout)
        self.topGroupBox.setLayout(self.topMainLayout)
        self.mainLayout.addWidget(self.topGroupBox, 25)
        self.mainLayout.addLayout(self.bottomLayout, 75)
        self.setLayout(self.mainLayout)

        ###############################Adding widgets###########################
        #############################Top layer widgets##########################
        self.topLayout.addWidget(self.progressBar)
        self.topLayout.addWidget(self.songTimerLabel)
        self.topLayout.addWidget(self.songLengthLabel)

        ###########################Middle layer widgets#########################
        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.addBtn)
        self.middleLayout.addWidget(self.shuffleBtn)
        self.middleLayout.addWidget(self.playBtn)
        self.middleLayout.addWidget(self.prevBtn)
        self.middleLayout.addWidget(self.nextBtn)
        self.middleLayout.addWidget(self.volSlider)
        self.middleLayout.addWidget(self.muteBtn)
        self.middleLayout.addStretch()

        ######################Bottom layer widgets##############################
        self.bottomLayout.addWidget(self.playList)



def main():
    App = QApplication(sys.argv)
    window = Player()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()

