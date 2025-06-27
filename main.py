import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt

import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("cost-aux")
        self.setGeometry(100, 200, 300, 400)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        # Main Text
        main_text = QLabel("America Ya :D")
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

        ## Open File Button
        open_file_button = QPushButton("Abrir Arquivo Excel")
        open_file_button.setFixedWidth(200)
        button_series.addWidget(open_file_button, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
    
        # On Click
        def find_file():
            files = os.listdir('.')
            xl_files = [f for f in files if f.endswith('.xlsx')]
            if not xl_files:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Erro")
                msg.setText("Nenhum arquivo com formato .xlsx encontrado na pasta raiz.")
                msg.exec()
            else:
                if len(xl_files) == 1:
                    text = f'Arquivo encontrado com sucesso! Abrindo "{xl_files[0]}"...'
                else:
                    text = f'Mais de um arquivo com formato .xlsx encontrado. Abrindo o primeiro...'
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Aviso")
                msg.setText(text)
                msg.exec()
                os.startfile(xl_files[0])

        open_file_button.clicked.connect(find_file)

        ## Edit BOM Button
        bom_button = QPushButton("Editar BOM")
        bom_button.setFixedWidth(200)
        button_series.addWidget(bom_button, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        layout.addLayout(button_series)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding))

        ### Footer
        footer_layout = QHBoxLayout()

        ## Footer Logo
        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        footer_layout.addWidget(logo_label, stretch=2, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        ## Footer Label
        footer_label = QLabel("Formula ITA - CostAux v1.0")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        footer_layout.addWidget(footer_label, stretch=5, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        layout.addLayout(footer_layout)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
