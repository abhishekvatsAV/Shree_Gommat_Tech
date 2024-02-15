"""This module handles all operations involving managing vendors."""

import csv
import os
import json
import validators
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QDialogButtonBox,
    QWidget,
    QCheckBox,
    QMainWindow,
    QDateEdit,
)

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QObject, QModelIndex, pyqtSignal
from ui import (
    ManageVendorsTab,
    AddVendor,
    AddVendor51,
    RemoveVendorDialog,
    ImportVersion,
    EditVendors51,
    EditVendors50,
)

# import ManageDB
import GeneralUtils
from GeneralUtils import JsonModel
from Constants import *
import datetime
from PyQt5.QtCore import QDate
import datetime
from PyQt5.QtCore import QDate

# from Settings import SettingsModel


class Vendor(JsonModel):
    """This holds a vendor's information

    :param name: The vendor's unique name (Mandatory)
    :param base_url: The base URL for making sushi report calls (must end with '/reports', mandatory)
    :param customer_id: The customer id used in sushi report calls
    :param requestor_id: The requestor id id used in sushi report calls
    :param api_key: The api key id used in sushi report calls
    :param platform: The platform id used in sushi report calls
    :param is_non_sushi: This indicates if this vendor is sushi compatible
    :param description: A description of this vendor
    :param companies: More information about the vendor
    """

    def __init__(
        self,
        name: str,
        base_url: str,
        customer_id: str,
        requestor_id: str,
        api_key: str,
        platform: str,
        is_non_sushi: bool,
        description: str,
        companies: str,
    ):
        self.name = name
        self.base_url = base_url
        self.customer_id = customer_id
        self.requestor_id = requestor_id
        self.api_key = api_key
        self.platform = platform
        self.is_non_sushi = is_non_sushi
        self.description = description
        self.companies = companies


class Vendor51(JsonModel):
    """This holds a vendor's information

    :param name: The vendor's unique name (Mandatory, unique enforced)
    :param is_version_5_0_or_5_1: Indicates if this is for version 5.0 or 5.1 (Mandatory)
    :param base_url: The base URL for making sushi report calls (must end with '/counter/r51/reports', mandatory for 5.0)
    :param starting_year: Starting year for this version (5.0 or 5.1) (Mandatory)
    :param customer_id: The customer id used in sushi report calls (Mandatory)
    :param requestor_id: The requestor id used in sushi report calls
    :param api_key: The api key used in sushi report calls
    :param platform: The platform id used in sushi report calls
    :param requires_two_attempts: Whether it requires two attempts per report (Y/N, mandatory)
    :param does_ip_checking: Whether it does IP checking (Y/N, mandatory)
    :param needs_throttling: Whether it needs requests throttled (Y/N, mandatory)
    :param notes: Additional notes
    :param provider: Provider information
    """

    def __init__(
        self,
        name: str,
        is_version_5_0_or_5_1: str,
        base_url: str,
        starting_year: str,
        customer_id: str,
        requestor_id: str,
        api_key: str,
        platform: str,
        requires_two_attempts: bool,
        does_ip_checking: bool,
        needs_throttling: bool,
        notes: str,
        provider: str,
    ):
        self.name = name
        self.is_version_5_0_or_5_1 = is_version_5_0_or_5_1  # "5.1"
        self.base_url = base_url  # https://...../counter/r51/reports
        self.starting_year = starting_year
        self.customer_id = customer_id
        self.requestor_id = requestor_id
        self.api_key = api_key
        self.platform = platform
        self.requires_two_attempts = requires_two_attempts  # True or False
        self.does_ip_checking = does_ip_checking  # True or False
        self.needs_throttling = needs_throttling  # True or False
        self.notes = notes
        self.provider = provider


