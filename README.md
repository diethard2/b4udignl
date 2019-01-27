b4udignl
========

The QGIS KLIC Viewer plugin, a python plugin that can be used to view Dutch b4udig information

Installation
------------
First you need an installation of QGIS! 
Download QGIS v. 2.18 from www.qgis.org.

Use QGIS Python Plugin Installer for installation of this plugin.

You can also manually unzip and place contents of b4udignl.zip
in your home folder ~/.qgis2/python/plugins/

Release notes
-------------
**version 2.0.3** 27/01/2018
Fixed loading detailkaarten (Themabijlagen) as rasterlayers.
Improved style of depth measurement object DiepteNAP en DiepteTovMaaiveld.
Forced garbage collect takes place after removing KLIC message.

**version 2.0.2** 19/01/2018
Renamed Quantum GIS to QGIS in documentation (and this file)
Now GML curves are also supported for Vector Geometry of pipelines
After loading each KLIC message, a full garbage collect is done after removing temporary datamodel

**version 2.0.1** 05/01/2018
fixed max qgis version to 2.99 so it will also be loaded in QGIS version 2.18.22.
fixed problem with not adding SVG path with style symbols for this plugin when no svg symbols were added.
Fixed problem with wrong style for Graafpolygoon (selected area to dig)
removed unit tests and testdata from packaged delivery

**Version 2.0.0** 31/12/2018
Major update where interface remains the same, but instead of loading rasters now also Vector information is loaded.
From 02/01/2019 the format of the result requested from Kadaster has changed a lot.
Previous versions of Klicviewer for QGIS can not be used to view the new results.
This new version can be used to view old KLIC messages.

**Version 1.4.3**
Added maximum version 2.18 as preparation for update to QGIS 4.3

**Version 1.4.2** 02/01/2015
fixed:
* encoding issue that prevented some messages from opening because xml included funny characters.

**Version 1.4.1** 
Updated metadata.txt and added a [webpage](http://diethard2.github.io/b4udignl). unfortunately forgot to release this version..

**Version 1.4.0** 20/06/2013
Updated plugin so it works as well for QGIS 2.0
Changed name of plugin from QGIS WION Result Viewer to
the QGIS KLIC Viewer.
Removed the grouping of loaded layers because the code was complicated
and because the QGIS grouping functions of layers behaved weird.
Updated the help function.


**Version 1.3.2** 27/06/2012
Moved this plugin to official QGIS plugins repository.
Tested for QGIS 1.8.0 and plugin still works great.
Repository from site http://wwww.gis-plugins.nl will be removed after
succesfull transfer.


**Version 1.3.1** 12/01/2011
New functionality:
*  now you are allowed to forget to open Wion Viewer plugin
   before opening a project. when you have stored information
   from plugin in project, the plugin will be filled with wion
   message information.


**Version 1.3.0** 27/12/2010
This new version can only be used for QGIS v. 1.6.0 and up!

New functionality:
* contents of plugin can now be stored in project.
  This is a major enhancement because now you can, after
  loading de wion messages, also add your own design layers
  or layers with dimensioning.
  When project is created and is saved from wion plugin
  in project, immediately everything is back in same state
  as when you saved the project. This means you can open
  pdf documents from wion message and use themes to set
  visibility.
* when selecting File - New project, all information from plugin is removed as well.
* plugin remembers width and height of plugin window you used before.

**Version 1.2.5** 11/12/2010
New functionality:
* plugin remembers position of window and starts in same position as before (no need to drag plugin window to pleasing position every time)
Fixed:
* when loading a second digalert message in 1.6.0., legend groups were still created in a nested way. Stopped creating legend groups for 1.6.0.
    
**Version 1.2.4** 04/12/2010
New functionality:
* new version that can be used as wel for QGIS v. 1.6.0
* in Themes Tab, 4 themes have been added, topo, location dimensioning and annotation.
* in 1.6.0 the layerGroups topo location dimension and annotation are not created in layers panel because adding groups was buggy. In 1.5.0 the layers are still created.
     

**Version 1.2.3** 30/11/2010
(last release before adding a new version for QGIS v. 1.6.0)
Fixed:
* loading a zipped folder under Ubuntu.  


Version 1.2.2 26/11/2010
New functionality:
* added tab Options where you can set default folder where to start searching as a user setting. 
Fixed:
* loading a zipped folder under Ubuntu.  


Versions 1.2.1 31/10/2010
New functionality:
* Improved performance!!
  * loading Wion Result (25.5 -> 16.5 seconds)
  * closing loaded Wion Result (9.5 -> 0.5 seconds)
  * changing visibility of a Theme (6.5 -> 2.3 seconds)
So I believe a new release is justifiable.
(Performance figures are based on using testmessage
 09G267447_1 which can be downloaded from www.klicviewer.nl
 on my own pretty old Windows PC). 


Version 1.2.0 28/10/2010
New functionality:
1. added functionality for improved control on visibilities of layers.
  * A Themes Tab to turn/of visibilities of several layers belonging to the same theme
  * Loading layers in legend groups, so you can turn al labels/dimensioning on or of.
2. added a button [Best scale] to get best view from Button.
3. added a button on Tabs theme [Refresh] to make refresh the status of themes whenever necessary.
4. improved understanding of Wion Result by actually adding a Map Legend in Themes Tab and named legend groups in layers panel.

Version 1.1.3
fixed: 
* Make plugin open any zipped files (test images/renamed zipfiles)
New functionality:
* When starting Wion Result Viewer, unit is changed to meters. This becomes visible after refresh or after first load.

version 1.1.2
Fixed: 
* Make plugin open zipped files delivered by Kadaster

version 1.1.1
Fixed: 
* Make plugin multilingual for QGIS Thethys as well

Version 1.1.0
New functionality:
1. Opening zipped file
2. better support for working with more loaded messages
  * Goto function loaded & selected message
  * Close message function to unload loaded message.
3. Open an accompanying documents instantly using doubleklic
4. Change visibility of buttons whether message is loaded.

This version is probably the last version that works with
previous releases of QGIS. The next one is only
supported from QGIS version 1.5 onwards! 

Version 1.0.2
First official release!

Tested with QGIS 1.0.2 (Kore), 1.3 (Mimas) and 1.4
(Enceladus) on following OS systems: Windows XP, Vista, 7,
Unbuntu & OSX (mac) Help manuals (browser) included!
Translations available: English and Dutch

Functionality (for more information manual from Help manual)
1. Load WION message from given Directory.
2. Many PNG's are made visible with Dutch RD coordinate system.
3. List of guiding documents and drawings is also filled.
4. Selected document(s) can be opened in favourite PDF reader
   using file association.
