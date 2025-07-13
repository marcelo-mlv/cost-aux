import sys
from PyQt6.QtWidgets import QApplication

from main_window import MainWindow
from file_manager import FileManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    file_manager = FileManager()
    window = MainWindow(file_manager)

    window.show()
    sys.exit(app.exec())
