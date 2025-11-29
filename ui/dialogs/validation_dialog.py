"""Modern validation results dialog"""
from typing import List
from PyQt6.QtWidgets import QMessageBox


class ValidationDialog:
    """Dialog for showing validation results with modern styling"""
    
    @staticmethod
    def show(parent, valid: int, invalid: int, errors: List[str]) -> None:
        msg = QMessageBox(parent)
        msg.setWindowTitle("📊 Validation Results")
        msg.setIcon(QMessageBox.Icon.Information)
        
        text = f"""
<div style='font-family: Segoe UI, sans-serif;'>
    <h3 style='color: #1E293B; margin-bottom: 16px;'>Validation Complete</h3>
    
    <div style='background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 12px; margin-bottom: 8px;'>
        <span style='color: #166534; font-size: 14px;'>✅ Valid accounts: <b>{valid}</b></span>
    </div>
    
    <div style='background: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px; padding: 12px;'>
        <span style='color: #991B1B; font-size: 14px;'>❌ Invalid accounts: <b>{invalid}</b></span>
    </div>
"""
        
        if errors:
            text += """
    <div style='margin-top: 16px;'>
        <p style='color: #64748B; font-size: 12px; margin-bottom: 8px;'>Errors found:</p>
        <div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; font-size: 11px; color: #475569;'>
"""
            for error in errors[:10]:
                text += f"• {error}<br/>"
            if len(errors) > 10:
                text += f"<br/><i>... and {len(errors) - 10} more errors</i>"
            text += "</div></div>"
        
        text += "</div>"
        
        msg.setTextFormat(msg.textFormat().RichText)
        msg.setText(text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 8px 24px;
                border-radius: 6px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        msg.exec()
