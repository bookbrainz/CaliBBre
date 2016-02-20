#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
from PyQt5.Qt import QWidget, QHBoxLayout, QLabel, QLineEdit
from calibre.utils.config import JSONConfig

__license__ = 'GPL v2+'
__copyright__ = '2015 Stanislaw Szczesniak'
__docformat__ = 'restructuredtext en'

names = JSONConfig('plugins/CaliBBre')

# Set defaults
names.defaults['Enter title or BookBrainz ID'] = 'Enter title or BookBrainz ID'
names.defaults['Search'] = 'Search'
names.defaults['Download data from BB'] = 'Download metadata from BookBrainz'
names.defaults['Apply changes'] = 'Apply changes'
names.defaults['About'] = 'About'
names.defaults['Window title'] = 'CaliBBre - BBID search_for_bbid'
names.defaults['Current Metadata'] = 'Old metadata'
names.defaults["Metadata from BookBrainz"] = 'Metadata from BookBrainz'
names.defaults['Author'] = 'Author'
names.defaults['Title'] = 'Title'
names.defaults['Languages'] = 'Languages'
names.defaults['Publisher name'] = 'Publisher name'
names.defaults['Date published'] = 'Date published'
names.defaults['Identifiers'] = 'Identifiers'
names.defaults['Searching ...'] = 'Searching...'
names.defaults['Downloading metadata...'] = 'Downloading metadata...'
names.defaults['Failed'] = 'Failed'
names.defaults['Book not found'] = 'Book not found'
names.defaults['{} was not found in BookBrainz'] = \
    '{} was not found in BookBrainz'
names.defaults['Downloading metadata from BookBrainz failed'] = \
    'Downloading metadata from BookBrainz failed'
names.defaults['Successfully applied'] = 'Successfully applied'
names.defaults['Metadata was successfully applied to selected book.'] = \
    'Metadata was successfully applied to selected book.'