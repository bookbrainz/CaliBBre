from qt.core import QMessageBox, QtCore, QtWidgets

#################################################
# Collection tab
#################################################


class CollectionTabMixin:
    def setup_collection_tab(self):
        self.collectionTab = QtWidgets.QWidget()
        self.collectionTab.setObjectName("collectionTab")
        self.tabWidget.addTab(self.collectionTab, "")

    def retranslate_collection_tab(self, _translate):
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.collectionTab),
            _translate("Dialog", "Collection"),
        )
