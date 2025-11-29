"""Input section widget with modern design"""
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QPlainTextEdit, 
    QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import pyqtSignal
from ..styles import INPUT_LABEL_STYLE, COUNT_LABEL_STYLE, get_button_style, COLORS


class InputSection(QGroupBox):
    """Modern account input widget"""
    
    load_clicked = pyqtSignal()
    clear_clicked = pyqtSignal()
    validate_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("📝 Account Input", parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 20, 16, 16)
        
        # Instructions with icon
        instructions = QLabel(
            "💡 Enter accounts in format: UID|PASSWORD|TOKEN (one per line)"
        )
        instructions.setStyleSheet(INPUT_LABEL_STYLE)
        layout.addWidget(instructions)
        
        # Text input with placeholder
        self.input_box = QPlainTextEdit()
        self.input_box.setPlaceholderText(
            "100048068360222|mypassword|SECRETTOKEN123\n"
            "100048433699046|password2|ANOTHERTOKEN456\n"
            "..."
        )
        self.input_box.setMinimumHeight(100)
        self.input_box.setMaximumHeight(150)
        layout.addWidget(self.input_box)
        
        # Button row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_load = QPushButton("📥 Load Accounts")
        self.btn_load.setMinimumHeight(40)
        self.btn_load.setStyleSheet(get_button_style(COLORS['primary'], 130, 12))
        self.btn_load.clicked.connect(self.load_clicked.emit)
        btn_layout.addWidget(self.btn_load)
        
        self.btn_validate = QPushButton("✅ Validate")
        self.btn_validate.setMinimumHeight(40)
        self.btn_validate.setStyleSheet(get_button_style(COLORS['success'], 100, 12))
        self.btn_validate.clicked.connect(self.validate_clicked.emit)
        btn_layout.addWidget(self.btn_validate)
        
        self.btn_clear = QPushButton("🗑️ Clear")
        self.btn_clear.setMinimumHeight(40)
        self.btn_clear.setStyleSheet(get_button_style(COLORS['gray'], 80, 12))
        self.btn_clear.clicked.connect(self.clear_clicked.emit)
        btn_layout.addWidget(self.btn_clear)
        
        btn_layout.addStretch()
        
        # Account count badge
        self.lbl_count = QLabel("📊 0 accounts")
        self.lbl_count.setStyleSheet(COUNT_LABEL_STYLE)
        btn_layout.addWidget(self.lbl_count)
        
        layout.addLayout(btn_layout)
    
    def get_text(self) -> str:
        return self.input_box.toPlainText().strip()
    
    def clear(self) -> None:
        self.input_box.clear()
    
    def set_count(self, count: int) -> None:
        self.lbl_count.setText(f"📊 {count} accounts")
