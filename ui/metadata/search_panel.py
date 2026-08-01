from qt.core import QtCore, QtGui, QtWidgets

#####################################################################
# Search-results panel (upper half of the Metadata tab)
#####################################################################

# Two stacked states: search results table and "Searching metadata..." label
# Within the results page there's a further sub-stack that swaps between
# the data table and a "no results" message


def setup_search_panel(self):
    # Outer container: stacked results / searching
    self.stackedWidget_searchResults_metadataTab = QtWidgets.QStackedWidget(
        parent=self.page
    )
    self.stackedWidget_searchResults_metadataTab.setObjectName(
        "stackedWidget_searchResults_metadataTab"
    )

    # Page 0: search results
    self.page_searchResults = QtWidgets.QWidget()
    self.page_searchResults.setObjectName("page_searchResults")
    self.verticalLayout_searchResults = QtWidgets.QVBoxLayout(self.page_searchResults)
    self.verticalLayout_searchResults.setContentsMargins(0, 10, 0, 0)
    self.verticalLayout_searchResults.setSpacing(5)

    self.label_searchResults_metadataTab = QtWidgets.QLabel(
        parent=self.page_searchResults
    )
    font = QtGui.QFont()
    font.setPointSize(13)
    self.label_searchResults_metadataTab.setFont(font)
    self.label_searchResults_metadataTab.setObjectName(
        "label_searchResults_metadataTab"
    )
    self.verticalLayout_searchResults.addWidget(self.label_searchResults_metadataTab)

    # Nested stack: page 0 = data table, page 1 = "no results" message
    self.stackedWidget_noResults_metadataTab = QtWidgets.QStackedWidget(
        parent=self.page_searchResults
    )
    self.stackedWidget_noResults_metadataTab.setObjectName(
        "stackedWidget_noResults_metadataTab"
    )

    # The table: read-only, row-select, 5 columns (Name, Authors, Language, BBID, SortName )
    self.tableWidget_metadataTab = QtWidgets.QTableWidget()
    sizePolicy = QtWidgets.QSizePolicy(
        QtWidgets.QSizePolicy.Policy.Expanding,
        QtWidgets.QSizePolicy.Policy.Expanding,
    )
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
        self.tableWidget_metadataTab.sizePolicy().hasHeightForWidth()
    )
    self.tableWidget_metadataTab.setSizePolicy(sizePolicy)
    self.tableWidget_metadataTab.setObjectName("tableWidget_metadataTab")
    self.tableWidget_metadataTab.setSelectionBehavior(
        QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
    )
    self.tableWidget_metadataTab.setEditTriggers(
        QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
    )
    self.tableWidget_metadataTab.setColumnCount(5)
    self.tableWidget_metadataTab.setRowCount(0)
    for col in range(5):
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_metadataTab.setHorizontalHeaderItem(col, item)
    self.tableWidget_metadataTab.horizontalHeader().setCascadingSectionResizes(False)
    self.tableWidget_metadataTab.horizontalHeader().setDefaultSectionSize(160)
    self.tableWidget_metadataTab.horizontalHeader().setHighlightSections(False)
    self.tableWidget_metadataTab.horizontalHeader().setMinimumSectionSize(10)
    self.tableWidget_metadataTab.horizontalHeader().setSortIndicatorShown(False)
    self.tableWidget_metadataTab.horizontalHeader().setStretchLastSection(True)
    self.tableWidget_metadataTab.verticalHeader().setCascadingSectionResizes(False)
    self.stackedWidget_noResults_metadataTab.addWidget(self.tableWidget_metadataTab)

    # "No matching books found" -> shown when the API returns an empty list
    self.label_noMetadata_metadataTab_2 = QtWidgets.QLabel()
    font = QtGui.QFont()
    font.setPointSize(13)
    self.label_noMetadata_metadataTab_2.setFont(font)
    self.label_noMetadata_metadataTab_2.setAlignment(
        QtCore.Qt.AlignmentFlag.AlignCenter
    )
    self.label_noMetadata_metadataTab_2.setObjectName("label_noMetadata_metadataTab_2")
    self.stackedWidget_noResults_metadataTab.addWidget(
        self.label_noMetadata_metadataTab_2
    )
    # Default to the "no results" page so the table isn't visible before
    self.stackedWidget_noResults_metadataTab.setCurrentIndex(1)
    self.verticalLayout_searchResults.addWidget(
        self.stackedWidget_noResults_metadataTab, 1
    )

    # "Fetch Book Metadata" button —> triggers the detail-fetch for the selected row
    self.pushButton_fetch_metadataTab = QtWidgets.QPushButton(
        parent=self.page_searchResults
    )
    sizePolicy = QtWidgets.QSizePolicy(
        QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
    )
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
        self.pushButton_fetch_metadataTab.sizePolicy().hasHeightForWidth()
    )
    self.pushButton_fetch_metadataTab.setSizePolicy(sizePolicy)
    self.pushButton_fetch_metadataTab.setMinimumSize(QtCore.QSize(0, 30))
    self.pushButton_fetch_metadataTab.setObjectName("pushButton_fetch_metadataTab")
    self.verticalLayout_searchResults.addWidget(self.pushButton_fetch_metadataTab)

    self.stackedWidget_searchResults_metadataTab.addWidget(self.page_searchResults)

    # Page 1: "Searching Metadata…" progress bar
    # Uses an indeterminate progress bar (maximum=0) so it pulses forever until the search thread finishes

    self.page_searchingMetadata = QtWidgets.QWidget()
    self.page_searchingMetadata.setObjectName("page_searchingMetadata")
    self.verticalLayout_searching = QtWidgets.QVBoxLayout(self.page_searchingMetadata)
    self.layoutWidget_searching = QtWidgets.QWidget(parent=self.page_searchingMetadata)
    self.layoutWidget_searching.setObjectName("layoutWidget_searching")
    self.horizontalLayout_searching = QtWidgets.QHBoxLayout(self.layoutWidget_searching)
    self.horizontalLayout_searching.setContentsMargins(0, 0, 0, 0)
    self.horizontalLayout_searching.setObjectName("horizontalLayout_searching")
    self.progressBar_searchingMetadata_metadataTab = QtWidgets.QProgressBar(
        parent=self.layoutWidget_searching
    )
    self.progressBar_searchingMetadata_metadataTab.setMaximum(0)
    self.progressBar_searchingMetadata_metadataTab.setProperty("value", -1)
    self.progressBar_searchingMetadata_metadataTab.setObjectName(
        "progressBar_searchingMetadata_metadataTab"
    )
    self.horizontalLayout_searching.addWidget(
        self.progressBar_searchingMetadata_metadataTab
    )
    self.label_searchingMetadata_metadataTab = QtWidgets.QLabel(
        parent=self.layoutWidget_searching
    )
    font = QtGui.QFont()
    font.setPointSize(16)
    self.label_searchingMetadata_metadataTab.setFont(font)
    self.label_searchingMetadata_metadataTab.setAlignment(
        QtCore.Qt.AlignmentFlag.AlignCenter
    )
    self.label_searchingMetadata_metadataTab.setObjectName(
        "label_searchingMetadata_metadataTab"
    )
    self.horizontalLayout_searching.addWidget(self.label_searchingMetadata_metadataTab)
    self.verticalLayout_searching.addStretch(1)
    self.verticalLayout_searching.addWidget(
        self.layoutWidget_searching, 0, QtCore.Qt.AlignmentFlag.AlignCenter
    )
    self.verticalLayout_searching.addStretch(1)

    self.stackedWidget_searchResults_metadataTab.addWidget(self.page_searchingMetadata)
    self.verticalLayout_5.addWidget(self.stackedWidget_searchResults_metadataTab)


def retranslate_search_panel(self, _translate):
    
    for col, text in enumerate(["Name", "Authors", "Language", "BBID", "Sort name"]):
        item = self.tableWidget_metadataTab.horizontalHeaderItem(col)
        item.setText(_translate("Dialog", text))

    self.label_searchResults_metadataTab.setText(_translate("Dialog", "Search results"))
    self.pushButton_fetch_metadataTab.setText(
        _translate("Dialog", "Fetch book metadata")
    )
    self.label_noMetadata_metadataTab_2.setText(
        _translate("Dialog", "No matching books found")
    )
    self.label_searchingMetadata_metadataTab.setText(
        _translate("Dialog", "Searching metadata...")
    )
