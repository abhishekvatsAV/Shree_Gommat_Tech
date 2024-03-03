import locale
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QDialog,
    QVBoxLayout,
    QLabel,
    QDialogButtonBox,
    QMessageBox,
    QLineEdit,
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
import os
from Search import SearchController
from Settings import SettingsController
from ui import (
    AddVendor,
    MainWindow,
    ManageVendorsTab,
    FetchReportsTab,
    SearchTab,
    Settingtab,
)
from ManageVendors import ManageVendorsController
from FetchReports import FetchReportsController

# from Settings import SettingsController
import GeneralUtils
import hashlib

# import ManageDB
# from Constants import *

"""
from FetchData import FetchReportsController, FetchSpecialReportsController
from Settings import SettingsController, SettingsModel

from ImportFile import ImportReportController
from Costs import CostsController
from Search import SearchController

from Visual import VisualController
from Visual2 import VisualController
"""

# region debug_stuff


def trap_exc_during_debug(*args):
    # when app raises an uncaught exception, print info
    print(args)


# install exception hook: without this, uncaught exception would cause the application to exit
sys.excepthook = trap_exc_during_debug

# endregion

if hasattr(Qt, "AA_EnableHighDpiScaling"):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, "AA_UseHighDpiPixmaps"):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


def trap_exc_during_debug(*args):
    # when app raises an uncaught exception, print info
    print(args)


# install exception hook: without this, uncaught exception would cause the application to exit
sys.excepthook = trap_exc_during_debug

# endregion

if hasattr(Qt, "AA_EnableHighDpiScaling"):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, "AA_UseHighDpiPixmaps"):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

authorized = False


