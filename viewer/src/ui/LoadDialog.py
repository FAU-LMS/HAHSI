from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class LoadDialog(QDialog):
    def __init__(self, signal_load, parent=None):
        super().__init__(parent)

        self.signal_load = signal_load

        self.setWindowTitle("Load hyperspectral video...")

        self.layout = QVBoxLayout()

        self.layout_path = QHBoxLayout()
        self.edit_path = QLineEdit("/DATA2_ONLY_LOCAL_BACKUP/fsippel/DATA_NO_BACKUP/hahsi-reconstructed/HAHSI-DB/tree/")
        self.button_path = QPushButton("Select folder")
        self.button_path.clicked.connect(self.select_folder)
        self.layout_path.addWidget(self.edit_path)
        self.layout_path.addWidget(self.button_path)
        self.layout.addLayout(self.layout_path)

        self.layout_start_frame = QHBoxLayout()
        self.label_start_frame = QLabel("Start frame:")
        self.edit_start_frame = QLineEdit("0")
        self.edit_start_frame.setValidator(QIntValidator())
        self.layout_start_frame.addWidget(self.label_start_frame)
        self.layout_start_frame.addWidget(self.edit_start_frame)
        self.layout.addLayout(self.layout_start_frame)

        self.layout_end_frame = QHBoxLayout()
        self.label_end_frame = QLabel("End frame:")
        self.edit_end_frame = QLineEdit("-1")
        self.edit_end_frame.setValidator(QIntValidator())
        self.layout_end_frame.addWidget(self.label_end_frame)
        self.layout_end_frame.addWidget(self.edit_end_frame)
        self.layout.addLayout(self.layout_end_frame)

        self.button_load = QPushButton("Load!")
        self.button_load.clicked.connect(self.load)
        self.layout.addWidget(self.button_load)

        self.setLayout(self.layout)

        self.setMinimumSize(500, 100)

    def select_folder(self):
        hs_image_folder = QFileDialog.getExistingDirectory(self, 'Open hyperspectral video directory')
        if hs_image_folder == "" or hs_image_folder is None:
            return

        self.edit_path.setText(hs_image_folder)

    def load(self):
        self.close()
        self.signal_load.emit(self.edit_path.text(), int(self.edit_start_frame.text()), int(self.edit_end_frame.text()))
