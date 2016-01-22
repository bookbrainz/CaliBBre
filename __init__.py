#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
# noinspection PyUnresolvedReferences,PyUnresolvedReferences,
# PyUnresolvedReferences
from calibre.customize import InterfaceActionBase

__license__ = 'GPL v3'
__copyright__ = '2015 Stanislaw Szczesniak'
__docformat__ = 'restructuredtext en'


class CalibreBookBrainzInit(InterfaceActionBase):
    name = 'CaliBBre'
    description = 'Plugin for Calibre that allows you to query BookBrainz database using BBID'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Stanislaw Szczesniak'
    version = (0, 0, 1)
    minimum_calibre_version = (0, 0, 0)

    actual_plugin = 'calibre_plugins.CaliBBre.ui:Interface'

    # noinspection PyMethodMayBeStatic
    def is_customizable(self):
        return False
