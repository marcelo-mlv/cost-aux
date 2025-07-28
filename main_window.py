from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QDialog, QRadioButton, QButtonGroup, QHBoxLayout, QSizePolicy, QSpacerItem, QStackedWidget, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget

from config import apply_button_style, ButtonStyle, apply_text_style, TextStyle
from ui_components import ButtonSeries, StandardFooter
from sheet_integration import save_tree_to_txt, create_hyperlinks_for_assemblies, print_hyperlink_report, get_BOM_tree

class MainWindow(QWidget):
    def __init__(self, file_manager):
        super().__init__()
        self.file_manager = file_manager
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 200, 100, 200)
        self.xl_filename = None
        self.BOM_root = None

        self.stacked_widget = QStackedWidget()

        self.start_menu = StartMenu(self)
        self.bom_window = BOMWindow(self)
        self.bom_viewer = BOMViewer(self)

        self.stacked_widget.addWidget(self.start_menu)
        self.stacked_widget.addWidget(self.bom_window)
        self.stacked_widget.addWidget(self.bom_viewer)

        self.stacked_widget.setCurrentWidget(self.start_menu)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

    def show_start_menu(self):
        self.start_menu.update_loaded_file_label()
        self.stacked_widget.setCurrentWidget(self.start_menu)
    
    def show_bom_window(self):
        self.bom_window.update_loaded_file_label()
        self.stacked_widget.setCurrentWidget(self.bom_window)

    def show_bom_viewer(self):
        self.bom_viewer.setup_pagination()
        self.stacked_widget.setCurrentWidget(self.bom_viewer)
    
    def check_loaded_file(self):
        if not self.file_manager.does_file_exist(self.xl_filename):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro")
            msg.setText(f"Arquivo movido ou deletado: {self.xl_filename}.")
            msg.exec()
            return False
        return True

class StartMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.file_manager = main_window.file_manager
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
        self.loaded_file_label = QLabel("Arquivo carregado: " + (self.main_window.xl_filename if self.main_window.xl_filename else "Nenhum arquivo carregado"))
        apply_text_style(self.loaded_file_label, TextStyle.LABEL)
        layout.addWidget(self.loaded_file_label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        footer = StandardFooter()
        layout.addLayout(footer)

        self.setLayout(layout)
    
    def load_file(self):
        xl_files = self.file_manager.search_files_by_extension('.', '.xlsx')
        msg = QMessageBox(self)

        if not xl_files:
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro")
            msg.setText("Nenhum arquivo com formato .xlsx encontrado na pasta raiz.")
        elif len(xl_files) == 1:
            self.main_window.xl_filename = xl_files[0]
            
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"Arquivo carregado com sucesso! \"{self.main_window.xl_filename}\"")
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
            self.main_window.xl_filename = xl_files[selected_id]

            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"Arquivo carregado com sucesso! \"{self.main_window.xl_filename}\"")
        msg.exec()
        self.get_BOM_tree_root()
        self.update_loaded_file_label()

    def update_loaded_file_label(self):
        if self.loaded_file_label is not None:
            self.loaded_file_label.setText("Arquivo carregado: " + (self.main_window.xl_filename if self.main_window.xl_filename else "Nenhum arquivo carregado"))

    def open_file(self):
        msg = QMessageBox(self)
        if not self.main_window.xl_filename:
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro")
            msg.setText("Arquivo não definido. Carregue-o antes no menu principal.")
        else:
            self.file_manager.start_file(self.main_window.xl_filename)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f'Abrindo "{self.main_window.xl_filename}"...')
        msg.exec()

    def edit_bom(self):
        if not self.main_window.xl_filename:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro")
            msg.setText("Arquivo não definido. Carregue-o antes no menu principal.")
            msg.exec()
        else:
            self.main_window.show_bom_window()
    
    def get_BOM_tree_root(self):
        self.main_window.BOM_root = get_BOM_tree(self.main_window.xl_filename)

class BOMWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.file_manager = main_window.file_manager
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
        return_button.clicked.connect(self.main_window.show_start_menu)

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
            ("Criar Hyperlinks Assembly→Parts", self.create_hyperlinks),
            ("Salvar BOM em txt", self.save_txt)
        ]

        button_series = ButtonSeries(button_list, ButtonStyle.MAIN_WINDOW)

        bom_layout.addLayout(button_series)

        bom_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding))

        # Loaded File Label
        self.loaded_file_label = QLabel("Arquivo carregado: " + (self.main_window.xl_filename if self.main_window.xl_filename else "Nenhum arquivo carregado"))
        apply_text_style(self.loaded_file_label, TextStyle.LABEL)
        bom_layout.addWidget(self.loaded_file_label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        bom_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        footer = StandardFooter()
        bom_layout.addLayout(footer)

        self.setLayout(bom_layout)

    def update_loaded_file_label(self):
        if self.loaded_file_label is not None:
            self.loaded_file_label.setText("Arquivo carregado: " + (self.main_window.xl_filename if self.main_window.xl_filename else "Nenhum arquivo carregado"))

    def save_txt(self):
        if not self.main_window.check_loaded_file():
            return
        
        save_tree_to_txt(self.main_window.BOM_root)
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Aviso")
        msg.setText("Arquivo salvo com sucesso em bom_tree.txt")
        msg.exec()

    def create_hyperlinks(self):
        if not self.main_window.check_loaded_file():
            return
        
        try:
            # Criar hyperlinks
            report = create_hyperlinks_for_assemblies(self.main_window.xl_filename)
            
            if 'error' in report:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Erro")
                msg.setText(f"Erro ao criar hyperlinks: {report['error']}")
                msg.exec()
            else:
                # Mostrar relatório
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Hyperlinks Criados")
                msg.setText(
                    f"Hyperlinks criados com sucesso!\n\n"
                    f"Assemblies processados: {report['assemblies_processed']}\n"
                    f"Total de hyperlinks: {report['hyperlinks_created']}\n"
                    f"Páginas não encontradas: {len(report['missing_sheets'])}"
                )
                msg.exec()
                
                # Imprimir relatório detalhado no console (opcional)
                print_hyperlink_report(report)
                
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Erro")
            msg.setText(f"Erro inesperado: {str(e)}")
            msg.exec()

    def add_item(self):
        pass

    def rm_item(self):
        pass

    def view_bom(self):
        if not self.main_window.check_loaded_file():
            return
        
        if not self.main_window.BOM_root:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro")
            msg.setText("BOM não carregado. Carregue um arquivo primeiro.")
            msg.exec()
            return
        
        self.main_window.show_bom_viewer()


class BOMViewer(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_page = 0
        self.subsystems = []
        
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Top bar with navigation
        top_bar = QHBoxLayout()
        
        # Return button
        return_button = QPushButton("<<")
        apply_button_style(return_button, ButtonStyle.NAVIGATION)
        return_button.clicked.connect(self.main_window.show_bom_window)
        top_bar.addWidget(return_button, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Title
        title_label = QLabel("Visualização do BOM")
        apply_text_style(title_label, TextStyle.TITLE)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_bar.addWidget(title_label, stretch=1)
        
        main_layout.addLayout(top_bar)
        
        # Pagination controls
        pagination_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("◀ Anterior")
        apply_button_style(self.prev_button, ButtonStyle.MAIN_WINDOW)
        self.prev_button.clicked.connect(self.prev_page)
        
        self.page_label = QLabel("Página 0 de 0")
        apply_text_style(self.page_label, TextStyle.LABEL)
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.next_button = QPushButton("Próximo ▶")
        apply_button_style(self.next_button, ButtonStyle.MAIN_WINDOW)
        self.next_button.clicked.connect(self.next_page)
        
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label, stretch=1)
        pagination_layout.addWidget(self.next_button)
        
        main_layout.addLayout(pagination_layout)
        
        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area)
        
        self.setLayout(main_layout)
    
    def setup_pagination(self):
        """Prepara os dados para paginação baseado na árvore BOM"""

        self.subsystems = list(self.main_window.BOM_root.children)
        self.current_page = 0
        
        self.update_page()
    
    def update_page(self):
        """Atualiza o conteúdo da página atual"""
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        if not self.subsystems:
            no_data_label = QLabel("Nenhum dado de BOM disponível")
            apply_text_style(no_data_label, TextStyle.LABEL)
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_layout.addWidget(no_data_label)
        else:
            if 0 <= self.current_page < len(self.subsystems):
                subsystem = self.subsystems[self.current_page]
                self.display_subsystem(subsystem)
        
        self.update_pagination_controls()
    
    def display_subsystem(self, subsystem):
        """Exibe um subsistema com seus assemblies e parts"""

        subsystem_title = QLabel(f"{subsystem.name}")
        apply_text_style(subsystem_title, TextStyle.TITLE)
        subsystem_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(subsystem_title)
        
        subsystem_frame = QFrame()
        subsystem_frame.setFrameStyle(QFrame.Shape.Box)
        subsystem_layout = QVBoxLayout(subsystem_frame)
        subsystem_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        assemblies = list(subsystem.children)
        
        if not assemblies:
            no_assemblies_label = QLabel("Nenhum assembly encontrado neste subsistema")
            apply_text_style(no_assemblies_label, TextStyle.LABEL)
            no_assemblies_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subsystem_layout.addWidget(no_assemblies_label)
        else:
            for assembly in assemblies:
                self.display_assembly(assembly, subsystem_layout)
        
        self.content_layout.addWidget(subsystem_frame)
    
    def display_assembly(self, assembly, parent_layout):
        """Exibe um assembly com suas parts"""
        
        assembly_frame = QFrame()
        assembly_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        assembly_layout = QVBoxLayout(assembly_frame)
        assembly_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        assembly_title = QLabel(assembly.name)
        apply_text_style(assembly_title, TextStyle.SUBTITLE)
        assembly_layout.addWidget(assembly_title)
        
        parts = list(assembly.children)
        
        if not parts:
            no_parts_label = QLabel("  Nenhuma part encontrada")
            apply_text_style(no_parts_label, TextStyle.LABEL)
            assembly_layout.addWidget(no_parts_label)
        else:
            for _, part in enumerate(parts):
                part_label = QLabel(f"  {part.name}")
                apply_text_style(part_label, TextStyle.LABEL)
                assembly_layout.addWidget(part_label)
        
        parent_layout.addWidget(assembly_frame)
    
    def update_pagination_controls(self):
        """Atualiza os controles de paginação"""
        total_pages = len(self.subsystems)
        
        if total_pages == 0:
            self.page_label.setText("Nenhuma página")
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
        else:
            self.page_label.setText(f"Página {self.current_page + 1} de {total_pages}")
            self.prev_button.setEnabled(self.current_page > 0)
            self.next_button.setEnabled(self.current_page < total_pages - 1)
    
    def prev_page(self):
        """Vai para a página anterior"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()
    
    def next_page(self):
        """Vai para a próxima página"""
        if self.current_page < len(self.subsystems) - 1:
            self.current_page += 1
            self.update_page()
