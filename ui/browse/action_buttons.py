from qt.core import QtCore, QtWidgets

#############################################################
# Browse-tab action buttons
#############################################################
#
# Two buttons below the results table:
# 1. "Add to Reading List" - adds the selected book to calibre ( with fetched metadata ) 
# 2. "Download Metadata"   - exports the selected book's fetched metadata as a JSON file


def setup_action_buttons(self):
    self.pushButton_addBook_browseTab = QtWidgets.QPushButton(parent=self.browseTab)
    self.pushButton_addBook_browseTab.setMinimumSize(QtCore.QSize(0, 30))
    self.pushButton_addBook_browseTab.setObjectName("pushButton_addBook_browseTab")
    self.verticalLayout_4.addWidget(self.pushButton_addBook_browseTab)

    self.pushButton_downloadMetadata_browseTab = QtWidgets.QPushButton(
        parent=self.browseTab
    )
    self.pushButton_downloadMetadata_browseTab.setMinimumSize(QtCore.QSize(0, 30))
    self.pushButton_downloadMetadata_browseTab.setObjectName(
        "pushButton_downloadMetadata_browseTab"
    )
    self.verticalLayout_4.addWidget(self.pushButton_downloadMetadata_browseTab)


def retranslate_action_buttons(self, _translate):
    self.pushButton_addBook_browseTab.setText(
        _translate("Dialog", "Add to Reading List")
    )
    self.pushButton_downloadMetadata_browseTab.setText(
        _translate("Dialog", "Download Metadata")
    )
