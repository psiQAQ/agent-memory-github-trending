@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
python -B "%~dp0collect-owner.py" %*
set "owner_exit=%errorlevel%"
if not "%~1"=="" exit /b %owner_exit%
echo.
echo Send the printed SUMMARY path to Codex.
pause
exit /b %owner_exit%
