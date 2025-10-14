@echo off
chcp 65001 >nul
title GEOPOLIS v3.0
color 0A

echo.
echo ================================================================
echo    GEOPOLIS v3.0 - Architecture Unifiee
echo ================================================================
echo.

REM Vérifier Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERREUR] Python non detecte
    pause
    exit /b 1
)

REM Installer dépendances si nécessaire
if not exist ".deps_v3_installed" (
    echo Installation des dependances...
    pip install -r requirements.txt
    echo. > .deps_v3_installed
)

REM Démarrer le serveur
echo Demarrage du serveur...
echo.

python app.py

pause
