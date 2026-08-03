from calibre.ebooks.metadata.book.base import Metadata
from qt.core import QDesktopServices, QMessageBox, Qt, QtCore, QtGui, QTimer, QtWidgets, QUrl

from ..dates import extended_date_to_datetime, format_extended_date
from ..languages import format_languages

from ..workers import (
    BookSearchWorker,
    GetEditionDetailsByBBID,
)
from .metadata.details_panel import retranslate_details_panel, setup_details_panel
from .metadata.placeholder_panel import (
    retranslate_placeholder,
    setup_no_book_placeholder,
)
from .metadata.search_panel import retranslate_search_panel, setup_search_panel

###########################################################################
# Metadata tab
###########################################################################
#
# Description:
# User selects a Calibre book, we auto-search in BookBrainz using its name,
# they pick the right edition, fetch full details, then update metadata
#
# Structure:
#   1. Search results table
#   2. Metadata details with cover art


class MetadataTabMixin:
    def setup_metadata_tab(self):
        # Outer container & stacked wrapper
        # stackedWidget_entire_metadataTab holds either the real tab content
        # or a "please select a book" message
        self.MetadataTab = QtWidgets.QWidget()
        self.MetadataTab.setObjectName("MetadataTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.MetadataTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.stackedWidget_entire_metadataTab = QtWidgets.QStackedWidget(
            parent=self.MetadataTab
        )
        self.stackedWidget_entire_metadataTab.setObjectName(
            "stackedWidget_entire_metadataTab"
        )

        # The inner "page" widget holds the search results + details
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        # Build the two content sections
        setup_search_panel(self)
        setup_details_panel(self)

        # Buttons: "Update book metadata" + "Open in BookBrainz"
        self.horizontalLayout_buttons_metadataTab = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons_metadataTab.setObjectName(
            "horizontalLayout_buttons_metadataTab"
        )

        self.pushButton_update_metadataTab = QtWidgets.QPushButton(parent=self.page)
        self.pushButton_update_metadataTab.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_update_metadataTab.setEnabled(False)
        self.pushButton_update_metadataTab.setObjectName(
            "pushButton_update_metadataTab"
        )
        self.horizontalLayout_buttons_metadataTab.addWidget(
            self.pushButton_update_metadataTab
        )

        self.pushButton_openBookBrainz_metadataTab = QtWidgets.QPushButton(
            parent=self.page
        )
        self.pushButton_openBookBrainz_metadataTab.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_openBookBrainz_metadataTab.setEnabled(False)
        self.pushButton_openBookBrainz_metadataTab.setObjectName(
            "pushButton_openBookBrainz_metadataTab"
        )
        self.horizontalLayout_buttons_metadataTab.addWidget(
            self.pushButton_openBookBrainz_metadataTab
        )

        self.verticalLayout_5.addLayout(self.horizontalLayout_buttons_metadataTab)

        # wiring the outer stacked widget
        self.stackedWidget_entire_metadataTab.addWidget(self.page)
        setup_no_book_placeholder(self)

        self.verticalLayout_2.addWidget(self.stackedWidget_entire_metadataTab)
        self.tabWidget.addTab(self.MetadataTab, "")

    def retranslate_metadata_tab(self, _translate):
        # sub-assembly translators
        retranslate_search_panel(self, _translate)
        retranslate_details_panel(self, _translate)
        retranslate_placeholder(self, _translate)

        self.pushButton_update_metadataTab.setText(
            _translate("Dialog", "Update book metadata")
        )
        self.pushButton_openBookBrainz_metadataTab.setText(
            _translate("Dialog", "Open in BookBrainz")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.MetadataTab),
            _translate("Dialog", "Metadata"),
        )

    def search_book(self):
        book_name = self.mi.title
        if not book_name:
            QMessageBox.warning(
                self, "Input error", "The book should have a valid name"
            )
            return

        self.stackedWidget_searchResults_metadataTab.setCurrentIndex(1)
        self.tableWidget_metadataTab.setRowCount(0)

        self.search_thread = BookSearchWorker(book_name)

        self.search_thread.results_found.connect(self.on_search_results_ready)
        self.search_thread.error_occurred.connect(self.on_search_error)
        self.search_thread.finished.connect(
            lambda: QTimer.singleShot(
                2000,
                lambda: self.stackedWidget_searchResults_metadataTab.setCurrentIndex(0),
            )
        )

        self.search_thread.start()

    def on_search_results_ready(self, results):
        if len(results) == 0:
            self.pushButton_fetch_metadataTab.setEnabled(False)
            self.pushButton_update_metadataTab.setEnabled(False)
            self.stackedWidget_noResults_metadataTab.setCurrentIndex(1)
            return
        else:
            self.stackedWidget_noResults_metadataTab.setCurrentIndex(0)
            for item in results:
                bbid = item.get("bbid")
                if not bbid:
                    continue
                bookTitle = item.get("defaultAlias", {}).get("name", "Unknown")
                bookLang = format_languages(item.get("languages"))
                bookSortTitle = item.get("defaultAlias", {}).get("sortName", bookTitle)

                row_position = self.tableWidget_metadataTab.rowCount()
                self.tableWidget_metadataTab.insertRow(row_position)

                self.tableWidget_metadataTab.setItem(
                    row_position, 0, QtWidgets.QTableWidgetItem(bookTitle)
                )
                self.tableWidget_metadataTab.setItem(
                    row_position, 2, QtWidgets.QTableWidgetItem(bookLang)
                )
                self.tableWidget_metadataTab.setItem(
                    row_position, 3, QtWidgets.QTableWidgetItem(bbid)
                )
                self.tableWidget_metadataTab.setItem(
                    row_position, 4, QtWidgets.QTableWidgetItem(bookSortTitle)
                )

    def on_search_error(self, error_msg):
        self.pushButton_fetch_metadataTab.setEnabled(False)
        self.pushButton_update_metadataTab.setEnabled(False)
        self.stackedWidget_noResults_metadataTab.setCurrentIndex(1)
        self.label_noMetadata_metadataTab_2.setText("Network error")
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_msg}")

    def fetch_metadata(self):
        self.stackedWidget_metadataDetails_metadataTab.setCurrentIndex(2)

        self.cached_cover_bytes = None
        self.cached_identifiers = None

        self.label_data_name_metadataTab.clear()
        self.label_data_author_metadataTab.clear()
        self.label_data_language_metadataTab.clear()
        self.label_data_publisher_metadataTab.clear()
        self.label_data_releaseDate_metadataTab.clear()
        self.label_data_disambiguation_metadataTab.clear()
        self.label_data_identifiers_metadataTab.clear()
        self.label_cover_metadataTab.setText("Loading...")

        selected_row = self.tableWidget_metadataTab.currentRow()
        if selected_row == -1:
            selected_row = 0
        selected_bbid = self.tableWidget_metadataTab.item(selected_row, 3).text()
        self.current_bbid = selected_bbid
        self.pushButton_update_metadataTab.setEnabled(False)
        self.pushButton_openBookBrainz_metadataTab.setEnabled(False)

        self.fetch_edition_data_thread = GetEditionDetailsByBBID(selected_bbid)
        self.fetch_edition_data_thread.error_occurred.connect(
            self.on_fetch_edition_data_error
        )
        self.fetch_edition_data_thread.edition_data_fetched.connect(
            self.on_fetch_edition_data_results_ready
        )
        self.fetch_edition_data_thread.identifiers_fetched.connect(
            self.on_fetch_identifiers_results_ready
        )
        self.fetch_edition_data_thread.cover_fetched.connect(self.on_cover_fetched)
        self.fetch_edition_data_thread.start()

    def _elide_text(self, label, text, default="Unknown"):
        if not text:
            return default
        metrics = QtGui.QFontMetrics(label.font())
        return metrics.elidedText(str(text), Qt.ElideRight, label.width() - 4)

    def on_fetch_edition_data_results_ready(self, results):
        self.stackedWidget_metadataDetails_metadataTab.setCurrentIndex(1)
        self.pushButton_update_metadataTab.setEnabled(True)
        self.pushButton_openBookBrainz_metadataTab.setEnabled(True)
        default_alias = results.get("defaultAlias") or {}
        book_name = default_alias.get("name", "Unknown")
        sort_name = default_alias.get("sortName") or ""
        if sort_name and sort_name != book_name:
            book_name = f"{book_name} ({sort_name})"
        self.label_data_name_metadataTab.setText(
            self._elide_text(self.label_data_name_metadataTab, book_name)
        )

        author_credits = results.get("authorCredits") or {}
        author_names = author_credits.get("names", [])
        authors = ", ".join([a.get("name", "") for a in author_names if a.get("name")])
        self.label_data_author_metadataTab.setText(
            self._elide_text(
                self.label_data_author_metadataTab,
                authors if authors else "Unknown",
            )
        )

        self.label_data_language_metadataTab.setText(
            format_languages(results.get("languages"))
        )

        publishers = results.get("publishers") or []
        publisher_names = ", ".join(
            [p.get("name", "") for p in publishers if p.get("name")]
        )
        self.label_data_publisher_metadataTab.setText(
            self._elide_text(
                self.label_data_publisher_metadataTab,
                publisher_names if publisher_names else "Unknown",
            )
        )

        self.label_data_releaseDate_metadataTab.setText(
            format_extended_date(results.get("releaseEventDate"))
        )

        disambiguation = results.get("disambiguation") or ""
        self.label_data_disambiguation_metadataTab.setText(
            self._elide_text(
                self.label_data_disambiguation_metadataTab,
                disambiguation if disambiguation else "None",
            )
        )

        self.cached_metadata = self.create_metadata_object(
            results, default_alias.get("name", "Unknown")
        )

    def on_fetch_edition_data_error(self, error_msg):
        QMessageBox.critical(
            self, "Error", f" failed to fetch edition data \n{error_msg}"
        )

    def open_in_bookbrainz(self):
        bbid = getattr(self, "current_bbid", None)
        if not bbid:
            QMessageBox.information(
                self, "No data", "Fetch metadata first to open a BookBrainz page"
            )
            return
        QDesktopServices.openUrl(QUrl(f"https://bookbrainz.org/edition/{bbid}"))

    def on_fetch_identifiers_results_ready(self, data):
        identifiers = data.get("identifiers", [])
        self.cached_identifiers = identifiers
        if not identifiers:
            self.label_data_identifiers_metadataTab.setText("None")
            return
        lines = []
        for id_item in identifiers:
            id_type = id_item.get("type", "Unknown")
            id_value = id_item.get("value", "")
            lines.append(f"{id_type}: {id_value}")
        self.label_data_identifiers_metadataTab.setText("\n".join(lines))

    def on_cover_fetched(self, cover_bytes):

        self.cached_cover_bytes = cover_bytes
        if cover_bytes is None:
            self.label_cover_metadataTab.setText("No cover found")
            return
        pixmap = QtGui.QPixmap()
        if pixmap.loadFromData(cover_bytes):
            scaled = pixmap.scaled(
                180,
                260,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            self.label_cover_metadataTab.setPixmap(scaled)
            self.label_cover_metadataTab.show()

    def update_metadata(self):
        if not hasattr(self, "cached_metadata") or self.cached_metadata is None:
            QMessageBox.warning(self, "No data", "No metadata has been fetched yet")
            return

        selected_ids = self.gui.library_view.get_selected_ids()
        if not selected_ids:
            QMessageBox.warning(self, "No selection", "No book selected")
            return

        book_id = selected_ids[0]
        db = self.gui.current_db.new_api

        if hasattr(self, "cached_identifiers") and self.cached_identifiers:
            existing = dict(self.cached_metadata.identifiers or {})
            for id_item in self.cached_identifiers:
                id_type = id_item.get("type", "")
                id_value = id_item.get("value", "")
                if id_type and id_value:
                    existing[id_type.lower()] = id_value
            self.cached_metadata.identifiers = existing

        db.set_metadata(book_id, self.cached_metadata)

        if hasattr(self, "cached_cover_bytes") and self.cached_cover_bytes:
            db.set_cover({book_id: self.cached_cover_bytes})

        QMessageBox.information(self, "Success", "Book metadata updated successfully")

    def create_metadata_object(self, bb_data, book_name):
        title = book_name

        authors = []

        author_credits = bb_data.get("authorCredits") or {}
        author_names = author_credits.get("names", [])
        for credit in author_names:
            name = credit.get("name", "")
            if name:
                authors.append(name)

        if not authors:
            authors = ["Unknown author"]

        mi = Metadata(title, authors)

        publishers = bb_data.get("publishers") or []
        if publishers:
            mi.publisher = publishers[0].get("name")

        pubdate = extended_date_to_datetime(bb_data.get("releaseEventDate"))
        mi.pubdate = pubdate if pubdate is not None else ""

        languages = bb_data.get("languages") or []
        if languages:
            mi.languages = languages

        tags = []
        status = bb_data.get("status")
        if status:
            tags.append(status)

        bbid = bb_data.get("bbid")
        if bbid:
            mi.identifiers = {"bbid": bbid}

        disambiguation = bb_data.get("disambiguation")
        if disambiguation:
            mi.comments = disambiguation

        return mi
