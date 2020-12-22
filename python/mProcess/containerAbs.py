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
## @file    mProcess/containerAbs.py @brief [ FILE   ] - Abstract container module.
## @package mProcess.containerAbs    @brief [ MODULE ] - Abstract container module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  importlib
import  inspect
import  argparse

from    Qt import QtCore

import  mCore.dateTimeLib
import  mCore.displayLib

import  mFileSystem.jsonFileLib

import  mProcess.dataLib
import  mProcess.exceptionLib
import  mProcess.processAbs



#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ ABSTRACT CLASS ] - Abstract container class.
class Container(QtCore.QObject):
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

    ## [ Signal ] - Signal should be used when a header needs to be displayed.
    signalDisplayHeader   = QtCore.Signal(str)

    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param parent   [ QObject               | None | in  ] - Parent.
    #  @param data     [ mProcess.dataLib.Data | None | in  ] - Data.
    #  @param dataFile [ str                   | None | in  ] - Absolute path of data file (JSON).
    #  @param kwargs   [ dict                  | None | in  ] - Keyword arguments.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, parent=None, data=None, dataFile=None, **kwargs):

        QtCore.QObject.__dict__['__init__'](self, parent)

        #

        ## [ mProcess.dataLib.Data ] - Data.
        self._data                      = data

        if not self._data:
            self._data = mProcess.dataLib.Data()

        ## [ mFileSystem.jsonFileLib.JSONFile ] - Data file.
        self._dataFile                  = mFileSystem.jsonFileLib.JSONFile()

        if dataFile:
            self.setDataFile(dataFile)

        ## [ dict ] - Keyword arguments.
        self._kwargs                    = kwargs

        ## [ list of mProcess.processAbs.Process ] - Classes that inherit mProcess.processAbs.Process abstract class.
        self._processList               = []

        ## [ bool ] - Whether the instance of this class has been initialized.
        self._hasInitialized            = False

        ## [ bool ] - Whether instance of process classes have been initialized.
        self._haveProcessesInitialized  = False

        #

        if not hasattr(self, '_name'):
            ## [ str ] - Name.
            self._name                  = None

        if not hasattr(self, '_description'):
            ## [ str ] - Description.
            self._description           = None

        if not hasattr(self, '_processListModule'):
            ## [ str ] - Process list module.
            self._processListModule     = None

        #

        if not hasattr(self, '_requiresUserDescription'):
            ## [ str ] - Whether this container requires user description to run.
            self._requiresUserDescription = True

        #

        if self.parent():
            pass
        else:
            self.signalDisplayHeader.connect(self.__displayHeader)
            self.signalInfoOccurred.connect(self.__containerInfoOccurred)
            self.signalSuccessOccurred.connect(self.__containerSuccessOccurred)
            self.signalWarningOccurred.connect(self.__containerWarningOccurred)
            self.signalFailureOccurred.connect(self.__containerFailureOccurred)

        self._editData()

        try:
            self._hasInitialized = self.shouldInitialize()
            if not self._hasInitialized:
                self._setFailure('"{}" container can not be initialized, reason is not stated by the developers.'.format(self._name))
            else:
                self._initializeProcesses()
        except Exception as error:
            if self._data.raiseExceptions():
                raise
            elif self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or \
                 self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kFailure:
                self._setFailure('"{}" container can not be initialized: {}'.format(self._name, str(error)))

    #
    ## @brief String representation.
    #
    #  @exception N/A
    #
    #  @return str - String representation.
    def __str__(self):

        return self.asStr()

    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    # HEADER RELATED METHODS
    #
    ## @brief Get container header for given string.
    #
    #  @param header [ str | None | in  ] - Header.
    #
    #  @exception N/A
    #
    #  @return str - Header.
    def __getContainerHeader(self, header):

        headerStr = ''

        if self._data.runMode() == mProcess.dataLib.RunMode.kGUI:
            pass

        elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
            headerStr  = '\n{}'.format('-' * 104)
            headerStr += '\n{}\n'.format(header)
            headerStr += '{}'.format('-' * 104)

        elif self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
            headerStr  = mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kHeaderLine).format('\n{}'.format('-' * 104))
            headerStr += mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kHeaderText).format('\n{}\n'.format(header))
            headerStr += mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kHeaderLine).format('{}'.format('-' * 104))

        return headerStr

    #
    ## @brief Get process header for given string.
    #
    #  @param header [ str | None | in  ] - Header.
    #
    #  @exception N/A
    #
    #  @return str - Header.
    def __getProcessHeader(self, header):

        headerStr = ''

        if self._data.runMode() == mProcess.dataLib.RunMode.kGUI:
            headerStr  = '{}'.format('-' * 100)
            headerStr += '\n{}\n'.format(header)
            headerStr += '{}'.format('-' * 100)

        elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
            headerStr += '\n    {}\n'.format(header)
            headerStr += '    {}'.format('-' * 100)

        elif self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
            headerStr += mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kHeaderText).format('\n    {}\n'.format(header))
            headerStr += mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kHeaderLine).format('    {}'.format('-' * 100))

        return headerStr

    #
    ## @brief Get dependency header for given string.
    #
    #  @param header [ str | None | in  ] - Header string.
    #
    #  @exception N/A
    #
    #  @return str - Header.
    def __getDependencyHeader(self, header):

        headerStr = ''

        if self._data.runMode() == mProcess.dataLib.RunMode.kGUI:
            headerStr  = '{}'.format('-' * 100)
            headerStr += '\n{}\n'.format(header)
            headerStr += '{}'.format('-' * 100)

        elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
            headerStr += '\n    {}\n'.format(header)
            headerStr += '    {}'.format('-' * 100)

        elif self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
            headerStr += mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kHeaderText).format('\n    {}\n'.format(header))
            headerStr += mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kHeaderLine).format('    {}'.format('-' * 100))

        return headerStr

    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE SLOTS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Slot displays headers.
    #
    #  @param header [ str | None | in  ] - Header needs to be displayed.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __displayHeader(self, header):

        if self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll:

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kHeaderText).format(header), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(header, startNewLine=False)

    #
    # CONTAINER MESSAGE RELATED METHODS
    #
    ## @brief Slot is used when a container info occurred.
    #
    #  @param infoMessage [ str | None | in  ] - Info message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __containerInfoOccurred(self, infoMessage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kInfo) and infoMessage:

            infoMessage = '    {} - INFO    : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), infoMessage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kInfo).format(infoMessage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(infoMessage, startNewLine=False)

    #
    ## @brief Slot is used when a container success occurred.
    #
    #  @param successMassage [ str | None | in  ] - Success message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __containerSuccessOccurred(self, successMassage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kSuccess) and successMassage:

            successMassage = '\n    {} - SUCCESS : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), successMassage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kSuccess).format(successMassage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(successMassage, startNewLine=False)

    #
    ## @brief Slot is used when a container warning occurred.
    #
    #  @param warningMassage [ str | None | in  ] - Warning message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __containerWarningOccurred(self, warningMassage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kWarning) and warningMassage:

            warningMassage = '\n    {} - WARNING : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), warningMassage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kWarning).format(warningMassage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(warningMassage, startNewLine=False)

    #
    ## @brief Slot is used when a container failure occurred.
    #
    #  @param failureMessage [ str | None | in  ] - Error message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __containerFailureOccurred(self, failureMessage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kFailure) and failureMessage:

            failureMessage = '\n    {} - FAILED  : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), failureMessage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kFailure).format(failureMessage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(failureMessage, startNewLine=False)

    #
    # PROCESS MESSAGE RELATED METHODS
    #
    ## @brief Slot is used when a process info occurred.
    #
    #  @param infoMessage [ str | None | in  ] - Info message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __processInfoOccurred(self, infoMessage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kInfo) and infoMessage:

            infoMessage = '    {} - INFO    : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), infoMessage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kInfo).format(infoMessage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(infoMessage, startNewLine=False)

    #
    ## @brief Slot is used when a process success occurred.
    #
    #  @param successMassage [ str | None | in  ] - Success message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __processSuccessOccurred(self, successMassage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kSuccess) and successMassage:

            successMassage = '    {} - SUCCESS : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), successMassage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kSuccess).format(successMassage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(successMassage, startNewLine=False)

    #
    ## @brief Slot is used when a process warning occurred.
    #
    #  @param warningMassage [ str | None | in  ] - Warning message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __processWarningOccurred(self, warningMassage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kWarning) and warningMassage:

            warningMassage = '    {} - WARNING : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), warningMassage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kWarning).format(warningMassage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(warningMassage, startNewLine=False)

    #
    ## @brief Slot is used when a process failure occurred.
    #
    #  @param failureMessage [ str | None | in  ] - Error message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __processFailureOccurred(self, failureMessage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kFailure) and failureMessage:

            failureMessage = '    {} - FAILED  : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), failureMessage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kFailure).format(failureMessage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(failureMessage, startNewLine=False)

    #
    # DEPENDENCY MESSAGE RELATED METHODS
    #
    ## @brief Slot is used when a dependency info occurred.
    #
    #  @param infoMessage [ str | None | in  ] - Info message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __dependencyInfoOccurred(self, infoMessage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kInfo) and infoMessage:

            infoMessage = '    {} - INFO    : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), infoMessage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kInfo).format(infoMessage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(infoMessage, startNewLine=False)

    #
    ## @brief Slot is used when a dependency success occurred.
    #
    #  @param successMassage [ str | None | in  ] - Success message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __dependencySuccessOccurred(self, successMassage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kSuccess) and successMassage:

            successMassage = '    {} - SUCCESS : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), successMassage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kSuccess).format(successMassage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(successMassage, startNewLine=False)

    #
    ## @brief Slot is used when a dependency warning occurred.
    #
    #  @param warningMassage [ str | None | in  ] - Warning message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __dependencyWarningOccurred(self, warningMassage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kWarning) and warningMassage:

            warningMassage = '    {} - WARNING : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), warningMassage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kWarning).format(warningMassage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(warningMassage, startNewLine=False)

    #
    ## @brief Slot is used when a dependency failure occurred.
    #
    #  @param failureMessage [ str | None | in  ] - Error message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __dependencyFailureOccurred(self, failureMessage):

        if (self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or
            self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kFailure) and failureMessage:

            failureMessage = '    {} - FAILED  : {}'.format(mCore.dateTimeLib.getDateTimeStamp(), failureMessage)

            if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
                mCore.displayLib.Display.display(mCore.displayLib.Display.getDisplayColor(mCore.displayLib.ColorName.kFailure).format(failureMessage), startNewLine=False)

            elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                mCore.displayLib.Display.display(failureMessage, startNewLine=False)

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

        self.signalInfoOccurred.emit(infoMessage)

    #
    ## @brief Set success.
    #
    #  Method emits signalSuccessOccurred signal.
    #
    #  @param successMessage [ str | 'OK' | in  ] - Success message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _setSuccess(self, successMessage='OK'):

        self.signalSuccessOccurred.emit(successMessage)

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

        self.signalWarningOccurred.emit(warningMessage)

    #
    ## @brief Set failure.
    #
    #  Method emits signalFailureOccurred signal.
    #
    #  @param failureMessage [ str | None | in  ] - Failure message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _setFailure(self, failureMessage):

        self.signalFailureOccurred.emit(failureMessage)

    #
    # PROCESS INITIALIZATION METHODS
    #
    ## @brief This method is invoked before process classes are initialized.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _beforeProcessClassesInitialized(self):

        pass

    #
    ## @brief This method is invoked process classes are initialized.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _afterProcessClassesInitialized(self):

        pass

    #
    ## @brief This method is invoked before each process class is initialized.
    #
    #  Implement your custom code to decide whether given process class object
    #  should be used. Return False if given classObject shouldn't be used,
    #  return True otherwise.
    #
    #  @warning Method must return True or False explicitly.
    #
    #  @param classObject [ class | None | in  ] - Process class object (not an instance).
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _beforeProcessClassInitialized(self, classObject):

        return True

    #
    ## @brief This method is called after each process class is initialized.
    #
    #  Implement your custom code to decide whether given process class instance
    #  should be used. Return False if given classInstance shouldn't be used,
    #  return True otherwise.
    #
    #  @warning Method must return True or False explicitly.
    #
    #  @param classInstance [ object | None | in  ] - Process class instance.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _afterProcessClassInitialized(self, classInstance):

        return True

    #
    #
    #
    ## @brief Sort processes.
    #
    #  Implement this method to sort the processes (sort _processList list member). This method
    #  will be called after all processes are initialized.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _sortProcesses(self):

        pass

    #
    ## @brief Initialize processes for current run mode.
    #
    #  @exception mProcess.exceptionLib.ContainerError - If no initialization method is available for this run mode.
    #
    #  @return None - None.
    def _initializeProcesses(self):

        initializationMethodOrder = []

        if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
            initializationMethodOrder = ['_initializeProcessesForTerminal',
                                         '_initializeProcessesForParentTerminal',
                                         '_initializeProcessesForGUI']

        elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
            initializationMethodOrder = ['_initializeProcessesForParentTerminal',
                                         '_initializeProcessesForTerminal',
                                         '_initializeProcessesForGUI']

        elif self._data.runMode() == mProcess.dataLib.RunMode.kGUI:
            initializationMethodOrder = ['_initializeProcessesForGUI',
                                         '_initializeProcessesForTerminal',
                                         '_initializeProcessesForParentTerminal']

        for method in initializationMethodOrder:

            if hasattr(self, method):

                try:
                    getattr(self, method)()
                except NotImplementedError as e:
                    continue

                self._sortProcesses()

                self._haveProcessesInitialized = True

                return

        raise mProcess.exceptionLib.ContainerError('No initialization method is available for this run mode.')

    #
    ## @brief Initialize processes for terminal.
    #
    #  This method lists process classes and store them in self._processList member. Process module's
    #  absolute import paths will be retrieved from a module assigned to self._processListModule member
    #  of this class. That module must contain PROCESS_LIST (list) member which should contain all the
    #  process modules as string instances.
    #
    #  Following callback are invoked by this method.
    #
    #  @see mProcess.containerAbs.Container._beforeProcessClassesInitialized
    #  @see mProcess.containerAbs.Container._afterProcessClassesInitialized
    #  @see mProcess.containerAbs.Container._beforeProcessClassInitialized
    #  @see mProcess.containerAbs.Container._afterProcessClassInitialized
    #
    #  @exception mProcess.exceptionLib.ContainerError - If process classes could not be retrieved.
    #
    #  @return None - None.
    def _initializeProcessesForTerminal(self):

        # Check whether process list module is defined
        if not self._processListModule:
            errorMessage = '{} : No process list module defined.'.format(self.__class__.__name__)
            raise mProcess.exceptionLib.ContainerError(errorMessage)

        _processListModule = None
        try:
            # Import process list module
            _processListModule = importlib.import_module(self._processListModule)
        except ImportError as error:
            errorMessage = '{} : Process list module "{}" couldn\'t be imported.'.format(self.__class__.__name__,
                                                                                         self._processListModule)
            raise mProcess.exceptionLib.ContainerError(errorMessage)
        except Exception as error:
            raise

        if not hasattr(_processListModule, 'PROCESS_LIST'):
            # Process list module doesn't have PROCESS_LIST attribute
            errorMessage = '{} : Process list module "{}" doesn\'t have PROCESS_LIST attribute which would list the process classes.'.format(self.__class__.__name__,
                                                                                                                                             self._processListModule)
            raise mProcess.exceptionLib.ContainerError(errorMessage)

        processModuleNameList = getattr(_processListModule, 'PROCESS_LIST')
        if not processModuleNameList:
            # Process module list doesn't have PROCESS_LIST attribute
            errorMessage = '{} : {}.PROCESS_LIST attribute is empty.'.format(_processListModule,
                                                                             self._processListModule)
            raise mProcess.exceptionLib.ContainerError(errorMessage)

        self._beforeProcessClassesInitialized()

        for moduleName in processModuleNameList:

            try:
                _processModule = importlib.import_module(moduleName)
            except ImportError as error:
                errorMessage = '{} - Process "{}" couldn\'t be imported: {}'.format(self._name, moduleName, str(error))
                raise mProcess.exceptionLib.ContainerError(errorMessage)
            except Exception as error:
                raise

            for name, _obj in inspect.getmembers(_processModule):

                if not inspect.isclass(_obj):
                    continue

                if not issubclass(_obj, mProcess.processAbs.Process):
                    continue

                if not self._beforeProcessClassInitialized(_obj):
                    continue

                _processClassInstance = _obj(self, self._data, **self._kwargs)

                if self._data.processesToRun() and not _processClassInstance.name() in self._data.processesToRun():
                    _processClassInstance.deleteLater()
                    continue

                if self._data.processesToIgnore() and _processClassInstance.name() in self._data.processesToIgnore():
                    _processClassInstance.deleteLater()
                    continue

                if not _processClassInstance.isActive():
                    _processClassInstance.deleteLater()
                    continue


                try:
                    if not _processClassInstance.shouldInitialize():
                        _processClassInstance.deleteLater()
                        continue
                except Exception as error:
                    _processClassInstance.deleteLater()
                    if self._data.raiseExceptions():
                        raise
                    else:
                        continue

                if not self._afterProcessClassInitialized(_processClassInstance):
                    _processClassInstance.deleteLater()
                    continue

                if not self.parent():
                    _processClassInstance.signalInfoOccurred.connect(self.__processInfoOccurred)
                    _processClassInstance.signalSuccessOccurred.connect(self.__processSuccessOccurred)
                    _processClassInstance.signalWarningOccurred.connect(self.__processWarningOccurred)
                    _processClassInstance.signalFailureOccurred.connect(self.__processFailureOccurred)

                    preDependencyList = _processClassInstance.preDependencyList()
                    if preDependencyList:
                        for _preDependencyClassInstance in preDependencyList:
                            _preDependencyClassInstance.signalInfoOccurred.connect(self.__dependencyInfoOccurred)
                            _preDependencyClassInstance.signalSuccessOccurred.connect(self.__dependencySuccessOccurred)
                            _preDependencyClassInstance.signalWarningOccurred.connect(self.__dependencyWarningOccurred)
                            _preDependencyClassInstance.signalFailureOccurred.connect(self.__dependencyFailureOccurred)

                    postDependencyList = _processClassInstance.postDependencyList()
                    if postDependencyList:
                        for _postDependencyClassInstance in postDependencyList:
                            _postDependencyClassInstance.signalInfoOccurred.connect(self.__dependencyInfoOccurred)
                            _postDependencyClassInstance.signalSuccessOccurred.connect(self.__dependencySuccessOccurred)
                            _postDependencyClassInstance.signalWarningOccurred.connect(self.__dependencyWarningOccurred)
                            _postDependencyClassInstance.signalFailureOccurred.connect(self.__dependencyFailureOccurred)


                self._processList.append(_processClassInstance)

        self._afterProcessClassesInitialized()

        self._haveProcessesInitialized = True

    #
    ## @brief Initialize processes for parent terminal.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return None - None.
    def _initializeProcessesForParentTerminal(self):

        raise NotImplementedError('Container._initializeProcessesForParentTerminal method has not been implemented.')

    #
    ## @brief Initialize processes for GUI.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return None - None.
    def _initializeProcessesForGUI(self):

        raise NotImplementedError('Container._initializeProcessesForGUI method has not been implemented.')

    #
    # RUN RELATED METHODS
    #
    ## @brief Method is invoked before the run command.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _beforeRun(self):

        return True

    #
    ## @brief Method is invoked after the run command.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _afterRun(self):

        return True

    #
    ## @brief Run the container based on run mode.
    #
    #  @exception mProcess.exceptionLib.ContainerError - No run method is available for this run mode.
    #
    #  @return bool - Result.
    def _run(self):


        if not self._processList:
            self._setFailure('No process found for this container: {}'.format(self._name))
            return False

        #

        if self._requiresUserDescription and not self._data.userDescription():
            errorMessage = 'User description is required, please set a user description via "{}.setUserDescription" method.'.format(self.__class__.__name__)
            if self._data.raiseExceptions():
                raise mProcess.exceptionLib.ContainerError(errorMessage)
            else:
                self._setFailure(errorMessage)
                return False

        #

        # try:
        #     if self._data.runMode() != mProcess.dataLib.RunMode.kGUI:
        #         if not self.shouldInitialize():
        #             self._setFailure('"{}" container can not be initialized, reason is not stated by the developers.'.format(self._name))
        #             return
        # except Exception as error:
        #     if self._data.raiseExceptions():
        #         raise
        #     elif self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or \
        #          self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kFailure:
        #         self._setFailure('"{}" container can not be initialized: {}'.format(self._name, str(error)))
        #     return False

        #

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
                try:
                    return getattr(self, method)()
                except NotImplementedError as e:
                    continue

        raise mProcess.exceptionLib.ContainerError('No run method is available for this run mode.')

    #
    ## @brief Run the container for terminal.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _runForTerminal(self):

        self.signalDisplayHeader.emit(self.__getContainerHeader('{} - CONTAINER'.format(self._name.upper())))

        result = True

        # Pre Dependencies
        if self._data.runLevel()  == mProcess.dataLib.RunLevel.kAll                     or \
            self._data.runLevel() == mProcess.dataLib.RunLevel.kPreDependenciesOnly     or \
            self._data.runLevel() == mProcess.dataLib.RunLevel.kPreAndPostDependenciesOnly:

            for _processClassInstance in self._processList:

                if _processClassInstance.isIgnored():
                    continue

                self.signalDisplayHeader.emit(self.__getDependencyHeader('{} - PRE DEPENDENCY'.format(_processClassInstance.name().upper())))

                if _processClassInstance.runPreDependencies() != True:

                    if self._data.ignoreFailedPreDependencies() and _processClassInstance.isIgnorable():
                        continue
                    else:
                        result = False

                QtCore.QCoreApplication.processEvents()

            if not result:
                self._setFailure('Pre dependency failed.')
                return result

        #

        # Display - as a separator
        if self._data.runLevel() == mProcess.dataLib.RunLevel.kAll or \
           self._data.runLevel() == mProcess.dataLib.RunLevel.kPreAndPostDependenciesOnly:

            if self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or \
               self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kInfo:

                if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal or \
                   self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                    mCore.displayLib.Display.display('    -')

        #

        # Process
        processResultList = []
        if self._data.runLevel() == mProcess.dataLib.RunLevel.kAll          or \
           self._data.runLevel() == mProcess.dataLib.RunLevel.kProcessOnly  or \
           self._data.runLevel() == mProcess.dataLib.RunLevel.kProcessAndPostDependenciesOnly:

            for _processClassInstance in self._processList:

                if _processClassInstance.isIgnored():
                    continue

                self.signalDisplayHeader.emit(self.__getProcessHeader('{} - PROCESS'.format(_processClassInstance.name().upper())))

                try:
                    processResultList.append(_processClassInstance.run())
                except Exception as error:
                    if self._data.raiseExceptions():
                        raise
                    else:
                        self._setFailure(str(error))

        processResultList = [x for x in processResultList if x == False]
        if processResultList:
            return False

        #

        # Display - as a separator
        if self._data.runLevel() == mProcess.dataLib.RunLevel.kAll or \
           self._data.runLevel() == mProcess.dataLib.RunLevel.kPreAndPostDependenciesOnly:

            if self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kAll or \
               self._data.displayMessages() == mProcess.dataLib.DisplayMessage.kInfo:

                if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal or \
                   self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
                    mCore.displayLib.Display.display('    -')

        #

        # Post Dependencies
        if self._data.runLevel()  == mProcess.dataLib.RunLevel.kAll                         or \
            self._data.runLevel() == mProcess.dataLib.RunLevel.kPostDependenciesOnly        or \
            self._data.runLevel() == mProcess.dataLib.RunLevel.kPreAndPostDependenciesOnly  or \
            self._data.runLevel() == mProcess.dataLib.RunLevel.kProcessAndPostDependenciesOnly:

            for _processClassInstance in self._processList:

                if _processClassInstance.isIgnored():
                    continue

                self.signalDisplayHeader.emit(self.__getDependencyHeader('{} - POST DEPENDENCY'.format(_processClassInstance.name().upper())))

                if _processClassInstance.runPostDependencies() != True:

                    if self._data.ignoreFailedPreDependencies() and _processClassInstance.isIgnorable():
                        continue
                    else:
                        result = False

                QtCore.QCoreApplication.processEvents()

            if not result:
                self._setFailure('Post dependency failed.')
                return result

        return True

    #
    ## @brief Run the container for parent terminal.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return bool - Result.
    def _runForParentTerminal(self):

        raise NotImplementedError('Container._runForParentTerminal method has not been implemented.')

    #
    ## @brief Run the container for GUI.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return bool - Result.
    def _runForGUI(self):

        raise NotImplementedError('Container._runForGUI method has not been implemented.')

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
    ## @brief Class instance that operates on data file.
    #
    #  @exception N/A
    #
    #  @return mFileSystem.jsonFileLib.JSONFile - Data file class instance.
    def dataFile(self):

        return self._dataFile

    #
    ## @brief Set data file.
    #
    #  @param dataFile [ str | None | in  ] - Absolute path of data file (JSON).
    #
    #  @exception mProcess.exceptionLib.DataFileDoesNotExist - If given `dataFile` does not exist.
    #
    #  @return bool - Result.
    def setDataFile(self, dataFile):

        if not self._dataFile.setFile(dataFile):
            raise mProcess.exceptionLib.DataFileDoesNotExist('Data fie does not exist: {}'.format(dataFile))

        self._dataFile.read()

        dataFileContent = self._dataFile.content()

        if dataFileContent:
            self._data.data().update(dataFileContent)

        return True

    #
    ## @brief Keyword arguments.
    #
    #  @exception N/A
    #
    #  @return dict - Keyword arguments.
    def kwargs(self):

        return self._kwargs

    #
    ## @brief Process list.
    #
    #  @exception N/A
    #
    #  @return list of mProcess.processAbs.Process - Processes.
    def processList(self):

        return self._processList

    #
    ## @brief Whether this class has been initialized.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def hasInitialized(self):

        return self._hasInitialized

    #
    ## @brief Set this class initialized.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setInitialized(self):

        self._hasInitialized = True

    #
    ## @brief Whether process classes have been initialized.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def haveProcessesInitialized(self):

        return self._haveProcessesInitialized

    #
    ## @brief Set process classes initialized.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setProcessesInitialized(self):

        self._haveProcessesInitialized = True

    #
    ## @brief User description.
    #
    #  @exception N/A
    #
    #  @return str - User description.
    def userDescription(self):

        return self._data.userDescription()

    #
    ## @brief Set user description.
    #
    #  @param userDescription [ str | None | in  ] - User description.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setUserDescription(self, userDescription):

        self._data.setUserDescription(userDescription)

    #
    ## @brief Ignore description.
    #
    #  @exception N/A
    #
    #  @return str - Ignore description.
    def ignoreDescription(self):

        return self._data.ignoreDescription()

    #
    ## @brief Set ignore description.
    #
    #  @param ignoreDescription [ str | None | in  ] - Ignore description.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setIgnoreDescription(self, ignoreDescription):

        self._data.setIgnoreDescription(ignoreDescription)

    #
    ## @brief Name of the container.
    #
    #  @exception N/A
    #
    #  @return str - Name.
    def name(self):

        return self._name

    #
    ## @brief Description about the container.
    #
    #  @exception N/A
    #
    #  @return str - Description.
    def description(self):

        return self._description

    #
    ## @brief Process list module.
    #
    #  @exception N/A
    #
    #  @return str - Process list module.
    def processListModule(self):

        return self._processListModule

    #
    ## @brief Whether this container requires user description to run.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def requiresUserDescription(self):

        return self._requiresUserDescription

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief String representation.
    #
    #  @exception N/A
    #
    #  @return str - String representation.
    def asStr(self):

        if not self._hasInitialized:
            return ''

        info = self.__getContainerHeader('{} - CONTAINER'.format(self._name))
        info = '{}\n{}'.format(info, '{}\n'.format(self._description))

        for _processInstance in self._processList:

            for _dependencyInstance in _processInstance.preDependencyList():
                info = '{}\n{}'.format(info, self.__getDependencyHeader('{} - PRE DEPENDENCY'.format(_dependencyInstance.name())))
                info = '{}\n{}'.format(info, '    {}\n'.format(_dependencyInstance.description()))

            info = '{}\n\n\n\n{}'.format(info, self.__getProcessHeader('{} - PROCESS'.format(_processInstance.name())))
            info = '{}\n{}\n\n\n'.format(info, '    {}\n'.format(_processInstance.description()))

            for _dependencyInstance in _processInstance.postDependencyList():
                info = '{}\n{}'.format(info, self.__getDependencyHeader('{} - POST DEPENDENCY'.format(_dependencyInstance.name())))
                info = '{}\n{}'.format(info, '    {}\n'.format(_dependencyInstance.description()))

        return info

    #
    ## @brief Whether this container should be initialized.
    #
    #  Implement this method to prevent child class instance from being initialized
    #  by raising mProcess.exceptionLib.ContainerError exception.
    #  Method must return True explicitly otherwise.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def shouldInitialize(self):

        return True

    #
    ## @brief Run the container meaning running all processes and their dependencies.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def run(self):

        if not self._hasInitialized:
            return False

        try:
            if not self._beforeRun():
                return False
        except Exception as error:
            if self._data.raiseExceptions():
                raise
            else:
                return self._setFailure(str(error))

        try:
            if not self._run():
                return False
        except Exception as error:
            if self._data.raiseExceptions():
                raise
            else:
                return self._setFailure(str(error))

        try:
            if not self._afterRun():
                return False
        except Exception as error:
            if self._data.raiseExceptions():
                raise
            else:
                return self._setFailure(str(error))

        return True

    #
    # ------------------------------------------------------------------------------------------------
    # CLASS METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Class method which can be used to run child classes of this class in command line.
    #
    #  @param cls [ object | None | in  ] - Class object.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @classmethod
    def runInCommandLine(cls):

        _parser = argparse.ArgumentParser(description='Container command line interface.')

        runModeHelp = ''
        runModeDict = mProcess.dataLib.RunMode.asDict()
        for i in runModeDict:
            runModeHelp = '{}{} for {}, '.format(runModeHelp, runModeDict[i], i)

        runLevelHelp = ''
        runLevelDict = mProcess.dataLib.RunLevel.asDict()
        for i in runLevelDict:
            runLevelHelp = '{}{} for {}, '.format(runLevelHelp, runLevelDict[i], i)

        displayMessagesHelp = ''
        displayMessagesDict = mProcess.dataLib.DisplayMessage.asDict()
        for i in displayMessagesDict:
            displayMessagesHelp = '{}{} for {}, '.format(displayMessagesHelp, displayMessagesDict[i], i)

        _parser.add_argument('-df',
                             '--data-file',
                             type=str,
                             default='',
                             help='Absolute path of data file.',
                             required=False)

        _parser.add_argument('-rm',
                             '--run-mode',
                             type=int,
                             help=runModeHelp,
                             default=mProcess.dataLib.RunMode.kTerminal,
                             choices=mProcess.dataLib.RunMode.listAttributes(stringOnly=False, getValues=True),
                             required=False)

        _parser.add_argument('-rl',
                             '--run-level',
                             type=int,
                             help=runLevelHelp,
                             default=mProcess.dataLib.RunLevel.kAll,
                             choices=mProcess.dataLib.RunLevel.listAttributes(stringOnly=False, getValues=True),
                             required=False)

        _parser.add_argument('-pr',
                             '--processes-to-run',
                             nargs='*',
                             help='Processes to run. -pr "A Release" "B Release"',
                             required=False)

        _parser.add_argument('-pi',
                             '--processes-to-ignore',
                             nargs='*',
                             help='Processes to ignore. -pi "A Release" "B Release"',
                             required=False)

        _parser.add_argument('-ifpred',
                             '--ignore-failed-pre-dependencies',
                             help='Whether to ignore failed ignorable pre dependencies. Default value is False.',
                             default=False,
                             required=False,
                             action='store_true')

        _parser.add_argument('-ifpostd',
                             '--ignore-failed-post-dependencies',
                             help='Whether to ignore failed ignorable post dependencies. Default value is False.',
                             default=False,
                             required=False,
                             action='store_true')

        _parser.add_argument('-re',
                             '--raise-exceptions',
                             help='Whether to raise exceptions. Default value is False.',
                             default=False,
                             required=False,
                             action='store_true')

        _parser.add_argument('-dm',
                             '--display-messages',
                             type=int,
                             help=displayMessagesHelp,
                             default=mProcess.dataLib.DisplayMessage.kAll,
                             choices=mProcess.dataLib.DisplayMessage.listAttributes(stringOnly=False, getValues=True),
                             required=False)

        _parser.add_argument('-ud',
                            '--user-description',
                            type=str,
                            default='',
                            help='User description',
                            required=False)

        _parser.add_argument('-id',
                            '--ignore-description',
                            type=str,
                            default='',
                            help='Ignore description',
                            required=False)

        _parser.add_argument('-di',
                             '--display-info',
                             help='Display info about this container.',
                             default=False,
                             required=False,
                             action='store_true')

        _args = _parser.parse_args()


        if _args.display_info:
            _processContainerInstance = cls()
            mCore.displayLib.Display.display(_processContainerInstance, startNewLine=False)
            return


        processesToRunList = _args.processes_to_run
        if not processesToRunList:
            processesToRunList = []

        processesToIgnoreList = _args.processes_to_ignore
        if not processesToIgnoreList:
            processesToIgnoreList = []

        _data = mProcess.dataLib.Data(runMode=_args.run_mode,
                                      runLevel=_args.run_level,
                                      processesToRun=processesToRunList,
                                      processesToIgnore=processesToIgnoreList,
                                      ignoreFailedPreDependencies=_args.ignore_failed_pre_dependencies,
                                      ignoreFailedPostDependencies=_args.ignore_failed_post_dependencies,
                                      raiseExceptions=_args.raise_exceptions,
                                      displayMessages=_args.display_messages,
                                      userDescription=_args.user_description,
                                      ignoreDescription=_args.ignore_description)

        _processContainerInstance = cls(data=_data, dataFile=_args.data_file)

        _processContainerInstance.run()

