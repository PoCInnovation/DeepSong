from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsDropShadowEffect
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QUrl, QThread
from src.verifier import verifyPath
from librosa import load, get_duration, frames_to_time
from librosa.beat import beat_track
from librosa.effects import harmonic, percussive
from threading import Thread
from time import sleep
import random
import pygame

class DeepSongApp(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.path = ""
        self.window = None
        self.music = None
        self.beat_track = None
        self.harmonics = None
        self.percussives = None
        self.duration : int = 0
        self.playing : bool = False
        self.thread_play : Thread = None
        self.pause : bool = False
        self.playInfoType = None
        self.loading_lvl : int = 0
        self.shadow_effect : QGraphicsDropShadowEffect = None

    def initMainWindow(self):
        self.window = QMainWindow()

    def initQMediaPlayer(self):
        pygame.mixer.music = QMediaPlayer()

    def setPath(self, path : str):
        self.path = path

    def getPath(self):
        return self.path

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self.window, 'Open file', '~')
        self.window.AudioLineEdit.setText(fname[0])
        verifyPath(self)

    def loadData(self, fn):
        fn()
        self.loading_lvl += 20
        self.window.FileLoadingProgressBar.setValue(self.loading_lvl)

    def loadBeatTrack(self):
        self.beat_track = frames_to_time(beat_track(y=self.music[0], sr=self.music[1])[1], sr=self.music[1])

    def loadHarmonics(self):
        self.harmonics = frames_to_time(beat_track(y=harmonic(y=self.music[0]), sr=self.music[1])[1], sr=self.music[1])

    def loadPercussions(self):
        self.percussives = frames_to_time(beat_track(y=percussive(y=self.music[0]), sr=self.music[1])[1], sr=self.music[1])

    def loadFile(self):
        self.loading_lvl = 0
        self.window.FileLoadingProgressBar.setValue(0)
        self.window.fileLoadingLabel.setText("Loading file into music sequence...")
        self.music = load(path=self.path, sr=None)
        self.window.FileLoadingProgressBar.setValue(20)
        self.loading_lvl = 20
        self.window.fileLoadingLabel.setText("Loading harmonics, percussives, beattrack with Threads...")

        ## Thread Loading ##
        loadBeatTrackThread = Thread(target=self.loadData, args=(self.loadBeatTrack,))
        loadHarmonicsThread = Thread(target=self.loadData, args=(self.loadHarmonics,))
        loadPercussivesThread = Thread(target=self.loadData, args=(self.loadPercussions,))

        loadBeatTrackThread.start()
        loadHarmonicsThread.start()
        loadPercussivesThread.start()
        loadBeatTrackThread.join()
        loadHarmonicsThread.join()
        loadPercussivesThread.join()

        pygame.mixer.music.load(self.path)

        self.duration = get_duration(y=self.music[0], sr=self.music[1])
        self.window.FileLoadingProgressBar.setValue(100)
        self.window.NoMusicLoadedErrorLabel.hide()
        self.window.fileLoadingLabel.setText("File loaded with librosa")


    def playInThread(self):
        
        seconds = 0
        r_c = lambda : hex(random.randint(6, 13)).replace("0x", "")
        next = 0

        pygame.mixer.music.play()
        while (self.playing and round(seconds / 1000, 3) < self.duration):

            color = None

            if (self.playInfoType == "harmonics" and len(self.harmonics) > next and round(seconds / 1000, 3) == round(self.harmonics[next], 3)):
                color = f"#{r_c()}{r_c()}{r_c()}"

            if (self.playInfoType == "beattrack" and len(self.beat_track) > next and round(seconds / 1000, 3) == round(self.beat_track[next], 3)):
                color = f"#{r_c()}{r_c()}{r_c()}"

            if (self.playInfoType == "percussives" and len(self.percussives) > next and round(seconds / 1000, 3) == round(self.percussives[next], 3)):
                color = f"#{r_c()}{r_c()}{r_c()}"

            if (color):
                self.shadow_effect.setColor(QColor(color))
                self.window.circle.setStyleSheet(f"background-color: {color};border: 1px solid gray;border-radius: 110px;")
                next += 1

            self.window.progressBar.setValue(int((round(seconds / 1000, 3) / self.duration) * 100))
            seconds += 1
            sleep(0.001)
            u = True
            while (self.pause):
                if (u):
                    pygame.mixer.music.pause()
                u = False
                continue


    def playSong(self):

        if (self.pause):
            self.pause = False
            pygame.mixer.music.unpause()

        if (not(self.music)):
            self.window.NoMusicLoadedErrorLabel.show()

        if (not(self.playInfoType)):
            self.window.labelErrorMode.show()

        if (self.music and (not(self.thread_play) or not(self.thread_play.is_alive())) and self.playInfoType):
            self.playing = True
            self.thread_play = Thread(target=self.playInThread, args=())
            self.thread_play.start()

    def closeApp(self):
        self.window.close()
        self.playing = False

    def pauseSong(self):
        self.pause = True

    def setPlayType(self, newType):
        self.playInfoType = newType
        self.window.labelErrorMode.hide()

    def stopSong(self):
        self.pause = False
        self.playing = False
        self.window.circle.setStyleSheet(f"background-color: #88f;border: 1px solid gray;border-radius: 110px;")
        self.window.progressBar.setValue(0)
