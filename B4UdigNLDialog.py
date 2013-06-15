"""
/***************************************************************************
B4UdigNL
A QGIS plugin
View the result of a Dutch B4Udig request
----------------------------------------------
begin                : 2010-05-18 
copyright            : (C) 2010 by Diethard Jansen
email                : diethard.jansen at gmail.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_B4UdigNL import Ui_B4UdigNL
import wv, ifaceqgis, os, helpform
import unzip, zipfile, pickle


# create the dialog
class B4UdigNLDialog(QDialog):
    layerGroups = ["Annotatie",
                   "Maatvoering",
                   "Ligging",
                   "Topo"]
    
    themeNames = {"data": "datatransport",
                  "gas_low": "gas lage druk", 
                  "gas_high": "gas hoge druk",
                  "danger": "buisleiding gevaarlijke inhoud",
                  "elec_low": "laagspanning",
                  "elec_mid": "middenspanning",
                  "elec_high": "hoogspanning",
                  "sewer_free": "riool vrijverval",
                  "sewer_pressure": "riool onder druk",
                  "heat": "warmte",
                  "water": "water",
                  "chemical": "(petro)chemie",
                  "orphan": "wees",
                  "other": "overig"}
    """
    now add to this shared class variable also the layerGroupThemes
    """
    for i_groupName in wv.Layer.layerGroupNames.keys():
        themeNames[i_groupName] = i_groupName

    def __init__(self, iface): 
        QDialog.__init__(self)
        self.__iface = iface
        self.__legend = iface.legendInterface()
        self.__dir = None
        self.__wv = None
        self.__wvs = []
        self.__themes = None
        self.__addGroupsBuggy = False
        self.__settings = self._userSettings()
        self.ui = Ui_B4UdigNL()
        self.ui.setupUi(self)
        self._themes2checkboxes()
        self.updateUi()
        self.makeConnections()
        self._setUnitToMeters()
        self.restoreMessages()
        
    def layerGroupNames(self):
        """returns dictionary with legend groups"""
        return {"Annotatie": self.tr("Annotatie"),
                "Maatvoering": self.tr("Maatvoering"),
                "Ligging": self.tr("Ligging"),
                "Topo": self.tr("Topo")}

    def _userSettings(self):
        """return dictionary with user settings"""
        l_settings = {"b4udignl/dir_preferred": ".",
                      "b4udignl/dir_last_used": ".",
                      "b4udignl/last_xpos_dialog": "0",
                      "b4udignl/last_ypos_dialog": "0",
                      "b4udignl/last_width_dialog": "0",
                      "b4udignl/last_height_dialog": "0"}
        s = QSettings()
        for i_key, i_value in l_settings.iteritems():
            # try to read user settings from system configuration
            try:
                l_user_value = s.value(i_key, type=str)
            except TypeError, e:
                l_user_value = ""
            if l_user_value != "" and l_user_value != i_value:
                # retrieved setting, now store in list and replace default
                # settings!
                l_settings[i_key] = l_user_value
        return l_settings
        
    def _themes2checkboxes(self):
        """
        to update visibilities of themes checkboxes they are stored
        in private attribute __themes which is a dictionary
        """
        l_ui = self.ui
        l_names = self.themeNames
        self.__themes = {l_names["data"]: l_ui.checkBoxData,
                         l_names["gas_low"]: l_ui.checkBoxGas_low,
                         l_names["gas_high"]: l_ui.checkBoxGas_high,
                         l_names["danger"]: l_ui.checkBoxDanger,
                         l_names["elec_low"]: l_ui.checkBoxElec_low,
                         l_names["elec_mid"]: l_ui.checkBoxElec_mid,
                         l_names["elec_high"]: l_ui.checkBoxElec_high,
                         l_names["sewer_free"]: l_ui.checkBoxSewer_free,
                         l_names["sewer_pressure"]: l_ui.checkBoxSewer_pressure,
                         l_names["heat"]: l_ui.checkBoxHeat,
                         l_names["water"]: l_ui.checkBoxWater,
                         l_names["chemical"]: l_ui.checkBoxChemical,
                         l_names["orphan"]: l_ui.checkBoxOrphan,
                         l_names["other"]: l_ui.checkBoxOther,
                         l_names["Annotatie"]: l_ui.annotationCheckBox,
                         l_names["Maatvoering"]: l_ui.dimensioningCheckBox,
                         l_names["Ligging"]: l_ui.locationCheckBox,
                         l_names["Topo"]: l_ui.topoCheckBox}

            
    def updateUi(self):
        """use to translate/update visibility of buttons"""
        l_ui = self.ui
        l_tree = l_ui.treeWidget
        #l_headers = "Type Document/Name Document" 
        l_headers = self.tr("Soort Bijlage/Naam Bijlage")
        l_tree.setHeaderLabels([l_headers])
        l_ui.textEditDirPreffered.setText(self.__settings["b4udignl/dir_preferred"])
        self._setVisibilities()

    def makeConnections(self):
        """makes all neccesary connections between signals and slots"""
        self.connect(self.ui.treeWidget,
                     SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"),
                     self._openPdf)
        # next connection does not work, a signal from QT can not
        # be connected to a slot method created in pyqt (maybe in future?)
        self.connect(self.__legend,
                     SIGNAL("groupIndexChanged(int, int)"),
                     self._updateLayerGroup)
        self.connect(self.ui.checkBoxData,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxDataStateChanged)
        self.connect(self.ui.checkBoxGas_low,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxGasLowStateChanged)
        self.connect(self.ui.checkBoxGas_high,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxGasHighStateChanged)
        self.connect(self.ui.checkBoxDanger,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxDangerStateChanged)
        self.connect(self.ui.checkBoxElec_low,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxElecLowStateChanged)
        self.connect(self.ui.checkBoxElec_mid,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxElecMidStateChanged)
        self.connect(self.ui.checkBoxElec_high,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxElecHighStateChanged)
        self.connect(self.ui.checkBoxSewer_free,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxSewerFreeStateChanged)
        self.connect(self.ui.checkBoxSewer_pressure,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxSewerPressureStateChanged)
        self.connect(self.ui.checkBoxHeat,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxHeatStateChanged)
        self.connect(self.ui.checkBoxWater,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxWaterStateChanged)
        self.connect(self.ui.checkBoxChemical,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxChemicalStateChanged)
        self.connect(self.ui.checkBoxOrphan,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxOrphanStateChanged)
        self.connect(self.ui.checkBoxOther,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxOtherStateChanged)
        self.connect(self.ui.annotationCheckBox,
                     SIGNAL("stateChanged(int)"),
                     self._annotationCheckBoxStateChanged)
        self.connect(self.ui.dimensioningCheckBox,
                     SIGNAL("stateChanged(int)"),
                     self._dimensioningCheckBoxStateChanged)
        self.connect(self.ui.locationCheckBox,
                     SIGNAL("stateChanged(int)"),
                     self._locationCheckBoxStateChanged)
        self.connect(self.ui.topoCheckBox,
                     SIGNAL("stateChanged(int)"),
                     self._topoCheckBoxStateChanged)
        self.connect(self.__iface,
                     SIGNAL("projectRead()"),
                     self.restoreMessages)
        self.connect(self.__iface,
                     SIGNAL("newProjectCreated()"),
                     self._removeMessages)

    def _checkBoxDataStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["data"], p_state)
    def _checkBoxGasLowStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["gas_low"], p_state)
    def _checkBoxGasHighStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["gas_high"], p_state)
    def _checkBoxDangerStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["danger"], p_state)
    def _checkBoxElecLowStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["elec_low"], p_state)
    def _checkBoxElecMidStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["elec_mid"], p_state)
    def _checkBoxElecHighStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["elec_high"], p_state)
    def _checkBoxSewerFreeStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["sewer_free"], p_state)
    def _checkBoxSewerPressureStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["sewer_pressure"], p_state)
    def _checkBoxHeatStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["heat"], p_state)
    def _checkBoxWaterStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["water"], p_state)
    def _checkBoxChemicalStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["chemical"], p_state)
    def _checkBoxOrphanStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["orphan"], p_state)
    def _checkBoxOtherStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["other"], p_state)
    def _annotationCheckBoxStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["Annotatie"], p_state)
    def _dimensioningCheckBoxStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["Maatvoering"], p_state)
    def _locationCheckBoxStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["Ligging"], p_state)
    def _topoCheckBoxStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["Topo"], p_state)

    def _themeStateChanged(self, p_theme, p_state):
        """
        a theme has changed and now the visibility of layers belonging
        to that theme will change (when neccesary)
        """
        l_theme = None
        l_doc = self.__wv
        if l_doc is not None:
            if l_doc.themes.has_key(p_theme):
                l_theme = l_doc.themes[p_theme]
                if p_state==0:
                    l_theme.setVisibility(False)
                    self._setStateOfVisibilitiesThemes(True)
                elif p_state==1:
                    #check if this is state is changed from
                    #setting a layer in legend on/of if the
                    #actual state of this theme is 0 then change
                    #state of checkbox to 2! Makes behaviour of
                    #theme checkboxes identical to layergroups checkboxes
                    l_value = l_theme.checkVisible(True)
                    if l_value == 0:
                        self.__themes[p_theme].setCheckState(2)
                elif p_state==2:
                    l_theme.setVisibility(True)
                    self._setStateOfVisibilitiesThemes(True)
            
    def _setVisibilities(self):
        """ update visibilities of buttons"""
        l_ui = self.ui
        if self.__wv is None:
            l_ui.gotoButton.setEnabled(False)
            l_ui.bestScaleButton.setEnabled(False)
            l_ui.removeMsgButton.setEnabled(False)
            l_ui.openDocButton.setEnabled(False)
            l_ui.saveButton.setEnabled(False)
            l_ui.refreshButton.setEnabled(False)
        else:
            l_ui.gotoButton.setEnabled(True)
            l_ui.bestScaleButton.setEnabled(True)
            l_ui.removeMsgButton.setEnabled(True)
            l_ui.openDocButton.setEnabled(True)
            l_ui.saveButton.setEnabled(True)
            l_ui.refreshButton.setEnabled(True)
        self._setVisibilitiesThemes()

    def _setVisibilitiesThemes(self):
        if self.__wv is None:
            for i_checkbox in self.__themes.itervalues():
                i_checkbox.setEnabled(False)
        else:
            for i_theme, i_checkbox in self.__themes.iteritems():
                if self.__wv.themes.has_key(i_theme):
                    i_checkbox.setEnabled(True)
                else:
                    i_checkbox.setEnabled(False)
 
    def _setStateOfVisibilitiesThemes(self, p_actual=False):
        """
        Set state of visibilies for themes.
        When p_actual is used current state is checked
        which is slower. 
        """
        l_doc = self.__wv
        for i_theme, i_checkbox in self.__themes.iteritems():
            if l_doc is None:
                i_checkbox.setCheckState(0)
            else:
                l_theme = None
                if l_doc.themes.has_key(i_theme):
                    l_theme = l_doc.themes[i_theme]
                if l_theme is not None:
                    l_value = l_theme.checkVisible(p_actual)
                    i_checkbox.setCheckState(l_value)
                else:
                    i_checkbox.setCheckState(0)
 
    @pyqtSignature("")
    def on_openMsgButton_clicked(self):
        """opens directory search dialog and sets my attribute __dir"""
        l_path = self._start_find_path()
        
        #l_request = "Select directory which hold result request Dig ALert"
        l_request = self.tr("Selecteer folder met resultaat WION bericht")
        l_dir_path = QFileDialog.getExistingDirectory(self, l_request, l_path)
        if not l_dir_path.isEmpty():
            self.__dir = l_dir_path
            QSettings().setValue("b4udignl/dir_last_used", l_dir_path)
            self._loadMsg()
            
    @pyqtSignature("")
    def on_openArchiveButton_clicked(self):
        """opens directory search dialog and sets my attribute __dir"""
        l_path = self._start_find_path()
        
        #l_request = "Select zipfile which holds result request Dig ALert"
        l_request = self.tr("Selecteer een zip bestand die een WION bericht bevat")
        l_filter = self.tr("Zip bestanden (*.zip *.ZIP)")
        l_fileName = QFileDialog.getOpenFileName(self, l_request, l_path, l_filter)
        if l_fileName=="":
            return
        #l_fileName = unicode(l_fileName)
        #first find out if zipfile contains a named directory being
        #ID of dig alert
        l_dirName = self._dirNameInArchive(l_fileName)
        l_dir = os.path.dirname(l_fileName)
        l_zipDir = os.path.join(l_dir,l_dirName)
        self.__dir = l_zipDir
        l_unzipper = unzip.unzip()
        l_unzipper.extract(l_fileName, l_zipDir)
        #try to find out if after extract, folder holds another folder
        #with message id
        l_dir_maybe = os.path.join(l_zipDir, l_dirName)
        if os.path.isdir(l_dir_maybe):
            self.__dir = l_dir_maybe
        self._loadMsg()

    def _start_find_path(self):
        """
        returns path that should be used to look for next wion message to load
        this path can be stored in user setting dir_preffered
        when user setting is not set it then uses last directory used
        to open a wion message. 
        """
        if self.__dir != None:
            l_path = self.__dir
        else:
            l_dir_preffered = self.__settings["b4udignl/dir_preferred"]
            if l_dir_preffered != ".":
                l_path = l_dir_preffered
            else:
                l_path = self.__settings["b4udignl/dir_last_used"]
        return l_path

    @pyqtSignature("")
    def on_refreshButton_clicked(self):
        """refreshes the state of all themes"""
        self._setStateOfVisibilitiesThemes(True)

    @pyqtSignature("")
    def on_saveButton_clicked(self):
        """save messages & state to project file"""
        self.saveMessages()

    def _dirNameInArchive(self, p_fileName):
        """
        l_filename = full path of zipfile
        Find out if given zip archive has a folder which
        contains result of Digalert (normal case)
        The testmessages  (Oefenbestand 1 en 2 from
        www.klicviewer.nl) do not contain folder in archive.
        """
        #first find out if zipfile contains a named directory being
        #ID of dig alert
        l_zipfile = zipfile.ZipFile(p_fileName)
        l_file_list = l_zipfile.infolist()
        l_dirName = ""
        try:
            l_a_zipped_file = l_file_list[0].filename
            l_index = l_a_zipped_file.index("/")
            l_dirName = l_a_zipped_file[:l_index]
        except:
            # this is probably testmessage
            l_dirName = os.path.basename(p_fileName)[:-4]
        return l_dirName

    @pyqtSignature("")
    def on_msgListWidget_itemSelectionChanged(self):
        """change the current document"""
        l_listWidget = self.ui.msgListWidget
        l_item = l_listWidget.currentItem()
        self._changeDoc(l_item)

    @pyqtSignature("")
    def on_openDocButton_clicked(self):
        """opens the selected document delivered in result digAlert request"""
        l_items = self.ui.treeWidget.selectedItems()
        for i_item in l_items:
            self._openPdf(i_item)

    @pyqtSignature("")
    def on_closeButton_clicked(self):
        """hides (closes) the window"""
        self.close()

    @pyqtSignature("")
    def on_helpButton_clicked(self):
        """opens the help manual"""
        self.helpHelp()
        
    @pyqtSignature("")
    def on_gotoButton_clicked(self):
        """goto extent of map current message"""
        if self.__wv != None:
            self.__wv.goto()

    @pyqtSignature("")
    def on_removeMsgButton_clicked(self):
        """remove selected message from list and all loaded layers"""
        l_msg_list = self.ui.msgListWidget
        l_item = l_msg_list.currentItem()
        l_doc = self._selectedMsg(l_item)
        # remove loaded layers
        if l_doc is None:
            return
        l_klicnumber = l_doc.klicnummer
        self._updateGroupIndexesB4Remove()
        l_mapCanvas = self.__iface.mapCanvas()
        l_mapCanvas.setRenderFlag(False)
        self._removeGroups()
        l_doc.removeLayers()
        l_mapCanvas.setRenderFlag(True)
        l_mapCanvas.refresh()
        # remove doc, populate message list, populate tree when neccesary
        l_new_docs = []
        l_new_current_doc = None
        
        for i_wv in self.__wvs:
            if l_klicnumber != i_wv.klicnummer:
                l_new_docs.append(i_wv)
                if l_new_current_doc is None:
                    l_new_current_doc = i_wv
        self.__wvs = l_new_docs
        self.__wv = l_new_current_doc
        self._populateMsgList()
        self._populateTree()
        self._setStateOfVisibilitiesThemes(True)
        self._setVisibilities()
        
    @pyqtSignature("")
    def on_bestScaleButton_clicked(self):
        """set best scale for current message"""
        if self.__wv != None:
            self.__wv.bestScale()

    @pyqtSignature("")
    def on_optionMsgDirButton_clicked(self):
        """
        select directory which will be used to start searching
        Wion result messages from when using openMsgButton
        """
        l_path = self.__settings["b4udignl/dir_preferred"]
        l_request = self.tr("Selecteer standaard folder met WION berichten")
        l_dir_path = QFileDialog.getExistingDirectory(self, l_request, l_path)
        if not l_dir_path.isEmpty():
            self.__settings["b4udignl/dir_preferred"] = l_dir_path
            QSettings().setValue("b4udignl/dir_preferred", l_dir_path)
            self.ui.textEditDirPreffered.setText(l_dir_path)

    def _loadMsg(self):
        l_doc = self._openMsg(unicode(self.__dir))
        if l_doc is None:
            return
        l_doc.iface = ifaceqgis.Iface(self.__iface)
        self.__wv = l_doc
        self.__wvs.append(l_doc)
        self._populateMsgList()
        self._populateTree()
        self._createLayerGroups(l_doc)
        l_iface = l_doc.iface
        l_iface.doRendering(False)
        l_doc.loadLayers()
        self._updateAllLayerGroups(len(l_doc.layers))
        self._moveLayersToGroups(l_doc)
        l_iface.doRendering(False)
        l_iface.refreshMap()
        self._setStateOfVisibilitiesThemes()
        self._setVisibilities()

    def _openMsg(self, p_path):
        """
        p_path = directory path where wion message can be found.
        returns object of type Doc holding all information read from xml
        found in given path.
        """
        try:
            l_doc = wv.Doc(p_path)
        except IOError:
            self._displayWrongMsg()
            return None
        return l_doc

    def _displayWrongMsg(self):
        """
        give a warning to user that wion message could not be read
        from selected folder
        """
        #l_titleMsg = "Problem reading result"
        l_titleMsg = self.tr("Fout WION bericht")
        #l_errorMsg = "Selected directory does not contain\n\
        #              result of Dutch Dig Alert or it can not be read!")
        l_errorMsg = self.tr("Geselecteerde folder bevat geen goed\n\
        WION bericht of kan niet worden geopend!")
        QMessageBox.warning(self, l_titleMsg, l_errorMsg)
        
    def _openPdf(self, pdfItem):
        """use name of PDF to get right pdf and open it"""
        l_pdfName = unicode(pdfItem.text(0))
        for i_pdf in self.__wv.pdfFiles:
            if i_pdf.name == l_pdfName:
                i_pdf.openPdf()
                break

    def _populateMsgList(self):
        """populates list of wion messages"""
        l_selected = None
        l_ui = self.ui
        l_list = l_ui.msgListWidget
        l_list.clear()
        for i_doc in self.__wvs:
            l_klicnummer = i_doc.klicnummer
            l_item = QListWidgetItem(QString(l_klicnummer))
            l_list.addItem(l_item)
            if l_klicnummer == self.__wv.klicnummer:
                l_selected = l_item
        if l_selected is not None:
            l_selected.setSelected(True)
            l_list.setCurrentItem(l_selected)
 
    def _populateTree(self):
        """populates tree with pdf document provided in DigAlert message"""
        selected = None
        l_ui = self.ui
        l_tree = l_ui.treeWidget
        l_tree.clear()
        if self.__wv is None:
            return
        l_tree.setColumnCount(1)
        l_tree.setItemsExpandable(True)
        parentTypePdf = {}
        for i_pdf in self.__wv.pdfFiles:
            parent = parentTypePdf.get(i_pdf.type)
            if parent is None:
                parent = QTreeWidgetItem(l_tree,[i_pdf.type])
            parentTypePdf[i_pdf.type] = parent
            item = QTreeWidgetItem(parent, [QString(i_pdf.name)])
            l_tree.expandItem(parent)
            l_tree.resizeColumnToContents(0)

    def _changeDoc(self, p_currentItem):
        """When user selects other message change other plugin elements as well"""
        l_doc = self._selectedMsg(p_currentItem)
        if l_doc != None:
            self.__wv = l_doc
            self._populateTree()
            self._setStateOfVisibilitiesThemes(True)
            self._setVisibilitiesThemes()
               
    def _selectedMsg(self, p_currentItem):
        """returns Doc being selected message in list"""
        if p_currentItem is None:
            return
        l_klicnummer = unicode(p_currentItem.text())
        for i_doc in self.__wvs:
            if i_doc.klicnummer == l_klicnummer:
                return i_doc

    def _layersInGroups(self):
        """
        Create legend groups (when this can be done properly)
        and move layers inside these legend groups
        This does not work in QGIS 1.6.0
        """
        self._createLayerGroups()
        if not self.__addGroupsBuggy:
            self._moveLayersToGroups()

    def _createLayerGroups(self, p_doc):
        """
        Create the layer groups that I want to use to move
        layers into.
        """
        l_legend = self.__legend
        l_groups = l_legend.groups()
        l_idLastGroup = 0
        l_groupNames = self.layerGroupNames() # dictionary for translations!
        l_groupIds = []
        
        for i_group in self.layerGroups: # list for order!
            l_groupName = l_groupNames[i_group]
            l_newGroupName = l_groupName
            l_index = 1
            
            while l_newGroupName in l_groups:
                # when exists create new groupname..
                l_index += 1
                l_newGroupName = l_groupName + str(l_index)
            
            l_id = l_legend.addGroup(l_newGroupName, True)
            l_groupIds.append(l_id)
            
            l_layerGroup = wv.LayerGroup(l_newGroupName)
            l_layerGroup.index = l_id
            p_doc.layerGroups[i_group] = l_layerGroup
        # in QGIS 1.6.0, unfortunately a bug was introduced.
        # the layergroups are nested and could not be used.
        # In that case remove added groups.
        if len(l_groupIds) > 1:
            if l_groupIds[1] == 0:
                self.__addGroupsBuggy = True
                l_legend.removeGroup(l_groupIds[0])

    def _moveLayersToGroups(self, p_doc):
        """
        Move the layers into groups that I want to use to move
        layers into
        """
        l_legend = self.__legend
        for i_layer in p_doc.layers:
            l_layer = i_layer.layer
            l_groupName = i_layer.groupName()
            l_layerGroup = p_doc.layerGroups[l_groupName]
#            l_layerName = i_layer.layerName()
#            l_string = "layer " + l_layerName +" verplaatsen naar " + l_groupName + "\nmet index " + str(l_layerGroup.index)
            l_legend.moveLayer(l_layer, l_layerGroup.index)
            self._updateAllLayerGroups(-1)
            
    def _updateGroupIndexesB4Remove(self):
        """
        reduce indexes of other groups of messages loaded at later stage
        before removing current message
        """
        l_doc = self.__wv
        l_nr = l_doc.klicnummer
        l_layer = l_doc.layers[0]
        l_groupName = l_layer.groupName()
        l_indexGroup = l_doc.layerGroups[l_groupName].index
        l_change = len(self.__wv.layers)+4
        for i_doc in self.__wvs:
            if i_doc.klicnummer == l_nr:
                continue
            if i_doc.layerGroups[l_groupName].index > l_indexGroup:
                self._updateLayerGroups(i_doc, -l_change)

    def _removeGroups(self):
        """
        removes legend groups and all layer groups underneath effectively
        """
        l_doc = self.__wv
        l_indexes = []
        for i_layerGroup in l_doc.layerGroups.itervalues():
            l_indexes.append(i_layerGroup.index)
        l_indexes.sort(reverse=True)
        l_legend = self.__legend
        for i_index in l_indexes:
            if l_legend.groupExists(i_index):
                l_legend.removeGroup(i_index)
            
    def _updateLayerGroup(self, p_oldIndex, p_new_index):
        """
        Keep index of groups synchronised with legend
        """
        QMessageBox.warning(self, "effe wachten", "update groepindex werkt!!")
        for i_doc in self.__wvs:
            for i_groupName, i_layerGroup in i_doc.layerGroups.iteritems():
                if p_oldIndex == i_layerGroup.index:
                    i_layerGroup.index = p_new_index
                    break
                
    def _updateAllLayerGroups(self, p_change):
        """
        As long signal does not work, just change all groupindexes by given change
        """
        for i_doc in self.__wvs:
            self._updateLayerGroups(i_doc, p_change)
    
    def _updateLayerGroups(self, p_doc, p_change):
        """
        As long signal does not work, just change all groupindexes by given change
        """
        for i_layerGroup in p_doc.layerGroups.itervalues():
            i_layerGroup.index += p_change
                
    def helpHelp(self):
        """
        starts the help manual which resides behind the help button
        """
        l_index = self.tr("index.html")
        form = helpform.HelpForm(l_index, self.tr("Wion Result Viewer"), self)
        form.show()

    def _setUnitToMeters(self):
        """
        set the units to meters when this plugin is activated.
        We do not want to bother user with setting mapunits from
        degrees to meters everytime. Now user can start to measure
        straight away distances in meters!
        """
        mapCanvas = self.__iface.mapCanvas()
        mapRenderer = mapCanvas.mapRenderer()
        mapRenderer.setMapUnits(0)

    def storeDialogPosition(self):
        """
        Store the current position of the dialog in a usersetting
        The next time the dialog is activated again the dialog
        should be there in the same place!
        """
        l_pos = self.pos()
        l_x = str(l_pos.x())
        l_y = str(l_pos.y())
        l_width = str(self.width())
        l_height = str(self.height())
        QSettings().setValue("b4udignl/last_xpos_dialog", l_x)
        QSettings().setValue("b4udignl/last_ypos_dialog", l_y)
        QSettings().setValue("b4udignl/last_width_dialog", l_width)
        QSettings().setValue("b4udignl/last_height_dialog", l_height)

    def restoreDialogPosition(self):
        """
        restore the current position of the dialog to the same
        position saved in the usersettings the last time
        the dialog was deactivated!
        """
        l_x = self.__settings["b4udignl/last_xpos_dialog"]
        l_y = self.__settings["b4udignl/last_ypos_dialog"]
        l_width = self.__settings["b4udignl/last_width_dialog"]
        l_height = self.__settings["b4udignl/last_height_dialog"]
        if l_x != "0" and l_y != "0":
            self.move(int(l_x), int(l_y))
            self.resize(int(l_width), int(l_height))

    def saveMessages(self):
        """
        Saves each wion message using pickle in textfile in a folder Wion
        next to Quantum GIS projectfile. Save also reference to this
        pickled object in project file itself.
        """
        l_project = QgsProject.instance()
        l_project_file = unicode(l_project.fileName())
        l_title = self.tr("Opslaan in project")
        if l_project_file == "":
            l_msg = self.tr("Nog niet opgeslagen als project!\nKies Bestand - Project opslaan...")
            QMessageBox.warning(self, l_title, l_msg)
        else:
            # save the project setting 'b4udignl' 'wv_docs_file' in project.
            # first it is added to the project object
            l_wvs_file = l_project_file.replace(".qgs", "_wv_docs.txt")
            l_wvs_file_name = os.path.basename(l_wvs_file)
            # write project setting
            l_project.writeEntry('b4udignl', 'wv_docs_file', l_wvs_file_name)
            l_file = open(l_wvs_file, 'w')
            l_wv_docs = self.docsToPickle()
            # use pickle to write a textfile holding object instance
            # that can be recreated.
            pickle.dump(l_wv_docs, l_file)
            # save the project immediately, this should be done otherwise
            # the project setting 'wv_docs_file' could be missing when
            # user decides upon leaving the project to Discard the changes.
            # Adding the project setting was considered a project change.
            l_action = self.__iface.actionSaveProject()
            # activate(0) triggers the action save project!
            l_action.activate(0)
            # inform the user that changes have been included in project.
            l_msg = self.tr("Wion berichten opgeslagen in project")
            QMessageBox.warning(self, l_title, l_msg)

    def docsToPickle(self):
        """
        return list of objects which easily can be written to textfile
        using pickle, it should be completely detached from QGIS.  
        """
        l_wv_docs =[]
        for i_wv_doc in self.__wvs:
            # for each wion document use pickle(), this method
            # gives back an object that can be saved to a textfile
            # using pickle!
            l_wv_docs.append(i_wv_doc.pickle())
        return l_wv_docs

    def restoreMessages(self):
        """
        Restores each wion message saved using pickle from textfile in a folder Wion
        next to Quantum GIS projectfile.
        """
        # now get from projectfile pickled objectstring from setting 'wvs_docs_file'
        l_project = QgsProject.instance()
        l_wvsFileName = unicode(l_project.readEntry('b4udignl', 'wv_docs_file')[0])
        #QMessageBox.warning(self, "opgehaalde settings", l_setting_wvs)
        
        if l_wvsFileName != "":
            l_dir = os.path.dirname(unicode(l_project.fileName()))
            l_fileName = os.path.join(l_dir, l_wvsFileName)
            l_file = open(l_fileName)
            # now use pickle to recreate object from file
            l_wvs = pickle.load(l_file)
            # connect qgis properly back to Wion messages.
            self.__wvs = l_wvs
            for i_wv in self.__wvs:
                i_wv.iface = ifaceqgis.Iface(self.__iface)
                i_wv.attachLayers()
                i_wv.attachThemes()
                
            if len(l_wvs)!= 0:
                self.__wv = l_wvs[0]
                self._populateMsgList()
                self._populateTree()
                self._setStateOfVisibilitiesThemes(True)
                self._setVisibilities()
                self._setUnitToMeters()
        
    def _removeMessages(self):
        """
        remove docs, empty message list, empty tree holding guiding documents
        This is called when create new project is called, then all layers are
        removed, so better also remove contents of other containers in plugin.
        """
        self.__wvs = []
        self.__wv = None
        self._populateMsgList()
        self._populateTree()
        self._setStateOfVisibilitiesThemes(True)
        self._setVisibilities()

        
