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
from __future__ import absolute_import

from builtins import str
from qgis.PyQt.QtCore import QSettings, pyqtSlot
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox, QListWidgetItem, QTreeWidgetItem
from qgis import utils
from qgis.core import QgsProject
from .ui_B4UdigNL import Ui_B4UdigNL
from ifaceqgis import Iface
import os, gc
from .core import wv
import unzip, zipfile

# create the dialog
class B4UdigNLDialog(QDialog):
    layerGroups = ["annotatie",
                   "maatvoering",
                   "ligging",
                   "topo"]

    themeNames = {"data": "datatransport",
                  "gas_low": "gaslagedruk",
                  "gas_high": "gashogedruk",
                  "danger": "buisleidinggevaarlijkeinhoud",
                  "elec_low": "laagspanning",
                  "elec_mid": "middenspanning",
                  "elec_high": "hoogspanning",
                  "elec_land": "landelijkhoogspanningsnet",
                  "sewer_free": "rioolvrijverval",
                  "sewer_pressure": "rioolonderoverofonderdruk",
                  "heat": "warmte",
                  "water": "water",
                  "chemical": "petrochemie",
                  "orphan": "wees",
                  "other": "overig"}
    """
    now add to this shared class variable also the layerGroupThemes
    """
    for i_groupName in list(wv.Layer.layerGroupNames.keys()):
        themeNames[i_groupName] = i_groupName

    def __init__(self, iface):
        QDialog.__init__(self)
        self.__iface = iface
