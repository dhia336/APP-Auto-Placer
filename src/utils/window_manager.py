import subprocess
from pywinauto import Application
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class WindowManager:
    """Manages window operations using pywinauto."""
    
    @staticmethod
    def open_app(shortcut_path: str) -> None:
        """Opens an application using its shortcut path."""
        try:
            subprocess.Popen(shortcut_path, shell=True)
        except Exception as e:
            logger.error(f"Failed to open app {shortcut_path}: {e}")
            raise

    @staticmethod
    def move_and_resize_window(executable_name: str, position: Tuple[int, int], size: Tuple[int, int]) -> None:
        """Moves and resizes a window by its executable name."""
        try:
            app = Application(backend='win32').connect(path=executable_name)
            window = app.top_window()
            window.move_window(x=position[0], y=position[1], width=size[0], height=size[1])
        except Exception as e:
            logger.error(f"Failed to move/resize window {executable_name}: {e}")
            raise 