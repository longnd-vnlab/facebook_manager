#!/usr/bin/env python3
"""Facebook Account Manager - Entry point"""
import sys
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler('facebook_login_debug.log'),
        logging.StreamHandler()
    ]
)

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QFontDatabase

from core.browser_launcher import BrowserManager
from core.facebook_login import FacebookLoginManager
from ui.main_window import MainWindow


def main() -> None:
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    
    app = QApplication(sys.argv)
    app.setApplicationName("Facebook Account Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("FBManager")
    
    # Try modern fonts, fallback to system default
    preferred_fonts = ["Segoe UI", "SF Pro Display", "Roboto", "Helvetica Neue", "Arial"]
    font_family = "Segoe UI"
    for pf in preferred_fonts:
        if pf in QFontDatabase.families():
            font_family = pf
            break
    
    font = QFont(font_family, 10)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(font)
    
    # Dependency injection
    browser_manager = BrowserManager()
    login_manager = FacebookLoginManager()
    
    window = MainWindow(browser_manager=browser_manager, login_manager=login_manager)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
