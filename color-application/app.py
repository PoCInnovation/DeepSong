import sys
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6 import uic
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QColor
from src.verifier import verifyPath
from src.classes import DeepSongApp
import pygame

def linkButtons(app : DeepSongApp):

    # Connect buttons
    app.window.closeButton.clicked.connect(app.closeApp)
    app.window.ValidateButton.clicked.connect(lambda: verifyPath(app))
    app.window.browse.clicked.connect(app.browsefiles)
    app.window.PlayButton.clicked.connect(lambda: app.playSong())
    app.window.PauseButton.clicked.connect(lambda: app.pauseSong())
    app.window.StopButton.clicked.connect(lambda: app.stopSong())
    app.window.radioButtonHarmonics.toggled.connect(lambda: app.setPlayType("harmonics"))
    app.window.radioButtonPercussives.toggled.connect(lambda: app.setPlayType("percussives"))
    app.window.radioButtonBeatTrack.toggled.connect(lambda: app.setPlayType("beattrack"))

    # Hide errors
    app.window.fileLoadingLabel.hide()
    app.window.FileLoadingProgressBar.hide()
    app.window.labelErrorMode.hide()
    app.window.NoMusicLoadedErrorLabel.hide()

    # add style
    app.shadow_effect = QGraphicsDropShadowEffect(
        offset=QPointF(0, 0), blurRadius=9.0, color=QColor("#88f")
    )
    app.window.circle.setStyleSheet(f"background-color: #88f;border: 1px solid gray;border-radius: 110px;")
    app.window.circle.setGraphicsEffect(app.shadow_effect)


def show_application():
 
    # pygame for audio
    pygame.init()

    app = DeepSongApp(sys.argv)
    app.initMainWindow()
    uic.loadUi("template/mainwindow.ui", app.window)
    app.window.show()
    linkButtons(app=app)
    app.exec()


if __name__ == '__main__':
    show_application()
