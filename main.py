import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QSlider, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl, QTimer


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.setGeometry(100, 100, 500, 200)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.mediaStatusChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        layout = QVBoxLayout()

        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.playClicked)
        layout.addWidget(self.playButton)

        self.stopButton = QPushButton("Stop")
        self.stopButton.clicked.connect(self.stopClicked)
        layout.addWidget(self.stopButton)

        self.seekSlider = QSlider(Qt.Horizontal)
        self.seekSlider.sliderMoved.connect(self.seekChanged)
        layout.addWidget(self.seekSlider)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.setTickPosition(QSlider.TicksBelow)
        self.volumeSlider.valueChanged.connect(self.changeVolume)
        layout.addWidget(self.volumeSlider)

        self.songLabel = QLabel("No song selected")
        layout.addWidget(self.songLabel)

        self.openButton = QPushButton("Open")
        self.openButton.clicked.connect(self.openFile)
        layout.addWidget(self.openButton)

        self.positionLabel = QLabel("00:00")
        layout.addWidget(self.positionLabel)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePosition)

    def playClicked(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def stopClicked(self):
        self.mediaPlayer.stop()

    def changeVolume(self, value):
        self.mediaPlayer.setVolume(value)

    def mediaStateChanged(self, state):
        if state == QMediaPlayer.LoadedMedia:
            self.songLabel.setText(self.mediaPlayer.media().canonicalUrl().fileName())
            self.seekSlider.setMaximum(self.mediaPlayer.duration())
            self.timer.start(1000)
        elif state == QMediaPlayer.EndOfMedia:
            self.stopClicked()

    def positionChanged(self, position):
        self.seekSlider.setValue(position)
        self.positionLabel.setText(self.formatTime(position))

    def durationChanged(self, duration):
        self.seekSlider.setMaximum(duration)

    def updatePosition(self):
        position = self.mediaPlayer.position()
        self.positionLabel.setText(self.formatTime(position))
        self.seekSlider.setValue(position)

    def seekChanged(self, value):
        self.mediaPlayer.setPosition(value)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Music File", "", "Audio Files (*.mp3 *.ogg *.wav)")
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))

    def formatTime(self, millis):
        seconds = millis // 1000
        minutes, seconds = divmod(seconds, 60)
        return "{:02d}:{:02d}".format(minutes, seconds)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec_())