class ManageVendorsController(QObject):
    """Controls the Manage Vendors tab

    :param manage_vendors_widget: The manage vendors widget.
    :param manage_vendors_ui: The UI for the manage_vendors_widget.
    """

    def __init__(
        self,
        manage_vendors_widget: QWidget,
        manage_vendors_ui: ManageVendorsTab.Ui_manage_vendor_tab,
    ):
        super().__init__()
        self.manage_vendors_widget = manage_vendors_widget
        self.curr_version = "5.1"

        self.add_vendor_button = manage_vendors_ui.addVendorButton
        self.edit_vendor_button = manage_vendors_ui.editvendorsbutton

        # button to see vendor list of version 5.0
        self.version50_button = manage_vendors_ui.version50
        self.version50_button.clicked.connect(self.on_click_version50)

        # button to see vendor list of version 5.1
        self.version51_button = manage_vendors_ui.version51
        self.version51_button.clicked.connect(self.on_click_version51)

        self.export_vendors_button = manage_vendors_ui.exportVendorsButton
        self.import_vendors_button = manage_vendors_ui.importVendorsButton

        self.add_vendor_button.clicked.connect(
            lambda: (
                self.on_add_vendor51_clicked()
                if self.curr_version == "5.1"
                else self.on_add_vendor_clicked()
            )
        )

        self.import_vendors_button.clicked.connect(self.on_import_vendors_clicked)
        self.export_vendors_button.clicked.connect(self.on_export_vendors_clicked)

        self.edit_vendor_button.clicked.connect(
            lambda: (
                self.edit_vendor51_window()
                if self.curr_version == "5.1"
                else self.edit_vendor50_window()
            )
        )
        self.vendor_list_view = manage_vendors_ui.vendorsListView
        self.vendor_list_view.clicked.connect(self.on_vendor_selected)

        # self.settings = settings

        self.vendors = []
        self.vendor_names = set()  # Hash set for faster operations
        self.vendors_v50: list[Vendor] = []
        self.vendors_v51: list[Vendor51] = []
        self.vendor_names_v50 = set()
        self.vendor_names_v51 = set()

        self.get_vendor_names_v50()
        self.get_vendor_names_v51()
        self.sort_vendors()
        self.on_click_version51()

    # """
    # Show List According to selected version Section
    # """

    def update_vendor_names(self):
        """Updates the local set of vendor names used for validation"""
        self.vendor_names_v50.clear()
        for vendor in self.vendors_v50:
            self.vendor_names_v50.add(vendor.name.lower())

        self.vendor_names_v51.clear()
        for vendor in self.vendors_v51:
            self.vendor_names_v51.add(vendor.name.lower())

    def sort_vendors(self):
        """Sorts the vendors alphabetically based their names"""
        self.vendors_v50 = sorted(
            self.vendors_v50, key=lambda vendor: vendor.name.lower()
        )
        self.vendors_v51 = sorted(
            self.vendors_v51, key=lambda vendor: vendor.name.lower()
        )

    def get_vendor_names_v50(self):
        """
        Retrieves vendor names and other information from a JSON file and populates the model.

        This method reads vendor data from a JSON file, creates Vendor objects, and populates the model
        with the vendor names. It also adds the lowercase version of each vendor name to a set for easy lookup.
        """
        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_directory, "vendors.dat")

            # Read JSON data from vendors.dat
            with open(file_path, "r") as file:
                vendors_data = json.load(file)

            # Populate the model with vendor names
            for vendor_data in vendors_data:
                vendor_name = vendor_data.get("name", "")
                base_url = vendor_data.get("base_url", "")
                customer_id = vendor_data.get("customer_id", "")
                requestor_id = vendor_data.get("requestor_id", "")
                api_key = vendor_data.get("api_key", "")
                platform = vendor_data.get("platform", "")
                is_non_sushi = vendor_data.get("is_non_sushi", False)
                description = vendor_data.get("description", "")
                companies = vendor_data.get("companies", "")

                # Create a Vendor object and append it to the array
                vendor_object = Vendor(
                    name=vendor_name,
                    base_url=base_url,
                    customer_id=customer_id,
                    requestor_id=requestor_id,
                    api_key=api_key,
                    platform=platform,
                    is_non_sushi=is_non_sushi,
                    description=description,
                    companies=companies,
                )
                if vendor_name:
                    self.vendors_v50.append(vendor_object)
                    vendor_name: str = vendor_name.lower()
                    self.vendor_names_v50.add(vendor_name)

        except Exception as e:
            print(f"Error loading vendors: {e}")

    def get_vendor_names_v51(self):
        """
        Retrieves vendor names and populates the model with vendor objects.

        This method reads JSON data from a file, creates Vendor objects, and appends them to an array.
        It also adds the lowercase version of each vendor name to a set for easy lookup.
        """
        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_directory, "vendors51.dat")

            # Read JSON data from vendors.dat
            with open(file_path, "r") as file:
                vendors_data = json.load(file)

            # Populate the model with vendor names
            for vendor_data in vendors_data:
                vendor_name = vendor_data.get("name", "")
                is_version_5_0_or_5_1 = vendor_data.get("is_version_5_0_or_5_1", "")
                base_url = vendor_data.get("base_url", "")
                starting_year = vendor_data.get("starting_year", "")
                customer_id = vendor_data.get("customer_id", "")
                requestor_id = vendor_data.get("requestor_id", "")
                api_key = vendor_data.get("api_key", "")
                platform = vendor_data.get("platform", "")
                requires_two_attempts = vendor_data.get("requires_two_attempts", False)
                does_ip_checking = vendor_data.get("does_ip_checking", False)
                needs_throttling = vendor_data.get("needs_throttling", False)
                notes = vendor_data.get("notes", "")
                provider = vendor_data.get("provider", "")

                # Create a Vendor object and append it to the array
                vendor_object = Vendor51(
                    name=vendor_name,
                    is_version_5_0_or_5_1=is_version_5_0_or_5_1,
                    base_url=base_url,
                    starting_year=starting_year,
                    customer_id=customer_id,
                    requestor_id=requestor_id,
                    api_key=api_key,
                    platform=platform,
                    requires_two_attempts=requires_two_attempts,
                    does_ip_checking=does_ip_checking,
                    needs_throttling=needs_throttling,
                    notes=notes,
                    provider=provider,
                )
                if vendor_name:
                    self.vendors_v51.append(vendor_object)
                    vendor_name: str = vendor_name.lower()
                    self.vendor_names_v51.add(vendor_name)

        except Exception as e:
            print(f"Error loading vendors: {e}")

    def on_click_version50(self):
        """
        Handle the click event for the version 5.0 button.
        Loads vendors data for version 5.0 and updates the vendor list view accordingly.
        """
        try:
            # Create a QStringListModel
            model = QStandardItemModel()

            for vendor_data in self.vendors_v50:
                vendor_name = vendor_data.name
                item = QStandardItem(vendor_name)
                item.setEditable(False)
                model.appendRow(item)

            self.version50_button.setStyleSheet("background-color: #2095E6;")
            self.version51_button.setStyleSheet("")
            # Set the model for the QListView
            self.vendor_list_view.setModel(model)
            self.curr_version = "5.0"

        except Exception as e:
            print(f"Error loading vendors: {e}")

    def on_click_version51(self):
        """
        Handle the click event for the version 5.1 button.
        Loads vendors_v51 data into the vendor_list_view.

        Raises:
            Exception: If there is an error loading vendors.
        """
        try:
            # Create a QStringListModel
            model = QStandardItemModel()

            for vendor_data in self.vendors_v51:
                vendor_name = vendor_data.name
                item = QStandardItem(vendor_name)
                item.setEditable(False)
                model.appendRow(item)

            self.version51_button.setStyleSheet("background-color: #2095E6;")
            self.version50_button.setStyleSheet("")

            # Set the model for the QListView
            self.vendor_list_view.setModel(model)
            self.curr_version = "5.1"

        except Exception as e:
            print(f"Error loading vendors: {e}")

    # """
    # Adding A New Vendor Section
    # """

    def add_vendor(
        self, new_vendor: Vendor51 | Vendor, version: str
    ) -> tuple[bool, str]:
        """Adds a new vendor to the system if the vendor is valid

        :param new_vendor: The new vendor to be added
        :returns: (is_successful, message) A Tuple with the completion status and a message
        """

        # Check if vendor name is valid
        is_valid, message = self.validate_new_name(new_vendor.name, "", version)
        if not is_valid:
            return is_valid, message

        if version == "5.0":
            if not new_vendor.is_non_sushi:
                is_valid, message = self.validate_url(new_vendor.base_url)
                if not is_valid:
                    return is_valid, message
                if new_vendor.customer_id == "":
                    return False, "Customer Id cannot be empty."
        else:
            is_valid, message = self.validate_url(new_vendor.base_url)
            if not is_valid:
                return is_valid, message
            if new_vendor.customer_id == "":
                return False, "Customer Id cannot be empty."

        if version == "5.1":
            self.vendors_v51.append(new_vendor)
            self.vendor_names_v51.add(new_vendor.name.lower())
            self.on_click_version51()
            self.update_vendors51_dat_file()
        else:
            self.vendors_v50.append(new_vendor)
            self.vendor_names_v50.add(new_vendor.name.lower())
            self.on_click_version50()
            self.update_vendors_dat_file()

        return True, ""

    def on_add_vendor51_clicked(self):
        """Handles the signal emitted when the add vendor button is clicked

        A dialog is show to allow the user to enter a new vendor's information. If the information entered is valid,
        the vendor is added to the system
        """
        vendor_dialog = QMainWindow()
        vendor_dialog_ui = AddVendor51.Ui_addVendor51Dialog()
        vendor_dialog_ui.setupUi(vendor_dialog)
        vendor_dialog.show()

        name_edit = vendor_dialog_ui.nameEdit
        base_url_edit = vendor_dialog_ui.baseUrlEdit

        start_year = vendor_dialog_ui.All_reports_edit_fetch
        # Get the current date and time
        current_date = datetime.datetime.now()
        # Calculate the date for the same day of the last year
        last_year_date = QDate(
            current_date.year - 1, current_date.month, current_date.day
        )
        # set previous year date to the start_year
        start_year.setDate(last_year_date)

        customer_id_edit = vendor_dialog_ui.customerIdEdit
        requestor_id_edit = vendor_dialog_ui.requestorIdEdit
        api_key_edit = vendor_dialog_ui.apiKeyEdit
        platform_edit = vendor_dialog_ui.platformEdit
        two_attempts_check_box = vendor_dialog_ui.two_attempts_check_box
        ip_checking_check_box = vendor_dialog_ui.ip_checking_check_box
        requests_throttled_check_box = vendor_dialog_ui.requests_throttled_check_box
        provider_edit = vendor_dialog_ui.providerEdit
        notes_edit = vendor_dialog_ui.notesEdit

        name_validation_label = vendor_dialog_ui.name_validation_label
        name_validation_label.hide()
        url_validation_label = vendor_dialog_ui.url_validation_label
        url_validation_label.hide()

        name_edit.textChanged.connect(
            lambda new_name: self.on_name_text_changed(
                new_name, "", name_validation_label, "5.1"
            )
        )

        base_url_edit.textChanged.connect(
            lambda url: self.on_url_text_changed(url, url_validation_label, True)
        )

        def attempt_add_vendor():
            vendor = Vendor51(
                name_edit.text(),
                "5.1",
                base_url_edit.text(),
                start_year.text(),
                customer_id_edit.text(),
                requestor_id_edit.text(),
                api_key_edit.text(),
                platform_edit.text(),
                two_attempts_check_box.isChecked(),
                ip_checking_check_box.isChecked(),
                requests_throttled_check_box.isChecked(),
                notes_edit.text(),
                provider_edit.text(),
            )

            is_valid, message = self.add_vendor(vendor, "5.1")
            if is_valid:
                self.sort_vendors()
                self.on_click_version51()
                self.update_vendors51_dat_file()
                self.update_vendor_names()
                self.selected_index = -1
                vendor_dialog.close()
            else:
                GeneralUtils.show_message(message)

        button_box = vendor_dialog_ui.buttonBox
        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.clicked.connect(attempt_add_vendor)
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.clicked.connect(lambda: vendor_dialog.close())

        vendor_dialog.exec_()

    def on_add_vendor_clicked(self):
        """
        Event handler for the "Add Vendor" button click.
        Opens a dialog to add a new vendor and performs necessary validations and actions.
        """
        vendor_dialog = QMainWindow()
        vendor_dialog_ui = AddVendor.Ui_addVendorDialog()

        vendor_dialog_ui.setupUi(vendor_dialog)
        vendor_dialog.show()

        name_edit = vendor_dialog_ui.nameEdit
        base_url_edit = vendor_dialog_ui.baseUrlEdit
        customer_id_edit = vendor_dialog_ui.customerIdEdit
        requestor_id_edit = vendor_dialog_ui.requestorIdEdit
        api_key_edit = vendor_dialog_ui.apiKeyEdit
        platform_edit = vendor_dialog_ui.platformEdit
        non_sushi_check_box = vendor_dialog_ui.non_Sushi_check_box
        description_edit = vendor_dialog_ui.descriptionEdit
        companies_edit = vendor_dialog_ui.companiesEdit

        name_validation_label = vendor_dialog_ui.name_validation_label
        name_validation_label.hide()
        url_validation_label = vendor_dialog_ui.url_validation_label
        url_validation_label.hide()

        name_edit.textChanged.connect(
            lambda new_name: self.on_name_text_changed(
                new_name, "", name_validation_label, "5.0"
            )
        )

        base_url_edit.textChanged.connect(
            lambda url: self.on_url_text_changed(
                url, url_validation_label, True, non_sushi_check_box
            )
        )

        def attempt_add_vendor():
            vendor = Vendor(
                name_edit.text(),
                base_url_edit.text(),
                customer_id_edit.text(),
                requestor_id_edit.text(),
                api_key_edit.text(),
                platform_edit.text(),
                non_sushi_check_box.isChecked(),
                description_edit.text(),
                companies_edit.text(),
            )

            is_valid, message = self.add_vendor(vendor, "5.0")
            if is_valid:
                self.sort_vendors()
                self.on_click_version50()
                self.update_vendors_dat_file()
                self.update_vendor_names()
                self.selected_index = -1
                vendor_dialog.close()
            else:
                GeneralUtils.show_message(message)

        button_box = vendor_dialog_ui.buttonBox
        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.clicked.connect(attempt_add_vendor)
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.clicked.connect(lambda: vendor_dialog.close())

        vendor_dialog.exec_()

    # """
    # Data Validation Section
    # """

    def on_name_text_changed(
        self,
        new_name: str,
        original_name: str,
        validation_label: QLabel,
        version: str = "5.1",
        validate: bool = True,
    ):
        """Handles the signal emitted when a vendor's name is changed

        :param new_name: The new name entered in the text field
        :param original_name: The vendor's original name
        :param validation_label: The label to show validation messages
        :param version: The version of the Vendor List to put the vendor
        :param validate: This indicates whether the new_name should be validated
        """
        if not validate:
            validation_label.hide()
            return

        is_valid, message = self.validate_new_name(new_name, original_name, version)

        if is_valid:
            validation_label.hide()
        else:
            validation_label.show()
            validation_label.setText(message)

    def validate_new_name(
        self, new_name: str, original_name: str = "", version: str = "5.1"
    ) -> tuple[bool, str]:
        """Validates a new vendor name

        :param new_name: The new name to be validated
        :param original_name: The original name
        :returns: (is_successful, message) A Tuple with the completion status and a message
        """
        if not new_name:
            return False, "Vendor name can't be empty"

        if version == "5.1":
            if (
                new_name.lower() in self.vendor_names_v51
                and new_name.lower() != original_name.lower()
            ):
                return False, "Duplicate vendor name"
            else:
                return True, ""
        elif version == "5.0":
            if (
                new_name.lower() in self.vendor_names_v50
                and new_name.lower() != original_name.lower()
            ):
                return False, "Duplicate vendor name"
            else:
                return True, ""
        else:
            return True, ""

    def on_url_text_changed(
        self,
        url: str,
        validation_label: QLabel,
        validate: bool,
        non_sushi_check_box: str | QCheckBox = "",
    ):
        """Handles the signal emitted when a vendor's URL is changed

        :param url: The URL entered in the text field
        :param validation_label: The label to show validation messages
        :param validate: This indicates whether the url should be validated
        :param non_sushi_check_box: The non_sushi checkbox indicator. If checked, the URL is not validated
        """
        if not validate:
            validation_label.hide()
            return

        if self.curr_version == "5.0" and non_sushi_check_box.isChecked():
            validation_label.hide()
            return

        is_valid, message = self.validate_url(url)
        if is_valid:
            validation_label.hide()
        else:
            validation_label.show()
            validation_label.setText(message)

    def validate_url(self, url: str) -> tuple[bool, str]:
        """Validates a new url

        :param url: The URL to be validated
        :returns: (is_successful, message) A Tuple with the completion status and a message
        """
        if not validators.url(url):
            return False, "Invalid Url"
        elif self.curr_version == "5.0" and not url.endswith("/reports"):
            return False, "URL must end with '/reports'"
        elif self.curr_version == "5.1" and not url.endswith("/counter/r51/reports"):
            return False, "URL must end with '/counter/r51/reports'"
        else:
            return True, ""

    # """
    # Update dat files Section
    # """

    def write_data_to_file(self, file_path: str, vendors: list[Vendor51 | Vendor]):
        """
        Write the data of vendors to a file in JSON format.

        Args:
            file_path (str): The path of the file to write the data to.
            vendors (list[Vendor51 | Vendor]): The list of vendors to write to the file.

        Returns:
            None
        """
        data = [vendor.__dict__ for vendor in vendors]
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)

    def update_vendors51_dat_file(self):
        """
        Updates the 'vendors51.dat' file with the data from 'self.vendors_v51'.
        """
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, "vendors51.dat")
        self.write_data_to_file(file_path, self.vendors_v51)

    def update_vendors_dat_file(self):
        """
        Updates the vendors.dat file with the data from self.vendors_v50.
        """
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, "vendors.dat")
        self.write_data_to_file(file_path, self.vendors_v50)

    # """
    # Import Export Section
    # """

    def import_vendor50_clicked(self, import_version_dialog):
        import_version_dialog.close()
        file_path = GeneralUtils.choose_file(TSV_FILTER)

        if file_path:
            self.import_vendors50_tsv(file_path)

    def import_vendors51_clicked(self, import_version_dialog):
        import_version_dialog.close()
        file_path = GeneralUtils.choose_file(TSV_FILTER)
        if file_path:
            self.import_vendors51_tsv(file_path)

    def on_import_vendors_clicked(self):
        """Handles the signal emitted when the import vendors button is clicked.
        A file select dialog is shown to allow the user to select the vendors TSV file to import. The selected file is then imported.
        """
        import_version_dialog = QMainWindow()
        import_version_dialog_ui = ImportVersion.Ui_importVersionDialog()

        import_version_dialog_ui.setupUi(import_version_dialog)
        import_version_dialog.show()

        select_version50_button = import_version_dialog_ui.importVersion50
        select_version51_button = import_version_dialog_ui.importVersion51

        select_version50_button.clicked.connect(
            lambda: self.import_vendor50_clicked(import_version_dialog)
        )
        select_version51_button.clicked.connect(
            lambda: self.import_vendors51_clicked(import_version_dialog)
        )

        import_version_dialog.exec_()

    def import_vendors51_tsv(self, file_path):
        """Imports the vendors version 5.1 from a TSV file path to the system

        :param file_path: The file path of the vendors TSV file
        """
        try:
            tsv_file = open(file_path, "r", encoding="utf-8", newline="")
            reader = csv.DictReader(tsv_file, delimiter="\t")
            for row in reader:
                if "requires_two_attempts" in row:
                    requires_two_attempts = (
                        row["requires_two_attempts"].lower() == "true"
                    )
                else:
                    requires_two_attempts = False

                if "does_ip_checking" in row:
                    does_ip_checking = row["does_ip_checking"].lower() == "true"
                else:
                    does_ip_checking = False

                if "needs_throttling" in row:
                    needs_throttling = row["needs_throttling"].lower() == "true"
                else:
                    needs_throttling = False

                vendor = Vendor51(
                    row["name"] if "name" in row else "",
                    (
                        row["is_version_5_0_or_5_1"]
                        if "is_version_5_0_or_5_1" in row
                        else ""
                    ),
                    row["base_url"] if "base_url" in row else "",
                    row["starting_year"] if "starting_year" in row else "",
                    row["customer_id"] if "customer_id" in row else "",
                    row["requestor_id"] if "requestor_id" in row else "",
                    row["api_key"] if "api_key" in row else "",
                    row["platform"] if "platform" in row else "",
                    requires_two_attempts,
                    does_ip_checking,
                    needs_throttling,
                    row["notes"] if "notes" in row else "",
                    row["provider"] if "provider" in row else "",
                )
                is_valid, message = self.add_vendor(vendor, "5.1")
                if not is_valid:
                    print(f"error in importing vendors version 5.1 : {message}")
                    # if self.settings.show_debug_messages: print(message)

            tsv_file.close()

            self.sort_vendors()
            self.selected_index = -1
            self.on_click_version51()
            self.update_vendor_names()
            self.update_vendors51_dat_file()

            GeneralUtils.show_message(f"Import successful!")
        except Exception as e:
            # if self.settings.show_debug_messages: print(f"File import failed: {e}")
            GeneralUtils.show_message(f"File import failed: {e}")

    def import_vendors50_tsv(self, file_path):
        """Imports the vendors in a TSV file path to the system

        :param file_path: The file path of the vendors TSV file
        """
        try:
            tsv_file = open(file_path, "r", encoding="utf-8", newline="")
            reader = csv.DictReader(tsv_file, delimiter="\t")
            for row in reader:
                if "is_non_sushi" in row:
                    is_non_sushi = row["is_non_sushi"].lower() == "true"
                else:
                    is_non_sushi = False
                vendor = Vendor(
                    row["name"] if "name" in row else "",
                    row["base_url"] if "base_url" in row else "",
                    row["customer_id"] if "customer_id" in row else "",
                    row["requestor_id"] if "requestor_id" in row else "",
                    row["api_key"] if "api_key" in row else "",
                    row["platform"] if "platform" in row else "",
                    is_non_sushi,
                    row["description"] if "description" in row else "",
                    row["companies"] if "companies" in row else "",
                )
                is_valid, message = self.add_vendor(vendor, "5.0")
                if not is_valid:
                    print(f"error in importing vendors version 5.0 : {message}")
                    # if self.settings.show_debug_messages: print(message)

            tsv_file.close()

            self.sort_vendors()
            self.selected_index = -1
            self.on_click_version50()
            self.update_vendor_names()
            self.update_vendors_dat_file()

            GeneralUtils.show_message(f"Import successful!")
        except Exception as e:
            # if self.settings.show_debug_messages: print(f"File import failed: {e}")
            GeneralUtils.show_message(f"File import failed: {e}")

    def on_export_vendors_clicked(self):
        """Handles the signal emitted when the export vendors button is clicked.

        A folder select dialog is shown to allow the user to select the target directory to export the vendors file to.
        A vendors TSV file containing all the vendors in the system is then exported
        """
        dir_path = GeneralUtils.choose_directory()
        if dir_path:
            self.export_vendors_tsv(dir_path)

    def export_vendors_tsv(self, dir_path):
        """Exports all vendor information as a TSV file to a directory

        :param dir_path: The directory path to export the vendors TSV file to
        """
        file_path_v50 = f"{dir_path}{EXPORT_VENDORS50_FILE_NAME}"
        column_names_v50 = [
            "name",
            "base_url",
            "customer_id",
            "requestor_id",
            "api_key",
            "platform",
            "is_non_sushi",
            "description",
            "companies",
        ]
        try:
            tsv_file = open(file_path_v50, "w", encoding="utf-8", newline="")
            tsv_dict_writer = csv.DictWriter(tsv_file, column_names_v50, delimiter="\t")
            tsv_dict_writer.writeheader()

            for vendor in self.vendors_v50:
                tsv_dict_writer.writerow(vendor.__dict__)

            tsv_file.close()
            GeneralUtils.show_message(f"Exported to {file_path_v50}")

        except Exception as e:
            # if self.settings.show_debug_messages: print(f"File export failed: {e}")
            GeneralUtils.show_message(f"File export failed: {e}")

        # Now we will save one more file for vendor version 5.1
        file_path_v51 = f"{dir_path}{EXPORT_VENDORS51_FILE_NAME}"
        column_names_v51 = [
            "name",
            "is_version_5_0_or_5_1",
            "base_url",
            "starting_year",
            "customer_id",
            "requestor_id",
            "api_key",
            "platform",
            "requires_two_attempts",
            "does_ip_checking",
            "needs_throttling",
            "notes",
            "provider",
        ]
        try:
            tsv_file = open(file_path_v51, "w", encoding="utf-8", newline="")
            tsv_dict_writer = csv.DictWriter(tsv_file, column_names_v51, delimiter="\t")
            tsv_dict_writer.writeheader()

            for vendor in self.vendors_v51:
                tsv_dict_writer.writerow(vendor.__dict__)

            tsv_file.close()
            GeneralUtils.show_message(f"Exported to {file_path_v51}")

        except Exception as e:
            # if self.settings.show_debug_messages: print(f"File export failed: {e}")
            GeneralUtils.show_message(f"File export failed: {e}")

    # """
    # Edit section
    # """

    def on_vendor_selected(self, model_index: QModelIndex):
        """Handles the signal emitted when a vendor is selected

        :param model_index: An object containing the location of the vendor on the vendor list
        """
        self.selected_index = model_index.row()

    def edit_vendor51_window(self):
        """Handles the signal emitted when the edit vendor button is clicked

        A dialog is show to allow the user to update vendor's information. If the information entered is valid,
        the vendor is updated to the system
        """
        edit_vendor_dialog = QMainWindow()
        edit_vendor_dialog_ui = EditVendors51.Ui_editVendors51()
        edit_vendor_dialog_ui.setupUi(edit_vendor_dialog)
        edit_vendor_dialog.show()

        name_edit = edit_vendor_dialog_ui.nameEdit
        base_url_edit = edit_vendor_dialog_ui.baseUrlEdit
        start_year = edit_vendor_dialog_ui.All_reports_edit_fetch
        customer_id_edit = edit_vendor_dialog_ui.customerIdEdit
        requestor_id_edit = edit_vendor_dialog_ui.requestorIdEdit
        api_key_edit = edit_vendor_dialog_ui.apiKeyEdit
        platform_edit = edit_vendor_dialog_ui.platformEdit
        two_attempts_check_box = edit_vendor_dialog_ui.two_attempts_check_box
        ip_checking_check_box = edit_vendor_dialog_ui.ip_checking_check_box
        requests_throttled_check_box = (
            edit_vendor_dialog_ui.requests_throttled_check_box
        )
        provider_edit = edit_vendor_dialog_ui.providerEdit
        notes_edit = edit_vendor_dialog_ui.notesEdit

        name_validation_label = edit_vendor_dialog_ui.name_validation_label
        name_validation_label.hide()
        url_validation_label = edit_vendor_dialog_ui.url_validation_label
        url_validation_label.hide()

        selected_vendor = self.vendors_v51[self.selected_index]

        name_edit.setText(selected_vendor.name)
        base_url_edit.setText(selected_vendor.base_url)
        current_date = datetime.datetime.now()
        starting_year = QDate(
            int(selected_vendor.starting_year), current_date.month, current_date.day
        )
        start_year.setDate(starting_year)
        customer_id_edit.setText(selected_vendor.customer_id)
        requestor_id_edit.setText(selected_vendor.requestor_id)
        api_key_edit.setText(selected_vendor.api_key)
        platform_edit.setText(selected_vendor.platform)
        two_attempts_check_box.setChecked(selected_vendor.requires_two_attempts)
        ip_checking_check_box.setChecked(selected_vendor.does_ip_checking)
        requests_throttled_check_box.setChecked(selected_vendor.needs_throttling)
        provider_edit.setText(selected_vendor.provider)
        notes_edit.setText(selected_vendor.notes)

        name_edit.textChanged.connect(
            lambda new_name: self.on_name_text_changed(
                new_name, selected_vendor.name, name_validation_label, "5.1"
            )
        )

        base_url_edit.textChanged.connect(
            lambda url: self.on_url_text_changed(url, url_validation_label, True)
        )

        def attempt_edit_vendor():
            vendor = Vendor51(
                name_edit.text(),
                "5.1",
                base_url_edit.text(),
                start_year.text(),
                customer_id_edit.text(),
                requestor_id_edit.text(),
                api_key_edit.text(),
                platform_edit.text(),
                two_attempts_check_box.isChecked(),
                ip_checking_check_box.isChecked(),
                requests_throttled_check_box.isChecked(),
                notes_edit.text(),
                provider_edit.text(),
            )

            is_valid, message = self.edit_vendor(vendor, selected_vendor, "5.1")
            if is_valid:
                self.sort_vendors()
                self.selected_index = -1
                self.on_click_version51()
                self.update_vendors51_dat_file()
                edit_vendor_dialog.close()
            else:
                GeneralUtils.show_message(message)

        save_changes = edit_vendor_dialog_ui.saveVendorChangesButton
        save_changes.clicked.connect(attempt_edit_vendor)

        undo_changes = edit_vendor_dialog_ui.undoVendorChangesButton
        undo_changes.clicked.connect(lambda: edit_vendor_dialog.close())

        remove_vendor = edit_vendor_dialog_ui.removeVendorButton
        remove_vendor.clicked.connect(
            lambda: self.on_remove_vendor_clicked(edit_vendor_dialog)
        )

        edit_vendor_dialog.exec_()

    def edit_vendor50_window(self):
        """Handles the signal emitted when the edit vendor button is clicked

        A dialog is show to allow the user to update vendor's information. If the information entered is valid,
        the vendor is updated to the system
        """
        edit_vendor_dialog = QMainWindow()
        edit_vendor_dialog_ui = EditVendors50.Ui_editVendors50()
        edit_vendor_dialog_ui.setupUi(edit_vendor_dialog)
        edit_vendor_dialog.show()

        name_edit = edit_vendor_dialog_ui.nameEdit
        base_url_edit = edit_vendor_dialog_ui.baseUrlEdit
        customer_id_edit = edit_vendor_dialog_ui.customerIdEdit
        requestor_id_edit = edit_vendor_dialog_ui.requestorIdEdit
        api_key_edit = edit_vendor_dialog_ui.apiKeyEdit
        platform_edit = edit_vendor_dialog_ui.platformEdit
        is_non_sushi_edit = edit_vendor_dialog_ui.is_non_sushi_edit
        description_edit = edit_vendor_dialog_ui.descriptionEdit
        companies_edit = edit_vendor_dialog_ui.companiesEdit

        name_validation_label = edit_vendor_dialog_ui.name_validation_label
        name_validation_label.hide()
        url_validation_label = edit_vendor_dialog_ui.url_validation_label
        url_validation_label.hide()

        selected_vendor: Vendor = self.vendors_v50[self.selected_index]

        name_edit.setText(selected_vendor.name)
        base_url_edit.setText(selected_vendor.base_url)
        customer_id_edit.setText(selected_vendor.customer_id)
        requestor_id_edit.setText(selected_vendor.requestor_id)
        api_key_edit.setText(selected_vendor.api_key)
        platform_edit.setText(selected_vendor.platform)
        is_non_sushi_edit.setChecked(selected_vendor.is_non_sushi)
        description_edit.setText(selected_vendor.description)
        companies_edit.setText(selected_vendor.companies)

        name_edit.textChanged.connect(
            lambda new_name: self.on_name_text_changed(
                new_name, selected_vendor.name, name_validation_label, "5.0"
            )
        )

        base_url_edit.textChanged.connect(
            lambda url: self.on_url_text_changed(
                url, url_validation_label, True, is_non_sushi_edit
            )
        )

        def attempt_edit_vendor():
            vendor = Vendor(
                name_edit.text(),
                base_url_edit.text(),
                customer_id_edit.text(),
                requestor_id_edit.text(),
                api_key_edit.text(),
                platform_edit.text(),
                is_non_sushi_edit.isChecked(),
                description_edit.text(),
                companies_edit.text(),
            )

            is_valid, message = self.edit_vendor(vendor, selected_vendor, "5.0")
            print("is valid in version 50 : ", is_valid, " , message : ", message)
            if is_valid:
                self.sort_vendors()
                self.selected_index = -1
                self.on_click_version50()
                self.update_vendors_dat_file()
                edit_vendor_dialog.close()
            else:
                GeneralUtils.show_message(message)

        save_changes = edit_vendor_dialog_ui.saveVendorChangesButton
        save_changes.clicked.connect(attempt_edit_vendor)

        undo_changes = edit_vendor_dialog_ui.undoVendorChangesButton
        undo_changes.clicked.connect(lambda: edit_vendor_dialog.close())

        remove_vendor = edit_vendor_dialog_ui.removeVendorButton
        remove_vendor.clicked.connect(
            lambda: self.on_remove_vendor_clicked(edit_vendor_dialog)
        )

        edit_vendor_dialog.exec_()

    def edit_vendor(
        self,
        new_vendor: Vendor51 | Vendor,
        original_vendor: Vendor51 | Vendor,
        version: str = "5.1",
    ) -> tuple[bool, str]:
        # Check if vendor name is valid
        is_valid, message = self.validate_new_name(
            new_vendor.name, original_vendor.name, version
        )
        if not is_valid:
            return is_valid, message

        if version == "5.0":
            if not new_vendor.is_non_sushi:
                is_valid, message = self.validate_url(new_vendor.base_url)
                if not is_valid:
                    return is_valid, message
                if new_vendor.customer_id == "":
                    return False, "Customer Id cannot be empty."
        else:
            is_valid, message = self.validate_url(new_vendor.base_url)
            if not is_valid:
                return is_valid, message
            if new_vendor.customer_id == "":
                return False, "Customer Id cannot be empty."

        if version == "5.1":
            self.vendors_v51[self.selected_index] = new_vendor
            self.vendor_names_v51.add(new_vendor.name.lower())
            self.vendor_names_v51.remove(original_vendor.name.lower())
            self.on_click_version51()
            self.update_vendors51_dat_file()
        else:
            self.vendors_v50[self.selected_index] = new_vendor
            self.vendor_names_v50.add(new_vendor.name.lower())
            self.vendor_names_v50.remove(original_vendor.name.lower())
            self.on_click_version50()
            self.update_vendors_dat_file()

        return True, ""

    def on_remove_vendor_clicked(self, edit_vendor_dialog: QMainWindow):
        """Handles the signal emitted when the remove vendor button is clicked.

        A confirmation dialog is shown to confirm the removal of the vendor. The vendor is removed from the system if
        confirmed
        """
        dialog_remove = QDialog()
        dialog_remove_ui = RemoveVendorDialog.Ui_Dialog_remove()
        dialog_remove_ui.setupUi(dialog_remove)

        def remove_vendor():
            if self.selected_index >= 0:
                if self.curr_version == "5.0":
                    self.vendors_v50.pop(self.selected_index)
                    self.selected_index = -1
                    self.on_click_version50()
                    self.update_vendor_names()
                    self.update_vendors_dat_file()
                else:
                    self.vendors_v51.pop(self.selected_index)
                    self.selected_index = -1
                    self.on_click_version51()
                    self.update_vendor_names()
                    self.update_vendors51_dat_file()
                dialog_remove.close()
                edit_vendor_dialog.close()

        button_box = dialog_remove_ui.buttonBox
        button_box.accepted.connect(remove_vendor)
        button_box.rejected.connect(lambda: dialog_remove.close())
        dialog_remove.exec_()


