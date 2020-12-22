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
## @file    mProcess/dataLib.py @brief [ FILE   ] - Data module.
## @package mProcess.dataLib    @brief [ MODULE ] - Data module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import mCore.enumAbs


#
# ----------------------------------------------------------------------------------------------------
# ENUM CLASSES
# ----------------------------------------------------------------------------------------------------
#
## @brief [ ENUM CLASS ] - Run level.
class RunLevel(mCore.enumAbs.Enum):

    ## [ int ] - Run pre dependencies, process and post dependencies.
    kAll                            = 0

    ## [ int ] - Run only pre dependencies.
    kPreDependenciesOnly            = 1

    ## [ int ] - Run only post dependencies.
    kPostDependenciesOnly           = 2

    ## [ int ] - Run only pre and post dependencies.
    kPreAndPostDependenciesOnly     = 3

    ## [ int ] - Run process only without pre and post dependencies.
    kProcessOnly                    = 4

    ## [ int ] - Run process and post dependencies only.
    kProcessAndPostDependenciesOnly = 5

#
## @brief [ ENUM CLASS ] - Run mode.
class RunMode(mCore.enumAbs.Enum):

    ## [ int ] - Terminal.
    kTerminal                   = 0

    ## [ int ] - Parent terminal, Maya batch, etc.
    kParentTerminal             = 1

    ## [ int ] - GUI.
    kGUI                        = 2

#
## @brief [ ENUM CLASS ] - Display messages.
class DisplayMessage(mCore.enumAbs.Enum):

    ## [ int ] - Do not display any messages.
    kNone                       = 0

    ## [ int ] - Display all messages.
    kAll                        = 1

    ## [ int ] - Display only info messages.
    kInfo                       = 2

    ## [ int ] - Display only success messages.
    kSuccess                    = 3

    ## [ int ] - Display only warning messages.
    kWarning                    = 4

    ## [ int ] - Display only failure messages.
    kFailure                    = 5

#
## @brief [ CLASS ] - Data class used by all the classes.
class Data(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param runMode                      [ enum        | mProcess.dataLib.RunMode.kTerminal   | in  ] - Run mode from mProcess.dataLib.RunMode enum class.
    #  @param runLevel                     [ enum        | mProcess.dataLib.RunLevel.kAll       | in  ] - Run level from mProcess.dataLib.RunLevel enum class.
    #  @param processesToRun               [ list of str | []                                   | in  ] - Processes to run.
    #  @param processesToIgnore            [ list of str | []                                   | in  ] - Processes to ignore.
    #  @param ignoreFailedPreDependencies  [ bool        | False                                | in  ] - Whether to ignore failed pre dependencies.
    #  @param ignoreFailedPostDependencies [ bool        | False                                | in  ] - Whether to ignore failed post dependencies.
    #  @param raiseExceptions              [ bool        | False                                | in  ] - Raise exceptions.
    #  @param displayMessages              [ enum        | mProcess.dataLib.DisplayMessage.kAll | in  ] - Display messages from mProcess.dataLib.DisplayMessage enum class.
    #  @param userDescription              [ str         | None                                 | in  ] - User description.
    #  @param ignoreDescription            [ str         | None                                 | in  ] - Ignore description.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self,
                 runMode=RunMode.kTerminal,
                 runLevel=RunLevel.kAll,
                 processesToRun=[],
                 processesToIgnore=[],
                 ignoreFailedPreDependencies=False,
                 ignoreFailedPostDependencies=False,
                 raiseExceptions=False,
                 displayMessages=DisplayMessage.kAll,
                 userDescription=None,
                 ignoreDescription=None):

        ## [ enum ] - Run mode from mProcess.dataLib.RunMode enum class.
        self._runMode                       = runMode

        ## [ enum ] - Run level from mProcess.dataLib.RunLevel enum class.
        self._runLevel                      = runLevel

        #

        ## [ list of str ] - Processes to run.
        self._processesToRun                = processesToRun

        ## [ list of str ] - Processes to ignore.
        self._processesToIgnore             = processesToIgnore

        #

        ## [ bool ] - Ignore failed pre dependencies
        self._ignoreFailedPreDependencies   = ignoreFailedPreDependencies

        ## [ bool ] - Ignore failed post dependencies
        self._ignoreFailedPostDependencies  = ignoreFailedPostDependencies

        #

        ## [ bool ] - Whether to raise exceptions.
        self._raiseExceptions               = raiseExceptions

        ## [ enum ] - Display messages from mProcess.dataLib.DisplayMessage enum class.
        self._displayMessages               = displayMessages

        #

        ## [ str ] - User description.
        self._userDescription               = userDescription

        ## [ str ] - Ignore description.
        self._ignoreDescription             = ignoreDescription

        #

        ## [ dict ] - Custom data used by other classes.
        self._data                          = {}

    #
    ## @brief Get item from data member.
    #
    #  @param key [ str | None | in  ] - Key.
    #
    #  @exception N/A
    #
    #  @return variant - Value.
    def __getitem__(self, key):

        return self._data[key]

    #
    ## @brief Set item of data member.
    #
    #  @param key   [ str | None | in  ] - Key.
    #  @param value [ str | None | in  ] - Value.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __setitem__(self, key, value):

        self._data[key] = value

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    ## @name PROPERTIES

    ## @{
    #
    ## @brief Run mode.
    #
    #  @exception N/A
    #
    #  @return enum - Result from mProcess.dataLib.RunMode enum class.
    def runMode(self):

        return self._runMode

    #
    ## @brief Run level.
    #
    #  @exception N/A
    #
    #  @return enum - Result from mProcess.dataLib.RunLevel enum class.
    def runLevel(self):

        return self._runLevel

    #
    ## @brief Processes to run.
    #
    #  @exception N/A
    #
    #  @return list of str - Processes.
    def processesToRun(self):

        return self._processesToRun

    #
    ## @brief Processes to ignore.
    #
    #  @exception N/A
    #
    #  @return list of str - Processes.
    def processesToIgnore(self):

        return self._processesToIgnore

    #
    ## @brief Whether to ignore failed pre dependencies.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def ignoreFailedPreDependencies(self):

        return self._ignoreFailedPreDependencies

    #
    ## @brief Whether to ignore failed post dependencies.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def ignoreFailedPostDependencies(self):

        return self._ignoreFailedPostDependencies

    #
    ## @brief Raise exceptions.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def raiseExceptions(self):

        return self._raiseExceptions

    #
    ## @brief Display messages.
    #
    #  @exception N/A
    #
    #  @return enum - Result from mProcess.dataLib.DisplayMessage enum class.
    def displayMessages(self):

        return self._displayMessages

    #
    ## @brief User description.
    #
    #  @exception N/A
    #
    #  @return str - User description.
    def userDescription(self):

        return self._userDescription

    #
    ## @brief Set user description.
    #
    #  @param userDescription [ str | None | in  ] - User description.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setUserDescription(self, userDescription):

        self._userDescription = userDescription

    #
    ## @brief Ignore description.
    #
    #  @exception N/A
    #
    #  @return str - Ignore description.
    def ignoreDescription(self):

        return self._ignoreDescription

    #
    ## @brief Set ignore description.
    #
    #  @param ignoreDescription [ str | None | in  ] - Ignore description.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setIgnoreDescription(self, ignoreDescription):

        self._ignoreDescription = ignoreDescription

    #
    ## @brief Data.
    #
    #  @exception N/A
    #
    #  @return dict - Data.
    def data(self):

        return self._data

    #
    ## @}
