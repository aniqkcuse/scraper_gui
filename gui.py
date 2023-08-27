from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PySide6.QtCore import Qt
import sys
from scraper import scraping

class widgetGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webscraping Script")

        self.layout_main = QVBoxLayout(self)

        self.title_text = QLabel("Webscraping eneba.com promotion code")
        self.script_log = QLineEdit()
        self.script_log.setReadOnly(True)
        self.title_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.script_button = QPushButton("Scraping!")
        self.script_button.clicked.connect(self.start_scraping)

        self.layout_main.addWidget(self.title_text)
        self.layout_main.addWidget(self.script_log)
        self.layout_main.addWidget(self.script_button)

    def start_scraping(self):
        self.setEnabled(False)
        scraping(self)

def start_gui():        
    app = QApplication(sys.argv)
    window = widgetGUI()

    window.show()
    app.exec()