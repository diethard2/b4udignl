QGIS KLIC Viewer Plugin
Author Diethard Jansen
OpenSource License GPL v.2 and up.


Installation
============
First you need an installation of Quantum GIS! 
Download QGIS v. 2.0 from www.qgis.org.

Use QGIS Python Plugin Installer for installation of this plugin.

You can also manually unzip and place contents of b4udignl.zip
in your home folder ~/.qgis2/python/plugins/

Release notes 20/06/2013
=============
Version 1.4.0

Updated plugin so it works as well for QGIS 2.0
Changed name of plugin from QGIS WION Result Viewer to
the QGIS KLIC Viewer.
Removed the grouping of loaded layers because the code was complicated
and because the QGIS grouping functions of layers behaved weird.
Updated the help function.

Release notes 27/06/2012
=============
Version 1.3.2

Moved this plugin to official QGIS plugins repository.
Tested for QGIS 1.8.0 and plugin still works great.
Repository from site http://wwww.gis-plugins.nl will be removed after
succesfull transfer.

Release notes 12/01/2011
=============
Version 1.3.1

New functionality:
    - now you are allowed to forget to open Wion Viewer plugin
      before opening a project. when you have stored information
      from plugin in project, the plugin will be filled with wion
      message information.

Release notes 27/12/2010
=============
Version 1.3.0
This new version can only be used for QGIS v. 1.6.0 and up!

New functionality:
    - contents of plugin can be now stored in project.
      This is a major enhancement because now you can, after
      loading de wion messages, also add your own design layers
      or layers with dimensioning.
      When project is created and from wion plugin it is saved
      in project, immediately everything is back in same state
      as when you saved the project. This means you can open
      pdf documents from wion message and use themes to set
      visibility.
    - when selecting File - New project, all information from
      plugin is removed as well.
    - plugin remembers width and height of plugin window you
      used before.

Release notes 11/12/2010
=============
Version 1.2.5
New functionality:
    -plugin remembers position of window and starts in same
     position as before (no need to drag plugin window to
     pleasing position every time)
Fixed:
    -when loading a second digalert message in 1.6.0., legend
     groups were still created in a nested way.
     Stopped creating legend groups for 1.6.0.
    
Release notes 04/12/2010
=============
Version 1.2.4
New functionality:
    -new version that can be used as wel for QGIS v. 1.6.0
    -in Themes Tab, 4 themes have been added, topo, location
     dimensioning and annotation.
    -in 1.6.0 the layerGroups topo location dimension and
     and annotation are not created in layers panel because
     adding groups was buggy. In 1.5.0 the layers are still
     created.
     
Release notes 30/11/2010
=============
Version 1.2.3
(last release before adding a new version for QGIS v. 1.6.0)
Fixed:
    -loading a zipped folder under Ubuntu.  

Release notes 26/11/2010
=============
Version 1.2.2
New functionality:
    -added tab Options where you can set default folder where
     to start searching as a user setting. 
Fixed:
    -loading a zipped folder under Ubuntu.  

Release notes 31/10/2010
=============
Versions 1.2.1
New functionality:
    Improved performance!!
    - loading Wion Result (25.5 -> 16.5 seconds)
    - closing loaded Wion Result (9.5 -> 0.5 seconds)
    - changing visibility of a Theme (6.5 -> 2.3 seconds)
So I believe a new release is justifiable.
(Performance figures are based on using testmessage
 09G267447_1 which can be downloaded from www.klicviewer.nl
 on my own pretty old Windows PC). 

Release notes 28/10/2010
=============
Version 1.2.0
New functionality:
1) added functionality for improved control on visibilities
   of layers.
   - A Themes Tab to turn/of visibilities of several layers
     belonging to the same theme
   - Loading layers in legend groups, so you can turn al
     labels/dimensioning on or of.
2) added a button [Best scale] to get best view from Button.
3) added a button on Tabs theme [Refresh] to make refresh the
   status of themes whenever necessary.
4) improved understanding of Wion Result by actually adding
   a Map Legend in Themes Tab and named legend groups in
   layers panel.

Version 1.1.3
fixed: Make plugin open any zipped files (test images/
    renamed zipfiles)
New functionality:
When starting Wion Result Viewer, unit is changed to meters.
This becomes visible after refresh or after first load.

version 1.1.2
Fixed: Make plugin open zipped files delivered by Kadaster

version 1.1.1
Fixed: Make plugin multilingual for Quantum GIS Thethys as well

Version 1.1.0

New functionality:
1) Opening zipped file
2) better support for working with more loaded messages
   Goto function loaded & selected message
   Close message function to unload loaded message.
3) Open an accompanying documents instantly using doubleklic
4) change visibility of buttons whether message is loaded.

This version is probably the last version that works with
previous releases of Quantum GIS. The next one is only
supported from QGIS version 1.5 onwards! 

Version 1.0.2

First official release!

Tested with Quantum GIS 1.0.2 (Kore), 1.3 (Mimas) and 1.4
(Enceladus)On following OS systems: Windows XP, Vista, 7,
Unbuntu & Imac Help manuals (browser) included!
Translations available: English and Dutch

Functionality (for more information manual from Help manual)
1) Load WION message from given Directory.
2) Many PNG's are made visible with Dutch RD coordinate system.
3) List of guiding documents and drawings is also filled.
4) Selected document(s) can be opened in favourite PDF reader
   using file association.
