from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QDialog, QRadioButton, QButtonGroup, QHBoxLayout, QSizePolicy, QSpacerItem, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget

from config import apply_button_style, ButtonStyle, apply_text_style, TextStyle
from ui_components import ButtonSeries, StandardFooter
from sheet_integration import save_tree_to_txt

class MainWindow(QWidget):
    def __init__(self, file_manager):
        super().__init__()
        self.file_manager = file_manager
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 200, 100, 200)
        self.xl_filename = None

        self.stacked_widget = QStackedWidget()

        self.main_menu = StartMenu(self)
        self.bom_window = BOMWindow(self)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.bom_window)

        self.stacked_widget.setCurrentWidget(self.main_menu)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)
    
    def show_bom_window(self):
        self.stacked_widget.setCurrentWidget(self.bom_window)


class StartMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.file_manager = main_window.file_manager
        self.xl_filename = main_window.xl_filename
        main_window.setWindowTitle("Main Menu")
        
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
            ("Abrir Arquivo Excel", self.open_file),
            ("Carregar Arquivo Excel", self.load_file),
            ("Editar BOM", self.edit_bom)
        ]

        button_series = ButtonSeries(button_list, ButtonStyle.MAIN_WINDOW)

        layout.addLayout(button_series)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding))

        # Loaded File Label
        self.loaded_file_label = QLabel("Arquivo carregado: " + (self.xl_filename if self.xl_filename else "Nenhum arquivo carregado"))
        apply_text_style(self.loaded_file_label, TextStyle.LABEL)
        layout.addWidget(self.loaded_file_label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        footer = StandardFooter()
        layout.addLayout(footer)

        self.setLayout(layout)
    
    def load_file(self):
        xl_files = self.file_manager.search_files_by_extension('.', '.xlsx')
        if not xl_files:
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro")
            msg.setText("Nenhum arquivo com formato .xlsx encontrado na pasta raiz.")
            msg.exec()
        elif len(xl_files) == 1:
            self.xl_filename = xl_files[0]
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"Arquivo carregado com sucesso! \"{self.xl_filename}\"")
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
            self.xl_filename = xl_files[selected_id]

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"Arquivo carregado com sucesso! \"{self.xl_filename}\"")
            msg.exec()
        self.update_loaded_file_label()

    def update_loaded_file_label(self):
        if self.loaded_file_label is not None:
            self.loaded_file_label.setText("Arquivo carregado: " + (self.xl_filename if self.xl_filename else "Nenhum arquivo carregado"))

    def open_file(self):
        msg = QMessageBox(self)
        if not self.xl_filename:
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro")
            msg.setText("Arquivo não definido. Carregue-o antes no menu principal.")
        else:
            self.file_manager.start_file(self.xl_filename)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f'Abrindo "{self.xl_filename}"...')
        msg.exec()

    def edit_bom(self):
        self.main_window.show_bom_window()

class BOMWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.file_manager = main_window.file_manager
        self.xl_filename = main_window.xl_filename
        main_window.setWindowTitle("Edit BOM")

        self.init_ui()

    def init_ui(self):
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        bom_layout = QVBoxLayout()

        top_bar = QHBoxLayout()

        # Top Bar
        ## Return Button
        return_button = QPushButton("<<")
        apply_button_style(return_button, ButtonStyle.NAVIGATION)

        ### On Click
        return_button.clicked.connect(self.main_window.show_main_menu)

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
        self.loaded_file_label = QLabel("Arquivo carregado: " + (self.xl_filename if self.xl_filename else "Nenhum arquivo carregado"))
        apply_text_style(self.loaded_file_label, TextStyle.LABEL)
        bom_layout.addWidget(self.loaded_file_label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        bom_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        footer = StandardFooter()
        bom_layout.addLayout(footer)

        self.setLayout(bom_layout)

    def save_txt(self):
        xl_files = self.file_manager.search_files_by_extension('.', '.xlsx')
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
