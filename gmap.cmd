@REM Remove files from SourceMod to allow it to be packed as GMod GMA
@echo off
powershell -File "%~dp0\script\gmod_map_addon.ps1" %*
