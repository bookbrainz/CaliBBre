from qt.core import QtCore, QtGui, QtWidgets

#############################################################
# Browse-tab search bar
#############################################################


def setup_search_bar(self):
    self.verticalLayout = QtWidgets.QVBoxLayout()
    self.verticalLayout.setObjectName("verticalLayout")

    self.lineEdit_searchbar_browseTab = QtWidgets.QLineEdit(parent=self.browseTab)
    sizePolicy = QtWidgets.QSizePolicy(
        QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
    )
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
        self.lineEdit_searchbar_browseTab.sizePolicy().hasHeightForWidth()
    )
    self.lineEdit_searchbar_browseTab.setSizePolicy(sizePolicy)
    self.lineEdit_searchbar_browseTab.setMinimumSize(QtCore.QSize(0, 40))
    self.lineEdit_searchbar_browseTab.setFrame(True)
    self.lineEdit_searchbar_browseTab.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
    self.lineEdit_searchbar_browseTab.setCursorPosition(0)
    self.lineEdit_searchbar_browseTab.setAlignment(
        QtCore.Qt.AlignmentFlag.AlignLeading
        | QtCore.Qt.AlignmentFlag.AlignLeft
        | QtCore.Qt.AlignmentFlag.AlignVCenter
    )
    self.lineEdit_searchbar_browseTab.setClearButtonEnabled(False)
    self.lineEdit_searchbar_browseTab.setTextMargins(8, 0, 0, 0)
    self.lineEdit_searchbar_browseTab.setObjectName("lineEdit_searchbar_browseTab")
    self.lineEdit_searchbar_browseTab.returnPressed.connect(self.search_book_by_name)
    self.verticalLayout.addWidget(self.lineEdit_searchbar_browseTab)

    # Search trigger button
    self.pushButton_search_browseTab = QtWidgets.QPushButton(parent=self.browseTab)
    self.pushButton_search_browseTab.setMinimumSize(QtCore.QSize(0, 40))
    self.pushButton_search_browseTab.setObjectName("pushButton_search_browseTab")
    self.verticalLayout.addWidget(self.pushButton_search_browseTab)

    self.verticalLayout_4.addLayout(self.verticalLayout)


def retranslate_search_bar(self, _translate):
    self.lineEdit_searchbar_browseTab.setPlaceholderText(
        _translate("Dialog", "Enter book title...")
    )
    self.pushButton_search_browseTab.setText(
        _translate("Dialog", "Search Book in BookBrainz")
    )
