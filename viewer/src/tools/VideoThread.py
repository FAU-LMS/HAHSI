from PyQt5.QtCore import *

import time

class VideoThread(QThread):

    def __init__(self, view_gray, view_rgb, hs_video, rgb_video, fps, signal_frame_changed):
        super().__init__()

        self.view_gray = view_gray
        self.view_rgb = view_rgb
        self.hs_video = hs_video
        self.rgb_video = rgb_video
        self.signal_frame_changed = signal_frame_changed
        self.running = True
        self.current_frame = 0
        self.fps = fps
        self.tpf = 1000/fps
        self.pause = False

    def set_running(self, running):
        self.running = running

    def set_pause(self, pause):
        self.pause = pause

    def invert_pause(self):
        self.pause = not self.pause

    def set_fps(self, fps):
        self.fps = fps
        self.tpf = 1000/fps

    def set_frame(self, frame):
        self.current_frame = frame
        if self.current_frame >= self.hs_video.shape[0]:
            self.current_frame = 0

    def run(self):
        while self.running:
            start = time.time()
            self.view_gray.set_data(self.hs_video[self.current_frame])
            self.view_rgb.set_data(self.rgb_video[self.current_frame])

            self.view_gray.update()
            self.view_rgb.update()

            if not self.pause:
                self.current_frame += 1
                if self.current_frame == self.hs_video.shape[0]:
                    self.current_frame = 0
                self.signal_frame_changed.emit(self.current_frame)

            duration = time.time() - start
            diff = int(self.tpf - duration)
            self.msleep(diff)

