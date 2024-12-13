@REM Decode string encoded with Base64 and copy decoded string to clipboard
@echo off
powershell -File "%~dp0\script\decode_base64.ps1" %*