"""


































"""

# old code
# class ManageVendorFunctionality:
#     def __init__(self, ui):
#         self.ui = ui
#         self.setup_functionality()

#     def setup_functionality(self):
#         self.ui.addVendorButton.clicked.connect(self.add_vendor)
#         self.ui.importVendorsButton.clicked.connect(self.import_vendors)
#         self.ui.exportVendorsButton.clicked.connect(self.export_vendors)
#         self.ui.pushButton.clicked.connect(self.edit_vendor)

#     def add_vendor(self):

#         print("Add New Vendor clicked!")

#     def import_vendors(self):

#         print("Import Vendors clicked!")


#     def export_vendors(self):

#         print("Export Vendors clicked!")


#     def edit_vendor(self):

#         print("Edit Vendor clicked!")


# class ManageVendorsController(QObject):
#     """Controls the Manage Vendors tab

#     :param manage_vendors_widget: The manage vendors widget.
#     :param manage_vendors_ui: The UI for the manage_vendors_widget.
#     """
#     vendors_changed_signal = pyqtSignal(list)

#     def __init__(self, manage_vendors_widget: QWidget, manage_vendors_ui: ManageVendorsTab.Ui_manage_vendor_tab ,
#                  settings: Settingtab):
#         super().__init__()
#         self.manage_vendors_widget = manage_vendors_widget
#         self.selected_index = -1

