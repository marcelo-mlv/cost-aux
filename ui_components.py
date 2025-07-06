from PyQt6.QtWidgets import QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from config import apply_text_style, TextStyle

class StandardFooter(QHBoxLayout):
    def __init__(
        self,
        logo_path='assets/logo.png',
        footer_text='Formula ITA - CostAux v1.0',
        logo_size=(50, 50)
    ):
        super().__init__()
        self.logo_path = logo_path
        self.footer_text = footer_text
        self.logo_size = logo_size
        self.create_footer()

    def create_footer(self):
        self.logo_label = QLabel()
        self.pixmap = QPixmap(self.logo_path)
        self.pixmap = self.pixmap.scaled(*self.logo_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(self.pixmap)
        self.addWidget(self.logo_label, stretch=2, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        self.footer_label = QLabel(self.footer_text)
        apply_text_style(self.footer_label, TextStyle.FOOTER)
        self.addWidget(self.footer_label, stretch=5, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
