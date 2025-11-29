#!/bin/bash
# Build script for Facebook Account Manager (macOS)

echo "🔵 Building Facebook Account Manager for macOS..."

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "📦 Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install python3
fi
echo "✅ Python3: $(python3 --version)"

# Check pip3
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Installing..."
    python3 -m ensurepip --upgrade
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

# Build the .app bundle
echo "🔨 Building macOS app bundle..."
pyinstaller \
    --onefile \
    --windowed \
    --name "FacebookManager" \
    --osx-bundle-identifier "com.fbmanager.app" \
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
echo "📁 App location: dist/FacebookManager.app"
echo ""
echo "To run: open dist/FacebookManager.app"