#         self.edit_vendor_details_frame = manage_vendors_ui.edit_vendor_details_frame
#         self.edit_vendor_options_frame = manage_vendors_ui.edit_vendor_options_frame

#         self.name_line_edit = manage_vendors_ui.nameEdit
#         self.customer_id_line_edit = manage_vendors_ui.customerIdEdit
#         self.base_url_line_edit = manage_vendors_ui.baseUrlEdit
#         self.requestor_id_line_edit = manage_vendors_ui.requestorIdEdit
#         self.api_key_line_edit = manage_vendors_ui.apiKeyEdit
#         self.platform_line_edit = manage_vendors_ui.platformEdit
#         self.non_Sushi_check_box = manage_vendors_ui.non_Sushi_check_box
#         self.description_text_edit = manage_vendors_ui.descriptionEdit
#         self.companies_text_edit = manage_vendors_ui.companiesEdit

#         manage_vendors_ui.non_sushi_help_button.clicked.connect(
#             lambda: GeneralUtils.show_message("Vendors that don't provide SUSHI service can be added to the list for "
#                                               "use with Import Reports"))

#         self.name_validation_label = manage_vendors_ui.name_validation_label
#         self.name_validation_label.hide()
#         self.url_validation_label = manage_vendors_ui.url_validation_label
#         self.url_validation_label.hide()

