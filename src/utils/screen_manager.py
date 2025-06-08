import tkinter as tk
from typing import Tuple, Optional
import logging
from pywinauto import Desktop
import win32gui
import win32con

logger = logging.getLogger(__name__)

class ScreenManager:
    """Manages screen-related operations and window position/size selection."""
    
    @staticmethod
    def get_screen_size() -> Tuple[int, int]:
        """Get the primary screen size."""
        try:
            desktop = Desktop(backend="win32")
            window = desktop.window()
            return (window.rectangle().width, window.rectangle().height)
        except Exception as e:
            logger.error(f"Failed to get screen size: {e}")
            # Fallback to a default size
            return (1920, 1080)

    @staticmethod
    def get_window_rect(window_title: str) -> Optional[Tuple[int, int, int, int]]:
        """Get the rectangle of a window by its title."""
        try:
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd:
                return win32gui.GetWindowRect(hwnd)
            return None
        except Exception as e:
            logger.error(f"Failed to get window rectangle: {e}")
            return None

class PositionSelector(tk.Toplevel):
    """A window for selecting window position and size visually."""
    
    def __init__(self, parent, initial_position: Tuple[int, int] = (0, 0), initial_size: Tuple[int, int] = (800, 600)):
        super().__init__(parent)
        self.title("Position and Size Selector")
        self.attributes('-topmost', True)
        
        # Make the window semi-transparent
        self.attributes('-alpha', 0.7)
        
        # Remove window decorations
        self.overrideredirect(True)
        
        # Set initial position and size
        self.geometry(f"{initial_size[0]}x{initial_size[1]}+{initial_position[0]}+{initial_position[1]}")
        
        # Add a border to make it visible
        self.configure(bg='blue')
        
        # Store current position and size
        self.current_position = initial_position
        self.current_size = initial_size
        
        # Bind mouse events
        self.bind('<Button-1>', self.start_move)
        self.bind('<B1-Motion>', self.on_move)
        self.bind('<Button-3>', self.start_resize)
        self.bind('<B3-Motion>', self.on_resize)
        self.bind('<Escape>', self.on_confirm)
        
        # Add instructions label
        self.instructions = tk.Label(
            self,
            text="Left click and drag to move\nRight click and drag to resize\nPress ESC to confirm",
            bg='blue',
            fg='white',
            font=('Arial', 12)
        )
        self.instructions.place(relx=0.5, rely=0.5, anchor='center')
        
        # Center the window on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - initial_size[0]) // 2
        y = (screen_height - initial_size[1]) // 2
        self.geometry(f"+{x}+{y}")
        
        # Update initial position after centering
        self.current_position = (x, y)

    def start_move(self, event):
        """Start moving the window."""
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        """Move the window."""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
        self.current_position = (x, y)

    def start_resize(self, event):
        """Start resizing the window."""
        self.start_x = event.x
        self.start_y = event.y
        self.start_width = self.winfo_width()
        self.start_height = self.winfo_height()

    def on_resize(self, event):
        """Resize the window."""
        width = self.start_width + (event.x - self.start_x)
        height = self.start_height + (event.y - self.start_y)
        self.geometry(f"{width}x{height}")
        self.current_size = (width, height)

    def on_confirm(self, event=None):
        """Handle confirmation of position and size."""
        self.result = (self.current_position, self.current_size)
        self.destroy()

    def get_position_and_size(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Get the current position and size of the window."""
        return self.result if self.result else (self.current_position, self.current_size) 