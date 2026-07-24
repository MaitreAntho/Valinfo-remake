@echo off
cd /d "%~dp0"

where git >nul 2>nul
if errorlevel 1 (
    echo Git n'est pas installe ou n'est pas dans le PATH.
    echo Telecharge-le sur https://git-scm.com/downloads
    pause
    exit /b 1
)

for /f "delims=" %%i in ('git rev-parse HEAD') do set "BEFORE=%%i"

echo Recuperation des dernieres mises a jour...
git pull
if errorlevel 1 (
    echo Echec de la mise a jour. Verifie ta connexion ou d'eventuels conflits git.
    pause
    exit /b 1
)

for /f "delims=" %%i in ('git rev-parse HEAD') do set "AFTER=%%i"

echo.
if "%BEFORE%"=="%AFTER%" (
    echo Deja a jour, aucune nouvelle mise a jour disponible.
) else (
    echo Mise a jour installee ! Changements recuperes :
    git log --oneline %BEFORE%..%AFTER%
    echo.
    echo Mise a jour des dependances...
    python -m pip install -q -r requirements.txt
)

echo.
echo Termine !
pause
