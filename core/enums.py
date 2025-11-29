"""Enums for status values"""
from enum import Enum


class BrowserStatus(Enum):
    READY = "Ready"
    LAUNCHING = "⏳ Launching..."
    RUNNING = "✅ Running"
    CLOSED = "Browser closed"
    ERROR = "❌ Error"


class LoginStatus(Enum):
    IDLE = "Ready"
    LOGGING_IN = "Logging in..."
    SUCCESS = "✅ Logged in"
    FAILED = "❌ Failed"
