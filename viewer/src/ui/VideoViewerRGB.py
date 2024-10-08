import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tools import Color

import time

class VideoViewerRGB(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.MAX_VALUE = np.iinfo(np.uint64).max
        self.SCALE = 0.8
        self.image_width = self.MAX_VALUE
        self.image_height = self.MAX_VALUE
        self.rgb_image = None
        self.selected_channel = 15
        self.mouse_x = -1
        self.mouse_y = -1
        self.mouse_last_x = -1
        self.mouse_last_y = -1
        self.left_mouse_pressed = False
        self.mouse_pressed_x = -1
        self.mouse_pressed_y = -1
        self.source_rect = QRectF(0, 0, self.MAX_VALUE, self.MAX_VALUE)
        self.source_rect_int = QRect()
        self.setMouseTracking(True)
        self.repaint()

    def paintEvent(self, event):
        if self.rgb_image is None:
            return

        self.check_bounds()

        qp = QPainter()
        qp.begin(self)

        image_cp = np.require(self.rgb_image, np.uint8, 'C')
        bytes_per_line = image_cp.shape[1] * image_cp.shape[2]
        qp_image = QImage(image_cp, image_cp.shape[1], image_cp.shape[0], bytes_per_line, QImage.Format_RGB888)

        qp.drawImage(QRectF(0, 0, self.width(), self.height()), qp_image, self.source_rect)

        qp.end()

    def wheelEvent(self, event):
        scroll_speed = event.angleDelta().y()
        screen_ar = self.width()/self.height()
        if scroll_speed > 0:
            new_height = self.source_rect.height() * self.SCALE
        else:
            new_height = self.source_rect.height()/self.SCALE

        if new_height < 50:
            new_height = 50

        new_width = new_height * screen_ar
        diff_width = self.source_rect.width() - new_width
        diff_height = self.source_rect.height() - new_height
        ratio_x = self.mouse_x/self.width()
        ratio_y = self.mouse_y/self.height()
        self.source_rect.moveTo(self.source_rect.x() + diff_width * ratio_x, self.source_rect.y() + diff_height * ratio_y)
        self.source_rect.setWidth(new_width)
        self.source_rect.setHeight(new_height)
        self.repaint()

    def mouseMoveEvent(self, event):
        self.mouse_x = event.pos().x()
        self.mouse_y = event.pos().y()
        if self.left_mouse_pressed:
            diff_x = self.mouse_x - self.mouse_last_x
            diff_y = self.mouse_y - self.mouse_last_y

            scale = self.source_rect.width() / self.width()
            self.source_rect.moveTo(self.source_rect.x() - diff_x * scale, self.source_rect.y() - diff_y * scale)

            self.repaint()

        self.mouse_last_x = self.mouse_x
        self.mouse_last_y = self.mouse_y

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.left_mouse_pressed = True

            self.mouse_pressed_x = event.pos().x()
            self.mouse_pressed_y = event.pos().y()

    def mouseReleaseEvent(self, event):
        if event.button() == 1:
            self.left_mouse_pressed = False
            self.repaint()

    def resizeEvent(self, event):
        screen_ar = self.width()/self.height()
        new_height = self.source_rect.height()
        new_width = new_height * screen_ar
        self.source_rect.setWidth(new_width)
        self.source_rect.setHeight(new_height)
        self.check_bounds()
        self.repaint()

    def screen_to_image(self, sx, sy):
        image_x = sx/self.width() * self.source_rect.width()
        image_y = sy/self.height() * self.source_rect.height()
        image_x += self.source_rect.x()
        image_y += self.source_rect.y()
        return image_x, image_y

    def image_to_screen(self, image_x, image_y):
        scale_x = self.source_rect.width()/self.width()
        scale_y = self.source_rect.height()/self.height()
        screen_x = (image_x - self.source_rect.x())/scale_x
        screen_y = (image_y - self.source_rect.y())/scale_y
        return screen_x, screen_y

    def image_pixel_size(self):
        return self.width()/int(self.source_rect.width())

    def check_bounds(self):
        if self.height() == 0 or self.image_height == 0:
            return
        image_ar = self.image_width/self.image_height
        screen_ar = self.width()/self.height()
        if image_ar < screen_ar:
            if self.source_rect.height() > self.image_height:
                self.source_rect.setWidth(self.image_height * screen_ar)
                self.source_rect.setHeight(self.image_height)
        else:
            if self.source_rect.width() > self.image_width:
                self.source_rect.setWidth(self.image_width)
                self.source_rect.setHeight(self.image_width/screen_ar)

        lower_x_bound = np.minimum((self.image_width - self.source_rect.width())//2, 0)
        lower_y_bound = np.minimum((self.image_height - self.source_rect.height())//2, 0)
        upper_x_bound = np.maximum(self.image_width - (self.image_width - self.source_rect.width())//2 - 1, self.image_width - 1)
        upper_y_bound = np.maximum(self.image_height - (self.image_height - self.source_rect.height())//2 - 1, self.image_height - 1)

        if self.source_rect.x() < lower_x_bound:
            self.source_rect.moveTo(lower_x_bound, self.source_rect.y())

        if self.source_rect.y() < lower_y_bound:
            self.source_rect.moveTo(self.source_rect.x(), lower_y_bound)

        if self.source_rect.x() > upper_x_bound - self.source_rect.width():
            self.source_rect.moveTo(upper_x_bound - self.source_rect.width(), self.source_rect.y())

        if self.source_rect.y() > upper_y_bound - self.source_rect.height():
            self.source_rect.moveTo(self.source_rect.x(), upper_y_bound - self.source_rect.height())

    def set_data(self, rgb_image):
        self.rgb_image = rgb_image
        self.image_width = self.rgb_image.shape[1]
        self.image_height = self.rgb_image.shape[0]