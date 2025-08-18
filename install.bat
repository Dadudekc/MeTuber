@echo off
REM MeTuber Installation Script for Windows
REM Run this script as Administrator for best results

echo MeTuber Installation Script
echo ==========================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip not found. Please ensure pip is installed with Python.
    pause
    exit /b 1
)

echo Python found. Creating virtual environment...

REM Remove existing virtual environment if it exists
if exist "venv" (
    echo Removing existing virtual environment...
    rmdir /s /q "venv"
)

REM Create virtual environment
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install core dependencies
echo Installing core dependencies...
pip install -r requirements-core.txt
if errorlevel 1 (
    echo WARNING: Some dependencies failed to install.
    echo You may need to install Visual C++ Build Tools.
)

REM Check dependencies
echo Checking dependencies...
python check_dependencies.py

if errorlevel 1 (
    echo.
    echo Installation completed with warnings.
    echo Check the output above for details.
) else (
    echo.
    echo Installation completed successfully!
    echo.
    echo To run MeTuber:
    echo   venv\Scripts\activate.bat
    echo   python webcam_filter_pyqt5.py
)

echo.
echo Note: You may need to install OBS Studio for virtual camera support.
echo Download from: https://obsproject.com/
echo.
pause


