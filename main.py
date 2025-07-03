import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QPushButton, QMessageBox, QRadioButton, QButtonGroup, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt

import os
from sheet_integration import save_tree_to_txt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("cost-aux")
        self.setGeometry(100, 200, 300, 400)
        self.filename = None

        self.init_ui()

    def init_ui(self):
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

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

        # Logo
        logo_label = QSvgWidget("assets/old-logo.svg")
        logo_label.setFixedSize(200, 80)
        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        
        # Menu Buttons
        button_series = QVBoxLayout()

        ## Open File Button
        open_file_button = QPushButton("Abrir Arquivo Excel")
        open_file_button.setFixedWidth(200)
        button_series.addWidget(open_file_button, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
    
        ### On Click
        open_file_button.clicked.connect(self.find_file)
        
        ## Load File Button
        load_file_button = QPushButton("Carregar Arquivo Excel")
        load_file_button.setFixedWidth(200)
        button_series.addWidget(load_file_button, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        ### On Click
        load_file_button.clicked.connect(self.load_file)

        ## Edit BOM Button
        bom_button = QPushButton("Editar BOM")
        bom_button.setFixedWidth(200)
        button_series.addWidget(bom_button, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        ### On Click
        bom_button.clicked.connect(self.open_bom_window)

        layout.addLayout(button_series)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding))

        # Footer
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

    def open_bom_window(self):
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        bom_layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        
        # Top Bar
        ## Return Button
        return_button = QPushButton("<<")
        return_button.setFixedWidth(40)
        return_button.clicked.connect(self.init_ui)
        top_bar.addWidget(return_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        ## Main Text
        bom_label = QLabel("BOM Editor")
        bom_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        font = bom_label.font()
        font.setPointSize(16)
        font.setBold(True)
        font.setFamily("Consolas")
        bom_label.setFont(font)
        top_bar.addWidget(bom_label, stretch=1, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        top_bar.setContentsMargins(0, 10, 0, 15)

        bom_layout.addLayout(top_bar)
        
        button_series = QVBoxLayout()
        
        # View BOM Button
        view_bom_button = QPushButton("Visualizar BOM")
        view_bom_button.setContentsMargins(0, 10, 0, 20)
        view_bom_button.setFixedWidth(200)
        button_series.addWidget(view_bom_button, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        ### On Click
        view_bom_button.clicked.connect(self.view_bom)

        # Add Item Button
        add_item_button = QPushButton("Adicionar Item ao BOM")
        add_item_button.setContentsMargins(0, 10, 0, 20)
        add_item_button.setFixedWidth(200)
        button_series.addWidget(add_item_button, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        ### On Click
        add_item_button.clicked.connect(self.add_item)

        # Remove Item Button
        remove_item_button = QPushButton("Remover Item do BOM")
        remove_item_button.setContentsMargins(0, 10, 0, 20)
        remove_item_button.setFixedWidth(200)
        button_series.addWidget(remove_item_button, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        ### On Click
        remove_item_button.clicked.connect(self.rm_item)

        # Save BOM Button
        save_bom_button = QPushButton("Salvar BOM em txt")
        save_bom_button.setContentsMargins(0, 10, 0, 20)
        save_bom_button.setFixedWidth(200)
        button_series.addWidget(save_bom_button, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        ### On Click
        save_bom_button.clicked.connect(self.save_txt)

        bom_layout.addLayout(button_series)

        bom_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding))

        # Footer
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

        bom_layout.addLayout(footer_layout)

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
