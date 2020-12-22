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
## @file    mProcess/dependencyAbs.py @brief [ FILE   ] - Abstract dependency module.
## @package mProcess.dependencyAbs    @brief [ MODULE ] - Abstract dependency module.


# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
from    Qt import QtCore

import  mProcess.dataLib
import  mProcess.exceptionLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ ABSTRACT CLASS ] - Abstract dependency class.
class Dependency(QtCore.QObject):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ int ] - Message padding.
    MESSAGE_PADDING       = 52

    #
    # ------------------------------------------------------------------------------------------------
    # SIGNALS
    # ------------------------------------------------------------------------------------------------
    ## [ Signal ] - Signal emitted by _setInfo method.
    signalInfoOccurred    = QtCore.Signal(str)

    ## [ Signal ] - Signal emitted by _setSuccess method.
    signalSuccessOccurred = QtCore.Signal(str)

    ## [ Signal ] - Signal emitted by _setWarning method.
    signalWarningOccurred = QtCore.Signal(str)

    ## [ Signal ] - Signal emitted by _setFailure method.
    signalFailureOccurred = QtCore.Signal(str)

    ## [ Signal ] - Signal emitted by _setInfo and _setFailure methods
    signalResultOccurred  = QtCore.Signal(bool)

    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param parent [ QObject               | None | in  ] - Parent.
    #  @param data   [ mProcess.dataLib.Data | None | in  ] - Data.
    #  @param kwargs [ dict                  | None | in  ] - Keyword arguments.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, parent=None, data=None, **kwargs):

        QtCore.QObject.__dict__['__init__'](self, parent)

        #

        ## [ mProcess.dataLib.Data ] - Data.
        self._data = data

        if not self._data:
            self._data = mProcess.dataLib.Data()

        ## [ dict ] - Keyword arguments.
        self._kwargs                            = kwargs

        #

        ## [ str ] - Name of the dependency.
        self._name                              = None

        ## [ str ] - Description of the dependency.
        self._description                       = None

        ## [ bool ] - Whether this dependency is currently active.
        self._isActive                          = True

        #

        ## [ bool ] - Whether this dependency has fix.
        self._hasFix                            = False

        ## [ bool ] - Whether auto fix should run automatically.
        self._runFixAutomatically               = False

        #

        ## [ bool ] - Whether this dependency has action.
        self._hasAction                         = False

        #

        ## [ bool ] - Whether this dependency is ignorable.
        self._isIgnorable                       = False

        ## [ bool ] - Whether this dependency is ignored.
        self._isIgnored                         = False

        #

        ## [ bool ] - Whether this dependency requires description when ignored.
        self._requiresDescriptionWhenIgnored    = True

        ## [ str ] - The last failure message that was recorded for this dependency.
        self._failureMessage                    = None

        #

        ## [ bool ] - Whether this dependency is executed.
        self._isExecuted                        = False

        ## [ bool ] - Whether this dependency succeeded after execution.
        self._isSucceeded                       = False

        #

        self._editData()

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief This method is invoked by the constructor.
    #
    #  Overwrite this method to customize _data member.
    #  @warning Do not delete anything in _data member.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _editData(self):

        pass

    #
    # MESSAGE RELATED METHODS
    #
    ## @brief Set info.
    #
    #  Method emits signalInfoOccurred signal.
    #
    #  @param infoMessage [ str | None | in  ] - Info message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _setInfo(self, infoMessage):

        self.signalInfoOccurred.emit('{} {} {}'.format(self._name.ljust(self.MESSAGE_PADDING), ':', infoMessage))

    #
    ## @brief Set success.
    #
    #  Method emits signalSuccessOccurred signal.
    #  Method emits signalResultOccurred signal with True argument.
    #
    #  @param successMessage [ str | 'OK' | in  ] - Success message.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _setSuccess(self, successMessage='OK'):

        self._isExecuted     = True
        self._isSucceeded    = True
        self._failureMessage = None

        self.signalSuccessOccurred.emit('{} {} {}'.format(self._name.ljust(self.MESSAGE_PADDING), ':', successMessage))
        self.signalResultOccurred.emit(True)

        return True

    #
    ## @brief Set warning.
    #
    #  Method emits signalWarningOccurred signal.
    #
    #  @param warningMessage [ str | None | in  ] - Warning message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _setWarning(self, warningMessage):

        self.signalWarningOccurred.emit('{} {} {}'.format(self._name.ljust(self.MESSAGE_PADDING), ':', warningMessage))

    #
    ## @brief Set failure.
    #
    #  Method emits signalFailureOccurred signal.
    #
    #  @param failureMessage [ str | None | in  ] - Failure message.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _setFailure(self, failureMessage=None):

        self._isExecuted     = True
        self._isSucceeded    = False
        if failureMessage:
            self._failureMessage = failureMessage

        if self._data.runLevel() == mProcess.dataLib.RunLevel.kAll or \
            self._data.runLevel() == mProcess.dataLib.RunLevel.kPreDependenciesOnly or \
            self._data.runLevel() == mProcess.dataLib.RunLevel.kPostDependenciesOnly or \
            self._data.runLevel() == mProcess.dataLib.RunLevel.kPreAndPostDependenciesOnly:

            if failureMessage:
                self.signalFailureOccurred.emit('{} {} {}'.format(self._name.ljust(self.MESSAGE_PADDING), ':', failureMessage))

        self.signalResultOccurred.emit(False)

        return False

    #
    # RUN RELATED METHODS
    #
    #
    ## @brief Run the dependency for terminal.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return bool - Result.
    def _runForTerminal(self):

        raise NotImplementedError('Dependency._runForTerminal method has not been implemented.')

    #
    ## @brief Run the dependency for parent terminal.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return bool - Result.
    def _runForParentTerminal(self):

        raise NotImplementedError('Dependency._runForParentTerminal method has not been implemented.')

    #
    ## @brief Run the dependency for GUI.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return bool - Result.
    def _runForGUI(self):

        raise NotImplementedError('Dependency._runForGUI method has not been implemented.')

    #
    ## @brief Run the fix for terminal.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _runFixForTerminal(self):

        return True

    #
    ## @brief Run the fix for parent terminal.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _runFixForParentTerminal(self):

        return True

    #
    ## @brief Run the fix for GUI.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _runFixForGUI(self):

        return True

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    ## @name PROPERTIES

    ## @{
    #
    ## @brief Data.
    #
    #  @exception N/A
    #
    #  @return mProcess.dataLib.Data - Data.
    def data(self):

        return self._data

    #
    ## @brief Keyword arguments.
    #
    #  @exception N/A
    #
    #  @return dict - Keyword arguments.
    def kwargs(self):

        return self._kwargs

    #
    ## @brief Name of the dependency.
    #
    #  @exception N/A
    #
    #  @return str - Name.
    def name(self):

        return self._name

    #
    ## @brief Description about the dependency.
    #
    #  @exception N/A
    #
    #  @return str - Description.
    def description(self):

        return self._description

    #
    ## @brief Whether this dependency is active.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def isActive(self):

        return self._isActive

    #
    ## @brief Whether this dependency has fix.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def hasFix(self):

        return self._hasFix

    #
    ## @brief Whether auto fix should run automatically.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def runFixAutomatically(self):

        return self._runFixAutomatically

    #
    ## @brief Whether this dependency has action.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def hasAction(self):

        return self._hasAction

    #
    ## @brief Whether this dependency is ignorable.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def isIgnorable(self):

        return self._isIgnorable

    #
    ## @brief Whether this dependency is ignored.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def isIgnored(self):

        return self._isIgnored

    #
    ## @brief Whether this dependency requires description when ignored.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def requiresDescriptionWhenIgnored(self):

        return self._requiresDescriptionWhenIgnored

    #
    ## @brief The last failure message that was recorded for this dependency.
    #
    #  @exception N/A
    #
    #  @return str - Message.
    def failureMessage(self):

        return self._failureMessage

    #
    ## @brief Whether this dependency is executed.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def isExecuted(self):

        return self._isExecuted

    #
    ## @brief Whether this dependency succeeded after execution.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def isSucceeded(self):

        return self._isSucceeded

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Display auto ignored message.
    #
    #  Ignorable dependencies could be ignored by the container if they fail. In such case, this method will be
    #  invoked to notify the user.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayAutoIgnoredMessage(self):

        self._setInfo('This dependency has been automatically ignored by the container.')

    #
    ## @brief Reset this dependency.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def reset(self):

        self._isExecuted     = False
        self._isSucceeded    = False
        self._failureMessage = None

    #
    ## @brief Run the dependency.
    #
    #  @exception mProcess.exceptionLib.DependencyError - No run method is available for this run mode.
    #
    #  @return bool - Result.
    def run(self):

        runMethodOrder = []

        if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
            runMethodOrder = ['_runForTerminal',
                              '_runForParentTerminal',
                              '_runForGUI']

        elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
            runMethodOrder = ['_runForParentTerminal',
                              '_runForTerminal',
                              '_runForGUI']

        elif self._data.runMode() == mProcess.dataLib.RunMode.kGUI:
            runMethodOrder = ['_runForGUI',
                              '_runForTerminal',
                              '_runParentTerminal']

        for method in runMethodOrder:

            if hasattr(self, method):

                self._isExecuted = True

                try:
                    return getattr(self, method)()
                except NotImplementedError as e:
                    continue

        raise mProcess.exceptionLib.DependencyError('No run method is available for this run mode.')


    #
    ## @brief Run fix.
    #
    #  @exception mProcess.exceptionLib.DependencyError - No run fix method is available for this run mode.
    #
    #  @return bool - Result.
    def runFix(self):

        if not self._hasFix:
            return False

        methodOrder = []

        if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
            methodOrder = ['_runFixForTerminal',
                           '_runFixForParentTerminal',
                           '_runFixForGUI']

        elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
            methodOrder = ['_runFixForParentTerminal',
                           '_runFixForTerminal',
                           '_runFixForGUI']

        elif self._data.runMode() == mProcess.dataLib.RunMode.kGUI:
            methodOrder = ['_runFixForGUI',
                           '_runFixForTerminal',
                           '_runFixParentTerminal']

        for method in methodOrder:

            if hasattr(self, method):

                try:
                    return getattr(self, method)()
                except NotImplementedError as e:
                    continue

        raise mProcess.exceptionLib.DependencyError('No run fix method is available for this run mode.')

    #
    ## @brief Run action.
    #
    #  @exception NotImplementedError - If this method is not implemented in child class when _hasAction True.
    #
    #  @return None - None.
    def runAction(self):

        if self._hasAction:
            raise NotImplementedError('{}: mProcess.dependencyAbs.Dependency.runAction method must be implemented in the child class when mProcess.dependencyAbs.Dependency._hasAction is True.'.format(self._name))

    #
    ## @brief Whether action is runnable for given condition.
    #
    #  This method is provided so GUI can decide whether to show the run action button.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def isActionRunnable(self):

        return False

    #
    ## @brief Whether this dependency should be initialized.
    #
    #  Implement this method to prevent child class instances from being initialized
    #  by raising mProcess.exceptionLib.DependencyError exception.
    #  Method must return True explicitly otherwise.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def shouldInitialize(self):

        return True