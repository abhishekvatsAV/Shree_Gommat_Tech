import unittest
import sys

sys.path.insert(0, "/Users/virus/Developer/Shree_Gommat_Tech/COUNTER-Release-5.1-main")
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from ui import VendorResultsWidget

app = QApplication(sys.argv)
vendor_results_widget = QMainWindow()
vendor_results_widget_ui = VendorResultsWidget.Ui_VendorResultsWidget()
vendor_results_widget_ui.setupUi(vendor_results_widget)


class VendorResultsWidgetTests(unittest.TestCase):
    def test_defaults(self):
        """Test the defaults"""
        doc = QTextDocument()
        doc.setHtml(vendor_results_widget_ui.vendor_label.text())
        plain_text = doc.toPlainText()
        self.assertEqual(plain_text, "Bioone")

        doc.setHtml(vendor_results_widget_ui.status_label.text())
        plain_text = doc.toPlainText()
        self.assertEqual(plain_text, "Success")

        doc.setHtml(vendor_results_widget_ui.label.text())
        plain_text = doc.toPlainText()
        self.assertEqual(plain_text, "SUCCESSFUL : ")

        doc.setHtml(vendor_results_widget_ui.label_4.text())
        plain_text = doc.toPlainText()
        self.assertEqual(plain_text, "WARNING : ")

        doc.setHtml(vendor_results_widget_ui.label_6.text())
        plain_text = doc.toPlainText()
        self.assertEqual(plain_text, "FAILED : ")

        doc.setHtml(vendor_results_widget_ui.label_8.text())
        plain_text = doc.toPlainText()
        self.assertEqual(plain_text, "CANCELLED : ")

        doc.setHtml(vendor_results_widget_ui.successful_reports_list.text())
        plain_text = doc.toPlainText()
        self.assertEqual(plain_text, "")

        doc.setHtml(vendor_results_widget_ui.warning_reports_list.text())
        plain_text = doc.toPlainText()
        self.assertEqual(plain_text, "")

        doc.setHtml(vendor_results_widget_ui.failed_reports_list.text())
        plain_text = doc.toPlainText()
        self.assertEqual(plain_text, "")

        doc.setHtml(vendor_results_widget_ui.cancelled_reports_list.text())
        plain_text = doc.toPlainText()
        self.assertEqual(plain_text, "")

if __name__ == "__main__":
    unittest.main()
