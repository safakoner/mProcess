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
## @file    mProcess/exceptionLib.py @brief [ FILE   ] - Exceptions.
## @package mProcess.exceptionLib    @brief [ MODULE ] - Exceptions.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ EXCEPTION CLASS ] - GUI error.
class GUIError(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - Container error.
class ContainerError(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - Process error.
class ProcessError(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - Dependency error.
class DependencyError(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - Data file does not exist error.
class DataFileDoesNotExist(Exception):

    pass
