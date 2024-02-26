"""This module handles all operations involving the user's settings."""

import json
from os import path
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, pyqtSignal
from ui import Settingtab
import ManageDB
from Constants import *
import GeneralUtils
from GeneralUtils import JsonModel


class Setting(Enum):
    """An enum of all settings"""

    YEARLY_DIR = 0
    OTHER_DIR = 1
    REQUEST_INTERVAL = 2
    REQUEST_TIMEOUT = 3
    CONCURRENT_VENDORS = 4
    CONCURRENT_REPORTS = 5
    USER_AGENT = 6


class SettingsModel(JsonModel):
    """This holds the user's settings.

    :param yearly_directory: The directory where yearly reports are saved. Yearly reports are reports that include all
        the available data for a year.
    :param other_directory: The default directory where non-yearly reports are saved.
    :param request_interval: The time to wait between each report request, per vendor.
    :param request_timeout: The time to wait before timing out a connection (seconds).
    :param concurrent_vendors: The max number of vendors to work on at a time.
    :param concurrent_reports: The max number of reports to work on at a time, per vendor.
    :param user_agent: The user-agent that's included in the header when making requests.
    """

    def __init__(
        self,
        # show_debug_messages: bool,
        yearly_directory: str,
        other_directory: str,
        request_interval: int,
        request_timeout: int,
        concurrent_vendors: int,
        concurrent_reports: int,
        user_agent: str,
        # default_currency: str,
    ):
        # self.show_debug_messages = show_debug_messages
        self.yearly_directory = path.abspath(yearly_directory) + path.sep
        self.other_directory = path.abspath(other_directory) + path.sep
        self.request_interval = request_interval
        self.request_timeout = request_timeout
        self.concurrent_vendors = concurrent_vendors
        self.concurrent_reports = concurrent_reports
        self.user_agent = user_agent
        # self.default_currency = default_currency

    @classmethod
    def from_json(cls, json_dict: dict):
        # show_debug_messages = (
        #     json_dict["show_debug_messages"]
        #     if "show_debug_messages" in json_dict
        #     else SHOW_DEBUG_MESSAGES
        # )
        yearly_directory = (
            json_dict["yearly_directory"]
            if "yearly_directory" in json_dict
            else YEARLY_DIR
        )
        other_directory = (
            json_dict["other_directory"]
            if "other_directory" in json_dict
            else OTHER_DIR
        )
        request_interval = (
            int(json_dict["request_interval"])
            if "request_interval" in json_dict
            else REQUEST_INTERVAL
        )
        request_timeout = (
            int(json_dict["request_timeout"])
            if "request_timeout" in json_dict
            else REQUEST_TIMEOUT
        )
        concurrent_vendors = (
            int(json_dict["concurrent_vendors"])
            if "concurrent_vendors" in json_dict
            else CONCURRENT_VENDORS
        )
        concurrent_reports = (
            int(json_dict["concurrent_reports"])
            if "concurrent_reports" in json_dict
            else CONCURRENT_REPORTS
        )
        user_agent = (
            json_dict["user_agent"] if "user_agent" in json_dict else USER_AGENT
        )
        # default_currency = (
        #     json_dict["default_currency"]
        #     if "default_currency" in json_dict
        #     else DEFAULT_CURRENCY
        # )

        return cls(
            # show_debug_messages,
            yearly_directory,
            other_directory,
            request_interval,
            request_timeout,
            concurrent_vendors,
            concurrent_reports,
            user_agent,
            # default_currency,
        )


