"""Modern beautiful styles for the application"""

# Color palette
COLORS = {
    'primary': '#3B82F6',      # Blue
    'primary_dark': '#2563EB',
    'success': '#10B981',      # Green
    'success_dark': '#059669',
    'danger': '#EF4444',       # Red
    'danger_dark': '#DC2626',
    'warning': '#F59E0B',      # Orange
    'warning_dark': '#D97706',
    'purple': '#8B5CF6',
    'purple_dark': '#7C3AED',
    'gray': '#6B7280',
    'gray_dark': '#4B5563',
    'bg_light': '#F8FAFC',
    'bg_card': '#FFFFFF',
    'border': '#E2E8F0',
    'text': '#1E293B',
    'text_secondary': '#64748B',
}

MAIN_STYLESHEET = """
    QMainWindow {
        background-color: #F1F5F9;
    }
    QGroupBox {
        font-weight: 600;
        font-size: 13px;
        color: #1E293B;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        margin-top: 16px;
        padding: 16px;
        background-color: #FFFFFF;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 16px;
        top: 4px;
        padding: 0 8px;
        background-color: #FFFFFF;
    }
    QPushButton {
        background-color: #3B82F6;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: #2563EB;
    }
    QPushButton:pressed {
        background-color: #1D4ED8;
    }
    QPushButton:disabled {
        background-color: #CBD5E1;
        color: #94A3B8;
    }
    QPlainTextEdit {
        border: 2px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px;
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        font-size: 12px;
        background-color: #F8FAFC;
        color: #1E293B;
        selection-background-color: #BFDBFE;
    }
    QPlainTextEdit:focus {
        border-color: #3B82F6;
        background-color: #FFFFFF;
    }
    QTableWidget {
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        gridline-color: #F1F5F9;
        background-color: #FFFFFF;
        alternate-background-color: #F8FAFC;
        selection-background-color: #DBEAFE;
        selection-color: #1E293B;
    }
    QTableWidget::item {
        padding: 8px 12px;
        border-bottom: 1px solid #F1F5F9;
    }
    QTableWidget::item:selected {
        background-color: #DBEAFE;
        color: #1E293B;
    }
    QHeaderView::section {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #3B82F6, stop:1 #2563EB);
        color: white;
        padding: 12px 8px;
        border: none;
        font-weight: 600;
        font-size: 12px;
    }
    QHeaderView::section:first {
        border-top-left-radius: 8px;
    }
    QHeaderView::section:last {
        border-top-right-radius: 8px;
    }
    QStatusBar {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #EFF6FF, stop:1 #DBEAFE);
        color: #1E40AF;
        font-weight: 500;
        padding: 8px;
        border-top: 1px solid #BFDBFE;
    }
    QScrollBar:vertical {
        background-color: #F1F5F9;
        width: 12px;
        border-radius: 6px;
        margin: 0;
    }
    QScrollBar::handle:vertical {
        background-color: #CBD5E1;
        border-radius: 6px;
        min-height: 30px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #94A3B8;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0;
    }
    QSplitter::handle {
        background-color: #E2E8F0;
        height: 2px;
    }
    QSplitter::handle:hover {
        background-color: #3B82F6;
    }
    QToolTip {
        background-color: #1E293B;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 11px;
    }
"""

BUTTON_STYLES = {
    'primary': '#3B82F6',
    'success': '#10B981',
    'danger': '#EF4444',
    'warning': '#F59E0B',
    'purple': '#8B5CF6',
    'gray': '#6B7280',
}

BUTTON_HOVER = {
    '#3B82F6': '#2563EB',
    '#10B981': '#059669',
    '#EF4444': '#DC2626',
    '#F59E0B': '#D97706',
    '#8B5CF6': '#7C3AED',
    '#6B7280': '#4B5563',
}


def get_button_style(color: str, min_width: int = 70, font_size: int = 11) -> str:
    """Generate modern button stylesheet"""
    hover = BUTTON_HOVER.get(color, color)
    return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            font-size: {font_size}px;
            font-weight: 600;
            padding: 8px 12px;
            min-width: {min_width}px;
            border: none;
            border-radius: 6px;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
        QPushButton:pressed {{
            background-color: {hover};
            padding-top: 9px;
            padding-bottom: 7px;
        }}
        QPushButton:disabled {{
            background-color: #CBD5E1;
            color: #94A3B8;
        }}
    """


def get_icon_button_style(color: str, size: int = 36) -> str:
    """Generate icon button style"""
    hover = BUTTON_HOVER.get(color, color)
    return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            font-size: 14px;
            min-width: {size}px;
            max-width: {size}px;
            min-height: {size}px;
            max-height: {size}px;
            border: none;
            border-radius: {size // 2}px;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
    """


FRAME_STYLES = {
    'browser': """
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #EFF6FF, stop:1 #DBEAFE);
            border: 1px solid #BFDBFE;
            border-radius: 12px;
            padding: 8px;
        }
    """,
    'login': """
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #F5F3FF, stop:1 #EDE9FE);
            border: 1px solid #DDD6FE;
            border-radius: 12px;
            padding: 8px;
        }
    """,
}

INPUT_LABEL_STYLE = """
    color: #64748B;
    font-size: 11px;
    font-weight: 500;
    padding: 4px 0;
"""

COUNT_LABEL_STYLE = """
    font-weight: 700;
    font-size: 14px;
    color: #3B82F6;
    background-color: #EFF6FF;
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid #BFDBFE;
"""

SECTION_TITLE_STYLE = """
    font-weight: 700;
    font-size: 13px;
    color: #1E293B;
"""