class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super(PasswordDialog, self).__init__(parent)
        self.setWindowTitle("Enter Password")
        self.setGeometry(200, 200, 300, 100)

        layout = QVBoxLayout()

        self.label = QLabel("Enter password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def check_password(self, hash_pass):
        entered_password = self.password_input.text()
        input_hash = hashlib.md5(entered_password.encode("utf8")).hexdigest()
        if input_hash == hash_pass:
            global authorized
            authorized = True
        return input_hash == hash_pass

    def accept(self):
        correct_password = "123"  # Replace with your actual password
        hash_pass = hashlib.md5(correct_password.encode("utf8")).hexdigest()
        if self.check_password(hash_pass):
            super().accept()
        else:
            QMessageBox.warning(
                self, "Access Denied", "Incorrect password. Access denied."
            )


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget {font-family: Segoe UI; font-size: 12pt;}")

    # correct_password = "12345678"  # Replace with your actual password

    main_window = QMainWindow()
    main_window_ui = MainWindow.Ui_mainWindow()
    main_window_ui.setupUi(main_window)

    settings_tab = QWidget(main_window)
    settings_ui = Settingtab.Ui_SettingTab()
    settings_ui.setupUi(settings_tab)
    settings_controller = SettingsController(settings_tab, settings_ui)

    manage_vendors_tab = QWidget(main_window)
    manage_vendors_ui = ManageVendorsTab.Ui_manage_vendor_tab()
    manage_vendors_ui.setupUi(manage_vendors_tab)
    manage_vendors_controller = ManageVendorsController(
        manage_vendors_tab, manage_vendors_ui, settings_controller.settings
    )

    main_window_ui.tab_widget.addTab(
        manage_vendors_tab, manage_vendors_tab.windowIcon(), "Manage Vendors"
    )

    def show_manage_vendors():
        password_dialog = PasswordDialog()
        if password_dialog.exec_() == QDialog.Accepted or authorized:
            main_window_ui.tab_widget.setCurrentWidget(manage_vendors_tab)
        else:
            QMessageBox.warning(
                main_window,
                "Access Denied",
                "Incorrect password. Access to 'Manage Vendors' denied.",
            )

    main_window_ui.tab_widget.setCurrentIndex(1)  # Set default tab index

    def handle_tab_change(index):
        if index == 0 and authorized == False:  # Index of "Manage Vendors" tab
            password_dialog = PasswordDialog()
            if password_dialog.exec_() != QDialog.Accepted:
                main_window_ui.tab_widget.setCurrentIndex(
                    1
                )  # Switch to another tab (index 1) if password is incorrect
                return

        # Allow changing to the selected tab
        main_window_ui.tab_widget.setCurrentIndex(index)

    main_window_ui.tab_widget.tabBarClicked.connect(handle_tab_change)

    fetch_reports_tab = QWidget(main_window)
    fetch_reports_ui = FetchReportsTab.Ui_FetchReports()
    fetch_reports_ui.setupUi(fetch_reports_tab)
    fetch_reports_controller = FetchReportsController(
        manage_vendors_controller.vendors_v50,
        manage_vendors_controller.vendors_v51,
        settings_controller.settings,
        fetch_reports_tab,
        fetch_reports_ui,
    )

    search_tab = QWidget(main_window)
    search_ui = SearchTab.Ui_Search()
    search_ui.setupUi(search_tab)
    search_controller = SearchController(search_ui, settings_controller.settings)

    # region Add tabs to main window
    main_window_ui.tab_widget.addTab(
        manage_vendors_tab, manage_vendors_tab.windowIcon(), "Manage Vendors"
    )
    main_window_ui.tab_widget.addTab(
        fetch_reports_tab, fetch_reports_tab.windowIcon(), "Fetch Reports"
    )
    main_window_ui.tab_widget.addTab(search_tab, search_tab.windowIcon(), "Search")
    main_window_ui.tab_widget.addTab(
        settings_tab, settings_tab.windowIcon(), "Settings"
    )
    main_window_ui.tab_widget.setCurrentIndex(1)
    # endregion
    main_window.show()
    sys.exit(app.exec_())


# DO NOT DELETE THE CODE BELOW, THIS WORKS BASED ON OUR PREVIOUS ITERATION OF THE PROJECT- USING MENUBAR
# class Main(QMainWindow):
#     def __init__(self):
#         super().__init__()


#     super(Main, self).__init__()
#     self.manage_vendors_tab_index = -1
#     self.fetch_report_tab_index = -1
#     self.search_tab_index = -1
#     self.settings_tab_index = -1
#     # Get the directory of the current script
#     script_dir = os.path.dirname(os.path.abspath(__file__))

#     # Construct the absolute path to the UI file
#     ui_file_path = os.path.join(script_dir, "ui", "MainWindow.ui")

#     # Load the UI file
#     loadUi(ui_file_path, self)
#     self.menu_num = 0
#     self.tabWidget.setStyleSheet("QTabBar::tab { color: black; }")
#     for i in range(self.tabWidget.count()):
#         self.tabWidget.setStyleSheet("QTabBar::tab { color: black; }")

#     self.menu_num = 0

#     self.MenuButton.clicked.connect(self.menubar)


# # Connect the manageVendorButton clicked signal to the show_manage_vendors slot
#     self.manageVendorsButton.clicked.connect(self.show_manage_vendors)
#     self.searchRepotsButton.clicked.connect(self.show_search)
#     self.settingsButton.clicked.connect(self.show_settingTab)
#     self.FetchReportsButton.clicked.connect(self.show_Fetch_reports)

# def show_manage_vendors(self):
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     manage_vendors_ui_file_path = os.path.join(script_dir, "ui", "ManageVendorsTab.ui")
#     manage_vendors_widget = QWidget()
#     loadUi(manage_vendors_ui_file_path, manage_vendors_widget)
#     if self.manage_vendors_tab_index == -1:
#         # Add the manage_vendors_widget to the QTabWidget
#         self.manage_vendors_tab_index = self.tabWidget.addTab(manage_vendors_widget, "Manage Vendors")
#     else:
#         # Switch to the existing manage vendors tab
#         self.tabWidget.setCurrentIndex(self.manage_vendors_tab_index)
#     self.tabWidget.show()

# def show_Fetch_reports(self):
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     # Construct the absolute path to the ManageVendorsTab UI file
#     fetch_reports_tab_ui_file_path = os.path.join(script_dir, "ui", "FetchReportsTab.ui")

#     # Create an instance of QWidget (or any other QWidget) and load the UI into it
#     fetch_reports_tab_widget = QWidget()
#     loadUi(fetch_reports_tab_ui_file_path, fetch_reports_tab_widget)

#     # Add the fetch_vendor_widget to the QTabWidget
#     if self.fetch_report_tab_index == -1:
#         # Add the manage_vendors_widget to the QTabWidget
#         self.fetch_report_tab_index = self.tabWidget.addTab(fetch_reports_tab_widget, "Fetch Reports")
#     else:
#         # Switch to the existing manage vendors tab
#         self.tabWidget.setCurrentIndex(self.fetch_report_tab_index)
#     self.tabWidget.show()


# def show_search(self):
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     # Construct the absolute path to the ManageVendorsTab UI file
#     search_ui_file_path = os.path.join(script_dir, "ui", "Search.ui")

#     # Create an instance of QWidget (or any other QWidget) and load the UI into it
#     search_widget = QWidget()
#     loadUi(search_ui_file_path, search_widget)

#     # Add the fetch_vendor_widget to the QTabWidget
#     if self.search_tab_index == -1:
#         # Add the manage_vendors_widget to the QTabWidget
#         self.search_tab_index = self.tabWidget.addTab(search_widget, "Search Vendors")
#     else:
#         # Switch to the existing manage vendors tab
#         self.tabWidget.setCurrentIndex(self.search_tab_index)
#     self.tabWidget.show()


# def show_settingTab(self):
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     # Construct the absolute path to the ManageVendorsTab UI file
#     settingTab_ui_file_path = os.path.join(script_dir, "ui", "Settingtab.ui")

#     # Create an instance of QWidget (or any other QWidget) and load the UI into it
#     settingTab_widget = QWidget()
#     loadUi(settingTab_ui_file_path, settingTab_widget)

#     # Add the fetch_vendor_widget to the QTabWidget
#     if self.settings_tab_index == -1:
#         # Add the manage_vendors_widget to the QTabWidget
#         self.settings_tab_index= self.tabWidget.addTab(settingTab_widget, "Settings")
#     else:
#         # Switch to the existing manage vendors tab
#         self.tabWidget.setCurrentIndex(self.settings_tab_index)
#     self.tabWidget.show()


# def menubar(self):
#     print("pressed")
#     if self.menu_num == 0:
#         self.animation = QPropertyAnimation(self.leftSubContainer, b"minimumWidth")
#         self.animation1 = QPropertyAnimation(self.leftMenu, b"minimumWidth")
#         self.animation.setDuration(250)
#         self.animation.setStartValue(55)
#         self.animation.setEndValue(250)
#         self.animation.setEasingCurve(QEasingCurve.InOutQuart)
#         self.animation.start()
#         self.animation1.setDuration(250)
#         self.animation1.setStartValue(55)
#         self.animation1.setEndValue(250)
#         self.animation1.setEasingCurve(QEasingCurve.InOutQuart)
#         self.animation1.start()
#         self.menu_num = 1

#     else:
#         self.animation = QPropertyAnimation(self.leftSubContainer, b"minimumWidth")
#         self.animation1 = QPropertyAnimation(self.leftMenu, b"minimumWidth")
#         self.animation.setDuration(250)
#         self.animation.setStartValue(250)
#         self.animation.setEndValue(40)
#         self.animation.setEasingCurve(QEasingCurve.InOutQuart)
#         self.animation.start()
#         self.animation1.setDuration(250)
#         self.animation1.setStartValue(250)
#         self.animation1.setEndValue(40)
#         self.animation1.setEasingCurve(QEasingCurve.InOutQuart)
#         self.animation1.start()
#         self.menu_num = 0

#         # Hide the Frame4 widget
#         self.frame_4.hide()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ui = Main()
#     ui.show()
#     sys.exit(app.exec_())
