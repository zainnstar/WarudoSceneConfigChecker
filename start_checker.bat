@echo off
title WarudoSceneConfigChecker Launcher
setlocal enabledelayedexpansion

echo ===========================================
echo  WarudoSceneConfigChecker Setup and Launch
echo ===========================================
echo.

rem Check if Python is installed
echo [START] Running batch file...
echo.

echo [CHECK] Verifying Python installation...
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found.
    echo [ERROR] Please install Python and try again.
    goto :ERROR
)

rem Display Python version
echo [INFO] Python version:
python --version
echo.

rem Check and create virtual environment
if not exist "venv" (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        echo [ERROR] Please check if Python version is 3.5 or higher.
        goto :ERROR
    )
)

rem Activate virtual environment
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    goto :ERROR
)

rem Install required packages
echo [SETUP] Installing packages...
python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to upgrade pip.
    goto :ERROR
)

python -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to install required packages.
    echo [INFO] Please check if requirements.txt exists.
    goto :ERROR
)

rem Run Python script
echo [RUN] Launching scene checker...
python warudo_scene_checker.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] An error occurred while running the program.
    goto :ERROR
)

rem Deactivate virtual environment
call venv\Scripts\deactivate.bat

echo.
echo [COMPLETE] Process finished successfully.
goto :END

:ERROR
echo.
echo [EXIT] Process terminated due to an error.
echo.

:END
echo.
echo Press any key to exit...
pause > nul
exit /b 0