#         self.save_vendor_changes_button = manage_vendors_ui.saveVendorChangesButton
#         self.undo_vendor_changes_button = manage_vendors_ui.undoVendorChangesButton
#         self.remove_vendor_button = manage_vendors_ui.removeVendorButton
#         self.add_vendor_button = manage_vendors_ui.addVendorButton
#         self.export_vendors_button = manage_vendors_ui.exportVendorsButton
#         self.import_vendors_button = manage_vendors_ui.importVendorsButton
#         self.save_vendor_changes_button.clicked.connect(self.modify_vendor)
#         self.undo_vendor_changes_button.clicked.connect(self.populate_edit_vendor_view)
#         self.remove_vendor_button.clicked.connect(self.on_remove_vendor_clicked)
#         self.add_vendor_button.clicked.connect(self.on_add_vendor_clicked)
#         self.export_vendors_button.clicked.connect(self.on_export_vendors_clicked)
#         self.import_vendors_button.clicked.connect(self.on_import_vendors_clicked)

#         self.vendor_list_view = manage_vendors_ui.vendorsListView
#         self.vendor_list_model = QStandardItemModel(self.vendor_list_view)
#         self.vendor_list_view.setModel(self.vendor_list_model)
#         self.vendor_list_view.clicked.connect(self.on_vendor_selected)

