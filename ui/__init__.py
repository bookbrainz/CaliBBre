from qt.core import QtCore, QtGui, QtWidgets

from .browse_tab import BrowseTabMixin
from .collection_tab import CollectionTabMixin
from .metadata_tab import MetadataTabMixin


# Top-level dialog that composes all three tab mixins
class Ui_Dialog(MetadataTabMixin, BrowseTabMixin, CollectionTabMixin):
    def setupUi(self, Dialog):
        # Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(826, 889)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(600, 600))
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("")

        # Root vertical layout: logo -> tab widget
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # BookBrainz logo
        self.label_BookBrainz_logo = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_BookBrainz_logo.sizePolicy().hasHeightForWidth()
        )
        self.label_BookBrainz_logo.setSizePolicy(sizePolicy)
        self.label_BookBrainz_logo.setMinimumSize(QtCore.QSize(0, 150))
        self.label_BookBrainz_logo.setText("")
        self.label_BookBrainz_logo.setPixmap(
            QtGui.QPixmap("./images/BookBrainz_logo.svg")
        )
        self.label_BookBrainz_logo.setScaledContents(False)
        self.label_BookBrainz_logo.setObjectName("label_BookBrainz_logo")
        self.verticalLayout_3.addWidget(
            self.label_BookBrainz_logo, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        # Tab widget
        self.tabWidget = QtWidgets.QTabWidget(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(222)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")
        # We install an event filter so we can re-distribute tab-bar widths
        # whenever the dialog is resized
        self.tabWidget.installEventFilter(self)

        # Delegate tab-page setup to the mixins
        self.setup_metadata_tab()
        self.setup_browse_tab()
        self.setup_collection_tab()

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)

        # Every stacked widget starts on its sensible default page so the user
        # never sees a blank or half-built panel on first launch
        self.stackedWidget_entire_metadataTab.setCurrentIndex(0)
        self.stackedWidget_searchResults_metadataTab.setCurrentIndex(0)
        self.stackedWidget_metadataDetails_metadataTab.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)

        self._update_tab_widths()
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    # Tab-bar width equaliser
    # By default Qt tabs are left-aligned and look tiny when there are only
    # two or three of them. We override that so each tab stretches evenly

    def eventFilter(self, obj, event):
        if obj == self.tabWidget and event.type() == QtCore.QEvent.Resize:
            self._update_tab_widths()
        return False

    def _update_tab_widths(self):
        tab_width = self.tabWidget.width() // self.tabWidget.count()
        self.tabWidget.tabBar().setStyleSheet(
            f"QTabBar::tab {{ min-width: {tab_width}px; }}"
        )

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BookBrainz Plugin"))

        self.retranslate_metadata_tab(_translate)
        self.retranslate_browse_tab(_translate)
        self.retranslate_collection_tab(_translate)