##        self.__legend = iface.legendInterface()
        self.__result_file = None
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

    def doc(self):
        return self.__wv

    def layerGroupNames(self):
        """returns dictionary with legend groups"""
        return {"annotatie": self.tr("Annotatie"),
                "maatvoering": self.tr("Maatvoering"),
                "ligging": self.tr("Ligging"),
                "topo": self.tr("Topo")}

    def _userSettings(self):
        """return dictionary with user settings"""
        l_settings = {"b4udignl/dir_preferred": ".",
                      "b4udignl/dir_last_used": "."}
        s = QSettings()
        for i_key, i_value in l_settings.items():
            # try to read user settings from system configuration
            try:
                l_user_value = s.value(i_key, type=str)
            except TypeError as e:
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
                         l_names["elec_land"]: l_ui.checkBoxElec_land,
                         l_names["sewer_free"]: l_ui.checkBoxSewer_free,
                         l_names["sewer_pressure"]: l_ui.checkBoxSewer_pressure,
                         l_names["heat"]: l_ui.checkBoxHeat,
                         l_names["water"]: l_ui.checkBoxWater,
                         l_names["chemical"]: l_ui.checkBoxChemical,
                         l_names["orphan"]: l_ui.checkBoxOrphan,
                         l_names["other"]: l_ui.checkBoxOther,
                         l_names["annotatie"]: l_ui.annotationCheckBox,
                         l_names["maatvoering"]: l_ui.dimensioningCheckBox,
                         l_names["ligging"]: l_ui.locationCheckBox,
                         l_names["topo"]: l_ui.topoCheckBox}

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
        self.ui.treeWidget.itemDoubleClicked.connect(self._openPdf)
        self.ui.checkBoxData.stateChanged.connect(self._checkBoxDataStateChanged)
        self.ui.checkBoxGas_low.stateChanged.connect(self._checkBoxGasLowStateChanged)
        self.ui.checkBoxGas_high.stateChanged.connect(self._checkBoxGasHighStateChanged)
        self.ui.checkBoxDanger.stateChanged.connect(self._checkBoxDangerStateChanged)
        self.ui.checkBoxElec_low.stateChanged.connect(self._checkBoxElecLowStateChanged)
        self.ui.checkBoxElec_mid.stateChanged.connect(self._checkBoxElecMidStateChanged)
        self.ui.checkBoxElec_high.stateChanged.connect(self._checkBoxElecHighStateChanged)
        self.ui.checkBoxElec_land.stateChanged.connect(self._checkBoxElecLandStateChanged)
        self.ui.checkBoxSewer_free.stateChanged.connect(self._checkBoxSewerFreeStateChanged)
        self.ui.checkBoxSewer_pressure.stateChanged.connect(self._checkBoxSewerPressureStateChanged)
        self.ui.checkBoxHeat.stateChanged.connect(self._checkBoxHeatStateChanged)
        self.ui.checkBoxWater.stateChanged.connect(self._checkBoxWaterStateChanged)
        self.ui.checkBoxChemical.stateChanged.connect(self._checkBoxChemicalStateChanged)
        self.ui.checkBoxOrphan.stateChanged.connect(self._checkBoxOrphanStateChanged)
        self.ui.checkBoxOther.stateChanged.connect(self._checkBoxOtherStateChanged)
        self.ui.rasterCheckBox.stateChanged.connect(self._rasterCheckBoxStateChanged)
        self.ui.vectorCheckBox.stateChanged.connect(self._vectorCheckBoxStateChanged)
        self.ui.annotationCheckBox.stateChanged.connect(self._annotationCheckBoxStateChanged)
        self.ui.dimensioningCheckBox.stateChanged.connect(self._dimensioningCheckBoxStateChanged)
        self.ui.locationCheckBox.stateChanged.connect(self._locationCheckBoxStateChanged)
        self.ui.topoCheckBox.stateChanged.connect(self._topoCheckBoxStateChanged)
        self.__iface.newProjectCreated.connect(self._removeMessages)

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
        self._themeStateChanged(self.themeNames["annotatie"], p_state)
    def _dimensioningCheckBoxStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["maatvoering"], p_state)
    def _locationCheckBoxStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["ligging"], p_state)
    def _topoCheckBoxStateChanged(self, p_state):
        self._themeStateChanged(self.themeNames["topo"], p_state)

    def _rasterCheckBoxStateChanged(self, p_state):
        isVector = False 
        self._rasterVectorCheckBoxStateChanged(p_state, isVector)

    def _vectorCheckBoxStateChanged(self, p_state):
        isVector = True
        self._rasterVectorCheckBoxStateChanged(p_state, isVector)

    def _rasterVectorCheckBoxStateChanged(self, p_state, isVector):
        doc = self.doc()
        if doc is not None:
            if p_state == 0:
                # turn of all raster/vector layers
                self._updateAllThemes(p_state, isVector)
                if isVector:
                    doc.showVector = p_state
                else:
                    doc.showRaster = p_state
            else:
                # turn on all raster/vector layers, but first change the state
                # of doc.showRaster/doc.showVector to be able to change
                # the visibility (otherwise changing the status will be ignored).
                if isVector:
                    doc.showVector = p_state
                else:
                    doc.showRaster = p_state
                self._updateAllThemes(p_state, isVector)

    def _updateAllThemes(self, p_state, isVector):
        doc = self.doc()
        for theme in list(doc.themes.keys()):
            self._themeStateChanged(theme, p_state, isVector)

    def _themeStateChanged(self, p_theme, p_state, isVector=None):
        """
        a theme has changed and now the visibility of layers belonging
        to that theme will change (when neccesary)
        """
        doc = self.doc()
        if doc is not None and p_theme in doc.themes:
            if p_state != 1:
                theme = doc.themes[p_theme]
                theme.setVisibility(p_state, isVector)
                self._setStateOfVisibilitiesThemes(True)
                doc.iface.refreshMap()

    def _displayThemeStateChanged(self, p_theme, p_state):
        """
        give a warning to user that KLIC message could not be read
        from selected folder
        """
        l_titleMsg = "Status Thema Gewijzigd"
        l_msg = "Status is nu %s voor thema %s" % (p_state, str(p_theme))
        QMessageBox.information(self, l_titleMsg, l_msg)


    def _checkEvs(self):
        """check if this delivery contains special PDF's with special instructions"""
        doc = self.doc()
        pdf_files = doc.pdfFiles
        evs = 0
        for i_pdf in pdf_files:
            type_pdf = i_pdf.type
            if type_pdf == "eisVoorzorgsmaatregel":
                evs +=1
        if evs > 0:
            self._displayEisVoorzorgsmaatregel(evs)
            

    def _displayEisVoorzorgsmaatregel(self, evs):
        """
        give a warning to user that this KLIC message contains an EV
        (Eis voorzorgsmaatregel), this means take contact with company
        that has issued this special warning.
        """
        l_titleMsg = "Dit bericht bevat "
        if evs > 1:
            l_titleMsg += "meerdere Eis Voorzorgsmaatregelen!"
        else:
            l_titleMsg += "een Eis Voorzorgsmaatregel!"
        l_msg = "Lees de Eis Voorzorgsmaatregel(en)!\n\n \
Hierin staat dat u verplicht bent contact op te nemen\n\
met de netbeheerder, voor aanvang van graafwerkzaamheden."
        QMessageBox.warning(self, l_titleMsg, l_msg)


    def _setVisibilities(self):
        """ update visibilities of buttons"""
        ui = self.ui
        doc = self.doc()
        if doc is None:
            ui.gotoButton.setEnabled(False)
            ui.bestScaleButton.setEnabled(False)
            ui.removeMsgButton.setEnabled(False)
            ui.openDocButton.setEnabled(False)
            ui.refreshButton.setEnabled(False)
            ui.rasterCheckBox.setEnabled(False)
            ui.vectorCheckBox.setEnabled(False)
            ui.resultFileWidget.setEnabled(True)
            ui.openMsgButton.setEnabled(True)
            ui.openArchiveButton.setEnabled(True)
        else:
            ui.openMsgButton.setEnabled(False)
            ui.openArchiveButton.setEnabled(False)
            ui.gotoButton.setEnabled(True)
            ui.bestScaleButton.setEnabled(True)
            ui.removeMsgButton.setEnabled(True)
            ui.openDocButton.setEnabled(True)
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
            for i_checkbox in self.__themes.values():
                i_checkbox.setEnabled(False)
        else:
            for i_theme, i_checkbox in self.__themes.items():
                if i_theme in doc.themes:
                    i_checkbox.setEnabled(True)
                else:
                    i_checkbox.setEnabled(False)

    def _setStateOfVisibilitiesThemes(self, p_actual=False):
        """
        Set state of visibilies for themes in menu.
        When actual is True actual state of visibilities is checked
        which is slower.
        """
        for i_theme in list(self.__themes.keys()):
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
        if theme_name in doc.themes:
            theme = doc.themes[theme_name]
            checkbox = self.__themes[theme_name]
            if theme is not None:
                try:
                    state = theme.checkVisible(actual)
                except ZeroDivisionError:
                    self._displayThemesVisibilyMsg(theme.name)
                    state = 1
                checkbox.setCheckState(state)

    def on_resultFileWidget_fileChanged(self):
        l_path = self.ui.resultFileWidget.filePath()
        self.__result_file = l_path
        title = u"Geopackage Selected"
        msg = "Geselecteerde geopackage is de volgende:\n%s" % l_path
        QMessageBox.information(self, title, msg)

    @pyqtSlot()
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

    @pyqtSlot()
    def on_openArchiveButton_clicked(self):
        """opens directory search dialog and sets my attribute __dir"""
        l_path = self._start_find_path()

        #l_request = "Select zipfile which holds result request Dig ALert"
        l_request = self.tr("Selecteer een zip bestand die een KLIC bericht bevat")
        l_filter = self.tr("Zip bestanden (*.zip *.ZIP)")
        l_fileName, __ = QFileDialog.getOpenFileName(self, l_request, l_path, l_filter)
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

    @pyqtSlot()
    def on_refreshButton_clicked(self):
        """refreshes the state of all themes"""
        self._setStateOfVisibilitiesThemes(True)

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

    @pyqtSlot()
    def on_msgListWidget_itemSelectionChanged(self):
        """change the current document"""
        l_listWidget = self.ui.msgListWidget
        l_item = l_listWidget.currentItem()
        self._changeDoc(l_item)

    @pyqtSlot()
    def on_openDocButton_clicked(self):
        """opens the selected document delivered in result digAlert request"""
        l_items = self.ui.treeWidget.selectedItems()
        for i_item in l_items:
            self._openPdf(i_item)

    @pyqtSlot()
    def on_closeButton_clicked(self):
        """hides (closes) the window"""
        self.close()

    @pyqtSlot()
    def on_helpButton_clicked(self):
        """opens the help manual"""
        self.helpHelp()

    @pyqtSlot()
    def on_gotoButton_clicked(self):
        """goto extent of map current message"""
        doc = self.doc()
        if doc is not None:
            doc.goto()

    @pyqtSlot()
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
        self.__wvs.remove(self.__wv)
        self.__wv = next(iter(self.__wvs), None)
        self._populateMsgList()
        self._populateTree()
        self._setStateOfVisibilitiesThemes(True)
        self._setVisibilities()
        gc.collect()

    @pyqtSlot()
    def on_bestScaleButton_clicked(self):
        """set best scale for current message"""
        doc = self.doc()
        if doc is not None:
            doc.bestScale()

    @pyqtSlot()
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
        doc = self._openMsg()
        if doc is None:
            return
        doc.iface = Iface(self.__iface)
        self.__wvs.append(doc)
        self.__wv = doc
        self._populateMsgList()
        self._populateTree()
        l_iface = doc.iface
        l_iface.doRendering(False)
        self._loadLayers()
        l_iface.refreshLegend()
        self._setStateOfVisibilitiesThemes()
        self._setVisibilities()
        l_iface.doRendering(True)
        self._checkEvs()

    def _loadLayers(self):
        doc = self.doc()
        s = QSettings()
        # prevent prompt for crs during load of layers
        oldValidation = s.value( "/Projections/defaultBehavior" )
        oldCrs = s.value('Projections/layerDefaultCrs')
        s.setValue( "/Projections/defaultBehavior", 'useGlobal' )
        s.setValue( "/Projections/layerDefaultCrs", 'EPSG:28992' )
        doc.loadLayers()
        s.setValue( "/Projections/defaultBehavior", oldValidation)        
        s.setValue( "/Projections/layerDefaultCrs", oldCrs)        

    def _openMsg(self):
        """
        Returns object of type Doc holding all information
        read from xml found in given path.
        """
        self._displayFolderToProcess()        
        doc = None
        try:
            doc = wv.Doc(self.__dir, self.__result_file)
        except IOError:
            self._displayWrongMsg()
            return None
        if doc.version is None:
            self._displayWrongMsg()
            return None
        return doc

    def _displayFolderToProcess(self):
        """
        give a warning to user that KLIC message could not be read
        from selected folder
        """
        title = "Folder KLIC bericht"
        msg = "Geselecteerde folder is de volgende:\n%s" % self.__dir
        QMessageBox.information(self, title, msg)

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
        for i_theme in list(self.__themes.keys()):
            theme = None
            if i_theme in doc.themes:
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
        l_pdfName = str(pdfItem.text(0))
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
            if l_klicnummer == self.doc().klicnummer:
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
            doc.goto()

    def _selectedMsg(self, p_currentItem):
        """returns Doc being selected message in list"""
        if p_currentItem is None:
            return
        l_klicnummer = str(p_currentItem.text())
        for i_doc in self.__wvs:
            if i_doc.klicnummer == l_klicnummer:
                return i_doc

    def helpHelp(self):
        """
        starts the help manual which resides behind the help button
        """
        utils.showPluginHelp()


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