#         self.settings = settings

#         self.vendors = []
#         self.vendor_names = set()  # Hash set for faster operations
#         vendors_json_string = GeneralUtils.read_json_file(VENDORS_FILE_PATH)
#         vendor_dicts = json.loads(vendors_json_string)
#         for json_dict in vendor_dicts:
#             vendor = Vendor.from_json(json_dict)
#             self.vendors.append(vendor)
#             self.vendor_names.add(vendor.name.lower())

#         self.update_vendors_ui()

#     def on_vendor_selected(self, model_index: QModelIndex):
#         """Handles the signal emitted when a vendor is selected

#         :param model_index: An object containing the location of the vendor on the vendor list
#         """
#         self.selected_index = model_index.row()
#         self.populate_edit_vendor_view()


#     def update_vendors_ui(self):
#         """Updates the UI to show all vendors"""
#         self.vendor_list_model.clear()
#         for vendor in self.vendors:
#             item = QStandardItem(vendor.name)
#             item.setEditable(False)
#             self.vendor_list_model.appendRow(item)

#         self.populate_edit_vendor_view()

#     def update_vendor_names(self):
#         """Updates the local set of vendor names used for validation"""
#         self.vendor_names.clear()
#         for vendor in self.vendors:
#             self.vendor_names.add(vendor.name.lower())

#     def add_vendor(self, new_vendor: Vendor) -> (bool, str):
#         """Adds a new vendor to the system if the vendor is valid

#         :param new_vendor: The new vendor to be added
#         :returns: (is_successful, message) A Tuple with the completion status and a message
#         """
#         # Check if vendor is valid
#         is_valid, message = self.validate_new_name(new_vendor.name)
#         if not is_valid:
#             return is_valid, message

#         if not new_vendor.is_non_sushi:
#             is_valid, message = self.validate_url(new_vendor.base_url)
#             if not is_valid:
#                 return is_valid, message

#         self.vendors.append(new_vendor)
#         self.vendor_names.add(new_vendor.name.lower())

#         return True, ""

#     def modify_vendor(self):
#         """Updates a vendor's information in the system if the vendor is valid"""
#         if self.selected_index < 0:
#             if self.settings.show_debug_messages: print("No vendor selected")
#             return

#         selected_vendor = self.vendors[self.selected_index]

#         # Check if entries are valid
#         new_name = self.name_line_edit.text()
#         original_name = selected_vendor.name
#         is_valid, message = self.validate_new_name(new_name, original_name)
#         if not is_valid:
#             GeneralUtils.show_message(message)
#             return

#         if not self.non_Sushi_check_box.isChecked():
#             url = self.base_url_line_edit.text()
#             is_valid, message = self.validate_url(url)
#             if not is_valid:
#                 GeneralUtils.show_message(message)
#                 return

#         # Apply Changes
#         if original_name != new_name:
#             self.update_name_of_file_and_folder(original_name, new_name)
#             ManageDB.update_vendor_in_all_tables(original_name, new_name)
#             for report_type in REPORT_TYPE_SWITCHER.keys():
#                 ManageDB.backup_costs_data(report_type)

#         selected_vendor.name = self.name_line_edit.text()
#         selected_vendor.base_url = self.base_url_line_edit.text()
#         selected_vendor.customer_id = self.customer_id_line_edit.text()
#         selected_vendor.requestor_id = self.requestor_id_line_edit.text()
#         selected_vendor.api_key = self.api_key_line_edit.text()
#         selected_vendor.platform = self.platform_line_edit.text()
#         selected_vendor.is_non_sushi = self.non_Sushi_check_box.checkState() == Qt.Checked
#         selected_vendor.description = self.description_text_edit.toPlainText()
#         selected_vendor.companies = self.companies_text_edit.toPlainText()

