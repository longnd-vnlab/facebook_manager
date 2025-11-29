"""UI helper functions"""
from typing import Optional
from PyQt6.QtWidgets import QTableWidget


def find_row_by_uid(table: QTableWidget, uid: str) -> Optional[int]:
    """Find table row index by UID"""
    for row in range(table.rowCount()):
        item = table.item(row, 1)
        if item and item.text() == uid:
            return row
    return None
