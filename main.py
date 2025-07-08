from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QPushButton, QMessageBox, QRadioButton, QButtonGroup, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt

import sys
import os

from sheet_integration import save_tree_to_txt
from config import ButtonStyle, TextStyle, apply_button_style, apply_text_style
from ui_components import StandardFooter, ButtonSeries

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("cost-aux")
        self.setGeometry(100, 200, 300, 400)
        self.filename = None
        self.loaded_file_label = None

        self.init_ui()

    def init_ui(self):
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        layout = QVBoxLayout()

        # Main Text
        main_text = QLabel("America Ya :D")
        apply_text_style(main_text, TextStyle.TITLE)
        main_text.setContentsMargins(0, 10, 0, 10)
        layout.addWidget(main_text, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        # Logo
        logo_label = QSvgWidget("assets/old-logo.svg")
        logo_label.setFixedSize(200, 80)
        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        
        # Main Menu Buttons
        button_list = [
            ("Abrir Arquivo Excel", self.find_file),
            ("Carregar Arquivo Excel", self.load_file),
            ("Editar BOM", self.open_bom_window)
        ]

        button_series = ButtonSeries(button_list, ButtonStyle.MAIN_WINDOW)

        layout.addLayout(button_series)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding))

        # Loaded File Label
        self.loaded_file_label = QLabel("Arquivo carregado: " + (self.filename if self.filename else "Nenhum arquivo carregado"))
        apply_text_style(self.loaded_file_label, TextStyle.LABEL)
        layout.addWidget(self.loaded_file_label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        footer = StandardFooter()
        layout.addLayout(footer)

        self.setLayout(layout)

    def update_loaded_file_label(self):
        if self.loaded_file_label is not None:
            self.loaded_file_label.setText("Arquivo carregado: " + (self.filename if self.filename else "Nenhum arquivo carregado"))

    def open_bom_window(self):
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        bom_layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        
        # Top Bar
        ## Return Button
        return_button = QPushButton("<<")
        apply_button_style(return_button, ButtonStyle.NAVIGATION)

        ### On Click
        return_button.clicked.connect(self.init_ui)

        top_bar.addWidget(return_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        ## Main Text
        bom_label = QLabel("BOM Editor")
        apply_text_style(bom_label, TextStyle.TITLE)
        bom_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        top_bar.addWidget(bom_label, stretch=1, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        top_bar.setContentsMargins(0, 10, 0, 15)

        bom_layout.addLayout(top_bar)

        # BOM Editor Buttons
        button_list = [
            ("Visualizar BOM", self.view_bom),
            ("Adicionar Item ao BOM", self.add_item),
            ("Remover Item do BOM", self.rm_item),
            ("Salvar BOM em txt", self.save_txt)
        ]

        button_series = ButtonSeries(button_list, ButtonStyle.MAIN_WINDOW)

        bom_layout.addLayout(button_series)

        bom_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding))

        # Loaded File Label
        self.loaded_file_label = QLabel("Arquivo carregado: " + (self.filename if self.filename else "Nenhum arquivo carregado"))
        apply_text_style(self.loaded_file_label, TextStyle.LABEL)
        bom_layout.addWidget(self.loaded_file_label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        bom_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        footer = StandardFooter()
        bom_layout.addLayout(footer)

        self.setLayout(bom_layout)

    def load_file(self):
        files = os.listdir('.')
        xl_files = [f for f in files if f.endswith('.xlsx')]
        if not xl_files:
            self.filename = None
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro")
            msg.setText("Nenhum arquivo com formato .xlsx encontrado na pasta raiz.")
            msg.exec()
        elif len(xl_files) == 1:
            self.filename = xl_files[0]
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"Arquivo carregado com sucesso! \"{self.filename}\"")
            msg.exec()
        else:
            choose_window = QMessageBox(self)
            choose_window.setIcon(QMessageBox.Icon.Question)
            choose_window.setWindowTitle("Escolha um arquivo")

            dialog = QDialog(self)
            dialog.setWindowTitle("Escolha um arquivo")
            vbox = QVBoxLayout(dialog)
            button_group = QButtonGroup(dialog)
            radio_buttons = []
            for i, file in enumerate(xl_files):
                rb = QRadioButton(file)
                button_group.addButton(rb, i)
                vbox.addWidget(rb)
                radio_buttons.append(rb)
            radio_buttons[0].setChecked(True)
            
            ok_button = QPushButton("OK")
            apply_button_style(ok_button, ButtonStyle.DIALOG)

            vbox.addWidget(ok_button)
            ok_button.clicked.connect(dialog.accept)
            dialog.setLayout(vbox)
            dialog.exec()
            selected_id = button_group.checkedId()
            self.filename = xl_files[selected_id]

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"Arquivo carregado com sucesso! \"{self.filename}\"")
            msg.exec()
        self.update_loaded_file_label()


    def find_file(self):
        msg = QMessageBox(self)
        if not self.filename:
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro")
            msg.setText("Arquivo não definido. Carregue-o antes no menu principal.")
        else:
            os.startfile(self.filename)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f'Abrindo "{self.filename}"...')
        msg.exec()
    
    def save_txt(self):
        files = os.listdir('.')
        xl_files = [f for f in files if f.endswith('.xlsx')]
        save_tree_to_txt(xl_files[0])
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Aviso")
        msg.setText("Arquivo salvo com sucesso em bom_tree.txt")
        msg.exec()

    def add_item(self):
        pass

    def rm_item(self):
        pass

    def view_bom(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
