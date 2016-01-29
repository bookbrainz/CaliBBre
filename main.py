# -*- coding: utf8 -*-

# Copyright (C) 2015, 2016  Stanisław Szcześniak

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
import json
import urllib2

from PyQt5.Qt import *
from PyQt5.QtCore import *
import uuid
# noinspection PyUnresolvedReferences
from calibre_plugins.CaliBBre.config import names
DEBUG = False

# noinspection PyTypeChecker,PyArgumentList,PyUnresolvedReferences
class CaliBBreDialog(QDialog):
    entity_attributes_order = \
        ['title', 'authors', 'pubdate',
            'publisher', 'languages', 'identifiers']

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config
        self.db = gui.current_db

        # Basic window configurations
        self.window_init(icon)

        # Adding BookBrainz logo to the plugin dialog
        img = QLabel()
        pixmap = QPixmap("images/bookbrainz_name.svg")
        img.setPixmap(pixmap)
        self.layout.addWidget(img)

        # Adding search_for_bbid query editor
        self.search_space = QLineEdit()
        self.search_space.setPlaceholderText(names['Enter title or BookBrainz ID'])
        self.layout.addWidget(self.search_space)

        # Adding search_for_bbid execution button
        self.searchExecutionButton = QPushButton(names['Search'], self)
        self.searchExecutionButton.clicked.connect(self.make_search)
        self.layout.addWidget(self.searchExecutionButton)

        # Download button
        self.downloadMetadataButton \
            = QPushButton(names['Download data from BB'])
        self.downloadMetadataButton.clicked.connect(self.make_download_metadata)
        self.layout.addWidget(self.downloadMetadataButton)

        # Table initialization
        self.table_init()

        self.applyButton = QPushButton(names['Apply changes'], self)
        self.applyButton.clicked.connect(self.apply_metadata)
        self.layout.addWidget(self.applyButton)

        self.aboutButton = QPushButton(names['About'], self)
        self.aboutButton.clicked.connect(self.about)
        self.layout.addWidget(self.aboutButton)

        self.search_space.setFocus()

        self.last_selected = None
        self.init_auto_table_update()

        if DEBUG:
            self.search_space.setText('b1e5b01d-c434-40fd-8ab7-f264da6c0989')
            self.searchExecutionButton.click()
            self.downloadMetadataButton.click()

    # Basic window configurations
    def window_init(self, icon):
        # Setting Dialog size
        self.resize(600, 500)

        # Setting Dialog layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Setting window title and icon
        self.setWindowTitle(names['Window title'])
        self.setWindowIcon(icon)

    # Results table initialization
    def table_init(self):
        self.table = QTableWidget(6, 2)

        self.table.setHorizontalHeaderLabels([
            names["Current Metadata"],
            names["Metadata from BookBrainz"]
        ])

        self.table.setVerticalHeaderLabels([
            names['Title'],
            names['Author'],
            names['Date published'],
            names['Publisher name'],
            names['Languages'],
            names['Identifiers']
        ])

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.verticalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.table)

    def init_auto_table_update(self):
        self.last_selected = None
        qtimer = QTimer(self)
        qtimer.timeout.connect(self.handle_select_changed)
        qtimer.start(100)

    def make_search(self):
        self.clear_table([1])

        search_value = self.search_space.text()
        try:
            if not is_uuid(search_value):
                query_bbid = self.search_for_book_title(search_value)
                self.search_space.setText(
                    self.search_space.text() +
                    '|{}'.format(query_bbid)
                )
            else:
                query_bbid = search_value
                self.search_for_bbid(query_bbid)


            self.table.setItem(0, 1,
                table_item(self.entity_query_data['default_alias']['name']))
            self.table.repaint()

            self.downloadMetadataButton.setFocus()
            self.searchExecutionButton.setText(names['Search'])
        except:
            dialog = QErrorMessage()
            dialog.setWindowTitle(names['Book not found'])
            dialog.showMessage(
                names['{} was not found in BookBrainz'].format(
                    self.search_space.text()
                )
            )
            dialog.exec_()
            self.clear_to_pre_search_state()

    def search_for_book_title(self, title):
        hits_dialog = QDialog(self)
        hits_dialog.setWindowTitle('Select your book')
        layout = QVBoxLayout()
        hits_dialog.setLayout(layout)

        hits_list = QListWidget()
        hits = self.title_query(title)

        if not hits:
            raise ValueError

        wait_loop = QEventLoop()
        hits_list.itemDoubleClicked.connect(wait_loop.quit)

        def close_handler(event):
            wait_loop.quit()
            event.accept()
        hits_dialog.closeEvent = close_handler

        layout.addWidget(hits_list)
        hits_dialog.show()

        for index, hit in enumerate(hits):
            entity_type = hit['_source']['_type']
            if not entity_type in ['Publication', 'Work', 'Edition']:
                continue

            item = QListWidgetItem(
                    '{}. {}'.format(
                            index+1,
                            hit['_source']['default_alias']['name']
                    ))

            color = QColor()
            if index%2:
                color.setRed(240)
                color.setGreen(255)
                color.setBlue(255)
            else:
                color.setRed(220)
                color.setGreen(255)
                color.setBlue(240)
            item.setBackground(QBrush(color))

            hits_list.addItem(item)
            hits_list.repaint()

        wait_loop.exec_()
        hits_dialog.close()

        index = hits_list.selectedIndexes()[0].row()
        self.entity_query_data = hits[index]['_source']
        return hits[index]['_id']

    def title_query(self, title):
        url = \
            "https://bookbrainz.org/ws/" \
            "search/?q=\{}\"&mode=\"search\""\
            .format(title)

        response = request_get_yolo(url)
        return response['hits']

    def search_for_bbid(self, query_bbid):
        self.searchExecutionButton.setText(names['Searching ...'])
        self.searchExecutionButton.setFocus()
        self.downloadMetadataButton.repaint()

        self.table.setFocus()

        json_short_data = request_get(
            "https://bookbrainz.org/ws/entity/{bbid}/".format(
                bbid=query_bbid
            )
        )

        json_data = request_get(
            json_short_data.get('uri', '')
        )

        self.entity_query_data = json_data

    def handle_select_changed(self):
        rows = self.gui.current_view().selectionModel().selectedRows()

        if rows:
            selected_index = rows[0].row()
        else:
            selected_index = None

        if selected_index != self.last_selected:
            self.last_selected = selected_index
            self.update_metadata_from_book(selected_index)

    def update_metadata_from_book(self, book_index):
        if book_index is not None:
            book =\
                self.gui.library_view.model().db.get_metadata(book_index)
        else:
            book = EmptyBook()

        self.table.setItem(0, 0, table_item(book.title))
        self.table.setItem(1, 0, table_item(book.authors))
        self.table.setItem(2, 0, table_item(book.pubdate))
        self.table.setItem(3, 0, table_item(book.publisher))
        self.table.setItem(4, 0, table_item(book.languages))
        self.table.setItem(5, 0, table_item(book.identifiers))
        self.table.repaint()

    def clear_to_pre_search_state(self):
        self.searchExecutionButton.setText(names['Search'])
        self.searchExecutionButton.setFocus()
        self.searchExecutionButton.repaint()
        self.clear_table([1])

    def make_download_metadata(self):
        self.downloadMetadataButton.setText(names['Downloading metadata...'])
        self.downloadMetadataButton.repaint()
        self.downloadMetadataButton.setFocus()
        try:
            self.download_metadata()
            self.downloadMetadataButton.setText(names['Download data from BB'])
            self.downloadMetadataButton.repaint()
            self.search_space.setText("")
            self.applyButton.setFocus()
        except:
            dialog = QErrorMessage()
            dialog.setWindowTitle(names['Failed'])
            dialog.showMessage(
                names['Downloading metadata from BookBrainz failed']
            )
            dialog.exec_()
            self.searchExecutionButton.setFocus()
            self.clear_table([1])
            self.search_space.clear()

    def download_metadata(self):
        self.fetch_title_from_bb()
        self.fetch_author_from_bb()
        self.fetch_release_date_from_bb()
        self.fetch_publisher_from_bb()
        self.fetch_language_from_bb()
        self.fetch_identifiers_from_bb()

    def fetch_title_from_bb(self):
        title = self.entity_query_data.get('default_alias', {}).get('name', '')
        self.table.setItem(0, 1, table_item(title))
        self.table.repaint()

    def fetch_author_from_bb(self):
        relationships_uri = self.entity_query_data.get('relationships_uri', '')
        if not relationships_uri:
            return
        json_data = \
            request_get_yolo(relationships_uri)
        author = self.get_author_name_from_relationships(json_data)
        self.table.setItem(1, 1, table_item(author))
        self.table.repaint()

    def get_author_name_from_relationships(self, json_data):
        author_uri = self.get_author_uri_from_relationships(json_data)
        if author_uri:
            author_json = request_get_yolo(author_uri)
            return author_json.get('default_alias', {}).get('name', None)
        else:
            return ''

    def get_author_uri_from_relationships(self, json_data):
        for relationship in json_data.get('objects', []):
            if relationship\
                    .get('relationship_type', {})\
                    .get('label', '') == 'Authored':
                for entity in relationship.get('entities', []):
                    if entity.get('position', 2) == 0:
                        author_uri = \
                            entity.get('entity', {}).get('uri', None)
                        if author_uri:
                            return author_uri
        return None

    def fetch_release_date_from_bb(self):
        release_date = self.entity_query_data.get('release_date', '')
        self.table.setItem(2, 1, table_item(release_date))
        self.table.repaint()

    def fetch_publisher_from_bb(self):
        publisher_uri = self.entity_query_data.get('publisher_uri', '')
        publisher_data = request_get_yolo(publisher_uri)
        publisher_name = \
            publisher_data.get('default_alias', {}).get('name', '')

        self.table.setItem(3, 1, table_item(publisher_name))
        self.table.repaint()

    def fetch_language_from_bb(self):
        language_name = \
            self.entity_query_data.get('language', {}).get('name', '')
        self.table.setItem(4, 1, table_item(language_name))
        self.table.repaint()

    def fetch_identifiers_from_bb(self):
        identifiers_uri = self.entity_query_data.get('identifiers_uri', '')
        identifiers_data = request_get_yolo(identifiers_uri)
        identifiers = []

        for identifier in identifiers_data.get('objects', []):
            identifier_type_label = \
                identifier.get('identifier_type', {}).get('label', '')
            identifier_value = identifier.get('value', '')

            identifiers.append(
                "{label}: {value}".format(
                    label=identifier_type_label,
                    value=identifier_value
                )
            )

        self.table.setItem(5, 1, table_item(identifiers))
        self.table.repaint()

    def apply_metadata(self):
        """ Apply fetched metadata to the selected book
        :return: None
        """
        book_id = self.get_selected_book_id()

        for attr in self.entity_attributes_order:
            value = self.get_attribute_value_from_column(attr, 1)

            self.db.new_api.set_field(
                attr,
                {book_id: value}
            )

        self.gui.iactions['Edit Metadata']\
            .refresh_books_after_metadata_edit({book_id})
        self.search_space.setFocus()
        self.search_space.clear()
        self.searchExecutionButton.setFocus()
        self.clear_table([1])

        dialog = QMessageBox()
        dialog.setWindowTitle(names['Successfully applied'])
        dialog.setIconPixmap(QPixmap('images/done_icon.png'))
        dialog.setText(
            names['Metadata was successfully applied to selected book.']
        )
        dialog.exec_()
        self.clear_to_pre_search_state()
        self.last_selected = None
        self.handle_select_changed()

    def get_attribute_value_from_column(self, attribute, column):
        attributes = ['title', 'authors', 'pubdate',
                      'publisher', 'languages', 'identifiers']
        return self.table.item(attributes.index(attribute), column).text()

    def get_selected_book_id(self):
        rows = self.gui.current_view().selectionModel().selectedRows()
        if not rows:
            return None
        else:
            return self.gui.library_view.model().id(rows[0])

    def config(self):
        self.do_user_config(parent=self)
        # Apply the changes
        self.label.setText(names['hello_world_msg'])

    def clear_table(self, columns_range=range(2)):
        for i in range(6):
            for j in columns_range:
                self.table.setItem(i, j, table_item(""))
        self.table.repaint()

    def about(self):
        text = get_resources('about.txt')
        QMessageBox.about(
                self, 'About CaliBBre', text.decode('utf-8')
        )


def request_get(url):
    """Returns json data obtained from the provided url

    :param url: Url to get the data from
    :return(dict): JSON formatted data
    """
    response = urllib2.urlopen(url)
    assert(response.getcode() == 200)
    data = json.load(response)
    return data


def request_get_yolo(url):
    """Version of request_get that catches all exceptions
    so it can be used anywhere without any try ... except's

    :param url: Url to get the data from
    :return: JSON formatted data
    """
    if not url:
        return {}

    try:
        data = request_get(url)
    except:
        return {}

    return data


def table_item(value):
    """ Creates QTableWidgetItem with the provided value

    :param value: value to fill the table_item with
    :return:
    """
    if type(value) == list:
        text = ''
        for i, list_value in enumerate(value):
            text = text + list_value
            if i < len(value):
                text = text + ', '
    else:
        text = str(value)
    item = QTableWidgetItem()
    item.setText(text)

    return item


class EmptyBook:
    title = ''
    authors = ''
    pubdate = ''
    publisher = ''
    languages = ''
    identifiers = ''


def is_uuid(uuid_string):
    try:
        val = uuid.UUID(uuid_string, version=4)
    except ValueError:
        return False

    return val.hex == uuid_string