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
 Include following statement in ui_B4UdigNL.py after updating with designer
 from qgis.gui import QgsColorButton

 and remove last line:
 from qgscolorbutton import QgsColorButton
"""

from PyQt4.QtCore import QSettings, SIGNAL, pyqtSignature
from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox, QListWidgetItem, \
     QTreeWidgetItem
from qgis import utils
from qgis.core import QgsProject
from ui_B4UdigNL import Ui_B4UdigNL
import ifaceqgis, os
from core import wv
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
                  "elec_land": "landelijk hoogspanningsnet",
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
        self.restoreMessages()

    def doc(self):
        return self.__wv

    def _iface(self):
        doc = self.doc()
        if doc is not None:
            return doc.iface
        
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
                         l_names["elec_land"]: l_ui.checkBoxElec_land,                        l_names["sewer_free"]: l_ui.checkBoxSewer_free,
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
        l_headers = self.tr("Soort Bijlage/Naam Bijlage")
        l_tree.setHeaderLabels([l_headers])
        l_ui.textEditDirPreffered.setText(self.__settings["b4udignl/dir_preferred"])
        self._setVisibilities()

    def makeConnections(self):
        """makes all neccesary connections between signals and slots"""
        self.connect(self.ui.treeWidget,
                     SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"),
                     self._openPdf)
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
        self.connect(self.ui.checkBoxElec_land,
                     SIGNAL("stateChanged(int)"),
                     self._checkBoxElecLandStateChanged)
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
        self.connect(self.ui.rasterCheckBox,
                     SIGNAL("stateChanged(int)"),
                     self._rasterCheckBoxStateChanged)
        self.connect(self.ui.vectorCheckBox,
                     SIGNAL("stateChanged(int)"),
                     self._vectorCheckBoxStateChanged)
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
    def _checkBoxElecLandStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["elec_land"], p_state)
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
    
    def _rasterCheckBoxStateChanged(self, p_state):
        self._turn_all_raster(p_state)
        doc = self.doc()
        doc.showRaster = p_state != 0

    def _vectorCheckBoxStateChanged(self, p_state):
        self._turn_all_vector(p_state)
        doc = self.doc()
        doc.showVector = p_state != 0

    def _turn_all_raster(self, p_state):
        doc = self.doc()
        show_vector = doc.showVector
        doc.showRaster = True
        doc.showVector = False
        # now turn of all raster!
        self._updateAllThemes(p_state)
        doc.showVector = show_vector
        
    def _turn_all_vector(self, p_state):
        doc = self.doc()
        show_raster = doc.showRaster
        doc.showRaster = False
        doc.showVector = True
        # now turn of all raster!
        self._updateAllThemes(p_state)
        doc.showRaster = show_raster

    def _updateAllThemes(self, p_state):
        doc = self.doc()
        state = 0
        if p_state != 0:
            state = 2
        for theme in doc.themes.keys():
            self._themeStateChanged(theme, state)

    def _themeStateChanged(self, p_theme, p_state):
        """
        a theme has changed and now the visibility of layers belonging
        to that theme will change (when neccesary)
        """
        doc = self.doc()
        if doc is not None and doc.themes.has_key(p_theme):
            if p_state <> 1:
                theme = doc.themes[p_theme]
                theme.setVisibility(p_state)
                self._setStateOfVisibilitiesThemes(True)
                self._iface().refreshMap()
            
    def _setVisibilities(self):
        """ update visibilities of buttons"""
        ui = self.ui
        doc = self.doc()
        if self.doc() is None:
            ui.gotoButton.setEnabled(False)
            ui.bestScaleButton.setEnabled(False)
            ui.removeMsgButton.setEnabled(False)
            ui.openDocButton.setEnabled(False)
            ui.saveButton.setEnabled(False)
            ui.refreshButton.setEnabled(False)
            ui.rasterCheckBox.setEnabled(False)
            ui.vectorCheckBox.setEnabled(False)
        else:
            ui.gotoButton.setEnabled(True)
            ui.bestScaleButton.setEnabled(True)
            ui.removeMsgButton.setEnabled(True)
            ui.openDocButton.setEnabled(True)
            # first release without save button enabled!
##            ui.saveButton.setEnabled(True)
            ui.refreshButton.setEnabled(True)
            # storage_version indicates if an imkl v1 or v2 is processed
            # imkl v1 does not have vectors, so do not enable the buttons
            # there are only rasters
            storage_version = doc._storage_version_to_use()
            if storage_version == 2:
                ui.rasterCheckBox.setEnabled(True)
                ui.vectorCheckBox.setEnabled(True)
                ui.rasterCheckBox.setCheckState(2)
                ui.vectorCheckBox.setCheckState(2)
            elif storage_version == 1:
                ui.rasterCheckBox.setEnabled(False)
                ui.vectorCheckBox.setEnabled(False)
                ui.rasterCheckBox.setCheckState(2)
                ui.vectorCheckBox.setCheckState(0)
        self._setVisibilitiesThemes()

    def _setVisibilitiesThemes(self):
        doc = self.doc()
        if doc is None:
            for i_checkbox in self.__themes.itervalues():
                i_checkbox.setEnabled(False)
        else:
            for i_theme, i_checkbox in self.__themes.iteritems():
                if doc.themes.has_key(i_theme):
                    i_checkbox.setEnabled(True)
                else:
                    i_checkbox.setEnabled(False)
 
    def _setStateOfVisibilitiesThemes(self, p_actual=False):
        """
        Set state of visibilies for themes in menu.
        When actual is True actual state of visibilities is checked
        which is slower. 
        """
        for i_theme in self.__themes.keys():
            if self.doc() is None:
                checkbox = self.__themes[i_theme]
                checkbox.setCheckState(0)
            else:
                self._setStateOfVisibilitiesTheme(i_theme, p_actual)

    def _setStateOfVisibilitiesTheme(self, theme_name, actual):
        """
        Set state of visibilies for a theme.
        When actual is True current state of visibility is checked
        which is slower. 
        """
        doc = self.doc()
        if doc.themes.has_key(theme_name):
            theme = doc.themes[theme_name]
            checkbox = self.__themes[theme_name]
            if theme is not None:
                try:
                    state = theme.checkVisible(actual)
                except ZeroDivisionError:
                    self._displayThemesVisibilyMsg(theme.name)
                    state = 1
                checkbox.setCheckState(state)
 
    @pyqtSignature("")
    def on_openMsgButton_clicked(self):
        """opens directory search dialog and sets my attribute __dir"""
        l_path = self._start_find_path()
        
        #l_request = "Select directory which hold result request Dig ALert"
        l_request = self.tr("Selecteer folder met KLIC bericht")
        l_dir_path = QFileDialog.getExistingDirectory(self, l_request, l_path)
        if l_dir_path: # evaluates to true when it contains anything
            self.__dir = str(l_dir_path)
            QSettings().setValue("b4udignl/dir_last_used", str(l_dir_path))
            self._loadMsg()
            
    @pyqtSignature("")
    def on_openArchiveButton_clicked(self):
        """opens directory search dialog and sets my attribute __dir"""
        l_path = self._start_find_path()
        
        #l_request = "Select zipfile which holds result request Dig ALert"
        l_request = self.tr("Selecteer een zip bestand die een KLIC bericht bevat")
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
        returns path that should be used to look for next b4udig message to load
        this path can be stored in user setting dir_preffered
        when user setting is not set it then uses last directory used
        to open a b4udig message. 
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
            # this is probably test KLIC message
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
        doc = self.doc()
        if doc is not None:
            doc.goto()

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
        l_mapCanvas = self.__iface.mapCanvas()
        l_mapCanvas.setRenderFlag(False)
        l_doc.removeLayers()
        l_mapCanvas.setRenderFlag(True)
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
        doc = self.doc()
        if doc is not None:
            doc.bestScale()

    @pyqtSignature("")
    def on_optionMsgDirButton_clicked(self):
        """
        select directory which will be used to start searching
        KLIC messages from when using openMsgButton
        """
        l_path = self.__settings["b4udignl/dir_preferred"]
        l_request = self.tr("Selecteer standaard folder met KLIC berichten")
        l_dir_path = QFileDialog.getExistingDirectory(self, l_request, l_path)
        if l_dir_path: # if l_dir_path is not empty this evaluates to true..
            self.__settings["b4udignl/dir_preferred"] = str(l_dir_path)
            QSettings().setValue("b4udignl/dir_preferred", l_dir_path)
            self.ui.textEditDirPreffered.setText(l_dir_path)

    def _loadMsg(self):
        doc = self._openMsg(unicode(self.__dir))
        if doc is None:
            return
        doc.iface = ifaceqgis.Iface(self.__iface)
        self.__wv = doc
        self.__wvs.append(doc)
        self._populateMsgList()
        self._populateTree()
        iface = doc.iface
        iface.doRendering(False)
        doc.loadLayers()
        iface.refreshLegend()
        self._setStateOfVisibilitiesThemes()
        self._setVisibilities()
        iface.doRendering(True)

    def _openMsg(self, p_path):
        """
        p_path = directory path where KLIC message can be found.
        returns object of type Doc holding all information read from xml
        found in given path.
        """
        try:
            doc = wv.Doc(p_path)
        except IOError:
            self._displayWrongMsg()
            return None
        if doc.version is None:
            self._displayWrongMsg()
            return None
        return doc

    def _displayWrongMsg(self):
        """
        give a warning to user that KLIC message could not be read
        from selected folder
        """
        l_titleMsg = self.tr("Fout KLIC bericht")
        l_errorMsg = self.tr("Geselecteerde folder bevat geen goed\n\
        KLIC bericht of kan niet worden geopend!")
        QMessageBox.warning(self, l_titleMsg, l_errorMsg)

    def _displayThemesVisibilyMsg(self, p_theme=None):
        title = u"ThemesVisibilities"
        msg = u"Toon Visibilities Themes\n"
        doc = self.doc()
        for i_theme in self.__themes.keys():
            theme = None
            if doc.themes.has_key(i_theme):
                if p_theme is not None and i_theme != p_theme:
                    continue
                theme = doc.themes[i_theme]
##                theme.checkVisible()
                layers = theme.layers
                themes_vis = {}
                for layer in layers:
                    themes_vis[layer.layerName] = layer.themes_visible
                theme_str = '%s: %i:\n%s \n' % (theme.name,
                                                theme.visible,
                                                themes_vis)
                msg += theme_str
        QMessageBox.information(self, title, msg)        

    def _openPdf(self, pdfItem):
        """use name of PDF to get right pdf and open it"""
        l_pdfName = unicode(pdfItem.text(0))
        doc = self.doc()
        for i_pdf in doc.pdfFiles:
            if i_pdf.name == l_pdfName:
                i_pdf.openPdf()
                break

    def _populateMsgList(self):
        """populates list of KLIC messages"""
        l_selected = None
        l_ui = self.ui
        l_list = l_ui.msgListWidget
        l_list.clear()
        for i_doc in self.__wvs:
##            QMessageBox.information(self, "Add message",
##                                    "Add klic message" + i_doc.klicnummer)
            l_klicnummer = i_doc.klicnummer
            l_item = QListWidgetItem(l_klicnummer)
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
        doc = self.doc()
        if doc is None:
            return
        l_tree.setColumnCount(1)
        l_tree.setItemsExpandable(True)
        parentTypePdf = {}
        pdf_files = doc.pdfFiles
        if pdf_files is None:
            return
        for i_pdf in pdf_files:
            parent = parentTypePdf.get(i_pdf.type)
            if parent is None:
                parent = QTreeWidgetItem(l_tree,[i_pdf.type])
            parentTypePdf[i_pdf.type] = parent
            item = QTreeWidgetItem(parent, [i_pdf.name])
            l_tree.expandItem(parent)
            l_tree.resizeColumnToContents(0)

    def _changeDoc(self, p_currentItem):
        """When user selects other message change other plugin elements as well"""
        doc = self._selectedMsg(p_currentItem)
        if doc != None:
            self.__wv = doc
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
               
    def helpHelp(self):
        """
        starts the help manual which resides behind the help button
        """
        utils.showPluginHelp()

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
        Saves each KLIC message using pickle in textfile in a folder KLIC
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
            l_msg = self.tr("KLIC berichten opgeslagen in project")
            QMessageBox.warning(self, l_title, l_msg)

    def docsToPickle(self):
        """
        return list of objects which easily can be written to textfile
        using pickle, it should be completely detached from QGIS.  
        """
        l_wv_docs =[]
        for i_wv_doc in self.__wvs:
            # for each KLIC document use pickle(), this method
            # gives back an object that can be saved to a textfile
            # using pickle!
            l_wv_docs.append(i_wv_doc.pickle())
        return l_wv_docs

    def restoreMessages(self):
        """
        Restores each KLIC message saved using pickle from textfile in a folder KLIC
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
            # connect qgis properly back to KLIC messages.
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

        
