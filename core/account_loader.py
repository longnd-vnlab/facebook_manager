"""Account Loader Module - Parsing and validation of Facebook account data"""
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple

from config import PROFILES_DIR


@dataclass
class Account:
    """Data class representing a Facebook account"""
    uid: str
    password: str
    token: str
    profile_path: str


class AccountLoader:
    """Handles loading and parsing of account data"""
    
    def __init__(self, profiles_base_dir: str = PROFILES_DIR):
        self.profiles_base_dir = profiles_base_dir
    
    def parse_line(self, line: str) -> Optional[Tuple[str, str, str]]:
        """Parse a single line: UID|PASSWORD|TOKEN"""
        line = line.strip()
        if not line or "|" not in line:
            return None
        
        parts = line.split("|")
        if len(parts) < 3:
            return None
        
        uid, password, token = parts[0].strip(), parts[1].strip(), parts[2].strip()
        return (uid, password, token) if uid and password and token else None
    
    def create_profile_directory(self, uid: str) -> str:
        """Create profile directory for UID, return absolute path"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        profile_path = os.path.join(base_dir, self.profiles_base_dir, uid)
        os.makedirs(profile_path, exist_ok=True)
        return profile_path
    
    def load_accounts(self, text_data: str) -> List[Account]:
        """Load accounts from multi-line text"""
        accounts = []
        for line in text_data.strip().split("\n"):
            parsed = self.parse_line(line)
            if parsed:
                uid, password, token = parsed
                accounts.append(Account(
                    uid=uid, password=password, token=token,
                    profile_path=self.create_profile_directory(uid)
                ))
        return accounts
    
    def validate_accounts(self, text_data: str) -> Tuple[int, int, List[str]]:
        """Validate account data, return (valid_count, invalid_count, errors)"""
        valid, invalid, errors = 0, 0, []
        
        for i, line in enumerate(text_data.strip().split("\n"), 1):
            line = line.strip()
            if not line:
                continue
            if self.parse_line(line):
                valid += 1
            else:
                invalid += 1
                display = f"'{line[:50]}...'" if len(line) > 50 else f"'{line}'"
                errors.append(f"Line {i}: Invalid format - {display}")
        
        return (valid, invalid, errors)
