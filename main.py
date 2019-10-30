import os
import sys
import sqlite3

import requests
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import *

from functions import get_path


class MainWindow(QMainWindow):
    pass


class WebEnginePage(QWebEnginePage):
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Sibenshtern's Browser")
    app.setOrganizationName("Sibenshtern")

    window = MainWindow()

    sys.exit()

