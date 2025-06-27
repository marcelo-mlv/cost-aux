import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy, QSpacerItem, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtSvgWidgets import QSvgWidget

from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("cost-aux")
        self.setGeometry(100, 200, 300, 400)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        # Main Text
        main_text = QLabel("Cost Auxilium")
        font = main_text.font()
        font.setPointSize(12)
        font.setBold(True)
        font.setFamily("Consolas")
        main_text.setFont(font)
        main_text.setContentsMargins(0, 10, 0, 10)
        layout.addWidget(main_text, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        ### Logo
        logo_label = QSvgWidget("assets/old-logo.svg")
        logo_label.setFixedSize(200, 80)
        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        
        ### Menu Buttons
        button_series = QVBoxLayout()

        open_file_button = QPushButton("Open Excel File")
        open_file_button.setFixedWidth(200)
        button_series.addWidget(open_file_button, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        bom_button = QPushButton("Edit BOM")
        bom_button.setFixedWidth(200)
        button_series.addWidget(bom_button, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        layout.addLayout(button_series)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding))

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
