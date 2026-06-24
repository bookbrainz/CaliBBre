from qt.core import QMessageBox, QtWidgets

#################################################
#  Browse tab
#################################################


class BrowseTabMixin:
    def setup_browse_tab(self):
        # Root container
        self.browseTab = QtWidgets.QWidget()
        self.browseTab.setObjectName("browseTab")
        self.tabWidget.addTab(self.browseTab, "")

    def retranslate_browse_tab(self, _translate):
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.browseTab),
            _translate("Dialog", "Browse"),
        )
