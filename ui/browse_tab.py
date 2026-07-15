import json

from calibre.gui2 import choose_save_file
from qt.core import QMessageBox, QtWidgets

from ..workers import BookSearchByNameWorker, GetEditionDetailsByBBID
from .browse.action_buttons import retranslate_action_buttons, setup_action_buttons
from .browse.results_panel import retranslate_results_panel, setup_results_panel
from .browse.search_bar import retranslate_search_bar, setup_search_bar

#################################################
#  Browse tab
#################################################
#
# Description:
# Type any book title, get results from BookBrainz,
# then add them to reading list or download metadata as JSON

# Structure:
#   1. Search bar  (input + button)
#   2. Results table  (with loading / no-results states)
#   3. Two action buttons at the bottom


class BrowseTabMixin:
    def setup_browse_tab(self):
        # Root container
        self.browseTab = QtWidgets.QWidget()
        self.browseTab.setObjectName("browseTab")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.browseTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # Build the three sections top-to-bottom
        setup_search_bar(self)
        setup_results_panel(self)
        setup_action_buttons(self)

        self.tabWidget.addTab(self.browseTab, "")

    def retranslate_browse_tab(self, _translate):
        retranslate_search_bar(self, _translate)
        retranslate_results_panel(self, _translate)
        retranslate_action_buttons(self, _translate)

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.browseTab),
            _translate("Dialog", "Browse"),
        )

    def search_book_by_name(self):
        search_query = self.lineEdit_searchbar_browseTab.text()
        if not search_query:
            QMessageBox.warning(self, "Input Error", "Please enter a search query.")
            return

        self.stackedWidget_browseTab.setCurrentIndex(1)
        self.tableWidget_browseTab.setRowCount(0)

        self.search_by_name_thread = BookSearchByNameWorker(search_query)

        self.search_by_name_thread.results_found.connect(
            self.on_search_by_name_results_ready
        )
        self.search_by_name_thread.error_occurred.connect(self.on_search_by_name_error)
        self.search_by_name_thread.finished.connect(
            self.search_by_name_thread.deleteLater
        )

        self.search_by_name_thread.start()

    def on_search_by_name_results_ready(self, results):
        self.stackedWidget_browseTab.setCurrentIndex(0)
        if not results:
            self.stackedWidget_noResults_browse.setCurrentIndex(1)
            return

        self.stackedWidget_noResults_browse.setCurrentIndex(0)
        for item in results:
            bbid = item.get("bbid")
            if not bbid:
                continue
            bookTitle = item.get("defaultAlias", {}).get("name", "Unknown")
            bookLang = item.get("defaultAlias", {}).get("language", "eng")
            bookSortTitle = item.get("defaultAlias", {}).get("sortName", bookTitle)

            row_position = self.tableWidget_browseTab.rowCount()
            self.tableWidget_browseTab.insertRow(row_position)

            self.tableWidget_browseTab.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(bookTitle)
            )
            self.tableWidget_browseTab.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(bookLang)
            )
            self.tableWidget_browseTab.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(bbid)
            )
            self.tableWidget_browseTab.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(bookSortTitle)
            )

    def on_search_by_name_error(self, error_msg):
        self.stackedWidget_browseTab.setCurrentIndex(0)
        self.stackedWidget_noResults_browse.setCurrentIndex(1)
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_msg}")

    def get_selected_bbid(self):
        selected_row = self.tableWidget_browseTab.currentRow()
        if selected_row == -1:
            return None
        item = self.tableWidget_browseTab.item(selected_row, 3)
        if item is None:
            return None
        return item.text()

    def start_browse_fetch(self, action):
        bbid = self.get_selected_bbid()
        if not bbid:
            QMessageBox.warning(
                self, "No Selection",
                "Please select a book from the search results.",
            )
            return

        self.pushButton_addBook_browseTab.setEnabled(False)
        self.pushButton_downloadMetadata_browseTab.setEnabled(False)

        if action == "add":
            self.pushButton_addBook_browseTab.setText("Fetching Metadata...")
        else:
            self.pushButton_downloadMetadata_browseTab.setText("Fetching Metadata...")

        self.browse_action = action
        self.browse_cached_metadata = None
        self.browse_cached_identifiers = []
        self.browse_cached_cover = None

        self.browse_fetch_thread = GetEditionDetailsByBBID(bbid)
        self.browse_fetch_thread.edition_data_fetched.connect(
            self.on_browse_metadata_fetched
        )
        self.browse_fetch_thread.identifiers_fetched.connect(
            self.on_browse_identifiers_fetched
        )
        self.browse_fetch_thread.cover_fetched.connect(
            self.on_browse_cover_fetched
        )
        self.browse_fetch_thread.error_occurred.connect(
            self.on_browse_fetch_error
        )
        self.browse_fetch_thread.finished.connect(
            self.on_browse_fetch_finished
        )
        self.browse_fetch_thread.start()

    def add_book_to_calibre(self):
        self.start_browse_fetch("add")

    def download_metadata(self):
        self.start_browse_fetch("download")

    def on_browse_metadata_fetched(self, data):
        self.browse_cached_metadata = data

    def on_browse_identifiers_fetched(self, data):
        self.browse_cached_identifiers = data.get("identifiers", [])

    def on_browse_cover_fetched(self, cover_bytes):
        self.browse_cached_cover = cover_bytes

    def on_browse_fetch_error(self, error_msg):
        self.pushButton_addBook_browseTab.setEnabled(True)
        self.pushButton_downloadMetadata_browseTab.setEnabled(True)
        self.pushButton_addBook_browseTab.setText("Add to Reading List")
        self.pushButton_downloadMetadata_browseTab.setText("Download Metadata")
        QMessageBox.critical(
            self, "Error", f"Failed to fetch book details:\n{error_msg}"
        )

    def on_browse_fetch_finished(self):
        if self.browse_cached_metadata is None:
            self.pushButton_addBook_browseTab.setEnabled(True)
            self.pushButton_downloadMetadata_browseTab.setEnabled(True)
            self.pushButton_addBook_browseTab.setText("Add to Reading List")
            self.pushButton_downloadMetadata_browseTab.setText("Download Metadata")
            return

        if self.browse_action == "add":
            self.pushButton_addBook_browseTab.setText("Adding to Calibre...")
            self.add_book_to_calibre_library()
        elif self.browse_action == "download":
            self.pushButton_downloadMetadata_browseTab.setText("Saving Metadata...")
            self.save_metadata_as_json()

        self.pushButton_addBook_browseTab.setEnabled(True)
        self.pushButton_downloadMetadata_browseTab.setEnabled(True)
        self.pushButton_addBook_browseTab.setText("Add to Reading List")
        self.pushButton_downloadMetadata_browseTab.setText("Download Metadata")

    def add_book_to_calibre_library(self):
        data = self.browse_cached_metadata
        default_alias = data.get("defaultAlias") or {}
        book_name = default_alias.get("name", "Unknown")

        mi = self.create_metadata_object(data, book_name)

        if self.browse_cached_identifiers:
            existing = dict(mi.identifiers or {})
            for id_item in self.browse_cached_identifiers:
                id_type = id_item.get("type", "")
                id_value = id_item.get("value", "")
                if id_type and id_value:
                    existing[id_type.lower()] = id_value
            mi.identifiers = existing

        db = self.gui.current_db.new_api
        book_ids, _duplicates = db.add_books(
            [(mi, {})], add_duplicates=True
        )
        if self.browse_cached_cover and book_ids:
            db.set_cover({book_ids[0]: self.browse_cached_cover})
        if book_ids:
            new_book_ids = list(book_ids)
            self.gui.library_view.model().refresh_ids(new_book_ids)
        QMessageBox.information(
            self, "Success", f"'{book_name}' has been added to Calibre library."
        )

    def save_metadata_as_json(self):
        data = self.browse_cached_metadata
        default_alias = data.get("defaultAlias") or {}

        authors = []
        author_credits = data.get("authorCredits") or {}
        for credit in author_credits.get("names", []):
            name = credit.get("name", "")
            if name:
                authors.append(name)

        identifiers = {}
        for id_item in self.browse_cached_identifiers:
            id_type = id_item.get("type", "")
            id_value = id_item.get("value", "")
            if id_type and id_value:
                identifiers[id_type.lower()] = id_value

        bbid = data.get("bbid", "")
        if bbid:
            identifiers["bbid"] = bbid

        publishers = data.get("publishers") or []
        publisher_name = publishers[0].get("name", "") if publishers else ""

        export_data = {
            "title": default_alias.get("name", "Unknown"),
            "sort_name": default_alias.get("sortName", ""),
            "authors": authors,
            "languages": data.get("languages", []),
            "publisher": publisher_name,
            "release_date": data.get("releaseEventDate", ""),
            "identifiers": identifiers,
            "disambiguation": data.get("disambiguation", ""),
            "status": data.get("status", ""),
        }

        save_path = choose_save_file(
            self.gui, "save-json", "books.json",
            filters=[("JSON Files", ["json"])],
        )

        if save_path:
            if not save_path.endswith(".json"):
                save_path += ".json"
            with open(save_path, "w", encoding="utf-8") as json_file:
                json.dump(export_data, json_file, indent=4, ensure_ascii=False)
            QMessageBox.information(
                self, "Success", f"Metadata saved to:\n{save_path}"
            )
