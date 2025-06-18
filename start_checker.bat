@echo off
setlocal enabledelayedexpansion
rem Simple batch file for WarudoSceneConfigChecker
title WarudoSceneConfigChecker

rem Set code page to UTF-8
chcp 65001 > nul

echo Starting WarudoSceneConfigChecker...
echo.

rem Check Python installation
python --version > nul 2> nul
if errorlevel 1 (
    echo ERROR: Python not found.
    echo Please install Python and try again.
    pause
    exit /b 1
)

rem Check for tkinter
python -c "import tkinter" > nul 2> nul
if errorlevel 1 (
    echo ERROR: Tkinter not found in Python installation.
    echo Please run setup_venv.bat first to verify your environment.
    pause
    exit /b 1
)

rem Run the application
echo Running scene checker...
python main.py
if errorlevel 1 (
    echo ERROR: Program execution failed.
    pause
    exit /b 1
)

echo Process completed successfully.

echo.
echo Press any key to exit...
pause > nul
exit /b 0