# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FetchReportsTab.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FetchReports(object):
    def setupUi(self, FetchReports):
        FetchReports.setObjectName("FetchReports")
        FetchReports.resize(1067, 693)
        FetchReports.setStyleSheet("*{\n"
"    \n"
"border:none;\n"
"background-color:transparent;\n"
"background:none;\n"
"padding:0;\n"
"margin:0;\n"
"color:#fff;\n"
"}\n"
"\n"
"\n"
"\n"
"#FetchReports{\n"
"background-color:#1f232a;\n"
"}\n"
"#EditVendor{\n"
"background-color:#16191d;\n"
"}\n"
"QPushButton{\n"
"text-align:left;\n"
"padding: 5px 10px;\n"
"\n"
"border-top-left-radius:5px;\n"
"border-bottom-left-radius:5px;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:grey;\n"
"text-align:left;\n"
"padding:2px 10px;\n"
"color:white;}")
        self.gridLayout_4 = QtWidgets.QGridLayout(FetchReports)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.centralwidget = QtWidgets.QWidget(FetchReports)
        self.centralwidget.setStyleSheet("*{\n"
"    \n"
"border:none;\n"
"background-color:transparent;\n"
"background:none;\n"
"padding:0;\n"
"margin:0;\n"
"color:#fff;\n"
"}\n"
"\n"
"\n"
"\n"
"#manage_vendor_tab{\n"
"background-color:#1f232a;\n"
"}\n"
"#EditVendor{\n"
"background-color:#16191d;\n"
"}\n"
"QPushButton{\n"
"text-align:left;\n"
"padding: 5px 10px;\n"
"\n"
"border-top-left-radius:5px;\n"
"border-bottom-left-radius:5px;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:grey;\n"
"text-align:left;\n"
"padding:2px 10px;\n"
"color:white;}")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setStyleSheet("")
        self.frame_4.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame_2 = QtWidgets.QFrame(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet("QFrame{\n"
"border: 2px solid grey ; \n"
"border-radius:15px;\n"
"\n"
"}\n"
"QPushButton{\n"
"border: 2px solid grey ;\n"
"border-radius:15px;\n"
"hover:grey\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        self.frame_6.setEnabled(True)
        self.frame_6.setAutoFillBackground(False)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.lblOptions = QtWidgets.QLabel(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblOptions.sizePolicy().hasHeightForWidth())
        self.lblOptions.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setBold(False)
        self.lblOptions.setFont(font)
        self.lblOptions.setStyleSheet("QLabel{\n"
"border: none ; \n"
"}")
        self.lblOptions.setAlignment(QtCore.Qt.AlignCenter)
        self.lblOptions.setObjectName("lblOptions")
        self.gridLayout_11.addWidget(self.lblOptions, 0, 0, 1, 1)
        self.standard_report_types_list_view = QtWidgets.QListView(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.standard_report_types_list_view.sizePolicy().hasHeightForWidth())
        self.standard_report_types_list_view.setSizePolicy(sizePolicy)
        self.standard_report_types_list_view.setStyleSheet("color:white;\n"
"background-color: #1E1E1E;\n"
"border-radius: 4px;\n"
"padding: 2px;")
        self.standard_report_types_list_view.setMovement(QtWidgets.QListView.Static)
        self.standard_report_types_list_view.setObjectName("standard_report_types_list_view")
        self.gridLayout_11.addWidget(self.standard_report_types_list_view, 1, 0, 1, 1)
        self.gridLayout_7.addWidget(self.frame_6, 1, 2, 1, 1)
        self.frmDateRange = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmDateRange.sizePolicy().hasHeightForWidth())
        self.frmDateRange.setSizePolicy(sizePolicy)
        self.frmDateRange.setAutoFillBackground(False)
        self.frmDateRange.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frmDateRange.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frmDateRange.setObjectName("frmDateRange")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.frmDateRange)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.lblBeginDate = QtWidgets.QLabel(self.frmDateRange)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.lblBeginDate.setFont(font)
        self.lblBeginDate.setStyleSheet("QLabel{\n"
"border: none ; \n"
"}")
        self.lblBeginDate.setObjectName("lblBeginDate")
        self.gridLayout_10.addWidget(self.lblBeginDate, 1, 0, 1, 1, QtCore.Qt.AlignVCenter)
        self.lblEndDate = QtWidgets.QLabel(self.frmDateRange)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.lblEndDate.setFont(font)
        self.lblEndDate.setStyleSheet("QLabel{\n"
"border: none ; \n"
"}")
        self.lblEndDate.setObjectName("lblEndDate")
        self.gridLayout_10.addWidget(self.lblEndDate, 2, 0, 1, 1, QtCore.Qt.AlignVCenter)
        self.label_3 = QtWidgets.QLabel(self.frmDateRange)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("Border:none;")
        self.label_3.setObjectName("label_3")
        self.gridLayout_10.addWidget(self.label_3, 1, 2, 1, 1)
        self.end_date_edit_fetch_year = QtWidgets.QDateEdit(self.frmDateRange)
        self.end_date_edit_fetch_year.setMinimumSize(QtCore.QSize(0, 20))
        self.end_date_edit_fetch_year.setStyleSheet("QDateEdit {\n"
"background-color: #2E2F30;\n"
"    border: 2px solid #808080;\n"
"    border-radius: 4px;\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"QDateEdit::up-button, QDateEdit::down-button {\n"
"    border: none;\n"
"    padding-right: 5px;\n"
"}\n"
"\n"
"QDateEdit::up-button {\n"
"    subcontrol-position: top right;\n"
"}\n"
"\n"
"QDateEdit::down-button {\n"
"    subcontrol-position: bottom right;\n"
"}\n"
"\n"
"QDateEdit::up-arrow, QDateEdit::down-arrow {\n"
"    border: 5px solid rgba(255, 255, 255, 0);\n"
"    width: 0;\n"
"    height: 0;\n"
"}\n"
"\n"
"QDateEdit::up-arrow {\n"
"    border-top: none;\n"
"    border-bottom-color: white;\n"
"}\n"
"\n"
"QDateEdit::down-arrow {\n"
"    border-bottom: none;\n"
"    border-top-color: white;\n"
"}")
        self.end_date_edit_fetch_year.setCalendarPopup(False)
        self.end_date_edit_fetch_year.setDate(QtCore.QDate(2024, 1, 1))
        self.end_date_edit_fetch_year.setObjectName("end_date_edit_fetch_year")
        self.gridLayout_10.addWidget(self.end_date_edit_fetch_year, 2, 1, 1, 1)
        self.begin_date_edit_fetch_year = QtWidgets.QDateEdit(self.frmDateRange)
        self.begin_date_edit_fetch_year.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.begin_date_edit_fetch_year.sizePolicy().hasHeightForWidth())
        self.begin_date_edit_fetch_year.setSizePolicy(sizePolicy)
        self.begin_date_edit_fetch_year.setMinimumSize(QtCore.QSize(0, 20))
        self.begin_date_edit_fetch_year.setStyleSheet("QDateEdit {\n"
"background-color: #2E2F30;\n"
"    border: 2px solid #808080;\n"
"    border-radius: 4px;\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"QDateEdit::up-button, QDateEdit::down-button {\n"
"    border: none;\n"
"    padding-right: 5px;\n"
"}\n"
"\n"
"QDateEdit::up-button {\n"
"    subcontrol-position: top right;\n"
"}\n"
"\n"
"QDateEdit::down-button {\n"
"    subcontrol-position: bottom right;\n"
"}\n"
"\n"
"QDateEdit::up-arrow, QDateEdit::down-arrow {\n"
"    border: 5px solid rgba(255, 255, 255, 0);\n"
"    width: 0;\n"
"    height: 0;\n"
"}\n"
"\n"
"QDateEdit::up-arrow {\n"
"    border-top: none;\n"
"    border-bottom-color: white;\n"
"}\n"
"\n"
"QDateEdit::down-arrow {\n"
"    border-bottom: none;\n"
"    border-top-color: white;\n"
"}")
        self.begin_date_edit_fetch_year.setDateTime(QtCore.QDateTime(QtCore.QDate(2023, 4, 5), QtCore.QTime(0, 0, 0)))
        self.begin_date_edit_fetch_year.setDisplayFormat("yyyy")
        self.begin_date_edit_fetch_year.setCalendarPopup(False)
        self.begin_date_edit_fetch_year.setDate(QtCore.QDate(2023, 4, 5))
        self.begin_date_edit_fetch_year.setObjectName("begin_date_edit_fetch_year")
        self.gridLayout_10.addWidget(self.begin_date_edit_fetch_year, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frmDateRange)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("Border:none;")
        self.label_4.setObjectName("label_4")
        self.gridLayout_10.addWidget(self.label_4, 2, 2, 1, 1)
        self.begin_month_combo_box = QtWidgets.QComboBox(self.frmDateRange)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.begin_month_combo_box.setFont(font)
        self.begin_month_combo_box.setStyleSheet("color:white;\n"
"border-radius: 0px;\n"
"background: #2E2F30;\n"
"padding-left: 5px;")
        self.begin_month_combo_box.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.begin_month_combo_box.setMinimumContentsLength(10)
        self.begin_month_combo_box.setObjectName("begin_month_combo_box")
        self.gridLayout_10.addWidget(self.begin_month_combo_box, 1, 3, 1, 1)
        self.end_month_combo_box = QtWidgets.QComboBox(self.frmDateRange)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.end_month_combo_box.setFont(font)
        self.end_month_combo_box.setStyleSheet("color:white;\n"
"border-radius: 0px;\n"
"background: #2E2F30;\n"
"padding-left: 5px;")
        self.end_month_combo_box.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.end_month_combo_box.setMinimumContentsLength(10)
        self.end_month_combo_box.setObjectName("end_month_combo_box")
        self.gridLayout_10.addWidget(self.end_month_combo_box, 2, 3, 1, 1)
        self.lblFetchAllReport_4 = QtWidgets.QLabel(self.frmDateRange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFetchAllReport_4.sizePolicy().hasHeightForWidth())
        self.lblFetchAllReport_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(12)
        font.setBold(False)
        self.lblFetchAllReport_4.setFont(font)
        self.lblFetchAllReport_4.setAutoFillBackground(False)
        self.lblFetchAllReport_4.setStyleSheet("border:none")
        self.lblFetchAllReport_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lblFetchAllReport_4.setObjectName("lblFetchAllReport_4")
        self.gridLayout_10.addWidget(self.lblFetchAllReport_4, 0, 0, 1, 4)
        self.gridLayout_7.addWidget(self.frmDateRange, 0, 2, 1, 1)
        self.frmSelectVenders = QtWidgets.QFrame(self.frame_2)
        self.frmSelectVenders.setAutoFillBackground(False)
        self.frmSelectVenders.setStyleSheet("QFrame{\n"
"border: 2px solid grey ; \n"
"}")
        self.frmSelectVenders.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frmSelectVenders.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frmSelectVenders.setObjectName("frmSelectVenders")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frmSelectVenders)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.deselect_allvendors_button = QtWidgets.QPushButton(self.frmSelectVenders)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.deselect_allvendors_button.setFont(font)
        self.deselect_allvendors_button.setStyleSheet("text-align:center;\n"
"")
        self.deselect_allvendors_button.setObjectName("deselect_allvendors_button")
        self.gridLayout_6.addWidget(self.deselect_allvendors_button, 3, 1, 1, 1)
        self.select_allvendors_button = QtWidgets.QPushButton(self.frmSelectVenders)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.select_allvendors_button.setFont(font)
        self.select_allvendors_button.setStyleSheet("text-align:center;")
        self.select_allvendors_button.setObjectName("select_allvendors_button")
        self.gridLayout_6.addWidget(self.select_allvendors_button, 3, 0, 1, 1)
        self.lblFetchAllReport_3 = QtWidgets.QLabel(self.frmSelectVenders)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(12)
        font.setBold(False)
        self.lblFetchAllReport_3.setFont(font)
        self.lblFetchAllReport_3.setAutoFillBackground(False)
        self.lblFetchAllReport_3.setStyleSheet("border:none;")
        self.lblFetchAllReport_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lblFetchAllReport_3.setObjectName("lblFetchAllReport_3")
        self.gridLayout_6.addWidget(self.lblFetchAllReport_3, 0, 0, 1, 2)
        self.vendors_list_view_fetch = QtWidgets.QListView(self.frmSelectVenders)
        self.vendors_list_view_fetch.setStyleSheet("\n"
"\n"
"color:white;\n"
"background-color: #1E1E1E;\n"
"border-radius: 4px;\n"
"padding: 2px;\n"
"\n"
"")
        self.vendors_list_view_fetch.setObjectName("vendors_list_view_fetch")
        self.gridLayout_6.addWidget(self.vendors_list_view_fetch, 4, 0, 1, 2)
        self.version_51_button = QtWidgets.QPushButton(self.frmSelectVenders)
        self.version_51_button.setStyleSheet("text-align:center;")
        self.version_51_button.setObjectName("version_51_button")
        self.gridLayout_6.addWidget(self.version_51_button, 1, 0, 1, 1)
        self.version_50_button = QtWidgets.QPushButton(self.frmSelectVenders)
        self.version_50_button.setStyleSheet("text-align:center;")
        self.version_50_button.setObjectName("version_50_button")
        self.gridLayout_6.addWidget(self.version_50_button, 1, 1, 1, 1)
        self.gridLayout_7.addWidget(self.frmSelectVenders, 0, 0, 2, 1)
        self.frmSelectReportType = QtWidgets.QFrame(self.frame_2)
        self.frmSelectReportType.setAutoFillBackground(False)
        self.frmSelectReportType.setStyleSheet("QFrame{\n"
"border: 2px solid grey ; \n"
"}")
        self.frmSelectReportType.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frmSelectReportType.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frmSelectReportType.setObjectName("frmSelectReportType")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frmSelectReportType)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.frame_8 = QtWidgets.QFrame(self.frmSelectReportType)
        self.frame_8.setStyleSheet("border:none")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_8.setObjectName("frame_8")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_8)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.select_more_options_button = QtWidgets.QPushButton(self.frame_8)
        self.select_more_options_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_more_options_button.sizePolicy().hasHeightForWidth())
        self.select_more_options_button.setSizePolicy(sizePolicy)
        self.select_more_options_button.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.select_more_options_button.setFont(font)
        self.select_more_options_button.setStyleSheet("border:2px solid grey;\n"
"text-align:center;")
        self.select_more_options_button.setObjectName("select_more_options_button")
        self.gridLayout_8.addWidget(self.select_more_options_button, 1, 0, 1, 1)
        self.gridLayout_9.addWidget(self.frame_8, 2, 0, 1, 2)
        self.frame_5 = QtWidgets.QFrame(self.frmSelectReportType)
        self.frame_5.setStyleSheet("")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.dr_master_report_checkbox = QtWidgets.QCheckBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.dr_master_report_checkbox.setFont(font)
        self.dr_master_report_checkbox.setObjectName("dr_master_report_checkbox")
        self.gridLayout_13.addWidget(self.dr_master_report_checkbox, 2, 1, 1, 1)
        self.tr_master_report_checkbox = QtWidgets.QCheckBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.tr_master_report_checkbox.setFont(font)
        self.tr_master_report_checkbox.setObjectName("tr_master_report_checkbox")
        self.gridLayout_13.addWidget(self.tr_master_report_checkbox, 2, 0, 1, 1)
        self.pr_master_report_checkbox = QtWidgets.QCheckBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.pr_master_report_checkbox.setFont(font)
        self.pr_master_report_checkbox.setObjectName("pr_master_report_checkbox")
        self.gridLayout_13.addWidget(self.pr_master_report_checkbox, 1, 0, 1, 1)
        self.ir_master_report_checkbox = QtWidgets.QCheckBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.ir_master_report_checkbox.setFont(font)
        self.ir_master_report_checkbox.setObjectName("ir_master_report_checkbox")
        self.gridLayout_13.addWidget(self.ir_master_report_checkbox, 1, 1, 1, 1)
        self.select_all_master_reports_button = QtWidgets.QPushButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.select_all_master_reports_button.setFont(font)
        self.select_all_master_reports_button.setStyleSheet("text-align:center;")
        self.select_all_master_reports_button.setObjectName("select_all_master_reports_button")
        self.gridLayout_13.addWidget(self.select_all_master_reports_button, 0, 0, 1, 1)
        self.deselect_all_master_reports_button = QtWidgets.QPushButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.deselect_all_master_reports_button.setFont(font)
        self.deselect_all_master_reports_button.setStyleSheet("text-align:center;")
        self.deselect_all_master_reports_button.setObjectName("deselect_all_master_reports_button")
        self.gridLayout_13.addWidget(self.deselect_all_master_reports_button, 0, 1, 1, 1)
        self.gridLayout_9.addWidget(self.frame_5, 1, 0, 1, 2)
        self.lblFetchAllReport_5 = QtWidgets.QLabel(self.frmSelectReportType)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFetchAllReport_5.sizePolicy().hasHeightForWidth())
        self.lblFetchAllReport_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(12)
        font.setBold(False)
        self.lblFetchAllReport_5.setFont(font)
        self.lblFetchAllReport_5.setAutoFillBackground(False)
        self.lblFetchAllReport_5.setStyleSheet("border:none")
        self.lblFetchAllReport_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lblFetchAllReport_5.setObjectName("lblFetchAllReport_5")
        self.gridLayout_9.addWidget(self.lblFetchAllReport_5, 0, 0, 1, 2)
        self.frame_9 = QtWidgets.QFrame(self.frmSelectReportType)
        self.frame_9.setStyleSheet("b")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_9.setLineWidth(1)
        self.frame_9.setObjectName("frame_9")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.frame_9)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_2 = QtWidgets.QLabel(self.frame_9)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel{\n"
"text-align: center;\n"
"border:none;\n"
" }\n"
" ")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_12.addWidget(self.label_2, 0, 0, 1, 1)
        self.custom_dir_edit = QtWidgets.QLineEdit(self.frame_9)
        self.custom_dir_edit.setStyleSheet("color:white;\n"
"background-color: #1E1E1E;")
        self.custom_dir_edit.setObjectName("custom_dir_edit")
        self.gridLayout_12.addWidget(self.custom_dir_edit, 1, 0, 1, 1)
        self.custom_dir_button = QtWidgets.QPushButton(self.frame_9)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.custom_dir_button.setFont(font)
        self.custom_dir_button.setStyleSheet("text-align:center;")
        self.custom_dir_button.setObjectName("custom_dir_button")
        self.gridLayout_12.addWidget(self.custom_dir_button, 2, 0, 1, 1)
        self.gridLayout_9.addWidget(self.frame_9, 4, 0, 1, 2)
        self.fetch_selected_reports_button = QtWidgets.QPushButton(self.frmSelectReportType)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fetch_selected_reports_button.sizePolicy().hasHeightForWidth())
        self.fetch_selected_reports_button.setSizePolicy(sizePolicy)
        self.fetch_selected_reports_button.setMinimumSize(QtCore.QSize(300, 0))
        self.fetch_selected_reports_button.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.fetch_selected_reports_button.setFont(font)
        self.fetch_selected_reports_button.setStyleSheet("QPushButton{\n"
"border:3px solid grey;\n"
"border-color:grey;\n"
"text-align:center;\n"
"border-radius:15px;\n"
"padding-top:10px;\n"
"padding-bottom:10px;\n"
"}")
        self.fetch_selected_reports_button.setObjectName("fetch_selected_reports_button")
        self.gridLayout_9.addWidget(self.fetch_selected_reports_button, 6, 0, 1, 2, QtCore.Qt.AlignHCenter)
        self.gridLayout_7.addWidget(self.frmSelectReportType, 0, 1, 2, 1)
        self.gridLayout_5.addWidget(self.frame_2, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame_4, 4, 0, 1, 1)
        self.lblAdvanceFetchReport = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setBold(False)
        font.setKerning(True)
        self.lblAdvanceFetchReport.setFont(font)
        self.lblAdvanceFetchReport.setAutoFillBackground(False)
        self.lblAdvanceFetchReport.setStyleSheet("QLabel{\n"
"border:2px solid grey;\n"
" border:none;}")
        self.lblAdvanceFetchReport.setAlignment(QtCore.Qt.AlignCenter)
        self.lblAdvanceFetchReport.setObjectName("lblAdvanceFetchReport")
        self.gridLayout_3.addWidget(self.lblAdvanceFetchReport, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setAutoFillBackground(False)
        self.frame_3.setStyleSheet("QFrame{\n"
"border:2px solid grey;\n"
"border-radius:15px;\n"
"\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblYear = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.lblYear.setFont(font)
        self.lblYear.setStyleSheet("QLabel{\n"
"border: none ; \n"
"alignment: AlignCenter;\n"
"\n"
"}")
        self.lblYear.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblYear.setObjectName("lblYear")
        self.horizontalLayout.addWidget(self.lblYear)
        self.All_reports_edit_fetch = QtWidgets.QDateEdit(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.All_reports_edit_fetch.sizePolicy().hasHeightForWidth())
        self.All_reports_edit_fetch.setSizePolicy(sizePolicy)
        self.All_reports_edit_fetch.setMinimumSize(QtCore.QSize(0, 23))
        self.All_reports_edit_fetch.setStyleSheet("QDateEdit {\n"
"background-color: #2E2F30;\n"
"    border: 2px solid #808080;\n"
"    border-radius: 4px;\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"QDateEdit::up-button, QDateEdit::down-button {\n"
"    border: none;\n"
"    padding-right: 5px;\n"
"}\n"
"\n"
"QDateEdit::up-button {\n"
"    subcontrol-position: top right;\n"
"}\n"
"\n"
"QDateEdit::down-button {\n"
"    subcontrol-position: bottom right;\n"
"}\n"
"\n"
"QDateEdit::up-arrow, QDateEdit::down-arrow {\n"
"    border: 5px solid rgba(255, 255, 255, 0);\n"
"    width: 0;\n"
"    height: 0;\n"
"}\n"
"\n"
"QDateEdit::up-arrow {\n"
"    border-top: none;\n"
"    border-bottom-color: white;\n"
"}\n"
"\n"
"QDateEdit::down-arrow {\n"
"    border-bottom: none;\n"
"    border-top-color: white;\n"
"}")
        self.All_reports_edit_fetch.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 12, 22), QtCore.QTime(0, 0, 0)))
        self.All_reports_edit_fetch.setObjectName("All_reports_edit_fetch")
        self.horizontalLayout.addWidget(self.All_reports_edit_fetch)
        self.fetch_all_data_button = QtWidgets.QPushButton(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.fetch_all_data_button.setFont(font)
        self.fetch_all_data_button.setStyleSheet("text-align:center;")
        self.fetch_all_data_button.setObjectName("fetch_all_data_button")
        self.horizontalLayout.addWidget(self.fetch_all_data_button)
        self.gridLayout_3.addWidget(self.frame_3, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.centralwidget, 0, 0, 1, 1)
        self.statusbar = QtWidgets.QStatusBar(FetchReports)
        self.statusbar.setGeometry(QtCore.QRect(0, 0, 3, 21))
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi(FetchReports)
        QtCore.QMetaObject.connectSlotsByName(FetchReports)

    def retranslateUi(self, FetchReports):
        _translate = QtCore.QCoreApplication.translate
        FetchReports.setWindowTitle(_translate("FetchReports", "MainWindow"))
        self.lblOptions.setText(_translate("FetchReports", "Select Standard View"))
        self.lblBeginDate.setText(_translate("FetchReports", "Begin Year"))
        self.lblEndDate.setText(_translate("FetchReports", "End Year"))
        self.label_3.setText(_translate("FetchReports", "Begin Month"))
        self.end_date_edit_fetch_year.setDisplayFormat(_translate("FetchReports", "yyyy"))
        self.label_4.setText(_translate("FetchReports", "End Month"))
        self.lblFetchAllReport_4.setText(_translate("FetchReports", "Date Range"))
        self.deselect_allvendors_button.setText(_translate("FetchReports", "Deselect All"))
        self.select_allvendors_button.setText(_translate("FetchReports", "Select All"))
        self.lblFetchAllReport_3.setText(_translate("FetchReports", "Select Vendors"))
        self.version_51_button.setText(_translate("FetchReports", "Version 5.1"))
        self.version_50_button.setText(_translate("FetchReports", "Version 5.0"))
        self.select_more_options_button.setText(_translate("FetchReports", "Select more options"))
        self.dr_master_report_checkbox.setText(_translate("FetchReports", "DR"))
        self.tr_master_report_checkbox.setText(_translate("FetchReports", "TR"))
        self.pr_master_report_checkbox.setText(_translate("FetchReports", "PR"))
        self.ir_master_report_checkbox.setText(_translate("FetchReports", "IR"))
        self.select_all_master_reports_button.setText(_translate("FetchReports", "Select all"))
        self.deselect_all_master_reports_button.setText(_translate("FetchReports", "Deselect all "))
        self.lblFetchAllReport_5.setText(_translate("FetchReports", "Select Report Types"))
        self.label_2.setText(_translate("FetchReports", "Report(s) will be saved to:"))
        self.custom_dir_button.setText(_translate("FetchReports", "Browse"))
        self.fetch_selected_reports_button.setText(_translate("FetchReports", "Fetch Selected Reports"))
        self.lblAdvanceFetchReport.setText(_translate("FetchReports", "Advanced Fetch Reports"))
        self.label.setText(_translate("FetchReports", "Fetch Report"))
        self.lblYear.setText(_translate("FetchReports", "Year"))
        self.All_reports_edit_fetch.setDisplayFormat(_translate("FetchReports", "yyyy"))
        self.fetch_all_data_button.setText(_translate("FetchReports", "Fetch All Reports"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FetchReports = QtWidgets.QWidget()
    ui = Ui_FetchReports()
    ui.setupUi(FetchReports)
    FetchReports.show()
    sys.exit(app.exec_())
