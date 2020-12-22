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
## @file    mProcess/processAbs.py @brief [ FILE   ] - Abstract process module.
## @package mProcess.processAbs    @brief [ MODULE ] - Abstract process module.


# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  importlib
import  inspect

from    Qt import QtCore

import  mProcess.dataLib
import  mProcess.dependencyAbs
import  mProcess.exceptionLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ ABSTRACT CLASS ] - Abstract dependency class.
class Process(QtCore.QObject):
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

    ## [ Signal ] - Signal emitted when step occurs (for progress bar).
    signalStepOccurred    = QtCore.Signal()

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
        self._data                          = data
        if not self._data:
            self._data = mProcess.dataLib.Data()

        ## [ dict ] - Keyword arguments.
        self._kwargs                        = kwargs

        #

        ## [ list ] - Pre dependencies.
        self._preDependencyList             = []

        ## [ list ] - Post dependencies.
        self._postDependencyList            = []

        #

        if not hasattr(self, '_name'):
            ## [ str ] - Name of the process.
            self._name                      = None

        if not hasattr(self, '_description'):
            ## [ str ] - Description about the process.
            self._description               = None

        if not hasattr(self, '_icon'):
            ## [ str ] - Absolute path of the icon.
            self._icon                      = None

        #

        if not hasattr(self, '_dependencyListModule'):
            ## [ str ] - Dependency list module.
            self._dependencyListModule      = None

        #

        if not hasattr(self, '_isActive'):
            ## [ bool ] - Whether this process is active.
            self._isActive                  = True

        if not hasattr(self, '_isIgnorable'):
            ## [ bool ] - Whether this process is ignorable.
            self._isIgnorable               = False

        if not hasattr(self, '_isIgnored'):
            ## [ bool ] - Whether this process is ignored.
            self._isIgnored                 = False

        if not hasattr(self, '_requiresDescriptionWhenIgnored'):
            ## [ bool ] - Whether this process requires description when ignored.
            self._requiresDescriptionWhenIgnored = True

        #

        if not hasattr(self, '_isCollapsed'):
            ## [ bool ] - Whether the process is collapsed on the GUI.
            self._isCollapsed               = False

        if not hasattr(self, '_areDependenciesCollapsed'):
            ## [ bool ] - Whether dependencies are collapsed on the GUI.
            self._areDependenciesCollapsed  = True

        #

        self._editData()

        self._initializeDependencies()

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

        self.signalInfoOccurred.emit('{} : {}'.format(self._name, infoMessage))

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

        self.signalSuccessOccurred.emit('{} : {}'.format(self._name, successMessage))

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

        self.signalWarningOccurred.emit('{} : {}'.format(self._name, warningMessage))

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

        if self._data.runLevel() == mProcess.dataLib.RunLevel.kAll or \
            self._data.runLevel() == mProcess.dataLib.RunLevel.kProcessOnly:

            if failureMessage:
                self.signalFailureOccurred.emit('{} : {}'.format(self._name, failureMessage))

        return False

    #
    # DEPENDENCY INITIALIZATION METHODS
    #
    ## @brief Callback that invoked by _initializeDependencies before dependency class
    #  initialization started.
    #
    #  @see csProcess.processAbs.Process._initializeDependencies
    #  @see csProcess.processAbs.Process._afterDependencyClassesInitialized
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _beforeDependencyClassesInitialized(self):

        pass

    #
    ## @brief Callback that invoked by _initializeDependencies member after dependency class
    #  initialization ended.
    #
    #  @see csProcess.processAbs.Process._initializeDependencies
    #  @see csProcess.processAbs.Process._beforeDependencyClassesInitialized
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _afterDependencyClassesInitialized(self):

        pass

    #
    ## @brief This method is invoked before each dependency class is initialized.
    #
    #  Implement your custom code to decide whether given dependency class object
    #  should be used. Return False if given classObject shouldn't be used,
    #  return True otherwise.
    #
    #  @warning Method must return True or False explicitly.
    #
    #  @param classObject [ class | None | in  ] - Dependency class object (not an instance).
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _beforeDependencyClassInitialized(self, classObject):

        return True

    #
    ## @brief This method is invoked after each dependency class is initialized.
    #
    #  Implement your custom code to decide whether given dependency class instance
    #  should be used. Return False if given classObject shouldn't be used,
    #  return True otherwise.
    #
    #  @warning Method must return True or False explicitly.
    #
    #  @param classInstance [ object | None | in  ] - Dependency class instance.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _afterDependencyClassInitialized(self, classInstance):

        return True

    #
    #
    #
    ## @brief Sort dependencies.
    #
    #  Implement this method to sort the dependencies (sort _preDependencyList and
    #  _postDependencyList list members). This method
    #  will be called after all dependencies are initialized.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _sortDependencies(self):

        pass

    #
    ## @brief This method initializes all dependency classes and store them in given list instance.
    #
    #  This method is invoked by mProcess.processAbs.Process._initializeDependencies method.
    #
    #  Following callbacks are invoked by this method.
    #
    #  @see mProcess.processAbs.Process._beforeDependencyClassInitialized
    #  @see mProcess.processAbs.Process._afterDependencyClassInitialized
    #
    #  @param moduleName   [ str  | None | in  ] - Module name.
    #  @param listInstance [ list | None | in  ] - List instance.
    #
    #  @exception mProcess.exceptionLib.ProcessError - If dependency classes could not be retrieved.
    #
    #  @return None - None.
    def _initializeDependencyClasses(self, moduleName, listInstance):

        _dependencyModule = None
        try:
            _dependencyModule = importlib.import_module(moduleName)
        except ImportError as error:
            errorMessage = '{} : Dependency module "{}" couldn\'t be imported: {}'.format(self._name,
                                                                                          moduleName,
                                                                                          str(error))
            if self._data.raiseExceptions():
                raise mProcess.exceptionLib.ProcessError(errorMessage)
            else:
                self._setFailure(errorMessage)
        except Exception as error:
            if self._data.raiseExceptions():
                raise
            else:
                self._setFailure(str(error))

        for name, _obj in inspect.getmembers(_dependencyModule):

            # If object is not a class skip it
            if not inspect.isclass(_obj):
                continue

            if not issubclass(_obj, mProcess.dependencyAbs.Dependency):
                continue

            if not self._beforeDependencyClassInitialized(_obj):
                continue

            _dependencyClassInstance = _obj(self, self._data, **self._kwargs)

            if not _dependencyClassInstance.isActive():
                _dependencyClassInstance.deleteLater()
                continue

            try:
                if not _dependencyClassInstance.shouldInitialize():
                    _dependencyClassInstance.deleteLater()
                    continue
            except Exception as error:
                _dependencyClassInstance.deleteLater()
                if self._data.raiseExceptions():
                    raise
                else:
                    continue

            if not self._afterDependencyClassInitialized(_dependencyClassInstance):
                _dependencyClassInstance.deleteLater()
                continue

            listInstance.append(_dependencyClassInstance)

    #
    ## @brief Initialize dependencies for current run mode.
    #
    #  @exception mProcess.exceptionLib.ProcessError - If no initialization method is available for this run mode.
    #
    #  @return None - None.
    def _initializeDependencies(self):

        initializationMethodOrder = []

        if self._data.runMode() == mProcess.dataLib.RunMode.kTerminal:
            initializationMethodOrder = ['_initializeDependenciesForTerminal',
                                         '_initializeDependenciesForParentTerminal',
                                         '_initializeDependenciesForGUI']

        elif self._data.runMode() == mProcess.dataLib.RunMode.kParentTerminal:
            initializationMethodOrder = ['_initializeDependenciesForParentTerminal',
                                         '_initializeDependenciesForTerminal',
                                         '_initializeDependenciesForGUI']

        elif self._data.runMode() == mProcess.dataLib.RunMode.kGUI:
            initializationMethodOrder = ['_initializeDependenciesForGUI',
                                         '_initializeDependenciesForTerminal',
                                         '_initializeDependenciesForParentTerminal']

        for method in initializationMethodOrder:
            if hasattr(self, method):

                try:
                    getattr(self, method)()
                except NotImplementedError as e:
                    continue

                self._sortDependencies()

                return

        raise mProcess.exceptionLib.ProcessError('No initialization method is available for this run mode.')

    #
    ## @brief This method initializes all dependency classes.
    #
    #  This method is invoked by csProcess.processAbs.Process._initializeDependencies method.
    #
    #  Following callbacks are invoked by this method.
    #
    #  @see mProcess.processAbs.Process._beforeDependencyClassInitialized
    #  @see mProcess.processAbs.Process._afterDependencyClassInitialized
    #
    #  @exception csProcess.exceptionLib.ProcessError - If dependency classes could not be retrieved.
    #
    #  @return None - None.
    def _initializeDependenciesForTerminal(self):

        if not self._dependencyListModule:
            raise mProcess.exceptionLib.ProcessError('{} : No dependency list module defined.'.format(self.__class__.__name__))

        _dependencyListModule = None
        try:
            _dependencyListModule = importlib.import_module(self._dependencyListModule)
        except ImportError as error:
            errorMessage = '{} : Dependency list module "{}" couldn\'t be imported: {}'.format(self.__class__.__name__,
                                                                                               self._dependencyListModule,
                                                                                               str(error))
            raise mProcess.exceptionLib.ProcessError(errorMessage)

        self._beforeDependencyClassesInitialized()

        if hasattr(_dependencyListModule, 'PRE_DEPENDENCY_LIST'):

            preDependencyModuleNameList = getattr(_dependencyListModule, 'PRE_DEPENDENCY_LIST')

            if preDependencyModuleNameList:

                for moduleName in preDependencyModuleNameList:

                    self._initializeDependencyClasses(moduleName, self._preDependencyList)

        if hasattr(_dependencyListModule, 'POST_DEPENDENCY_LIST'):

            postDependencyModuleNameList = getattr(_dependencyListModule, 'POST_DEPENDENCY_LIST')

            if postDependencyModuleNameList:

                for moduleName in postDependencyModuleNameList:

                    self._initializeDependencyClasses(moduleName, self._postDependencyList)

        self._afterDependencyClassesInitialized()

    #
    ## @brief Initialize dependencies for parent terminal.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return None - None.
    def _initializeDependenciesForParentTerminal(self):

        raise NotImplementedError('Process._initializeDependenciesForParentTerminal method has not been implemented.')

    #
    ## @brief Initialize dependencies for GUI.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return None - None.
    def _initializeDependenciesForGUI(self):

        raise NotImplementedError('Process._initializeDependenciesForGUI method has not been implemented.')

    #
    # RUN RELATED METHODS
    #
    ## @brief Run the process for terminal.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return bool - Result.
    def _runForTerminal(self):

        raise NotImplementedError('Process._runForTerminal method has not been implemented.')

    #
    ## @brief Run the process for parent terminal.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return bool - Result.
    def _runForParentTerminal(self):

        raise NotImplementedError('Process._runForParentTerminal method has not been implemented.')

    #
    ## @brief Run the process for GUI.
    #
    #  @exception N/A
    #
    #  @exception NotImplementedError - If this method is not implemented.
    #
    #  @return bool - Result.
    def _runForGUI(self):

        raise NotImplementedError('Process._runForGUI method has not been implemented.')

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
    ## @brief Pre dependencies.
    #
    #  @exception N/A
    #
    #  @return list - Pre dependencies.
    def preDependencyList(self):

        return self._preDependencyList

    #
    ## @brief Post dependencies.
    #
    #  @exception N/A
    #
    #  @return list - Post dependencies.
    def postDependencyList(self):

        return self._postDependencyList

    #
    ## @brief Name of the process.
    #
    #  @exception N/A
    #
    #  @return str - Name.
    def name(self):

        return self._name

    #
    ## @brief Description about the process.
    #
    #  @exception N/A
    #
    #  @return str - Description.
    def description(self):

        return self._description

    #
    ## @brief Icon.
    #
    #  @exception N/A
    #
    #  @return str - Absolute path of the icon.
    def icon(self):

        return self._icon

    #
    ## @brief Dependency list module.
    #
    #  @exception N/A
    #
    #  @return str - Dependency list module.
    def dependencyListModule(self):

        return self._dependencyListModule

    #
    ## @brief Whether this process is active.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def isActive(self):

        return self._isActive

    #
    ## @brief Whether this process is ignorable.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def isIgnorable(self):

        return self._isIgnorable

    #
    ## @brief Whether this process is ignored.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def isIgnored(self):

        return self._isIgnored

    #
    ## @brief Set the process ignored.
    #
    #  @param state [ bool | None | in  ] - Value to be set.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def setIgnored(self, state):

        if not self._isIgnorable:
            return False

        self._isIgnored = state == True

        return True

    #
    ## @brief Whether this process requires description when ignored.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def requiresDescriptionWhenIgnored(self):

        return self._requiresDescriptionWhenIgnored

    #
    ## @brief Whether the process is collapsed on the GUI.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def isCollapsed(self):

        return self._isCollapsed

    #
    ## @brief Whether dependencies are collapsed on the GUI.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def areDependenciesCollapsed(self):

        return self._areDependenciesCollapsed

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Whether this process should be initialized.
    #
    #  Implement this method to prevent child class instance from being initialized
    #  by raising mProcess.exceptionLib.ProcessError exception.
    #  Method must return True explicitly otherwise.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def shouldInitialize(self):

        return True

    #
    ## @brief Run the process.
    #
    #  @exception mProcess.exceptionLib.ProcessError - No run method is available for this run mode.
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

                try:
                    return getattr(self, method)()
                except NotImplementedError as e:
                    continue

        raise mProcess.exceptionLib.ProcessError('No run method is available for this run mode.')

    #
    ## @brief Run pre dependencies.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def runPreDependencies(self):

        if not self._preDependencyList:
            return True

        resultList = []
        for _dependencyClassInstance in self._preDependencyList:

            if _dependencyClassInstance.isIgnored():
                continue

            runResult = False
            try:
                runResult = _dependencyClassInstance.run()
            except Exception as error:
                if self._data.ignoreFailedPreDependencies() and _dependencyClassInstance.isIgnorable():
                    _dependencyClassInstance.displayAutoIgnoredMessage()
                    continue
                else:
                    if self._data.raiseExceptions():

                        raise
                    else:
                        self._setFailure(str(error))

            if not runResult:

                if self._data.ignoreFailedPreDependencies() and _dependencyClassInstance.isIgnorable():
                    _dependencyClassInstance.displayAutoIgnoredMessage()
                    continue
                elif _dependencyClassInstance.hasFix() and _dependencyClassInstance.runFixAutomatically():
                    runFixResult = _dependencyClassInstance.runFix()
                    if not runFixResult:
                        if self._data.ignoreFailedPreDependencies():
                            _dependencyClassInstance.setIgnored(True)
                            runResult = True

            resultList.append(runResult)

        return not (False in resultList)

    #
    ## @brief Run post dependencies.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def runPostDependencies(self):

        if not self._postDependencyList:
            return True

        resultList = []
        for _dependencyClassInstance in self._postDependencyList:

            if _dependencyClassInstance.isIgnored():
                continue

            runResult = False
            try:
                runResult = _dependencyClassInstance.run()
            except Exception as error:
                if self._data.raiseExceptions():
                    raise
                else:
                    self._setFailure(str(error))

            if not runResult:

                if _dependencyClassInstance.hasFix() and _dependencyClassInstance.runFixAutomatically():
                    runFixResult = _dependencyClassInstance.runFix()
                    if not runFixResult:
                        if self._data.ignoreFailedPreDependencies():
                            _dependencyClassInstance.setIgnored(True)
                            runResult = True

            resultList.append(runResult)

        return not (False in resultList)
