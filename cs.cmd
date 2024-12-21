@REM Convert game screenshot
@echo off
set "PYTHONDONTWRITEBYTECODE=1"
set "PYTHONPATH=%~dp0\script\library"
python "%~dp0\script\convert_screenshot.pyw" %*
