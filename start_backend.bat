@echo off
chcp 65001 >nul
echo ==================================================
echo  SkinSense AI - Backend Baslatiliyor
echo ==================================================
echo.
echo API: http://localhost:5000
echo.
cd /d "%~dp0backend"
python app.py
pause
