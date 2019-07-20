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
import os, sys
from qgis.PyQt.QtCore import QSettings

# add svg path that holds svg symbols to settings when neccesary
plugin_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(plugin_path)
svg_path = os.path.join(plugin_path, 'styles', 'svg')
# first check if we a settings exist for SVG paths, if not add it first!
if not 'svg/searchPathsForSVG' in QSettings().allKeys():
    QSettings().setValue('svg/searchPathsForSVG', [svg_path])
# next check if path exists in setting, if not add it!
svg_paths = QSettings().value('svg/searchPathsForSVG')
# fix a problem from the past (setting exist but does not hold list)
if type(svg_paths) is not list:
    QSettings().setValue('svg/searchPathsForSVG', [svg_path])
    svg_paths = QSettings().value('svg/searchPathsForSVG')
# finally when setting existed, was a list and does not contain svg_path
# to symbols used for plugin, add it to the list.
if svg_path not in svg_paths:
    svg_paths.append(svg_path)
    QSettings().setValue('svg/searchPathsForSVG', svg_paths)

def classFactory(iface):
    # load B4UdigNL class from file B4UdigNL
    from .B4UdigNL import B4UdigNL
    return B4UdigNL(iface)