class SettingsController(QObject):
    """Controls the Settings tab

    :param settings_widget: The settings widget.
    :param settings_ui: The UI for settings_widget.
    """

    settings_changed_signal = pyqtSignal(SettingsModel)

    def __init__(self, settings_widget: QWidget, settings_ui: Settingtab.Ui_SettingTab):
        # region General
        super().__init__()
        self.settings_widget = settings_widget

        json_string = GeneralUtils.read_json_file(
            SETTINGS_FILE_DIR + SETTINGS_FILE_NAME
        )
        json_dict = json.loads(json_string)
        self.settings = SettingsModel.from_json(json_dict)

        # self.show_debug_checkbox = settings_ui.show_debug_check_box
        # self.show_debug_checkbox.setChecked(self.settings.show_debug_messages)
        # endregion

        # region Reports
        self.dir_edit = settings_ui.directory_edit
        self.dir_type_comboBox = settings_ui.directory_type_comboBox
        self.request_interval_spin_box = settings_ui.request_interval_spin_box
        self.request_timeout_spin_box = settings_ui.request_timeout_spin_box
        self.concurrent_vendors_spin_box = settings_ui.concurrent_vendors_spin_box
        self.concurrent_reports_spin_box = settings_ui.concurrent_reports_spin_box
        self.user_agent_edit = settings_ui.user_agent_edit

        self.dir_edit.textChanged.connect(self.on_dir_edit_changed)
        self.dir_type_comboBox.currentIndexChanged.connect(self.update_dir_edit)
        # self.yearly_dir_edit.setText(self.settings.yearly_directory)
        # self.other_dir_edit.setText(self.settings.other_directory)
        self.request_interval_spin_box.setValue(self.settings.request_interval)
        self.request_timeout_spin_box.setValue(self.settings.request_timeout)
        self.concurrent_vendors_spin_box.setValue(self.settings.concurrent_vendors)
        self.concurrent_reports_spin_box.setValue(self.settings.concurrent_reports)
        self.user_agent_edit.setText(self.settings.user_agent)

        settings_ui.select_directory_button.clicked.connect(
            self.on_directory_setting_clicked
        )
        # settings_ui.yearly_directory_button.clicked.connect(
        #     lambda: self.on_directory_setting_clicked(Setting.YEARLY_DIR)
        # )
        # settings_ui.other_directory_button.clicked.connect(
        #     lambda: self.on_directory_setting_clicked(Setting.OTHER_DIR)
        # )

        # region Search
        # set up restore database button
        self.is_rebuilding_database = False
        self.update_database_dialog = ManageDB.UpdateDatabaseProgressDialogController(
            self.settings_widget
        )
        self.rebuild_database_button = settings_ui.settings_rebuild_database_button
        self.rebuild_database_button.clicked.connect(self.on_rebuild_database_clicked)
        # endregion

        settings_ui.save_button.clicked.connect(self.on_save_button_clicked)

    def update_dir_edit(self, index):
        if self.dir_type_comboBox.currentText() == "Yearly reports":
            self.dir_edit.setText(self.settings.yearly_directory)
        elif self.dir_type_comboBox.currentText() == "Other reports":
            self.dir_edit.setText(self.settings.other_directory)
        else:
            self.dir_edit.setText("")

    def on_dir_edit_changed(self, new_text):
        if self.dir_type_comboBox.currentText() == "Yearly reports":
            self.settings.yearly_directory = new_text
        elif self.dir_type_comboBox.currentText() == "Other reports":
            self.settings.other_directory = new_text

    def on_directory_setting_clicked(self):
        """Handles the signal emitted when a choose folder button is clicked

        :param setting: The setting to be changed
        """
        if self.dir_type_comboBox.currentText() == "Yearly reports":
            setting = Setting.YEARLY_DIR
        elif self.dir_type_comboBox.currentText() == "Other reports":
            setting = Setting.OTHER_DIR
        dir_path = GeneralUtils.choose_directory()
        if dir_path:
            if setting == Setting.YEARLY_DIR:
                # self.yearly_dir_edit.setText(dir_path)
                self.settings.yearly_directory = dir_path
            elif setting == Setting.OTHER_DIR:
                # self.other_dir_edit.setText(dir_path)
                self.settings.other_directory = dir_path

            self.dir_edit.setText(dir_path)

    def on_save_button_clicked(self):
        """Handles the signal emitted when the save button is clicked"""
        self.update_settings()
        self.save_settings_to_disk()
        self.settings_changed_signal.emit(self.settings)
        GeneralUtils.show_message("Changes saved!")

    def on_rebuild_database_clicked(self):
        """Restores the database when the restore database button is clicked"""
        if not self.is_rebuilding_database:  # check if already running
            if GeneralUtils.ask_confirmation(
                "Are you sure you want to rebuild the database?"
            ):
                self.is_rebuilding_database = True
                self.update_database_dialog.update_database(
                    ManageDB.get_all_report_files() + ManageDB.get_all_cost_files(),
                    True,
                )
                self.is_rebuilding_database = False
        else:
            # if self.settings.show_debug_messages:
            #     print("Database is already being rebuilt")
            pass

    def update_settings(self):
        """Updates the app's settings using the values entered on the UI"""
        # self.settings.show_debug_messages = self.show_debug_checkbox.isChecked()
        # self.settings.yearly_directory = self.yearly_dir_edit.text()
        # self.settings.other_directory = self.other_dir_edit.text()
        self.settings.request_interval = self.request_interval_spin_box.value()
        self.settings.request_timeout = self.request_timeout_spin_box.value()
        self.settings.concurrent_vendors = self.concurrent_vendors_spin_box.value()
        self.settings.concurrent_reports = self.concurrent_reports_spin_box.value()
        self.settings.user_agent = self.user_agent_edit.text()
        # self.settings.default_currency = self.default_currency_combobox.currentText()

    def save_settings_to_disk(self):
        """Saves all settings to disk"""
        json_string = json.dumps(self.settings, default=lambda o: o.__dict__)
        GeneralUtils.save_json_file(SETTINGS_FILE_DIR, SETTINGS_FILE_NAME, json_string)
