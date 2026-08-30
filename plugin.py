from qt.core import QtWidgets

from .ui import Ui_Dialog


class BookBrainzPlugin(QtWidgets.QDialog, Ui_Dialog):
    """
    Main plugin class,
    Inherits from QDialog for the popup window and Ui_Dialog for all the UI widgets
    """

    def __init__(self, gui):
        super(BookBrainzPlugin, self).__init__()

        self.gui = gui
        self.setupUi(self)

        # Wire up the action buttons
        self.pushButton_fetch_metadataTab.clicked.connect(self.fetch_metadata)
        self.pushButton_update_metadataTab.clicked.connect(self.update_metadata)
        self.pushButton_search_browseTab.clicked.connect(self.search_book_by_name)
        self.pushButton_addBook_browseTab.clicked.connect(self.add_book_to_calibre)
        self.pushButton_downloadMetadata_browseTab.clicked.connect(
            self.download_metadata
        )
        self.pushButton_openBookBrainz_metadataTab.clicked.connect(
            self.open_in_bookbrainz
        )

        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget_metadataDetails_metadataTab.setCurrentIndex(0)
        selected_ids = self.gui.library_view.get_selected_ids()

        db = self.gui.current_db.new_api
        if not selected_ids:
            # No book selected -> show the "No Book Selected" placeholder
            self.stackedWidget_entire_metadataTab.setCurrentIndex(1)
            return
        else:
            first_book_id = selected_ids[0]
            self.mi = db.get_metadata(first_book_id)
            self.search_book()
