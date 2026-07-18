"""
/***************************************************************************
B4UdigNL
A QGIS plugin
View the result of a Dutch B4Udig request
                             -------------------
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
# Import the PyQt and QGIS libraries
from builtins import object
from qgis.PyQt.QtCore import QSettings, QTranslator
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtGui import QIcon, QAction
from qgis.core import QgsApplication
from qgis import utils
# Initialize Qt resources from file resources.py
from . import qrc_resources
# Add translations to translator
application = QgsApplication.instance()
localeName = QSettings().value("locale/userLocale", type=str)
translator = QTranslator()
translator.load("B4UdigNL_"+str(localeName), ":/")
# Add translator to application
application.installTranslator(translator)

# Import the code for the dialog
from .B4UdigNLDialog import B4UdigNLDialog

class B4UdigNL(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.dialog = None

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/b4udignl.png"), \
            QApplication.translate("B4UdigNL","KLIC Viewer"), self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(QApplication.translate("B4UdigNL","&KLIC Viewer"), self.action)
        self.help_action = QAction(QIcon(":/b4udignl.png"),
                                   "KLIC Viewer...",
                                   self.iface.mainWindow())
        # Add the action to the Help menu
        self.iface.pluginHelpMenu().addAction(self.help_action)
        self.help_action.triggered.connect(self.show_help)

    @staticmethod
    def show_help():
        """ Open the help manual for this plugin. """
        utils.showPluginHelp()
        
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(QApplication.translate("B4UdigNL","&KLIC Viewer"),self.action)
        self.iface.removeToolBarIcon(self.action)
        self.iface.pluginHelpMenu().removeAction(self.help_action)
        del self.help_action

    # run method that performs all the real work
    def run(self):
        # create and show the dialog
        if self.dialog is None:
            self.dialog = B4UdigNLDialog(self.iface)

        # show the dialog
        l_dialog = self.dialog
        l_dialog.show()
        result = l_dialog.exec()
