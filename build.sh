#!/bin/bash
# Build script for Facebook Account Manager (Linux)

echo "🔵 Building Facebook Account Manager for Linux..."

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Installing..."
    sudo apt-get update && sudo apt-get install -y python3
fi
echo "✅ Python3: $(python3 --version)"

# Check pip3
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Installing..."
    sudo apt-get install -y python3-pip
fi
echo "✅ pip3: $(pip3 --version)"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Check PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 PyInstaller not found. Installing..."
    pip3 install pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Build the executable
echo "🔨 Building executable..."
pyinstaller \
    --onefile \
    --windowed \
    --name "FacebookManager" \
    --add-data "config.py:." \
    --add-data "core:core" \
    --add-data "ui:ui" \
    --hidden-import "PyQt6.QtCore" \
    --hidden-import "PyQt6.QtWidgets" \
    --hidden-import "PyQt6.QtGui" \
    --hidden-import "DrissionPage" \
    --hidden-import "pyotp" \
    main.py

echo ""
echo "✅ Build complete!"
echo "📁 Executable location: dist/FacebookManager"
