import sys
import sqlite3

import requests
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import *

from functions import *


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # get homepage from sqlite table
        self.homepage = get_homepage()  # function from functions
        self.get_statistic = True

        # Connect database
        self.con = sqlite3.connect('database.sql')
        self.cur = self.con.cursor()

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon(get_image('web.svg')))

        # Create and customize the tab bar
        self.tabs = QTabWidget()
        self.tabs.setTabBar(TabBar())
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        # Create and customize the navigation bar
        nav_bar = QToolBar('Navigation')
        nav_bar.setIconSize(QSize(24, 24))
        nav_bar.setStyleSheet("padding: 2px;")
        nav_bar.setMovable(False)

        self.addToolBar(nav_bar)

        # Create and customize buttons(actions) for navigation bar
        back_button = QAction(QIcon(get_image('arrow_back.svg')),
                              'Previous page', self)
        back_button.setStatusTip('Back to previous page')
        back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        nav_bar.addAction(back_button)

        next_button = QAction(QIcon(get_image('arrow_forward.svg')),
                              'Next page', self)
        next_button.setStatusTip('Forward to next page')
        next_button.triggered.connect(lambda:
                                      self.tabs.currentWidget().forward())
        nav_bar.addAction(next_button)

        reload_button = QAction(QIcon(get_image('refresh.svg')), 'Reload page',
                                self)
        reload_button.setStatusTip('Reload page')
        reload_button.triggered.connect(lambda:
                                        self.tabs.currentWidget().reload())
        nav_bar.addAction(reload_button)

        home_button = QAction(QIcon(get_image('home.svg')), 'Homepage', self)
        home_button.setStatusTip('Homepage')
        home_button.triggered.connect(self.go_to_homepage)
        nav_bar.addAction(home_button)

        nav_bar.addSeparator()

        # Buttons which show, what type of connection use website (http or https)
        # This is actually a bad way to check for security.
        self.connection_icon = QLabel()
        self.connection_icon.setPixmap(QPixmap(get_image('http.svg')))
        nav_bar.addWidget(self.connection_icon)

        # Custom font (this is actually need only for the url bar)
        font = QFont('sans-serif')
        font.setPointSize(13)

        self.url_bar = QLineEdit()
        self.url_bar.setFont(font)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        # Create and customize menu
        file_menu = self.menuBar().addMenu('File')

        new_tab_action = QAction(QIcon(get_image('add_tab.svg')), 'New tab',
                                 self)
        new_tab_action.setStatusTip('Open a new tab')
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        help_menu = self.menuBar().addMenu('Help')

        about_action = QAction(QIcon(get_image('info.svg')), 'About', self)
        about_action.setStatusTip('Find out more about Browser')
        about_action.triggered.connect(self.about_dialog)
        help_menu.addAction()

        self.add_new_tab()

    # Functions for tab bar correct work
    def add_new_tab(self, qurl=None, title="New tab"):

        def combining_func(cls):
            nonlocal index, browser
            cls.tabs.setTabText(index, browser.page().title())
            cls.update_title(cls.tabs.currentWidget())

        if qurl is None:
            qurl = QUrl("https://google.com")

        if qurl == self.homepage:
            title = 'Homepage'

        browser = QWebEngineView()
        page = WebEnginePage(browser)
        browser.setPage(page)
        browser.load(qurl)
        index = self.tabs.addTab(browser, title)

        self.tabs.setCurrentIndex(index)

        browser.urlChanged.connect(lambda url:
                                   self.update_url_bar(url, browser))
        browser.loadFinished.connect(lambda: combining_func(self))

    def current_tab_changed(self, index):
        qurl = self.tabs.currentWidget().url()
        self.update_url_bar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

        if self.get_statistic:
            if not qurl.toString().startswith('https://google.com/search'):
                statistic(self.tabs.currentWidget())

    def tab_open_doubleclick(self, index):
        if index == -1:  # No tab under the click
            self.add_new_tab()

    def close_current_tab(self, index):
        if self.tabs.count() < 2:
            return None  # To prevent the application from closing

        self.tabs.removeTab(index)

    # Functions for url bar correct work
    def update_url_bar(self, qurl, browser):
        # If the signal is not from the current tab, ignore it
        if browser != self.tabs.currentWidget():
            return None
        else:
            if qurl.scheme() == 'https':
                self.connection_icon.setPixmap(QPixmap(get_image('https.svg')))
            else:
                self.connection_icon.setPixmap(QPixmap(get_image('http.svg')))

            self.url_bar.setText(qurl.toString())
            self.url_bar.setCursorPosition(0)

    # Functions for browser correct work
    def update_title(self, browser):
        # If the signal is not from the current tab, ignore it
        if browser != self.tabs.currentWidget():
            return None

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(f"{title} - Sibenshtern's browser")

    def navigate_to_url(self):
        url = self.url_bar.text()

        try:
            # Check that the string obtained from url_bar is a link
            if url.startswith('https://') or url.startwith('http://'):
                request = requests.get(url)
            else:
                request = requests.get(f'http://{url}')
        except Exception:
            # If string isn't link, search string in search machine
            url = QUrl(f'https://google.com/search?q={url}')
            self.tabs.currentWidget().setUrl(url)
        else:
            # If string is link, follow the link
            url = QUrl(url)

            if url.scheme() == '':
                url.setScheme('http')

            self.tabs.currentWidget().setUrl(url)

    def go_to_homepage(self):
        """Changes url for current tab to self.homepage."""
        self.tabs.currentWidget().setUrl(QUrl(self.homepage))

    # Functions for correct work menu
    # Nothing :)


class WebEnginePage(QWebEnginePage):

    def createWindow(self, window_type):
        page = WebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @pyqtSlot(QUrl)
    def on_url_changed(self, url):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()


class TabBar(QTabBar):

    def tabSizeHint(self, index):
        height = 28

        if self.count() > 6:
            return QSize(int(self.width() / self.count()), height)
        else:
            size = QTabBar.tabSizeHint(self, index)
            return QSize(size.width(), size.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Sibenshtern's Browser")
    app.setOrganizationName("Sibenshtern")

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec_())
