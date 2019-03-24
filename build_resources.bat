@ECHO OFF
 
set OSGEO4W_ROOT=C:\OSGeo4W64
 
set PATH=%OSGEO4W_ROOT%\bin;%PATH%
set PATH=%PATH%;%OSGEO4W_ROOT%\apps\qgis\bin
 
@echo off
call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W_ROOT%\bin\py3_env.bat"
@echo off
path %OSGEO4W_ROOT%\apps\qgis-dev\bin;%PATH%
::no grass - path %OSGEO4W_ROOT%\apps\grass\grass-7.2.2\lib;%OSGEO4W_ROOT%\apps\grass\grass-7.2.2\bin;%PATH%
 
cd /d %~dp0
 
@ECHO ON
::Ui Compilation
call pyuic5 B4UdigNL.ui -o ui_B4UdigNL.py          
 
::Resources
call pyrcc5 resources.qrc -o qrc_resources.py
 
@ECHO OFF
GOTO END
 
:ERROR
   echo "Failed!"
   set ERRORLEVEL=%ERRORLEVEL%
   pause
 
:END
@ECHO ON