#         self.update_vendors_ui()
#         self.update_vendor_names()
#         self.vendors_changed_signal.emit(self.vendors)
#         self.save_all_vendors_to_disk()

#         GeneralUtils.show_message("Changes Saved!")

#     def update_name_of_file_and_folder(self,original_name, new_name):
#         DO_NOT_MODIFY_json_path = os.getcwd() + os.path.sep + "all_data" + os.path.sep + ".DO_NOT_MODIFY" + os.path.sep + "_json"
#         DO_NOT_MODIFY_year_path = os.getcwd() + os.path.sep + "all_data" + os.path.sep + ".DO_NOT_MODIFY"
#         default_year_path = os.getcwd() + os.path.sep + "all_data" + os.path.sep + "yearly_files"
#         default_other_path = os.getcwd() + os.path.sep + "all_data" + os.path.sep + "other_files"

#         custom_year_path = self.settings.yearly_directory
#         custom_other_path = self.settings.other_directory

#         if os.path.exists(DO_NOT_MODIFY_json_path):
#             folderList = os.listdir(DO_NOT_MODIFY_json_path)
#             for folder in folderList:
#                 if folder[0] == "2" and folder[1] == "0":
#                     year_path = DO_NOT_MODIFY_json_path + os.path.sep + folder

#                     original_folder_path = year_path + os.path.sep + original_name
#                     new_folder_path = year_path + os.path.sep + new_name

#                     if os.path.exists(original_folder_path):
#                         filesList = os.listdir(original_folder_path)

#                         for theFile in filesList:
#                             old_file_path = original_folder_path + os.path.sep + theFile
#                             new_file_path = original_folder_path + os.path.sep + theFile.replace(original_name,new_name)
#                             os.rename(old_file_path,new_file_path)

#                         os.rename(original_folder_path,new_folder_path)

#         if (os.path.exists(DO_NOT_MODIFY_year_path)):
#             folderList = os.listdir(DO_NOT_MODIFY_json_path)
#             for folder in folderList:
#                 if folder[0] == "2" and folder[1] == "0":
#                     year_path = DO_NOT_MODIFY_year_path + os.path.sep + folder

#                     original_folder_path = year_path + os.path.sep + original_name
#                     new_folder_path = year_path + os.path.sep + new_name

#                     if os.path.exists(original_folder_path):
#                         filesList = os.listdir(original_folder_path)

#                         for theFile in filesList:
#                             old_file_path = original_folder_path + os.path.sep + theFile
#                             new_file_path = original_folder_path + os.path.sep + theFile.replace(original_name, new_name)

#                             os.rename(old_file_path, new_file_path)

#                         os.rename(original_folder_path, new_folder_path)

#         if (os.path.exists(default_year_path)):
#             folderList = os.listdir(DO_NOT_MODIFY_json_path)
#             for folder in folderList:
#                 if folder[0] == "2" and folder[1] == "0":
#                     year_path = default_year_path + os.path.sep + folder

#                     original_folder_path = year_path + os.path.sep + original_name
#                     new_folder_path = year_path + os.path.sep + new_name

#                     if os.path.exists(original_folder_path):
#                         filesList = os.listdir(original_folder_path)

#                         for theFile in filesList:
#                             old_file_path = original_folder_path + os.path.sep + theFile
#                             new_file_path = original_folder_path + os.path.sep + theFile.replace(original_name, new_name)

#                             os.rename(old_file_path, new_file_path)

#                         os.rename(original_folder_path, new_folder_path)

#         if (os.path.exists(default_other_path)):
#             original_folder_path = default_other_path + os.path.sep + original_name
#             new_folder_path = default_other_path + os.path.sep + new_name

#             if os.path.exists(original_folder_path):
#                 filesList = os.listdir(original_folder_path)

#                 for theFile in filesList:
#                     old_file_path = original_folder_path + os.path.sep + theFile
#                     new_file_path = original_folder_path + os.path.sep + theFile.replace(original_name,
#                                                                                          new_name)
#                     os.rename(old_file_path, new_file_path)

#                 os.rename(original_folder_path, new_folder_path)

#         if (os.path.exists(custom_year_path)):
#             folderList = os.listdir(custom_year_path)
#             for folder in folderList:
#                 if folder[0] == "2" and folder[1] == "0":
#                     year_path = custom_year_path + os.path.sep + folder

#                     original_folder_path = year_path + os.path.sep + original_name
#                     new_folder_path = year_path + os.path.sep + new_name

#                     if os.path.exists(original_folder_path):
#                         filesList = os.listdir(original_folder_path)

#                         for theFile in filesList:
#                             old_file_path = original_folder_path + os.path.sep + theFile
#                             new_file_path = original_folder_path + os.path.sep + theFile.replace(original_name,
#                                                                                                  new_name)
#                             os.rename(old_file_path, new_file_path)

#                         os.rename(original_folder_path, new_folder_path)

#         if (os.path.exists(custom_other_path)):
#             original_folder_path = custom_other_path + os.path.sep + original_name
#             new_folder_path = custom_other_path + os.path.sep + new_name

#             if os.path.exists(original_folder_path):
#                 filesList = os.listdir(original_folder_path)

#                 for theFile in filesList:
#                     old_file_path = original_folder_path + os.path.sep + theFile
#                     new_file_path = original_folder_path + os.path.sep + theFile.replace(original_name,
#                                                                                                  new_name)
#                     os.rename(old_file_path, new_file_path)

#                 os.rename(original_folder_path, new_folder_path)

#     def on_add_vendor_clicked(self):
#         """Handles the signal emitted when the add vendor button is clicked

#         A dialog is show to allow the user to enter a new vendor's information. If the information entered is valid,
#         the vendor is added to the system
#         """
#         vendor_dialog = QDialog()
#         vendor_dialog_ui = AddVendorDialog.Ui_addVendorDialog()
#         vendor_dialog_ui.setupUi(vendor_dialog)

#         name_edit = vendor_dialog_ui.nameEdit
#         base_url_edit = vendor_dialog_ui.baseUrlEdit
#         customer_id_edit = vendor_dialog_ui.customerIdEdit
#         requestor_id_edit = vendor_dialog_ui.requestorIdEdit
#         api_key_edit = vendor_dialog_ui.apiKeyEdit
#         platform_edit = vendor_dialog_ui.platformEdit
#         non_sushi_check_box = vendor_dialog_ui.non_Sushi_check_box
#         description_edit = vendor_dialog_ui.descriptionEdit
#         companies_edit = vendor_dialog_ui.companiesEdit

#         vendor_dialog_ui.non_sushi_help_button.clicked.connect(
#             lambda: GeneralUtils.show_message("Vendors that don't provide SUSHI service can be added to the list for "
#                                               "use with Import Reports"))

#         name_validation_label = vendor_dialog_ui.name_validation_label
#         name_validation_label.hide()
#         url_validation_label = vendor_dialog_ui.url_validation_label
#         url_validation_label.hide()

#         name_edit.textChanged.connect(
#             lambda new_name: self.on_name_text_changed(new_name, "", name_validation_label))
#         base_url_edit.textChanged.connect(
#             lambda url: self.on_url_text_changed(url, url_validation_label, True, non_sushi_check_box))

#         def attempt_add_vendor():
#             vendor = Vendor(name_edit.text(), base_url_edit.text(), customer_id_edit.text(), requestor_id_edit.text(),
#                             api_key_edit.text(), platform_edit.text(), non_sushi_check_box.checkState() == Qt.Checked,
#                             description_edit.toPlainText(), companies_edit.toPlainText())

#             is_valid, message = self.add_vendor(vendor)
#             if is_valid:
#                 self.sort_vendors()
#                 self.selected_index = -1
#                 self.update_vendors_ui()
#                 self.populate_edit_vendor_view()
#                 self.vendors_changed_signal.emit(self.vendors)
#                 self.save_all_vendors_to_disk()
#                 vendor_dialog.close()
#             else:
#                 GeneralUtils.show_message(message)

