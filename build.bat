@echo off
REM Build script for Facebook Account Manager (Windows)

echo 🔵 Building Facebook Account Manager for Windows...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo ✅ Python found

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip not found! Installing...
    python -m ensurepip --upgrade
)
echo ✅ pip found

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Check PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 📦 PyInstaller not found. Installing...
    pip install pyinstaller
)

REM Clean previous builds
echo 🧹 Cleaning previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul

REM Build the executable
echo 🔨 Building executable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "FacebookManager" ^
    --add-data "config.py;." ^
    --add-data "core;core" ^
    --add-data "ui;ui" ^
    --hidden-import "PyQt6.QtCore" ^
    --hidden-import "PyQt6.QtWidgets" ^
    --hidden-import "PyQt6.QtGui" ^
    --hidden-import "DrissionPage" ^
    --hidden-import "pyotp" ^
    main.py

echo.
echo ✅ Build complete!
echo 📁 Executable location: dist\FacebookManager.exe
pause
