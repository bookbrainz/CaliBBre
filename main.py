#!/usr/bin/env python2
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
import sys
import json
import urllib2

from PyQt5.Qt import *
from calibre_plugins.CaliBBre.config import prefs

__license__ = 'GPL v3'
__copyright__ = '2015 Stanislaw Szczesniak'
__docformat__ = 'restructuredtext en'


class CaliBBreDialog(QDialog):
    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config
        self.db = gui.current_db

        # Basic window configurations
        self.window_init(icon)

        # Adding BookBrainz logo to the plugin dialog
        self.img = QLabel()
        pixmap = QPixmap("images/BBt.svg")
        self.img.setPixmap(pixmap)
        self.l.addWidget(self.img)

        # Adding search space
        self.search_space = QLineEdit()
        self.search_space.setPlaceholderText(prefs['enterbbid'])
        self.l.addWidget(self.search_space)

        # Adding search execution button
        self.searchExecutionButton = QPushButton(prefs['searchandfetch'], self)
        self.searchExecutionButton.clicked.connect(self.search)
        self.l.addWidget(self.searchExecutionButton)

        # Download button
        self.downloadMetadataButton \
            = QPushButton(prefs['dmetbb'])
        self.downloadMetadataButton.clicked.connect(self.download_metadata)
        self.l.addWidget(self.downloadMetadataButton)

        # Table initalization
        self.table_init()

        self.applyButton = QPushButton(prefs['apply_changes'], self)
        self.applyButton.clicked.connect(self.apply_metadata)
        self.l.addWidget(self.applyButton)

        self.aboutButton = QPushButton(prefs['about'], self)
        self.aboutButton.clicked.connect(self.about)
        self.l.addWidget(self.aboutButton)

        self.search_space.setFocus()

    # Basic window configurations
    def window_init(self, icon):
        # Setting Dialog size
        self.resize(600, 500)

        # Setting Dialog layout
        self.l = QVBoxLayout()
        self.setLayout(self.l)

        # Setting window title and icon
        self.setWindowTitle(prefs['window_title'])
        self.setWindowIcon(icon)

    # Results table initialization
    def table_init(self):
        self.table = QTableWidget(6, 2)
        self.table.setHorizontalHeaderLabels([prefs["Current Metadata"], prefs["Metadata from BookBrainz"]])
        self.table.setVerticalHeaderLabels(
            [prefs['Title'],
             prefs['Author'],
             prefs['Date published'],
             prefs['Publisher name'],
             prefs['Languages'],
             prefs['Identifiers']])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.l.addWidget(self.table)

    def download_metadata(self):
        self.downloadMetadataButton.setText(prefs['Downloading metadata...'])
        self.downloadMetadataButton.repaint()
        self.downloadMetadataButton.setFocus()
        self.book_id = 0
        rows = self.gui.current_view().selectionModel().selectedRows()
        if len(rows) == 0:
            return
        self.book_id = self.gui.library_view.model().id(rows[0])

        # title
        try:
            title = self.actjs['default_alias']['name']
            self.table.setItem(0, 1, new_qitem(title))
            self.table.repaint()
        except:
            pass

        # Author
        try:
            rurl = self.actjs['relationships_uri']
            js = request_get(rurl)
            found = False
            author = ""
            for o in js['objects']:
                for e in o['entities']:
                    if e['entity']['_type'] == 'Creator':
                        auri = e['entity']['uri']
                        js2 = request_get(auri)
                        author = js2['default_alias']['name']
                        found = True
                        break
                if found:
                    break
            self.table.setItem(1, 1, new_qitem(author))
            self.table.repaint()
        except:
            pass

        # date_published
        try:
            date_published = self.actjs['release_date']
            self.table.setItem(2, 1, new_qitem(date_published))
            self.table.repaint()
        except:
            pass

        # publisher_name
        try:
            purl = self.actjs['publisher_uri']
            publisher_name = ""
            if purl is not None:
                prj = request_get(purl)
                publisher_name = prj['default_alias']['name']
            self.table.setItem(3, 1, new_qitem(publisher_name))
            self.table.repaint()
        except:
            pass

        # language_name - works fine with translations of names of languages(tested)
        try:
            language_name = self.actjs['language']['name']
            self.table.setItem(4, 1, new_qitem(language_name))
            self.table.repaint()
        except:
            pass

        # identifiers
        try:
            identifiers = ""
            iuri = self.actjs['identifiers_uri']
            irj = request_get(iuri)
            for o in irj['objects']:
                id_type = o['identifier_type']['label']
                id_value = o['value']
                identifiers += id_type + "::" + id_value + ","
            identifiers = identifiers[:-1]
            # might ask about adding or succession
            self.table.setItem(5, 1, new_qitem(identifiers))
            self.table.repaint()
        except:
            pass

        self.search_space.setText("")
        rows[0].row()

        self.downloadMetadataButton.setText(prefs['dmetbb'])
        self.downloadMetadataButton.repaint()
        self.applyButton.setFocus()

    # Apply downloaded metadata to the selected book
    def apply_metadata(self):
        categories = ['title', 'authors', 'pubdate', 'publisher', 'languages', 'identifiers']
        for key in categories:
            try:
                if key not in ["", None]:
                    self.db.new_api.set_field(key, {self.book_id: self.table.item(categories.index(key), 1).text()})
            except:
                pass

        self.gui.iactions['Edit Metadata'].refresh_books_after_metadata_edit({self.book_id})
        self.search_space.setFocus()

    # Search for book in BBID and
    def search(self):
        self.searchExecutionButton.setText(prefs['Searching ...'])
        self.searchExecutionButton.setFocus()
        self.downloadMetadataButton.repaint()
        text = self.search_space.text()
        self.last_text = text
        print(text)
        # self.table.clear()
        self.clear_table()
        self.table.setFocus()
        num_queries = 0
        js = {}
        try:
            for entity_type in ['edition', 'publication', 'work']:
                rurl = "https://bookbrainz.org/ws/" + entity_type + "/" + text + "/"
                # print(rurl)
                js = request_get(rurl)
                self.actjs = js
                if '_type' not in js:
                    continue
                num_queries = 1
                break
            if num_queries == 0:
                return
        except:
            self.searchExecutionButton.setText(prefs['searchandfetch'])
            self.clear_table()
            self.searchExecutionButton.setFocus()
            return
        rows = self.gui.current_view().selectionModel().selectedRows()
        if len(rows) == 0:
            self.search_space.setText("")
        else:
            mi = self.gui.library_view.model().db.get_metadata(rows[0].row())
            self.table.setItem(0, 0, new_qitem(mi.title))
            self.table.setItem(1, 0, new_qitem(mi.authors))
            self.table.setItem(2, 0, new_qitem(mi.pubdate))
            self.table.setItem(3, 0, new_qitem(mi.publisher))
            self.table.setItem(4, 0, new_qitem(mi.languages))
            self.table.setItem(5, 0, new_qitem(mi.identifiers))
        self.table.setItem(0, 1, new_qitem(js['default_alias']['name']))
        self.table.repaint()

        self.queryResult = js
        self.searchExecutionButton.setText(prefs['searchandfetch'])
        self.searchExecutionButton.repaint()
        self.downloadMetadataButton.setFocus()

    def config(self):
        self.do_user_config(parent=self)
        # Apply the changes
        self.label.setText(prefs['hello_world_msg'])

    def clear_table(self):
        for i in range(6):
            for j in range(2):
                self.table.setItem(i, j, new_qitem(""))
        self.table.repaint()

    # noinspection PyCallByClass,PyTypeChecker
    def about(self):
        text = get_resources('about.txt')
        QMessageBox.about(self, 'About the CaliBBre',
                          text.decode('utf-8'))


# Return json data obtained by using provided url
def request_get(url):
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data


# Creates QTableWidgetItem with the provided text
def new_qitem(text):
    if type(text) == list:
        ctext = ""
        for x in text:
            ctext += str(x) + ','
        text = ctext[:-1]
    else:
        text = str(text)

    item = QTableWidgetItem()
    item.setText(text)
    return item
