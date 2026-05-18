import sys

from PyQt6.QtWidgets import QApplication

from main_gui import EnergyConverterApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnergyConverterApp()
    window.show()
    sys.exit(app.exec())