#         button_box = vendor_dialog_ui.buttonBox
#         ok_button = button_box.button(QDialogButtonBox.Ok)
#         ok_button.clicked.connect(attempt_add_vendor)
#         cancel_button = button_box.button(QDialogButtonBox.Cancel)
#         cancel_button.clicked.connect(lambda: vendor_dialog.close())

#         vendor_dialog.exec_()

#     def on_import_vendors_clicked(self):
#         """Handles the signal emitted when the import vendors button is clicked.

#         A file select dialog is shown to allow the user to select the vendors TSV file to import. The selected file is
#         then imported.
#         """
#         file_path = GeneralUtils.choose_file(TSV_FILTER)
#         if file_path:
#             self.import_vendors_tsv(file_path)

#     def on_export_vendors_clicked(self):
#         """Handles the signal emitted when the export vendors button is clicked.

#         A folder select dialog is shown to allow the user to select the target directory to export the vendors file to.
#         A vendors TSV file containing all the vendors in the system is then exported
#         """
#         dir_path = GeneralUtils.choose_directory()
#         if dir_path:
#             self.export_vendors_tsv(dir_path)

#     def populate_edit_vendor_view(self):
#         """Populates the edit vendor view with the selected vendors's information"""
#         if self.selected_index >= 0:
#             selected_vendor = self.vendors[self.selected_index]

#             self.name_line_edit.textChanged.connect(
#                 lambda new_name: self.on_name_text_changed(new_name, selected_vendor.name, self.name_validation_label))
#             self.name_line_edit.setText(selected_vendor.name)

#             self.base_url_line_edit.textChanged.connect(
#                 lambda url: self.on_url_text_changed(url, self.url_validation_label, True, self.non_Sushi_check_box))
#             self.base_url_line_edit.setText(selected_vendor.base_url)

#             self.customer_id_line_edit.setText(selected_vendor.customer_id)
#             self.requestor_id_line_edit.setText(selected_vendor.requestor_id)
#             self.api_key_line_edit.setText(selected_vendor.api_key)
#             self.platform_line_edit.setText(selected_vendor.platform)
#             self.non_Sushi_check_box.setChecked(selected_vendor.is_non_sushi)
#             self.description_text_edit.setPlainText(selected_vendor.description)
#             self.companies_text_edit.setPlainText(selected_vendor.companies)

#             self.set_edit_vendor_view_state(True)
#         else:
#             self.name_line_edit.textChanged.connect(
#                 lambda new_name: self.on_name_text_changed(new_name, "", self.name_validation_label, False))
#             self.name_line_edit.setText("")
#             self.name_line_edit.textChanged.emit("")  # Hide validation_label if showing

#             self.base_url_line_edit.textChanged.connect(
#                 lambda url: self.on_url_text_changed(url, self.url_validation_label, False, self.non_Sushi_check_box))
#             self.base_url_line_edit.setText("")
#             self.base_url_line_edit.textChanged.emit("")

#             self.customer_id_line_edit.setText("")
#             self.base_url_line_edit.setText("")
#             self.requestor_id_line_edit.setText("")
#             self.api_key_line_edit.setText("")
#             self.platform_line_edit.setText("")
#             self.non_Sushi_check_box.setChecked(False)
#             self.description_text_edit.setPlainText("")
#             self.companies_text_edit.setPlainText("")

#             self.set_edit_vendor_view_state(False)

#     def set_edit_vendor_view_state(self, is_enabled):
#         """Enables or disables the elements in the edit vendor view

#         :param is_enabled: This indicates whether the edit vendor view should be enabled
#         """
#         if is_enabled:
#             self.edit_vendor_details_frame.setEnabled(True)
#             self.edit_vendor_options_frame.setEnabled(True)
#         else:
#             self.edit_vendor_details_frame.setEnabled(False)
#             self.edit_vendor_options_frame.setEnabled(False)

#     def on_remove_vendor_clicked(self):
#         """Handles the signal emitted when the remove vendor button is clicked.

#         A confirmation dialog is shown to confirm the removal of the vendor. The vendor is removed from the system if
#         confirmed
#         """
#         dialog_remove = QDialog()
#         dialog_remove_ui = RemoveVendorDialog.Ui_dialog_remove()
#         dialog_remove_ui.setupUi(dialog_remove)

#         def remove_vendor():
#             if self.selected_index >= 0:
#                 self.vendors.pop(self.selected_index)
#                 self.selected_index = -1

#                 self.update_vendors_ui()
#                 self.update_vendor_names()
#                 self.populate_edit_vendor_view()
#                 self.vendors_changed_signal.emit(self.vendors)
#                 self.save_all_vendors_to_disk()

#         button_box = dialog_remove_ui.buttonBox
#         button_box.accepted.connect(remove_vendor)
#         dialog_remove.exec_()

#     def save_all_vendors_to_disk(self):
#         """Saves all the vendors in the system to disk"""
#         json_string = json.dumps(self.vendors, default=lambda o: o.__dict__, indent=4)
#         GeneralUtils.save_json_file(VENDORS_FILE_DIR, VENDORS_FILE_NAME, json_string)

#     def sort_vendors(self):
#         """Sorts the vendors alphabetically based their names"""
#         self.vendors = sorted(self.vendors, key=lambda vendor: vendor.name.lower())

#     def import_vendors_tsv(self, file_path):
#         """Imports the vendors in a TSV file path to the system

#         :param file_path: The file path of the vendors TSV file
#         """
#         try:
#             tsv_file = open(file_path, 'r', encoding="utf-8", newline='')
#             reader = csv.DictReader(tsv_file, delimiter='\t')
#             for row in reader:
#                 if 'is_non_sushi' in row:
#                     is_non_sushi = row['is_non_sushi'].lower() == "true"
#                 else:
#                     is_non_sushi = False
#                 vendor = Vendor(row['name'] if 'name' in row else "",
#                                 row['base_url'] if 'base_url' in row else "",
#                                 row['customer_id'] if 'customer_id' in row else "",
#                                 row['requestor_id'] if 'requestor_id' in row else "",
#                                 row['api_key'] if 'api_key' in row else "",
#                                 row['platform'] if 'platform' in row else "",
#                                 is_non_sushi,
#                                 row['description'] if 'description' in row else "",
#                                 row['companies'] if 'companies' in row else "")

#                 is_valid, message = self.add_vendor(vendor)
#                 if not is_valid:
#                     if self.settings.show_debug_messages: print(message)

#             tsv_file.close()

#             self.sort_vendors()
#             self.selected_index = -1
#             self.update_vendors_ui()
#             self.update_vendor_names()
#             self.populate_edit_vendor_view()
#             self.vendors_changed_signal.emit(self.vendors)
#             self.save_all_vendors_to_disk()

#             GeneralUtils.show_message(f"Import successful!")
#         except Exception as e:
#             if self.settings.show_debug_messages: print(f"File import failed: {e}")
#             GeneralUtils.show_message(f"File import failed: {e}")

#     def export_vendors_tsv(self, dir_path):
#         """Exports all vendor information as a TSV file to a directory

#         :param dir_path: The directory path to export the vendors TSV file to
#         """
#         file_path = f"{dir_path}{EXPORT_VENDORS_FILE_NAME}"
#         column_names = ["name",
#                         "base_url",
#                         "customer_id",
#                         "requestor_id",
#                         "api_key",
#                         "platform",
#                         "is_non_sushi",
#                         "description",
#                         "companies"]
#         try:
#             tsv_file = open(file_path, 'w', encoding="utf-8", newline='')
#             tsv_dict_writer = csv.DictWriter(tsv_file, column_names, delimiter='\t')
#             tsv_dict_writer.writeheader()

#             for vendor in self.vendors:
#                 tsv_dict_writer.writerow(vendor.__dict__)

#             tsv_file.close()
#             GeneralUtils.show_message(f"Exported to {file_path}")

#         except Exception as e:
#             if self.settings.show_debug_messages: print(f"File export failed: {e}")
#             GeneralUtils.show_message(f"File export failed: {e}")
