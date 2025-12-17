from PyQt6.QtCore import QUrl, pyqtProperty, Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSlider, QDialog, QComboBox


class QLabel_clickable(QLabel):
    clicked=pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
class Settings(QDialog):
    def __init__(self,icon,audioPlayer,SoundPlayer,tracks, parent=None):
        super().__init__(parent)
        self.setGeometry(parent.width()//2+50, parent.height()//2, 100, 300)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(icon))

        self.MusicLabel=QLabel("Music volume :")
        self.MusicLabel.setObjectName("SettingsLabel")
        self.musicSlider = QSlider(Qt.Orientation.Horizontal)
        self.musicSlider.setObjectName("settingsSlider")
        self.musicSlider.setRange(0,100)
        self.musicSlider.setValue(100)
        self.musicSlider.valueChanged.connect(lambda: self.SliderValuesChanged())
        self.SoundLabel=QLabel("Sound effect volume :")
        self.SoundLabel.setObjectName("SettingsLabel")
        self.soundSlider = QSlider(Qt.Orientation.Horizontal)
        self.soundSlider.setObjectName("settingsSlider")
        self.soundSlider.setRange(0, 100)
        self.soundSlider.setValue(100)
        self.soundSlider.valueChanged.connect(lambda : self.SliderValuesChanged())
        self.mainLayout = QVBoxLayout()
        self.TracksLabel=QLabel("Switch tracks :")
        self.TracksLabel.setObjectName("SettingsLabel")
        self.tracksSelecter = QComboBox()
        self.tracksSelecter.addItems(tracks)
        self.tracksSelecter.currentIndexChanged.connect(lambda : self.changeTracks())
        self.mainLayout.addWidget(self.MusicLabel)
        self.mainLayout.addWidget(self.musicSlider)
        self.mainLayout.addWidget(self.SoundLabel)
        self.mainLayout.addWidget(self.soundSlider)
        self.mainLayout.addWidget(self.TracksLabel)
        self.mainLayout.addWidget(self.tracksSelecter)
        self.audioPlayer=audioPlayer
        self.SoundPlayer=SoundPlayer
        self.mainLayout.addStretch()
        self.setLayout(self.mainLayout)


    def SliderValuesChanged(self):
        self.audioPlayer.SetVolume(self.musicSlider.value()/100)
        self.SoundPlayer.SetVolume(self.soundSlider.value()/100)

    def changeTracks(self):
        self.audioPlayer.playAt(self.tracksSelecter.currentIndex())


class AudioPlayer(QWidget):
    def __init__(self,audioSources,trackNames,parent=None):
        super().__init__(parent)
        self.audio_output = QAudioOutput()
        # QMediaPlayer handles loading and controlling playback of audio or video
        self.player = QMediaPlayer()
        # Connect the player to the audio output (so sound can actually play)
        self.player.setAudioOutput(self.audio_output)
        self.sounds = audioSources
        self.trackNames = trackNames
        self.selected=0
        self.player.setSource(QUrl.fromLocalFile(self.sounds[0]))
        self.audio_output.setVolume(1)
    def CurrentTrack(self):
        return self.trackNames[self.selected]
    def AllTracks(self):
        return self.trackNames
    def SetVolume(self,vol):
        self.audio_output.setVolume(vol)
    def SelectTrack(self,track):
        if track>=len(self.sounds):
            return
        self.selected = track
        self.player.setSource(QUrl.fromLocalFile(self.sounds[track]))
    def play(self):
        if self.player.mediaStatus() != QMediaPlayer.MediaStatus.NoMedia:
            self.player.play()
    def playAt(self,index):
        self.SelectTrack(index)
        self.play()
    def stop(self):
        self.player.stop()

"""
Handles the redrawing of the pixmap to simulate a cardflip
Defines Handlers for QPropertyanimations()
"""
class FlippableCard(QLabel):
    def __init__(self, front: QPixmap, back: QPixmap,parent=None):
        super().__init__(parent)
        self.front = front
        self.back = back
        self._flip = 0.0
        self.setFixedSize(front.size())

    @pyqtProperty(float)
    def flip(self):
        return self._flip

    @flip.setter
    def flip(self, value: float):
        self._flip = value
        if value <= 0.5:
            scale = 1.0 - (value * 2)
            pixmap = self.front
        else:
            scale = (value - 0.5) * 2
            pixmap = self.back
        new_width = int(pixmap.width() * scale)
        scaled = pixmap.scaled(new_width, pixmap.height())

        # center offset
        x_offset = (self.width() - new_width) // 2
        result = QPixmap(self.size())
        result.fill(Qt.GlobalColor.transparent)
        painter = QPainter(result)
        painter.drawPixmap(x_offset, 0, scaled)
        painter.end()
        self.setPixmap(result)
