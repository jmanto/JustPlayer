import os.path
import math
import glob

from PyQt5 import QtWidgets, QtMultimedia, QtMultimediaWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.duration = 0
        self.position = 0

        self.setWindowTitle("JustPlayer")
        self.setWindowIcon(QtGui.QIcon('assets/JustPlayer.png'))

        self.open_icon = self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon)
        self.openDir_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon)

        self.play_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay)
        self.pause_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause)
        self.stop_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop)

        self.previous_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaSkipBackward)
        self.next_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaSkipForward)
        self.seekBW_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekBackward)
        self.seekFW_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekForward)

        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.player = QtMultimedia.QMediaPlayer()

        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        self.toolbar = QtWidgets.QToolBar()

        # ACTIONS
        self.act_open = self.toolbar.addAction(self.open_icon, "Open File")
        self.act_openDir = self.toolbar.addAction(self.openDir_icon, "Open Directory")

        self.act_play = self.toolbar.addAction(self.play_icon, "Play")

        self.act_previous = self.toolbar.addAction(self.previous_icon, "Previous")
        self.act_seekBW = self.toolbar.addAction(self.seekBW_icon, "Move Backward")
        self.act_stop = self.toolbar.addAction(self.stop_icon, "Stop")
        self.act_pause = self.toolbar.addAction(self.pause_icon, "Pause")
        self.act_seekFW = self.toolbar.addAction(self.seekFW_icon, "Move Forward")
        self.act_next = self.toolbar.addAction(self.next_icon, "Next")


    def modify_widgets(self):
        self.positionSlider.setRange(0, 0)
        self.positionSlider.setStyleSheet("""
                                            background-color: black;
                                            height: 20px;
                                            width: 40px;
                                            """)

    def create_layouts(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

    def add_widgets_to_layouts(self):
        self.addToolBar(self.toolbar)

        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)

        self.layout.addWidget(self.video_widget)
        self.layout.addWidget(self.positionSlider)

        self.player.setVideoOutput(self.video_widget)
        wid.setLayout(self.layout)

    def setup_connections(self):
        self.act_open.triggered.connect(self.open)
        self.act_openDir.triggered.connect(self.openDir)

        self.act_play.triggered.connect(self.play)

        self.act_seekBW.triggered.connect(self.seek_backward)
        self.act_previous.triggered.connect(self.play_previous)
        self.act_pause.triggered.connect(self.player.pause)
        self.act_stop.triggered.connect(self.player.stop)
        self.act_next.triggered.connect(self.play_next)
        self.act_seekFW.triggered.connect(self.seek_forward)

        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.player.stateChanged.connect(self.update_buttons)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)

    def open(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setMimeTypeFilters(["video/mp4, video/mkv"])

        movies_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.MoviesLocation)
        file_dialog.setDirectory(movies_dir)

        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
            movie = file_dialog.selectedUrls()[0]
            self.all_image = [movie]

            self.id = 0
            self.nb_images = 1
            fileName = self.all_image[self.id]
            movie = QtCore.QUrl(fileName)

            self.player.setMedia(QtMultimedia.QMediaContent(movie))
            self.player.play()

    def openDir(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.Directory)

        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Sélectionner un répertoire", "", QtWidgets.QFileDialog.ShowDirsOnly)

        if directory:
            gen = glob.iglob(directory + r"/**/*.*", recursive=True)
            res = [f for f in gen if ".mp4" in f or ".mpg" in f or ".mkv" in f or ".mov" in f or ".wmv" in f]
            self.all_image = list()

            for file in res:
                self.all_image.append(file.replace("\\", "/"))

            self.id = 0
            self.nb_images = len(self.all_image)
            fileName = self.all_image[self.id]
            movie = QtCore.QUrl(fileName)

            self.player.setMedia(QtMultimedia.QMediaContent(movie))

            self.player.play()

    def play(self):
        self.player.play()
        self.video_widget.resize(QtCore.QSize(1, 1))

    def play_previous(self):
        self.id = self.id = (self.id - 1) % self.nb_images

        fileName = self.all_image[self.id]
        movie = QtCore.QUrl(fileName)

        self.player.setMedia(QtMultimedia.QMediaContent(movie))
        self.player.play()

    def play_next(self):
        self.id = self.id = (self.id + 1) % self.nb_images

        fileName = self.all_image[self.id]
        movie = QtCore.QUrl(fileName)

        self.player.setMedia(QtMultimedia.QMediaContent(movie))
        self.player.play()

    def seek_backward(self):
        new_position = math.floor(self.duration / 20)
        self.position = max(self.position - new_position, 0)
        self.player.setPosition(self.position)

    def seek_forward(self):
        new_position = math.floor(self.duration / 20)
        self.position = min(self.position + new_position, self.duration)
        self.player.setPosition(self.position)

    def positionChanged(self, position):
        self.position = position
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.duration = duration
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.player.setPosition(position)

    def update_buttons(self, state):
        self.act_play.setDisabled(state == QtMultimedia.QMediaPlayer.PlayingState)
        self.act_pause.setDisabled(state == QtMultimedia.QMediaPlayer.PausedState)
        self.act_stop.setDisabled(state == QtMultimedia.QMediaPlayer.StoppedState)

