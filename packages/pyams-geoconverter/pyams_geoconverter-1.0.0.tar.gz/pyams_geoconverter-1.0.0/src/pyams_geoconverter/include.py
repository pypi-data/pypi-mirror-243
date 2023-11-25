#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS GeoConverter.include module

This module is used for Pyramid integration
"""

import re
import os.path

import pyams_geoconverter


__docformat__ = 'restructuredtext'

from pyams_geoconverter.interfaces import REST_CONVERTER_ROUTE


def include_package(config):
    """Pyramid package include"""

    # add translations
    config.add_translation_dirs('pyams_geoconverter:locales')

    config.add_route(REST_CONVERTER_ROUTE,
                     config.registry.settings.get('pyams_geoconverter.rest_converter_route',
                                                  '/api/geoconverter/rest'))

    config.scan()
