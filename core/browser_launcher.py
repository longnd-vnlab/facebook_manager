"""Browser Launcher Module - Chrome browser management with DrissionPage"""
import logging
import socket
import subprocess
from typing import Optional, Tuple, Dict

from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication
from DrissionPage import ChromiumPage, ChromiumOptions

from config import CHROME_PATH, GRID_COLS, GRID_ROWS

logger = logging.getLogger(__name__)


def find_free_port() -> int:
    """Get an available port number"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def get_screen_size() -> Tuple[int, int]:
    """Get primary screen size"""
    try:
        app = QApplication.instance()
        if app:
            screen = app.primaryScreen()
            if screen:
                size = screen.availableGeometry()
                return size.width(), size.height()
    except Exception as e:
        logger.warning(f"Failed to get screen size: {e}")
    return 1920, 1080


def kill_existing_chrome_processes(profile_path: str) -> None:
    """Kill any existing Chrome processes using the same profile"""
    try:
        result = subprocess.run(
            ['pgrep', '-f', f'--user-data-dir={profile_path}'],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            for pid in result.stdout.strip().split('\n'):
                try:
                    subprocess.run(['kill', '-9', pid], capture_output=True)
                except Exception as e:
                    logger.warning(f"Failed to kill process {pid}: {e}")
    except Exception as e:
        logger.warning(f"Failed to kill Chrome processes: {e}")


class BrowserLaunchWorker(QThread):
    """Worker thread for launching Chrome browser"""
    
    started_signal = pyqtSignal(str)
    success_signal = pyqtSignal(str, object)
    error_signal = pyqtSignal(str, str)
    finished_signal = pyqtSignal(str)
    
    def __init__(self, uid: str, profile_path: str, proxy: Optional[str] = None,
                 window_position: Optional[Tuple[int, int]] = None,
                 window_size: Optional[Tuple[int, int]] = None, parent=None):
        super().__init__(parent)
        self.uid = uid
        self.profile_path = profile_path
        self.proxy = proxy
        self.window_position = window_position
        self.window_size = window_size
        self.driver: Optional[ChromiumPage] = None
    
    def run(self) -> None:
        try:
            self.started_signal.emit(self.uid)
            kill_existing_chrome_processes(self.profile_path)
            
            self.driver = self._create_chrome_driver()
            if self.driver:
                self._set_window_geometry()
                self.success_signal.emit(self.uid, self.driver)
            else:
                self.error_signal.emit(self.uid, "Failed to create driver")
        except Exception as e:
            logger.exception(f"Browser launch failed for {self.uid}")
            self.error_signal.emit(self.uid, str(e))
        finally:
            self.finished_signal.emit(self.uid)
    
    def _set_window_geometry(self) -> None:
        """Set window position and size"""
        if not (self.window_position and self.window_size):
            return
        try:
            import time
            time.sleep(0.5)
            w, h = self.window_size
            x, y = self.window_position
            
            try:
                self.driver.set.window.size(w, h)
                self.driver.set.window.location(x, y)
            except Exception:
                self.driver.run_js(f'window.resizeTo({w}, {h}); window.moveTo({x}, {y});')
            
            logger.info(f"[{self.uid}] Window set to: pos=({x},{y}), size=({w}x{h})")
        except Exception as e:
            logger.warning(f"Failed to set window geometry: {e}")
    
    def _create_chrome_driver(self) -> Optional[ChromiumPage]:
        """Create Chrome driver with DrissionPage"""
        try:
            port = find_free_port()
            options = ChromiumOptions()
            options.set_paths(local_port=port, user_data_path=self.profile_path)
            options.set_paths(CHROME_PATH)
            
            arguments = [
                f'--user-data-dir={self.profile_path}',
                '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
                '--disable-features=IsolateOrigins,site-per-process,TranslateUI,Translate',
                '-no-first-run', '-force-color-profile=srgb', '-metrics-recording-only',
                '-password-store=basic', '-use-mock-keychain', '-no-default-browser-check',
                '-disable-background-mode', '-deny-permission-prompts',
            ]
            
            if self.window_size:
                arguments.append(f'--window-size={self.window_size[0]},{self.window_size[1]}')
            if self.window_position:
                arguments.append(f'--window-position={self.window_position[0]},{self.window_position[1]}')
            
            if self.proxy:
                arguments.append(f'--proxy-server={self.proxy}')
            else:
                arguments.extend(['--no-proxy-server', '--proxy-server="direct://"', '--proxy-bypass-list=*'])
            
            for arg in arguments:
                options.set_argument(arg)
            
            return ChromiumPage(options)
        except Exception as e:
            logger.exception(f"Chrome driver creation failed: {e}")
            raise


class BrowserManager(QObject):
    """Manages multiple browser instances"""
    
    browser_starting = pyqtSignal(str)
    browser_started = pyqtSignal(str)
    browser_error = pyqtSignal(str, str)
    browser_closed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.workers: Dict[str, BrowserLaunchWorker] = {}
        self.drivers: Dict[str, ChromiumPage] = {}
        self.browser_count = 0
        self._calculate_grid()
    
    def _calculate_grid(self) -> None:
        screen_w, screen_h = get_screen_size()
        self.browser_width = max(screen_w // GRID_COLS, 400)
        self.browser_height = max(screen_h // GRID_ROWS, 300)
        logger.info(f"Grid: {screen_w}x{screen_h} -> {self.browser_width}x{self.browser_height}")
    
    def _get_next_position(self) -> Tuple[int, int]:
        self._calculate_grid()
        idx = self.browser_count % (GRID_COLS * GRID_ROWS)
        col, row = idx % GRID_COLS, idx // GRID_COLS
        x, y = col * self.browser_width, row * self.browser_height
        self.browser_count += 1
        logger.debug(f"Browser #{self.browser_count}: pos=({x},{y})")
        return (x, y)
    
    def launch_browser(self, uid: str, profile_path: str, proxy: Optional[str] = None) -> None:
        if uid in self.drivers or (uid in self.workers and self.workers[uid].isRunning()):
            logger.info(f"Browser already running/launching for {uid}")
            return
        
        position = self._get_next_position()
        size = (self.browser_width, self.browser_height)
        
        worker = BrowserLaunchWorker(uid, profile_path, proxy, position, size, self)
        worker.started_signal.connect(lambda u: self.browser_starting.emit(u))
        worker.success_signal.connect(self._on_browser_started)
        worker.error_signal.connect(lambda u, e: self.browser_error.emit(u, e))
        worker.finished_signal.connect(self._on_worker_finished)
        
        self.workers[uid] = worker
        worker.start()
    
    def _on_browser_started(self, uid: str, driver: ChromiumPage) -> None:
        self.drivers[uid] = driver
        self.browser_started.emit(uid)
    
    def _on_worker_finished(self, uid: str) -> None:
        if uid in self.workers:
            worker = self.workers[uid]
            if worker.isRunning():
                worker.wait(1000)
            worker.deleteLater()
            del self.workers[uid]
    
    def close_browser(self, uid: str) -> None:
        if uid in self.drivers:
            try:
                self.drivers[uid].quit()
            except Exception as e:
                logger.warning(f"Failed to close browser {uid}: {e}")
            del self.drivers[uid]
            self.browser_closed.emit(uid)
    
    def close_all_browsers(self) -> None:
        for uid in list(self.drivers.keys()):
            self.close_browser(uid)
    
    def is_browser_running(self, uid: str) -> bool:
        return uid in self.drivers
    
    def is_browser_launching(self, uid: str) -> bool:
        return uid in self.workers and self.workers[uid].isRunning()
    
    def get_driver(self, uid: str) -> Optional[ChromiumPage]:
        return self.drivers.get(uid)
    
    def cleanup(self) -> None:
        for worker in list(self.workers.values()):
            if worker.isRunning():
                worker.wait(2000)
        self.close_all_browsers()
