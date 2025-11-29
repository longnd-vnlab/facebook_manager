"""Modern toolbar widget with action buttons"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal
from ..styles import FRAME_STYLES, get_button_style, COLORS


class Toolbar(QWidget):
    """Modern toolbar with browser and login controls"""
    
    select_all_clicked = pyqtSignal()
    deselect_all_clicked = pyqtSignal()
    open_selected_clicked = pyqtSignal()
    close_selected_clicked = pyqtSignal()
    close_all_clicked = pyqtSignal()
    clear_table_clicked = pyqtSignal()
    login_selected_clicked = pyqtSignal()
    exit_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Browser controls frame
        browser_frame = QFrame()
        browser_frame.setStyleSheet(FRAME_STYLES['browser'])
        browser_layout = QHBoxLayout(browser_frame)
        browser_layout.setContentsMargins(12, 10, 12, 10)
        browser_layout.setSpacing(8)
        
        # Section label
        browser_label = QLabel("🌐 Browser")
        browser_label.setStyleSheet("font-weight: 700; color: #1E40AF; font-size: 12px;")
        browser_layout.addWidget(browser_label)
        
        browser_layout.addWidget(self._create_separator())
        
        # Selection buttons
        self.btn_select_all = self._create_button("☑️ All", COLORS['primary'], 65)
        self.btn_select_all.setToolTip("Select All Accounts")
        self.btn_select_all.clicked.connect(self.select_all_clicked.emit)
        browser_layout.addWidget(self.btn_select_all)
        
        self.btn_deselect_all = self._create_button("⬜ None", COLORS['gray'], 65)
        self.btn_deselect_all.setToolTip("Deselect All")
        self.btn_deselect_all.clicked.connect(self.deselect_all_clicked.emit)
        browser_layout.addWidget(self.btn_deselect_all)
        
        browser_layout.addWidget(self._create_separator())
        
        # Browser action buttons
        self.btn_open = self._create_button("🚀 Open", COLORS['success'], 75)
        self.btn_open.setToolTip("Open Selected Browsers")
        self.btn_open.clicked.connect(self.open_selected_clicked.emit)
        browser_layout.addWidget(self.btn_open)
        
        self.btn_close = self._create_button("⏹️ Close", COLORS['warning'], 75)
        self.btn_close.setToolTip("Close Selected Browsers")
        self.btn_close.clicked.connect(self.close_selected_clicked.emit)
        browser_layout.addWidget(self.btn_close)
        
        self.btn_close_all = self._create_button("❌ All", COLORS['danger'], 60)
        self.btn_close_all.setToolTip("Close All Browsers")
        self.btn_close_all.clicked.connect(self.close_all_clicked.emit)
        browser_layout.addWidget(self.btn_close_all)
        
        browser_layout.addWidget(self._create_separator())
        
        self.btn_clear = self._create_button("🗑️ Clear", COLORS['gray'], 70)
        self.btn_clear.setToolTip("Clear Table")
        self.btn_clear.clicked.connect(self.clear_table_clicked.emit)
        browser_layout.addWidget(self.btn_clear)
        
        layout.addWidget(browser_frame)
        layout.addStretch()
        
        # Login frame
        login_frame = QFrame()
        login_frame.setStyleSheet(FRAME_STYLES['login'])
        login_layout = QHBoxLayout(login_frame)
        login_layout.setContentsMargins(12, 10, 12, 10)
        login_layout.setSpacing(10)
        
        login_label = QLabel("🔐 Facebook")
        login_label.setStyleSheet("font-weight: 700; color: #6D28D9; font-size: 12px;")
        login_layout.addWidget(login_label)
        
        self.btn_login = self._create_button("▶️ Login Selected", COLORS['purple'], 130)
        self.btn_login.setToolTip("Login to Facebook for Selected Accounts")
        self.btn_login.clicked.connect(self.login_selected_clicked.emit)
        login_layout.addWidget(self.btn_login)
        
        layout.addWidget(login_frame)
        
        # Exit button
        self.btn_exit = self._create_button("⏻ Exit", COLORS['danger'], 70)
        self.btn_exit.setToolTip("Exit Application")
        self.btn_exit.clicked.connect(self.exit_clicked.emit)
        layout.addWidget(self.btn_exit)
    
    def _create_button(self, text: str, color: str, min_width: int) -> QPushButton:
        btn = QPushButton(text)
        btn.setMinimumHeight(36)
        btn.setStyleSheet(get_button_style(color, min_width, 11))
        return btn
    
    def _create_separator(self) -> QFrame:
        sep = QFrame()
        sep.setFixedWidth(1)
        sep.setFixedHeight(24)
        sep.setStyleSheet("background-color: #CBD5E1;")
        return sep
