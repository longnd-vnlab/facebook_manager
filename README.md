# 🔵 Facebook Account Manager
<img width="1410" height="894" alt="Screenshot from 2025-11-29 23-18-58" src="https://github.com/user-attachments/assets/0eae0458-2d3b-467f-915a-db443a4f49b8" />


A modern PyQt6 GUI application for managing multiple Facebook accounts with separate Chrome profiles using DrissionPage.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **Multi-Account Management**: Import and manage multiple Facebook accounts
- **Separate Chrome Profiles**: Each account gets its own isolated Chrome profile
- **Auto 2FA Login**: Automatic login with TOTP 2FA code generation
- **Grid Browser Layout**: Opens browsers in a 3x2 grid layout
- **Non-blocking UI**: Browser operations run in background threads
- **Modern UI**: Beautiful, responsive interface with status indicators
- **Batch Operations**: Select multiple accounts for bulk actions

## 📁 Project Structure

```
facebook_manager/
├── main.py                     # Application entry point
├── config.py                   # Configuration constants
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── core/                       # Core business logic
│   ├── __init__.py
│   ├── enums.py               # Status enums (BrowserStatus, LoginStatus)
│   ├── account_loader.py      # Account parsing and validation
│   ├── browser_launcher.py    # Chrome browser management
│   └── facebook_login.py      # Facebook login with 2FA
│
├── ui/                         # User interface
│   ├── __init__.py
│   ├── main_window.py         # Main window shell (~200 lines)
│   ├── styles.py              # CSS styles and colors
│   ├── helpers.py             # UI utility functions
│   │
│   ├── widgets/               # Reusable UI components
│   │   ├── __init__.py
│   │   ├── input_section.py   # Account input text area
│   │   ├── toolbar.py         # Action buttons toolbar
│   │   └── account_table.py   # Account list table
│   │
│   └── dialogs/               # Dialog windows
│       ├── __init__.py
│       └── validation_dialog.py
│
└── profiles/                   # Auto-generated Chrome profiles
    └── <UID>/                  # One folder per account
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- Linux/macOS/Windows

### 1. Clone or Download

```bash
cd /path/to/your/project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install PyQt6 DrissionPage pyotp
```

### 3. Verify Chrome Path

The default Chrome paths are:
- **Linux**: `/usr/bin/google-chrome`
- **macOS**: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

To customize, edit `config.py`:

```python
CHROME_PATH = '/your/custom/chrome/path'
```

## 📖 Usage

### Start the Application

```bash
python main.py
```

### Input Format

Enter accounts in the text area, one per line:

```
UID|PASSWORD|2FA_TOKEN
```

**Example:**
```
100048068360222|MyPassword123|JBSWY3DPEHPK3PXP
100048433699046|AnotherPass456|GEZDGNBVGY3TQOJQ
100070800064339|SecurePass789|MFRGGZDFMY4TQMZQ
```

> **Note**: The 2FA token is the secret key from your authenticator app (base32 encoded)

### Step-by-Step Guide

1. **Load Accounts**
   - Paste account data into the input area
   - Click **📥 Load Accounts**
   - Accounts appear in the table

2. **Open Browsers**
   - Click **🌐 Open** button for individual accounts, or
   - Select multiple accounts (checkbox) → Click **🚀 Open**
   - Browsers open in a 3x2 grid layout

3. **Login to Facebook**
   - After browser is running (✅ Running status)
   - Click **🔐 Login** for individual accounts, or
   - Select accounts → Click **▶️ Login Selected**
   - App auto-fills credentials and 2FA code

4. **Close Browsers**
   - **⏹️ Close**: Close selected browsers
   - **❌ All**: Close all browsers
   - **⏻ Exit**: Exit application (closes all browsers)

### Toolbar Buttons

| Button | Action |
|--------|--------|
| ☑️ All | Select all accounts |
| ⬜ None | Deselect all accounts |
| 🚀 Open | Open browsers for selected |
| ⏹️ Close | Close selected browsers |
| ❌ All | Close all browsers |
| 🗑️ Clear | Clear table |
| ▶️ Login Selected | Login selected accounts |
| ⏻ Exit | Exit application |

### Status Indicators

| Status | Meaning |
|--------|---------|
| Ready | Account loaded, ready to open browser |
| ⏳ Launching... | Browser is starting |
| ✅ Running | Browser is open and running |
| Browser closed | Browser was closed |
| ❌ Error | Failed to launch browser |
| Logging in... | Login in progress |
| ✅ Logged in | Successfully logged in |
| ❌ Failed | Login failed |

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Chrome executable path
CHROME_PATH = '/usr/bin/google-chrome'

# Profile storage directory
PROFILES_DIR = 'profiles'

# Browser grid layout
GRID_COLS = 3  # Columns
GRID_ROWS = 2  # Rows

# Account format hint
ACCOUNT_FORMAT = "UID|PASSWORD|TOKEN"
```

## 🏗️ Architecture

### Design Patterns

- **Dependency Injection**: Managers injected into MainWindow
- **Signal/Slot**: Qt signals for async communication
- **Worker Threads**: Non-blocking browser operations
- **MVC-like**: Separation of UI widgets and core logic

### Key Classes

| Class | Purpose |
|-------|---------|
| `MainWindow` | Main application window shell |
| `AccountLoader` | Parse and validate account data |
| `BrowserManager` | Manage Chrome browser instances |
| `FacebookLoginManager` | Handle Facebook login process |
| `BrowserLaunchWorker` | Background thread for browser launch |
| `FacebookLoginWorker` | Background thread for login |

### Signals Flow

```
User Action → Widget Signal → MainWindow Handler → Manager → Worker Thread
                                                      ↓
UI Update ← Widget Method ← MainWindow Handler ← Manager Signal
```

## 🔧 Troubleshooting

### Chrome Not Found

```bash
# Check Chrome location
which google-chrome
# or
whereis google-chrome
```

Update `config.py` with correct path.

### Permission Denied

```bash
chmod 755 profiles/
chmod +x main.py
```

### PyQt6 Import Error

```bash
pip install PyQt6 PyQt6-Qt6 PyQt6-sip
```

### Browser Won't Start

1. Check if Chrome is installed
2. Kill existing Chrome processes:
   ```bash
   pkill -f chrome
   ```
3. Delete corrupted profile:
   ```bash
   rm -rf profiles/<UID>
   ```

### 2FA Code Invalid

- Ensure token is base32 encoded (uppercase letters A-Z, digits 2-7)
- Check system time is synchronized
- Token should be ~16-32 characters

## 📦 Building Executable

### Using PyInstaller

```bash
pip install pyinstaller

# Build single executable
pyinstaller --onefile --windowed --name "FacebookManager" main.py
```

### Build Script (Linux/macOS)

```bash
#!/bin/bash
pyinstaller \
    --onefile \
    --windowed \
    --name "FacebookManager" \
    --add-data "ui:ui" \
    --add-data "core:core" \
    --add-data "config.py:." \
    main.py
```

Output will be in `dist/FacebookManager`

## 📝 Logging

Logs are saved to `facebook_login_debug.log`:

```bash
tail -f facebook_login_debug.log
```

Log levels:
- INFO: Normal operations
- WARNING: Non-critical issues
- ERROR: Failures
- DEBUG: Detailed debugging

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push branch: `git push origin feature/new-feature`
5. Submit Pull Request

## 📄 License

MIT License - feel free to use and modify.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Use responsibly and in accordance with Facebook's Terms of Service. The authors are not responsible for any misuse or account restrictions.
