from qt.core import QtCore, QtGui, QtWidgets

#############################################################
#  Browse-tab results panel
#############################################################
#
# (Simillar to metadataTab search_panel)
# Toggles between:
# 0 - The search-results table
# 1 - A "Searching Book…" state 


def setup_results_panel(self):
    self.stackedWidget_browseTab = QtWidgets.QStackedWidget(parent=self.browseTab)
    self.stackedWidget_browseTab.setObjectName("stackedWidget_browseTab")

    #  Page 0: results table
    self.page_searchResultBooks = QtWidgets.QWidget()
    self.page_searchResultBooks.setObjectName("page_searchResultBooks")
    self.verticalLayout_searchResults_browse = QtWidgets.QVBoxLayout(
        self.page_searchResultBooks
    )
    self.verticalLayout_searchResults_browse.setContentsMargins(0, 5, 0, 0)
    self.verticalLayout_searchResults_browse.setSpacing(5)

    self.label_searchResults_browseTab = QtWidgets.QLabel(
        parent=self.page_searchResultBooks
    )
    font = QtGui.QFont()
    font.setPointSize(13)
    self.label_searchResults_browseTab.setFont(font)
    self.label_searchResults_browseTab.setObjectName("label_searchResults_browseTab")
    self.verticalLayout_searchResults_browse.addWidget(
        self.label_searchResults_browseTab
    )

    # Inner stack: table and "no results"
    self.stackedWidget_noResults_browse = QtWidgets.QStackedWidget(
        parent=self.page_searchResultBooks
    )
    self.stackedWidget_noResults_browse.setObjectName("stackedWidget_noResults_browse")

    self.tableWidget_browseTab = QtWidgets.QTableWidget()
    self.tableWidget_browseTab.setObjectName("tableWidget_browseTab")
    self.tableWidget_browseTab.setSelectionBehavior(
        QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
    )
    self.tableWidget_browseTab.setSelectionMode(
        QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
    )
    self.tableWidget_browseTab.setEditTriggers(
        QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
    )
    self.tableWidget_browseTab.setColumnCount(5)
    self.tableWidget_browseTab.setRowCount(0)
    for col in range(5):
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_browseTab.setHorizontalHeaderItem(col, item)
    self.tableWidget_browseTab.horizontalHeader().setCascadingSectionResizes(False)
    self.tableWidget_browseTab.horizontalHeader().setDefaultSectionSize(160)
    self.tableWidget_browseTab.horizontalHeader().setSortIndicatorShown(False)
    self.tableWidget_browseTab.horizontalHeader().setStretchLastSection(True)
    header_font = self.tableWidget_browseTab.horizontalHeader().font()
    header_font.setBold(False)
    self.tableWidget_browseTab.horizontalHeader().setFont(header_font)
    self.stackedWidget_noResults_browse.addWidget(self.tableWidget_browseTab)

    self.label_searchPrompt_browseTab = QtWidgets.QLabel()
    font = QtGui.QFont()
    font.setPointSize(16)
    self.label_searchPrompt_browseTab.setFont(font)
    self.label_searchPrompt_browseTab.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    self.label_searchPrompt_browseTab.setObjectName("label_searchPrompt_browseTab")
    self.stackedWidget_noResults_browse.addWidget(self.label_searchPrompt_browseTab)

    self.label_noBookFound_browseTab = QtWidgets.QLabel()
    font = QtGui.QFont()
    font.setPointSize(16)
    self.label_noBookFound_browseTab.setFont(font)
    self.label_noBookFound_browseTab.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    self.label_noBookFound_browseTab.setObjectName("label_noBookFound_browseTab")
    self.stackedWidget_noResults_browse.addWidget(self.label_noBookFound_browseTab)
    self.stackedWidget_noResults_browse.setCurrentIndex(1)
    self.verticalLayout_searchResults_browse.addWidget(
        self.stackedWidget_noResults_browse, 1
    )

    self.stackedWidget_browseTab.addWidget(self.page_searchResultBooks)

    # Page 1: "Searching Book…" state
    self.page_searchingBook = QtWidgets.QWidget()
    self.page_searchingBook.setObjectName("page_searchingBook")
    self.verticalLayout_searchingBook = QtWidgets.QVBoxLayout(self.page_searchingBook)
    self.layoutWidget_searchingBook = QtWidgets.QWidget(parent=self.page_searchingBook)
    self.layoutWidget_searchingBook.setObjectName("layoutWidget_searchingBook")
    self.horizontalLayout_searchingBook = QtWidgets.QHBoxLayout(
        self.layoutWidget_searchingBook
    )
    self.horizontalLayout_searchingBook.setContentsMargins(0, 0, 0, 0)
    self.horizontalLayout_searchingBook.setObjectName("horizontalLayout_searchingBook")
    self.progressBar_searchingMetadata_metadataTab_2 = QtWidgets.QProgressBar(
        parent=self.layoutWidget_searchingBook
    )
    self.progressBar_searchingMetadata_metadataTab_2.setMaximum(0)
    self.progressBar_searchingMetadata_metadataTab_2.setProperty("value", -1)
    self.progressBar_searchingMetadata_metadataTab_2.setObjectName(
        "progressBar_searchingMetadata_metadataTab_2"
    )
    self.horizontalLayout_searchingBook.addWidget(
        self.progressBar_searchingMetadata_metadataTab_2
    )
    self.label_searchingBook_browseTab = QtWidgets.QLabel(
        parent=self.layoutWidget_searchingBook
    )
    font = QtGui.QFont()
    font.setPointSize(16)
    self.label_searchingBook_browseTab.setFont(font)
    self.label_searchingBook_browseTab.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    self.label_searchingBook_browseTab.setObjectName("label_searchingBook_browseTab")
    self.horizontalLayout_searchingBook.addWidget(self.label_searchingBook_browseTab)
    self.verticalLayout_searchingBook.addStretch(1)
    self.verticalLayout_searchingBook.addWidget(
        self.layoutWidget_searchingBook,
        0,
        QtCore.Qt.AlignmentFlag.AlignCenter,
    )
    self.verticalLayout_searchingBook.addStretch(1)

    self.stackedWidget_browseTab.addWidget(self.page_searchingBook)
    self.verticalLayout_4.addWidget(self.stackedWidget_browseTab, 1)


def retranslate_results_panel(self, _translate):
    for col, text in enumerate(["Name", "Authors", "Language", "BBID", "SortName"]):
        item = self.tableWidget_browseTab.horizontalHeaderItem(col)
        item.setText(_translate("Dialog", text))

    self.label_searchResults_browseTab.setText(_translate("Dialog", "Search Results"))
    self.label_searchPrompt_browseTab.setText(
        _translate("Dialog", "Search for a book by title")
    )
    self.label_noBookFound_browseTab.setText(
        _translate("Dialog", "Could not find this book on BookBrainz")
    )
    self.label_searchingBook_browseTab.setText(
        _translate("Dialog", "Searching Book...")
    )
