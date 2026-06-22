from qt.core import QtCore, QtGui, QtWidgets

#############################################################
# Metadata details panel (lower half of the Metadata tab)
#############################################################
#
# Three stacked states:
#   0 -> "Select a book to view details" (placeholder before any row is picked)
#   1 ->  Filled-in metadata with cover art (grid of label/value pairs after a successful fetch)
#   2 -> "Fetching Details…" spinner (while the API call is in flight)


def setup_details_panel(self):
    self.stackedWidget_metadataDetails_metadataTab = QtWidgets.QStackedWidget(
        parent=self.page
    )
    self.stackedWidget_metadataDetails_metadataTab.setObjectName(
        "stackedWidget_metadataDetails_metadataTab"
    )

    # Page 0: "Select a book" placeholder
    self.page_noBookSelected = QtWidgets.QWidget()
    self.page_noBookSelected.setObjectName("page_noBookSelected")
    self.verticalLayout_noDetails = QtWidgets.QVBoxLayout(self.page_noBookSelected)
    self.label_noMetadataDetails_metadataTab = QtWidgets.QLabel()
    font = QtGui.QFont()
    font.setPointSize(13)
    self.label_noMetadataDetails_metadataTab.setFont(font)
    self.label_noMetadataDetails_metadataTab.setAlignment(
        QtCore.Qt.AlignmentFlag.AlignCenter
    )
    self.label_noMetadataDetails_metadataTab.setWordWrap(True)
    self.label_noMetadataDetails_metadataTab.setObjectName(
        "label_noMetadataDetails_metadataTab"
    )
    self.verticalLayout_noDetails.addStretch(1)
    self.verticalLayout_noDetails.addWidget(self.label_noMetadataDetails_metadataTab)
    self.verticalLayout_noDetails.addStretch(1)
    self.stackedWidget_metadataDetails_metadataTab.addWidget(self.page_noBookSelected)

    # Page 1: metadata detail grid + cover
    self.page_metadataDetails = QtWidgets.QWidget()
    self.page_metadataDetails.setObjectName("page_metadataDetails")
    self.verticalLayout_details = QtWidgets.QVBoxLayout(self.page_metadataDetails)
    self.verticalLayout_details.setContentsMargins(15, 9, 15, 10)
    self.verticalLayout_details.setSpacing(10)

    self.label_metadataDetails_metadataTab = QtWidgets.QLabel()
    font = QtGui.QFont()
    font.setPointSize(14)
    self.label_metadataDetails_metadataTab.setFont(font)
    self.label_metadataDetails_metadataTab.setObjectName(
        "label_metadataDetails_metadataTab"
    )
    self.verticalLayout_details.addWidget(self.label_metadataDetails_metadataTab)

    # Horizontal layout: grid on left, cover on right
    self.horizontalLayout_content = QtWidgets.QHBoxLayout()
    self.horizontalLayout_content.setSpacing(15)

    # Left side: vertical layout with the field grid
    self.verticalLayout_left = QtWidgets.QVBoxLayout()
    self.verticalLayout_left.setSpacing(10)

    # Two-column grid: field label / field value
    self.gridLayout_details = QtWidgets.QGridLayout()
    self.gridLayout_details.setSpacing(10)
    self.gridLayout_details.setColumnMinimumWidth(0, 120)

    fields = [
        ("label_name_metadataTab", "label_data_name_metadataTab"),
        ("label_sortname_metadataTab", "label_data_sortname_metadataTab"),
        ("label_author_metadataTab", "label_data_author_metadataTab"),
        ("label_language_metadataTab", "label_data_language_metadataTab"),
        ("label_publisher_metadataTab", "label_data_publisher_metadataTab"),
        ("label_releaseDate_metadataTab", "label_data_releaseDate_metadataTab"),
        ("label_disambiguation_metadataTab_2", "label_data_disambiguation_metadataTab"),
        ("label_identifiers_metadataTab", "label_data_identifiers_metadataTab"),
    ]
    for row, (label_name, data_name) in enumerate(fields):
        lbl = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(600)
        lbl.setFont(font)
        lbl.setObjectName(label_name)
        self.gridLayout_details.addWidget(lbl, row, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        data_lbl = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        data_lbl.setFont(font)
        data_lbl.setObjectName(data_name)
        self.gridLayout_details.addWidget(
            data_lbl, row, 1, QtCore.Qt.AlignmentFlag.AlignTop
        )

        setattr(self, label_name, lbl)
        setattr(self, data_name, data_lbl)

    self.gridLayout_details.setColumnStretch(1, 1)
    for i in range(len(fields)):
        self.gridLayout_details.setRowMinimumHeight(i, 25)
    self.verticalLayout_left.addLayout(self.gridLayout_details)
    self.verticalLayout_left.addStretch(1)
    self.horizontalLayout_content.addLayout(self.verticalLayout_left, 1)

    # Right side: cover image
    self.label_cover_metadataTab = QtWidgets.QLabel()
    self.label_cover_metadataTab.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    self.label_cover_metadataTab.setObjectName("label_cover_metadataTab")
    self.label_cover_metadataTab.setFixedWidth(180)
    self.label_cover_metadataTab.setFixedHeight(260)
    self.label_cover_metadataTab.setText("Loading...")
    self.horizontalLayout_content.addWidget(self.label_cover_metadataTab, 0)

    self.verticalLayout_details.addLayout(self.horizontalLayout_content)
    self.verticalLayout_details.addStretch(1)
    self.stackedWidget_metadataDetails_metadataTab.addWidget(self.page_metadataDetails)

    # Page 2: "Fetching Details…" state
    self.page_searchingDetails = QtWidgets.QWidget()
    self.page_searchingDetails.setObjectName("page_searchingDetails")
    self.verticalLayout_searchingDetails = QtWidgets.QVBoxLayout(
        self.page_searchingDetails
    )
    self.layoutWidget_searchingDetails = QtWidgets.QWidget(
        parent=self.page_searchingDetails
    )
    self.layoutWidget_searchingDetails.setObjectName("layoutWidget_searchingDetails")
    self.horizontalLayout_searchingDetails = QtWidgets.QHBoxLayout(
        self.layoutWidget_searchingDetails
    )
    self.horizontalLayout_searchingDetails.setContentsMargins(0, 0, 0, 0)
    self.horizontalLayout_searchingDetails.setObjectName(
        "horizontalLayout_searchingDetails"
    )
    self.progressBar_fetchDetails_metadataTab = QtWidgets.QProgressBar(
        parent=self.layoutWidget_searchingDetails
    )
    self.progressBar_fetchDetails_metadataTab.setMaximum(0)
    self.progressBar_fetchDetails_metadataTab.setProperty("value", -1)
    self.progressBar_fetchDetails_metadataTab.setObjectName(
        "progressBar_fetchDetails_metadataTab"
    )
    self.horizontalLayout_searchingDetails.addWidget(
        self.progressBar_fetchDetails_metadataTab
    )
    self.label_fetchingDetails_metadataTab = QtWidgets.QLabel(
        parent=self.layoutWidget_searchingDetails
    )
    font = QtGui.QFont()
    font.setPointSize(16)
    self.label_fetchingDetails_metadataTab.setFont(font)
    self.label_fetchingDetails_metadataTab.setAlignment(
        QtCore.Qt.AlignmentFlag.AlignCenter
    )
    self.label_fetchingDetails_metadataTab.setObjectName(
        "label_fetchingDetails_metadataTab"
    )
    self.horizontalLayout_searchingDetails.addWidget(
        self.label_fetchingDetails_metadataTab
    )
    self.verticalLayout_searchingDetails.addStretch(1)
    self.verticalLayout_searchingDetails.addWidget(
        self.layoutWidget_searchingDetails,
        0,
        QtCore.Qt.AlignmentFlag.AlignCenter,
    )
    self.verticalLayout_searchingDetails.addStretch(1)
    self.stackedWidget_metadataDetails_metadataTab.addWidget(self.page_searchingDetails)
    self.verticalLayout_5.addWidget(self.stackedWidget_metadataDetails_metadataTab)


def retranslate_details_panel(self, _translate):
    self.label_noMetadataDetails_metadataTab.setText(
        _translate("Dialog", "Select a book to view details")
    )
    self.label_metadataDetails_metadataTab.setText(
        _translate("Dialog", "Metadata Details ")
    )

    # Map each label/data pair to their display strings
    self.label_name_metadataTab.setText(_translate("Dialog", "Name:"))
    self.label_data_name_metadataTab.setText(_translate("Dialog", ""))
    self.label_sortname_metadataTab.setText(_translate("Dialog", "Sort Name:"))
    self.label_data_sortname_metadataTab.setText(_translate("Dialog", ""))
    self.label_author_metadataTab.setText(_translate("Dialog", "Author(s) :"))
    self.label_data_author_metadataTab.setText(_translate("Dialog", ""))
    self.label_language_metadataTab.setText(_translate("Dialog", "Language:"))
    self.label_data_language_metadataTab.setText(_translate("Dialog", ""))
    self.label_publisher_metadataTab.setText(_translate("Dialog", "Publisher:"))
    self.label_data_publisher_metadataTab.setText(_translate("Dialog", ""))
    self.label_releaseDate_metadataTab.setText(_translate("Dialog", "Releasedate:"))
    self.label_data_releaseDate_metadataTab.setText(_translate("Dialog", ""))
    self.label_disambiguation_metadataTab_2.setText(
        _translate("Dialog", "Disambiguation:")
    )
    self.label_data_disambiguation_metadataTab.setText(_translate("Dialog", ""))
    self.label_identifiers_metadataTab.setText(_translate("Dialog", "Identifiers:"))
    self.label_data_identifiers_metadataTab.setText(_translate("Dialog", ""))
    self.label_fetchingDetails_metadataTab.setText(
        _translate("Dialog", "Fetching Details...")
    )
