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
from PyQt4.QtCore import QSettings, QTranslator, QObject, SIGNAL
from PyQt4.QtGui import QApplication, QAction, QIcon
from qgis.core import QgsApplication
# Initialize Qt resources from file resources.py
import qrc_resources
# Add translations to translator
application = QgsApplication.instance()
localeName = QSettings().value("locale/userLocale", type=str)
translator = QTranslator()
translator.load("B4UdigNL_"+localeName, ":/")
# Add translator to application
application.installTranslator(translator)

# Import the code for the dialog
from B4UdigNLDialog import B4UdigNLDialog

class B4UdigNL: 

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.dialog = None

    def initGui(self):  
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/b4udignl.png"), \
            QApplication.translate("B4UdigNL","KLIC Viewer"), self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run) 

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(QApplication.translate("B4UdigNL","&KLIC Viewer"), self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        if self.dialog != None:
            self.dialog.storeDialogPosition()
        self.iface.removePluginMenu(QApplication.translate("B4UdigNL","&KLIC Viewer"),self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self): 
        # create and show the dialog
        if self.dialog is None:
            self.dialog = B4UdigNLDialog(self.iface)
        
        # show the dialog
        l_dialog = self.dialog
        # move the dialog to where it was the last time it was used!
        l_dialog.restoreDialogPosition()
        l_dialog.show()
        result = l_dialog.exec_()

