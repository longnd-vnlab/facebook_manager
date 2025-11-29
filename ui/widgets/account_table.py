"""Modern account table widget"""
from typing import Optional, List
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

from core.account_loader import Account
from core.enums import BrowserStatus
from ..styles import get_button_style, COLORS
from ..helpers import find_row_by_uid
from .toolbar import Toolbar


class AccountTable(QGroupBox):
    """Modern account list table with toolbar"""
    
    open_chrome_clicked = pyqtSignal(str, str)
    login_clicked = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__("📋 Account List", parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 20, 16, 16)
        
        # Toolbar
        self.toolbar = Toolbar()
        layout.addWidget(self.toolbar)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "✓", "UID", "Password", "Token", "Profile", "Browser", "Login", "Status"
        ])
        
        # Configure header
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        
        self.table.setColumnWidth(0, 35)   # Checkbox
        self.table.setColumnWidth(1, 130)  # UID
        self.table.setColumnWidth(2, 80)   # Password
        self.table.setColumnWidth(5, 100)  # Browser
        self.table.setColumnWidth(6, 100)  # Login
        self.table.setColumnWidth(7, 150)  # Status
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(48)
        
        layout.addWidget(self.table)
    
    def add_account(self, account: Account) -> None:
        """Add account to table with modern styling"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Checkbox
        chk = QTableWidgetItem()
        chk.setCheckState(Qt.CheckState.Unchecked)
        chk.setFlags(chk.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        self.table.setItem(row, 0, chk)
        
        # UID with monospace font
        uid_item = QTableWidgetItem(account.uid)
        uid_item.setFlags(uid_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        uid_item.setForeground(QColor("#1E40AF"))
        self.table.setItem(row, 1, uid_item)
        
        # Password (masked)
        pw_item = QTableWidgetItem("••••••••")
        pw_item.setToolTip("Click to reveal")
        pw_item.setData(Qt.ItemDataRole.UserRole, account.password)
        pw_item.setFlags(pw_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        pw_item.setForeground(QColor("#64748B"))
        self.table.setItem(row, 2, pw_item)
        
        # Token (truncated)
        token_display = account.token[:16] + "..." if len(account.token) > 16 else account.token
        token_item = QTableWidgetItem(token_display)
        token_item.setToolTip(account.token)
        token_item.setFlags(token_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        token_item.setForeground(QColor("#64748B"))
        self.table.setItem(row, 3, token_item)
        
        # Profile path (shortened)
        profile_short = "..." + account.profile_path[-30:] if len(account.profile_path) > 30 else account.profile_path
        path_item = QTableWidgetItem(profile_short)
        path_item.setToolTip(account.profile_path)
        path_item.setFlags(path_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        path_item.setForeground(QColor("#94A3B8"))
        self.table.setItem(row, 4, path_item)
        
        # Browser button
        btn = QPushButton("🌐 Open")
        btn.setStyleSheet(get_button_style(COLORS['success'], 70, 10))
        btn.setMinimumHeight(28)
        btn.setMaximumWidth(90)
        btn.clicked.connect(lambda _, u=account.uid, p=account.profile_path: self.open_chrome_clicked.emit(u, p))
        self.table.setCellWidget(row, 5, btn)
        
        # Login button
        login_btn = QPushButton("🔐 Login")
        login_btn.setStyleSheet(get_button_style(COLORS['purple'], 70, 10))
        login_btn.setMinimumHeight(28)
        login_btn.setMaximumWidth(90)
        login_btn.clicked.connect(lambda _, u=account.uid: self.login_clicked.emit(u))
        self.table.setCellWidget(row, 6, login_btn)
        
        # Status with badge style
        status_item = QTableWidgetItem(BrowserStatus.READY.value)
        status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        status_item.setForeground(QColor("#64748B"))
        self.table.setItem(row, 7, status_item)
    
    def clear(self) -> None:
        self.table.setRowCount(0)
    
    def select_all(self) -> None:
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                item.setCheckState(Qt.CheckState.Checked)
    
    def deselect_all(self) -> None:
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                item.setCheckState(Qt.CheckState.Unchecked)
    
    def get_selected_uids(self) -> List[str]:
        uids = []
        for row in range(self.table.rowCount()):
            chk = self.table.item(row, 0)
            if chk and chk.checkState() == Qt.CheckState.Checked:
                uid_item = self.table.item(row, 1)
                if uid_item:
                    uids.append(uid_item.text())
        return uids
    
    def update_browser_button(self, uid: str, text: str, enabled: bool, color: str) -> None:
        row = find_row_by_uid(self.table, uid)
        if row is not None:
            btn = self.table.cellWidget(row, 5)
            if btn:
                btn.setText(text)
                btn.setEnabled(enabled)
                btn.setStyleSheet(get_button_style(color, 70, 10))
    
    def update_login_button(self, uid: str, text: str, enabled: bool, color: str) -> None:
        row = find_row_by_uid(self.table, uid)
        if row is not None:
            btn = self.table.cellWidget(row, 6)
            if btn:
                btn.setText(text)
                btn.setEnabled(enabled)
                btn.setStyleSheet(get_button_style(color, 70, 10))
    
    def update_status(self, uid: str, status: str) -> None:
        row = find_row_by_uid(self.table, uid)
        if row is not None:
            item = self.table.item(row, 7)
            if item:
                item.setText(status)
                # Color based on status
                if "✅" in status:
                    item.setForeground(QColor(COLORS['success']))
                elif "❌" in status:
                    item.setForeground(QColor(COLORS['danger']))
                elif "⏳" in status:
                    item.setForeground(QColor(COLORS['warning']))
                else:
                    item.setForeground(QColor("#64748B"))
    
    def get_account_info(self, uid: str) -> Optional[tuple]:
        row = find_row_by_uid(self.table, uid)
        if row is not None:
            path_item = self.table.item(row, 4)
            if path_item:
                # Get full path from tooltip
                return (uid, path_item.toolTip() or path_item.text())
        return None
    
    def reset_all_buttons(self) -> None:
        for row in range(self.table.rowCount()):
            btn = self.table.cellWidget(row, 5)
            if btn:
                btn.setText("🌐 Open")
                btn.setEnabled(True)
                btn.setStyleSheet(get_button_style(COLORS['success'], 70, 10))
            
            status_item = self.table.item(row, 7)
            if status_item:
                status_item.setText(BrowserStatus.CLOSED.value)
                status_item.setForeground(QColor("#64748B"))
