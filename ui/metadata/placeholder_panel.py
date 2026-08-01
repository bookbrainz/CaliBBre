from qt.core import QtCore, QtGui, QtWidgets

#############################################
# "No Book Selected" placeholder
#############################################
#
# Replaces the entire Metadata tab content when the user opens the plugin
# without having a book selected in the Calibre library
#
# The stacked-widget parent (stackedWidget_entire_metadataTab) flips between
# this page (index 1) and the real content page (index 0)


def setup_no_book_placeholder(self):
    self.page_2 = QtWidgets.QWidget()
    self.page_2.setObjectName("page_2")
    self.verticalLayout_noBook = QtWidgets.QVBoxLayout(self.page_2)
    self.verticalLayout_noBook.addStretch(1)

    self.layoutWidget_noBook = QtWidgets.QWidget(parent=self.page_2)
    self.layoutWidget_noBook.setObjectName("layoutWidget_noBook")
    self.verticalLayout_noBookInner = QtWidgets.QVBoxLayout(self.layoutWidget_noBook)
    self.verticalLayout_noBookInner.setContentsMargins(0, 0, 0, 0)
    self.verticalLayout_noBookInner.setObjectName("verticalLayout_noBookInner")

    # Heading
    self.label_noBookSelectedHeader_metadataTab = QtWidgets.QLabel(
        parent=self.layoutWidget_noBook
    )
    font = QtGui.QFont()
    font.setPointSize(20)
    font.setBold(True)
    font.setWeight(75)
    self.label_noBookSelectedHeader_metadataTab.setFont(font)
    self.label_noBookSelectedHeader_metadataTab.setAlignment(
        QtCore.Qt.AlignmentFlag.AlignCenter
    )
    self.label_noBookSelectedHeader_metadataTab.setWordWrap(True)
    self.label_noBookSelectedHeader_metadataTab.setObjectName(
        "label_noBookSelectedHeader_metadataTab"
    )
    self.verticalLayout_noBookInner.addWidget(
        self.label_noBookSelectedHeader_metadataTab
    )

    # Description underneath
    self.label_noBookSelected_description_metadataTab = QtWidgets.QLabel(
        parent=self.layoutWidget_noBook
    )
    font = QtGui.QFont()
    font.setPointSize(13)
    self.label_noBookSelected_description_metadataTab.setFont(font)
    self.label_noBookSelected_description_metadataTab.setAlignment(
        QtCore.Qt.AlignmentFlag.AlignCenter
    )
    self.label_noBookSelected_description_metadataTab.setWordWrap(True)
    self.label_noBookSelected_description_metadataTab.setObjectName(
        "label_noBookSelected_description_metadataTab"
    )
    self.verticalLayout_noBookInner.addWidget(
        self.label_noBookSelected_description_metadataTab
    )

    self.verticalLayout_noBook.addWidget(
        self.layoutWidget_noBook, 0, QtCore.Qt.AlignmentFlag.AlignCenter
    )
    self.verticalLayout_noBook.addStretch(1)

    self.stackedWidget_entire_metadataTab.addWidget(self.page_2)


def retranslate_placeholder(self, _translate):
    self.label_noBookSelectedHeader_metadataTab.setText(
        _translate("Dialog", "No book selected")
    )
    self.label_noBookSelected_description_metadataTab.setText(
        _translate(
            "Dialog", "Select a book from your calibre library to use this feature"
        )
    )
