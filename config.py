"""Configuration constants for Facebook Account Manager"""
import sys

# Chrome paths per OS
if sys.platform == "darwin":
    CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
else:
    CHROME_PATH = "/usr/bin/google-chrome"

PROFILES_DIR = "profiles"
GRID_COLS = 3
GRID_ROWS = 2
ACCOUNT_FORMAT = "UID|PASSWORD|TOKEN"
