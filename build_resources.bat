@ECHO OFF
 
set OSGEO4W_ROOT=C:\Program Files\QGIS 3.42.3
call "%OSGEO4W_ROOT%\bin\o4w_env.bat"

cd /d %~dp0
 
REM @ECHO ON

::Ui Compilation
call pyuic5 B4UdigNL.ui -o ui_B4UdigNL.py       
 
::Resources
call pyrcc5 resources.qrc -o qrc_resources.py