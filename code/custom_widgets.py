from tkinter.tix import Select

from PyQt6.QtCore import QUrl, pyqtProperty, Qt
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QWidget, QLabel


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
