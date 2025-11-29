"""Facebook Login Module - Automated login with 2FA support"""
import time
import logging
from typing import Optional, Dict, Callable, Any

import pyotp
from PyQt6.QtCore import QThread, pyqtSignal
from DrissionPage import ChromiumPage

logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class FacebookLoginWorker(QThread):
    """Worker thread for Facebook login process"""
    
    status_signal = pyqtSignal(str, str)
    progress_signal = pyqtSignal(str, int)
    success_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str, str)
    finished_signal = pyqtSignal(str)
    
    FB_LOGIN_URL = "https://www.facebook.com/"
    
    def __init__(self, driver: ChromiumPage, uid: str, password: str, token_2fa: str, parent=None):
        super().__init__(parent)
        self.driver = driver
        self.uid = uid
        self.password = password
        self.token_2fa = token_2fa
        self._is_cancelled = False
    
    def cancel(self) -> None:
        self._is_cancelled = True
    
    def run(self) -> None:
        try:
            self.status_signal.emit(self.uid, "Starting login...")
            self.progress_signal.emit(self.uid, 10)
            
            if not self._navigate_to_facebook():
                return
            if not self._enter_credentials():
                return
            if not self._handle_2fa():
                return
            if not self._verify_login():
                return
            
            self.progress_signal.emit(self.uid, 100)
            self.status_signal.emit(self.uid, "Login successful!")
            self.success_signal.emit(self.uid)
        except Exception as e:
            logger.exception(f"[{self.uid}] Login failed")
            self.error_signal.emit(self.uid, str(e))
        finally:
            self.finished_signal.emit(self.uid)
    
    def _navigate_to_facebook(self) -> bool:
        if self._is_cancelled:
            return False
        try:
            self.status_signal.emit(self.uid, "Navigating to Facebook...")
            self.progress_signal.emit(self.uid, 20)
            self.driver.get(self.FB_LOGIN_URL)
            time.sleep(2)
            return True
        except Exception as e:
            self.error_signal.emit(self.uid, f"Navigation failed: {e}")
            return False
    
    def _enter_credentials(self) -> bool:
        if self._is_cancelled:
            return False
        try:
            self.status_signal.emit(self.uid, "Entering credentials...")
            self.progress_signal.emit(self.uid, 40)
            
            email_field = self._find_element(['#email', 'input[name="email"]'])
            if not email_field:
                self.error_signal.emit(self.uid, "Email field not found")
                return False
            email_field.clear()
            email_field.input(self.uid)
            time.sleep(0.5)
            
            password_field = self._find_element(['#pass', 'input[name="pass"]', 'input[type="password"]'])
            if not password_field:
                self.error_signal.emit(self.uid, "Password field not found")
                return False
            password_field.clear()
            password_field.input(self.password)
            time.sleep(0.5)
            
            self.progress_signal.emit(self.uid, 50)
            
            login_btn = self._find_element(['button[name="login"]', 'button[type="submit"]', '#loginbutton'])
            if login_btn:
                login_btn.click()
            else:
                password_field.input('\n')
            
            time.sleep(3)
            return True
        except Exception as e:
            self.error_signal.emit(self.uid, f"Credentials failed: {e}")
            return False
    
    def _handle_2fa(self) -> bool:
        if self._is_cancelled:
            return False
        try:
            current_url = self.driver.url
            logger.debug(f"[{self.uid}] URL after login: {current_url}")
            
            is_2fa = 'checkpoint' in current_url or 'two_step' in current_url
            if not is_2fa:
                tfa_elem = self._find_element(['input[name="approvals_code"]', '#approvals_code'])
                is_2fa = tfa_elem is not None
            
            if not is_2fa:
                self.status_signal.emit(self.uid, "No 2FA required")
                return True
            
            self.status_signal.emit(self.uid, "2FA detected, generating code...")
            self.progress_signal.emit(self.uid, 70)
            
            code = self._generate_2fa_code()
            if not code:
                self.error_signal.emit(self.uid, "Failed to generate 2FA code")
                return False
            
            logger.info(f"[{self.uid}] Generated 2FA code: {code}")
            self.status_signal.emit(self.uid, f"Entering 2FA code: {code}")
            time.sleep(3)
            
            code_field = self._find_2fa_input()
            if not code_field:
                self.error_signal.emit(self.uid, "2FA input field not found")
                return False
            
            try:
                code_field.clear()
            except Exception:
                pass
            code_field.input(code)
            time.sleep(1)
            
            self.progress_signal.emit(self.uid, 80)
            
            submit_btn = self._find_element([
                'button[type="submit"]', '#checkpointSubmitButton',
                'button[name="submit[Continue]"]', 'input[type="submit"]'
            ])
            if submit_btn:
                submit_btn.click()
            else:
                code_field.input('\n')
            
            time.sleep(3)
            self._handle_trust_device()
            return True
        except Exception as e:
            logger.exception(f"[{self.uid}] 2FA failed")
            self.error_signal.emit(self.uid, f"2FA failed: {e}")
            return False
    
    def _generate_2fa_code(self) -> Optional[str]:
        try:
            clean_token = self.token_2fa.replace(" ", "").upper()
            return pyotp.TOTP(clean_token).now()
        except Exception as e:
            logger.exception(f"[{self.uid}] 2FA code generation failed")
            return None
    
    def _find_2fa_input(self) -> Optional[Any]:
        """Find 2FA input field using multiple methods"""
        # CSS selectors
        selectors = [
            'input[name="approvals_code"]', '#approvals_code',
            'input[autocomplete="one-time-code"]',
            'input[type="text"]', 'input[type="tel"]', 'input[type="number"]'
        ]
        for sel in selectors:
            try:
                elem = self.driver.ele(sel, timeout=1)
                if elem and elem.attr('name') not in ['email', 'pass']:
                    return elem
            except Exception:
                continue
        
        # JavaScript fallback
        try:
            js = """
            var inputs = document.querySelectorAll('input[type="text"], input[type="tel"], input[type="number"]');
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].offsetParent !== null && inputs[i].name !== 'email' && inputs[i].name !== 'pass') {
                    inputs[i].focus();
                    return true;
                }
            }
            return false;
            """
            if self.driver.run_js(js):
                return self.driver.ele('@focused', timeout=1)
        except Exception:
            pass
        return None
    
    def _handle_trust_device(self) -> None:
        """Handle 'Trust this device' prompt"""
        try:
            time.sleep(2)
            if 'checkpoint' not in self.driver.url:
                return
            
            logger.info(f"[{self.uid}] Trust device page detected")
            
            # Try JavaScript click
            js = """
            var buttons = document.querySelectorAll('div[role="button"], span[role="button"], button');
            for (var i = 0; i < buttons.length; i++) {
                var text = buttons[i].innerText.toLowerCase();
                if (text.includes('trust') || text.includes('tin tưởng')) {
                    buttons[i].click();
                    return true;
                }
            }
            return false;
            """
            if self.driver.run_js(js):
                logger.info(f"[{self.uid}] Clicked Trust button")
                time.sleep(3)
        except Exception as e:
            logger.warning(f"[{self.uid}] Trust device handling failed: {e}")
    
    def _verify_login(self) -> bool:
        if self._is_cancelled:
            return False
        try:
            self.status_signal.emit(self.uid, "Verifying login...")
            self.progress_signal.emit(self.uid, 90)
            time.sleep(2)
            
            url = self.driver.url
            success_indicators = ['facebook.com/home', 'facebook.com/?sk=', 'facebook.com/feed']
            failure_indicators = ['login', 'checkpoint', 'recover', 'disabled']
            
            is_success = any(ind in url for ind in success_indicators)
            is_failure = any(ind in url for ind in failure_indicators)
            
            if is_success and not is_failure:
                return True
            
            user_elem = self._find_element(['[aria-label="Your profile"]', '[aria-label="Account"]'])
            if user_elem:
                return True
            
            if 'checkpoint' in url:
                self.error_signal.emit(self.uid, "Additional verification required")
                return False
            
            return True
        except Exception as e:
            self.error_signal.emit(self.uid, f"Verification failed: {e}")
            return False
    
    def _find_element(self, selectors: list) -> Optional[Any]:
        for sel in selectors:
            try:
                elem = self.driver.ele(sel, timeout=2)
                if elem:
                    return elem
            except Exception:
                continue
        return None


