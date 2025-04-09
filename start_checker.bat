@echo off
rem Simple batch file for WarudoSceneConfigChecker
title WarudoSceneConfigChecker

echo Starting setup and launch process...
echo.

rem Check Python installation
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python not found.
    echo Please install Python and try again.
    goto end
)

echo Python version:
python --version
echo.

rem Setup virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        goto end
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    goto end
)

echo Installing packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages.
    goto end
)

echo Running scene checker...
python warudo_scene_checker.py
if errorlevel 1 (
    echo ERROR: Program execution failed.
    goto end
)

call venv\Scripts\deactivate.bat
echo Process completed successfully.

:end
echo.
echo Press any key to exit...
pause
exit /b