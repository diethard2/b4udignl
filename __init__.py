"""
/***************************************************************************
B4UdigNL
A QGIS plugin
View the result of a Dutch B4Udig request
                             -------------------
begin                : 2010-05-18 
copyright            : (C) 2011 by Diethard Jansen
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
 This script initializes the plugin, making it known to QGIS.
"""

def name(): 
    return "WION result viewer" 
def description():
    return "View the result of a Dutch B4Udig request"
def version():
    return "Version 1.3.2" 
def icon():
    return "images/b4udig48.png"
def qgisMinimumVersion():
    return "1.6"
def classFactory(iface): 
    # load B4UdigNL class from file B4UdigNL
    from B4UdigNL import B4UdigNL
    return B4UdigNL(iface)

    
    
    
    


