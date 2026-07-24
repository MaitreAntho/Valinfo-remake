@echo off
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python n'est pas installe ou n'est pas dans le PATH.
    echo Telecharge-le sur https://www.python.org/downloads/
    pause
    exit /b 1
)

python -m pip install -q -r requirements.txt
python main.py --config
pause