class FacebookLoginManager:
    """Manages Facebook login operations"""
    
    def __init__(self):
        self.workers: Dict[str, FacebookLoginWorker] = {}
    
    def start_login(self, driver: ChromiumPage, uid: str, password: str, token_2fa: str,
                    status_callback: Optional[Callable] = None,
                    progress_callback: Optional[Callable] = None,
                    success_callback: Optional[Callable] = None,
                    error_callback: Optional[Callable] = None,
                    finished_callback: Optional[Callable] = None) -> bool:
        if uid in self.workers and self.workers[uid].isRunning():
            return False
        
        worker = FacebookLoginWorker(driver, uid, password, token_2fa)
        
        if status_callback:
            worker.status_signal.connect(status_callback)
        if progress_callback:
            worker.progress_signal.connect(progress_callback)
        if success_callback:
            worker.success_signal.connect(success_callback)
        if error_callback:
            worker.error_signal.connect(error_callback)
        if finished_callback:
            worker.finished_signal.connect(finished_callback)
        
        self.workers[uid] = worker
        worker.start()
        return True
    
    def cancel_login(self, uid: str) -> None:
        if uid in self.workers:
            self.workers[uid].cancel()
    
    def is_logging_in(self, uid: str) -> bool:
        return uid in self.workers and self.workers[uid].isRunning()
    
    def cleanup(self) -> None:
        for worker in list(self.workers.values()):
            if worker.isRunning():
                worker.cancel()
                worker.wait(2000)
        self.workers.clear()
