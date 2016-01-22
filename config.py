#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
from PyQt5.Qt import QWidget, QHBoxLayout, QLabel, QLineEdit
from calibre.utils.config import JSONConfig

__license__ = 'GPL v3'
__copyright__ = '2015 Stanislaw Szczesniak'
__docformat__ = 'restructuredtext en'

prefs = JSONConfig('plugins/CaliBBre')

# Set defaults
prefs.defaults['enterbbid'] = 'Enter your BBID here'
prefs.defaults['searchandfetch'] = 'Search'
prefs.defaults['dmetbb'] = 'Download metadata from BookBrainz'
prefs.defaults['apply_changes'] = 'Apply changes'
prefs.defaults['about'] = 'About'
prefs.defaults['window_title'] = 'CaliBBre - BBID search'
prefs.defaults['Current Metadata'] = 'Old metadata'
prefs.defaults["Metadata from BookBrainz"] = 'Metadata from BookBrainz'
prefs.defaults['Author'] = 'Author'
prefs.defaults['Title'] = 'Title'
prefs.defaults['Languages'] = 'Languages'
prefs.defaults['Publisher name'] = 'Publisher name'
prefs.defaults['Date published'] = 'Date published'
prefs.defaults['Identifiers'] = 'Identifiers'
prefs.defaults['Searching ...'] = 'Searching...'
prefs.defaults['Downloading metadata...'] = 'Downloading metadata...'
