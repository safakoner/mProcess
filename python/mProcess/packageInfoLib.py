#
# Copyright 2020 Safak Oner.
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @package mProcess                   @brief [ PACKAGE   ] - Abstract classes for processes and their dependencies.
## @dir     mProcess/python            @brief [ DIRECTORY ] - Python path.
## @dir     mProcess/python/mProcess   @brief [ DIRECTORY ] - Python package.
## @file    mProcess/packageInfoLib.py @brief [ FILE      ] - Package info module.
## @package mProcess.packageInfoLib    @brief [ MODULE    ] - Package info module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
## [ str ] - Name of the package.
NAME                = 'mProcess'

## [ str ] - Version of the package.
VERSION             = '1.0.0'

## [ str ] - Description about the package.
DESCRIPTION         = 'Abstract classes for processes and their dependencies.'

## [ list of str ] - Keywords to find this package.
KEYWORDS            = ['container', 'process', 'dependency']

## [ list of str ] - Platforms which this package meant to be used on.
PLATFORMS           = ['Linux', 'Darwin', 'Windows']

## [ list of dict ] - Documentations about the package, keys of dict instances are: title, url.
DOCUMENTS           = []

## [ list of str ] - Applications which this package meant to be initialized for.
APPLICATIONS        = ['all']

## [ list of str ] - Python versions supported by this package.
PYTHON_VERSIONS     = ['2', '3']

## [ bool ] - Whether this package is active (in use).
IS_ACTIVE           = True

## [ bool ] - Whether this package is external (third party).
IS_EXTERNAL         = False

## [ list of str ] - E-mail addresses of the developers.
DEVELOPERS          = ['safak@safakoner.com']

## [ list of str ] - Dependent packages.
DEPENDENT_PACKAGES  = ['mCore',
                       'mFileSystem'
                       ]

## [ list of str ] - Python packages contained by this package.
PYTHON_PACKAGES     = ['mProcess']