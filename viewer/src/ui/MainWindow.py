from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import qdarktheme

from tools import VideoThread
from data import Dataloader
from . import VideoViewerRGB, VideoViewerGrayscale, LoadDialog

class HyperspectralVideoViewer(QMainWindow):
    signal_frame_changed = pyqtSignal(int)
    signal_load_video = pyqtSignal(str, int, int)

    def __init__(self, parent=None):
        super(HyperspectralVideoViewer, self).__init__(parent)

        self.signal_frame_changed.connect(self.frame_changed)
        self.signal_load_video.connect(self.load)

        self.video_thread = None
        self.start_frame = 0
        self.end_frame = 30

        self.setup_menubar()

        layout_main = QVBoxLayout()
        layout_views = QHBoxLayout()

        '''VIEWS'''
        self.view_grayscale = VideoViewerGrayscale.VideoViewerGrayscale()
        self.view_rgb = VideoViewerRGB.VideoViewerRGB()
        layout_views.addWidget(self.view_grayscale, 1)
        layout_views.addWidget(self.view_rgb, 1)

        layout_main.addLayout(layout_views, 100)

        '''SETTINGS'''
        layout_settings = QVBoxLayout()

        layout_channel = QHBoxLayout()
        label_slider = QLabel("Channel: ")
        layout_channel.addWidget(label_slider)

        self.slider_channel = QSlider(Qt.Horizontal)
        self.slider_channel.setRange(1, 31)
        self.slider_channel.setValue(self.view_grayscale.get_channel())
        self.slider_channel.valueChanged.connect(self.update_channel)
        layout_channel.addWidget(self.slider_channel)

        self.label_channel = QLabel("400 nm")
        layout_channel.addWidget(self.label_channel)

        layout_temporal = QHBoxLayout()
        self.label_fps = QLabel("FPS: ")
        layout_temporal.addWidget(self.label_fps, 1)

        self.text_fps = QLineEdit("30")
        self.text_fps.setValidator(QIntValidator(1, 120))
        self.text_fps.textChanged.connect(self.change_fps)
        layout_temporal.addWidget(self.text_fps, 1)

        self.button_stop_play = QPushButton("Stop/Play")
        self.button_stop_play.clicked.connect(self.stop_play)
        layout_temporal.addWidget(self.button_stop_play, 1)

        layout_frame = QHBoxLayout()
        label_frame = QLabel("Frame: ")
        layout_frame.addWidget(label_frame)

        self.slider_frame = QSlider(Qt.Horizontal)
        self.slider_frame.setRange(1, 30)
        self.slider_frame.setValue(1)
        self.slider_frame.valueChanged.connect(self.update_frame)
        layout_frame.addWidget(self.slider_frame)
        layout_temporal.addLayout(layout_frame, 100)

        self.label_frame = QLabel("0")
        layout_temporal.addWidget(self.label_frame)

        layout_settings.addLayout(layout_channel, 100)
        layout_settings.addLayout(layout_temporal)
        layout_main.addLayout(layout_settings, 1)
        '''END'''

        widget_main = QWidget()
        widget_main.setLayout(layout_main)
        self.setCentralWidget(widget_main)

        stylesheet = qdarktheme.load_stylesheet('dark')
        self.setStyleSheet(stylesheet)
        self.setMinimumSize(1000, 600)
        self.setWindowFlags(Qt.WindowFullscreenButtonHint)
        self.setWindowTitle("Hyperspectral Video Viewer")

    def setup_menubar(self):
        menu_file = QMenu("File", self)
        load_ms_image = QAction("Load HS Image...", self)
        load_ms_image.triggered.connect(self.show_load_dialog)
        menu_file.addAction(load_ms_image)
        self.menuBar().addMenu(menu_file)

    def show_load_dialog(self):
        dlg = LoadDialog.LoadDialog(self.signal_load_video, self)
        dlg.exec()

    def load(self, hs_image_folder, start_frame=0, end_frame=-1):
        if self.video_thread is not None:
            self.video_thread.set_running(False)
            self.video_thread.wait()
        print("Loading video...")
        self.start_frame, self.end_frame = start_frame, end_frame
        hs_video, rgb_video = Dataloader.load_video(hs_image_folder, start_frame=self.start_frame, end_frame=self.end_frame)
        if self.end_frame == -1:
            self.end_frame = hs_video.shape[0]
        if hs_video is None:
            return
        print("Done!")
        self.slider_channel.setRange(1, hs_video.shape[1])
        self.slider_frame.setRange(0, hs_video.shape[0] - 1)
        self.slider_frame.setValue(0)
        self.label_frame.setText(str(self.start_frame + self.slider_frame.value()))
        self.update_label()
        self.video_thread = VideoThread.VideoThread(self.view_grayscale, self.view_rgb, hs_video, rgb_video, self.get_fps_from_lineedit(), self.signal_frame_changed)
        self.video_thread.start()

    def stop_play(self):
        self.video_thread.invert_pause()

    def update_channel(self):
        self.update_label()
        channel = self.slider_channel.value()
        self.view_grayscale.set_channel(channel - 1)

    def update_label(self):
        channel = self.slider_channel.value()
        wl = (channel - 1) * 10 + 400
        self.label_channel.setText(str(wl) + ' nm')

    def update_frame(self):
        frame = self.slider_frame.value()
        self.label_frame.setText(str(self.start_frame + frame))
        if self.video_thread is not None:
            self.video_thread.set_frame(frame)

    def frame_changed(self, frame):
        self.slider_frame.blockSignals(True)
        self.slider_frame.setValue(frame)
        self.label_frame.setText(str(self.start_frame +frame))
        self.slider_frame.blockSignals(False)

    def change_fps(self):
        if self.video_thread is not None:
            self.video_thread.set_fps(self.get_fps_from_lineedit())

    def get_fps_from_lineedit(self):
        text = self.text_fps.text()
        if text == '':
            return 1
        fps = int(text)
        return fps


    def closeEvent(self, event):
        if self.video_thread is not None:
            self.video_thread.set_running(False)
            self.video_thread.wait()

def start():
    import sys

    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print("Error!")
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    camsi = HyperspectralVideoViewer()
    camsi.show()
    sys.exit(app.exec_())
