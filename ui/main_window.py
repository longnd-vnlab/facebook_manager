"""Main Window - Modern shell with beautiful UI"""
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QSplitter, 
    QStatusBar, QMessageBox, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.account_loader import AccountLoader, Account
from core.browser_launcher import BrowserManager
from core.facebook_login import FacebookLoginManager
from core.enums import BrowserStatus, LoginStatus
from .styles import MAIN_STYLESHEET, COLORS
from .widgets import InputSection, AccountTable
from .dialogs import ValidationDialog

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Modern main application window"""
    
    def __init__(self, browser_manager: BrowserManager = None, 
                 login_manager: FacebookLoginManager = None):
        super().__init__()
        self.account_loader = AccountLoader()
        self.browser_manager = browser_manager or BrowserManager(self)
        self.login_manager = login_manager or FacebookLoginManager()
        self.accounts = []
        self.account_data = {}
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self) -> None:
        self.setWindowTitle("🔵 Facebook Account Manager")
        self.setMinimumSize(1200, 700)
        self.resize(1400, 850)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 0, 8, 8)
        
        title = QLabel("🔵 Facebook Account Manager")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #1E293B;
            padding: 8px 0;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        version = QLabel("v1.0.0")
        version.setStyleSheet("""
            font-size: 11px;
            color: #94A3B8;
            background-color: #F1F5F9;
            padding: 4px 10px;
            border-radius: 10px;
        """)
        header_layout.addWidget(version)
        
        layout.addWidget(header)
        
        # Splitter
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(8)
        
        self.input_section = InputSection()
        splitter.addWidget(self.input_section)
        
        self.account_table = AccountTable()
        splitter.addWidget(self.account_table)
        
        splitter.setSizes([220, 580])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #EFF6FF, stop:1 #DBEAFE);
                color: #1E40AF;
                font-weight: 500;
                padding: 10px 16px;
                border-top: 1px solid #BFDBFE;
                font-size: 12px;
            }
        """)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✨ Ready - Enter accounts and click 'Load Accounts' to begin")
        
        self.setStyleSheet(MAIN_STYLESHEET)
    
    def _connect_signals(self) -> None:
        # Input section
        self.input_section.load_clicked.connect(self._load_accounts)
        self.input_section.clear_clicked.connect(self._clear_input)
        self.input_section.validate_clicked.connect(self._validate_accounts)
        
        # Toolbar
        tb = self.account_table.toolbar
        tb.select_all_clicked.connect(self.account_table.select_all)
        tb.deselect_all_clicked.connect(self.account_table.deselect_all)
        tb.open_selected_clicked.connect(self._open_selected_browsers)
        tb.close_selected_clicked.connect(self._close_selected_browsers)
        tb.close_all_clicked.connect(self._close_all_browsers)
        tb.clear_table_clicked.connect(self._clear_table)
        tb.login_selected_clicked.connect(self._login_selected)
        tb.exit_clicked.connect(self.close)
        
        # Table
        self.account_table.open_chrome_clicked.connect(self._open_chrome)
        self.account_table.login_clicked.connect(self._login_single)
        
        # Browser manager
        self.browser_manager.browser_starting.connect(self._on_browser_starting)
        self.browser_manager.browser_started.connect(self._on_browser_started)
        self.browser_manager.browser_error.connect(self._on_browser_error)
        self.browser_manager.browser_closed.connect(self._on_browser_closed)
    
    def _load_accounts(self) -> None:
        text = self.input_section.get_text()
        if not text:
            self._show_warning("Please enter account data first!")
            return
        
        self.account_table.clear()
        self.accounts = self.account_loader.load_accounts(text)
        
        if not self.accounts:
            self._show_warning("No valid accounts found!\nCheck format: UID|PASSWORD|TOKEN")
            return
        
        self.account_data.clear()
        for acc in self.accounts:
            self.account_table.add_account(acc)
            self.account_data[acc.uid] = acc
        
        self.input_section.set_count(len(self.accounts))
        self.status_bar.showMessage(f"✅ Loaded {len(self.accounts)} accounts successfully")
    
    def _clear_input(self) -> None:
        self.input_section.clear()
        self.status_bar.showMessage("🗑️ Input cleared")
    
    def _validate_accounts(self) -> None:
        text = self.input_section.get_text()
        if not text:
            self._show_warning("Please enter account data first!")
            return
        valid, invalid, errors = self.account_loader.validate_accounts(text)
        ValidationDialog.show(self, valid, invalid, errors)
    
    def _open_chrome(self, uid: str, profile_path: str) -> None:
        if self.browser_manager.is_browser_running(uid):
            self._show_info(f"Browser already running for UID: {uid}")
            return
        self.browser_manager.launch_browser(uid, profile_path)
        self.status_bar.showMessage(f"🚀 Launching browser for {uid}...")
    
    def _open_selected_browsers(self) -> None:
        count = 0
        for uid in self.account_table.get_selected_uids():
            info = self.account_table.get_account_info(uid)
            if info and not self.browser_manager.is_browser_running(uid):
                self.browser_manager.launch_browser(info[0], info[1])
                count += 1
        self.status_bar.showMessage(f"🚀 Launching {count} browsers..." if count else "⚠️ No accounts to launch")
    
    def _close_selected_browsers(self) -> None:
        count = 0
        for uid in self.account_table.get_selected_uids():
            if self.browser_manager.is_browser_running(uid):
                self.browser_manager.close_browser(uid)
                count += 1
        self.status_bar.showMessage(f"⏹️ Closed {count} browsers" if count else "⚠️ No running browsers selected")
    
    def _close_all_browsers(self) -> None:
        self.browser_manager.close_all_browsers()
        self.account_table.reset_all_buttons()
        self.status_bar.showMessage("❌ All browsers closed")
    
    def _clear_table(self) -> None:
        if QMessageBox.question(self, "🗑️ Confirm", "Clear table and close all browsers?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                ) == QMessageBox.StandardButton.Yes:
            self._close_all_browsers()
            self.account_table.clear()
            self.accounts.clear()
            self.input_section.set_count(0)
            self.status_bar.showMessage("🗑️ Table cleared")
    
    def _on_browser_starting(self, uid: str) -> None:
        self.account_table.update_browser_button(uid, "⏳ Opening...", False, COLORS['warning'])
        self.account_table.update_status(uid, BrowserStatus.LAUNCHING.value)
    
    def _on_browser_started(self, uid: str) -> None:
        self.account_table.update_browser_button(uid, "✅ Running", False, COLORS['success'])
        self.account_table.update_status(uid, BrowserStatus.RUNNING.value)
        self.status_bar.showMessage(f"✅ Browser started for {uid}")
    
    def _on_browser_closed(self, uid: str) -> None:
        self.account_table.update_browser_button(uid, "🌐 Open", True, COLORS['success'])
        self.account_table.update_status(uid, BrowserStatus.CLOSED.value)
        self.status_bar.showMessage(f"⏹️ Browser closed for {uid}")
    
    def _on_browser_error(self, uid: str, error: str) -> None:
        self.account_table.update_browser_button(uid, "🌐 Open", True, COLORS['success'])
        self.account_table.update_status(uid, BrowserStatus.ERROR.value)
        logger.warning(f"Browser error for {uid}: {error}")
        self._show_error(f"Failed to launch browser for UID: {uid}\n\n{error}")
    
    def _login_single(self, uid: str) -> None:
        if not self.browser_manager.is_browser_running(uid):
            self._show_warning(f"Open Chrome first for UID: {uid}")
            return
        acc = self.account_data.get(uid)
        driver = self.browser_manager.drivers.get(uid)
        if acc and driver:
            self._start_login(acc, driver)
    
    def _login_selected(self) -> None:
        count = 0
        for uid in self.account_table.get_selected_uids():
            if self.browser_manager.is_browser_running(uid) and not self.login_manager.is_logging_in(uid):
                acc = self.account_data.get(uid)
                driver = self.browser_manager.drivers.get(uid)
                if acc and driver:
                    self._start_login(acc, driver)
                    count += 1
        self.status_bar.showMessage(f"🔐 Starting login for {count} accounts..." if count else "⚠️ No accounts to login")
    
    def _start_login(self, acc: Account, driver) -> None:
        self.account_table.update_status(acc.uid, LoginStatus.LOGGING_IN.value)
        self.account_table.update_login_button(acc.uid, "⏳ ...", False, COLORS['warning'])
        self.login_manager.start_login(
            driver=driver, uid=acc.uid, password=acc.password, token_2fa=acc.token,
            status_callback=lambda u, s: self.account_table.update_status(u, s),
            success_callback=lambda u: (
                self.account_table.update_status(u, LoginStatus.SUCCESS.value),
                self.account_table.update_login_button(u, "✅ Done", False, COLORS['success'])
            ),
            error_callback=lambda u, e: (
                self.account_table.update_status(u, f"❌ {e[:25]}..."),
                self.account_table.update_login_button(u, "🔐 Login", True, COLORS['purple'])
            )
        )
    
    def _show_warning(self, msg: str) -> None:
        QMessageBox.warning(self, "⚠️ Warning", msg)
    
    def _show_info(self, msg: str) -> None:
        QMessageBox.information(self, "ℹ️ Info", msg)
    
    def _show_error(self, msg: str) -> None:
        QMessageBox.critical(self, "❌ Error", msg)
    
    def closeEvent(self, event) -> None:
        self.browser_manager.cleanup()
        self.login_manager.cleanup()
        event.accept()
