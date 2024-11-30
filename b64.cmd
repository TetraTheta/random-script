@REM Decode string encoded with Base64 and copy decoded string to clipboard
@echo off
powershell -File "%~dp0\script\b64.ps1" %*
