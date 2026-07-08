from qt.core import QtWidgets

from .ui import Ui_Dialog


class BookBrainzPlugin(QtWidgets.QDialog, Ui_Dialog):
    """
    Main plugin class,
    Inherits from QDialog for the popup window and Ui_Dialog for all the UI widgets
    """
