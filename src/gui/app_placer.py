import customtkinter as ctk
from typing import List, Tuple
import logging
from time import sleep
import json
from ..utils.window_manager import WindowManager
from ..utils.config_manager import AppConfig, ConfigManager
from ..utils.screen_manager import PositionSelector, ScreenManager

logger = logging.getLogger(__name__)

class AppPlacerGUI:
    """Main GUI application for the Auto-Placer."""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AUTO-PLACER")
        self.apps: List[List[ctk.CTkWidget]] = []
        self.current_row = 0
        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the main UI components."""
        # Title
        title_label = ctk.CTkLabel(self.root, text="AUTO-PLACER", font=("", 30))
        title_label.pack(padx=20, pady=10)

        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.root)
        buttons_frame.pack(pady=10, padx=20)

        # Main buttons
        self.add_button = ctk.CTkButton(buttons_frame, text="ADD", command=self.add_app)
        self.add_button.pack(side=ctk.LEFT, padx=10, pady=5)

        self.remove_button = ctk.CTkButton(buttons_frame, text="REMOVE", command=self.remove_app)
        self.remove_button.pack(side=ctk.LEFT, padx=10, pady=10)

        self.open_button = ctk.CTkButton(buttons_frame, text="OPEN", command=self.open_apps)
        self.open_button.pack(side=ctk.LEFT, padx=10, pady=5)

        # Import/Export buttons
        self.import_button = ctk.CTkButton(buttons_frame, text="IMPORT", command=self.import_config)
        self.import_button.pack(side=ctk.LEFT, padx=10, pady=5)

        self.export_button = ctk.CTkButton(buttons_frame, text="EXPORT", command=self.export_config)
        self.export_button.pack(side=ctk.LEFT, padx=10, pady=5)

        # Windows frame
        self.windows_frame = ctk.CTkFrame(self.root)
        self.windows_frame.pack(pady=10, padx=20)

        # Add initial app row
        self.add_app()

    def add_app(self) -> None:
        """Adds a new app configuration row."""
        if self.current_row >= 8:
            return

        app_widgets = [
            ctk.CTkButton(
                self.windows_frame,
                text="Click to choose an app!",
                command=lambda: self.choose_shortcut(app_widgets[0])
            ),
            ctk.CTkButton(
                self.windows_frame,
                text="Select Position",
                command=lambda: self.select_position(app_widgets[2], app_widgets[3])
            ),
            ctk.CTkEntry(
                self.windows_frame,
                width=140,
                placeholder_text="Position (e.g., 500*300)"
            ),
            ctk.CTkEntry(
                self.windows_frame,
                width=90,
                placeholder_text="Size"
            )
        ]

        for col, widget in enumerate(app_widgets):
            widget.grid(column=col, row=self.current_row, padx=10, pady=10)

        self.apps.append(app_widgets)
        self.current_row += 1

    def remove_app(self) -> None:
        """Removes the last app configuration row."""
        if self.current_row <= 1:
            return

        for widget in self.apps[-1]:
            widget.grid_forget()
        self.apps.pop()
        self.current_row -= 1

    def choose_shortcut(self, button: ctk.CTkButton) -> None:
        """Opens a file dialog to choose an application shortcut."""
        file_path = ctk.filedialog.askopenfilename(
            title="Choose a shortcut file",
            filetypes=(
                ("Executables", "*.exe"),
                ("Shortcuts", "*.lnk")
            )
        )
        if file_path:
            button.configure(text=file_path)

    def select_position(self, position_entry: ctk.CTkEntry, size_entry: ctk.CTkEntry) -> None:
        """Opens a visual position and size selector."""
        # Get current values if they exist
        try:
            current_pos = self.parse_position_size(position_entry.get())
            current_size = self.parse_position_size(size_entry.get())
        except ValueError:
            # Default to center of screen if no valid values
            screen_size = ScreenManager.get_screen_size()
            current_pos = (screen_size[0] // 4, screen_size[1] // 4)
            current_size = (screen_size[0] // 2, screen_size[1] // 2)

        # Create and show the position selector
        selector = PositionSelector(self.root, current_pos, current_size)
        self.root.wait_window(selector)

        # Get the selected position and size
        position, size = selector.get_position_and_size()
        
        # Update the entry fields
        position_entry.delete(0, 'end')
        position_entry.insert(0, f"{position[0]}*{position[1]}")
        
        size_entry.delete(0, 'end')
        size_entry.insert(0, f"{size[0]}*{size[1]}")

    def parse_position_size(self, value: str) -> Tuple[int, int]:
        """Parses position or size string into a tuple of integers."""
        try:
            x, y = map(int, value.split("*"))
            return (x, y)
        except ValueError:
            raise ValueError(f"Invalid format: {value}. Expected format: number*number")

    def get_app_configs(self) -> List[AppConfig]:
        """Gets the current configuration for all apps."""
        configs = []
        for app_widgets in self.apps:
            shortcut_path = app_widgets[0].cget("text")
            if shortcut_path == "Click to choose an app!":
                continue

            try:
                position = self.parse_position_size(app_widgets[2].get())
                size = self.parse_position_size(app_widgets[3].get())
                configs.append(AppConfig(shortcut_path, position, size))
            except ValueError as e:
                logger.error(f"Invalid configuration: {e}")
                continue

        return configs

    def toggle_widgets(self, state: str) -> None:
        """Enables or disables all widgets."""
        for app_widgets in self.apps:
            for widget in app_widgets:
                widget.configure(state=state)
        
        self.add_button.configure(state=state)
        self.remove_button.configure(state=state)
        self.open_button.configure(state=state)
        self.import_button.configure(state=state)
        self.export_button.configure(state=state)

    def open_apps(self) -> None:
        """Opens and positions all configured applications."""
        self.toggle_widgets("disabled")
        
        try:
            configs = self.get_app_configs()
            
            # Open all apps first
            for config in configs:
                WindowManager.open_app(config.shortcut_path)
            
            # Wait for apps to open
            sleep(2)
            
            # Position all windows
            for config in configs:
                WindowManager.move_and_resize_window(
                    config.shortcut_path,
                    config.position,
                    config.size
                )
        except Exception as e:
            logger.error(f"Error during app placement: {e}")
        finally:
            self.toggle_widgets("normal")

    def import_config(self) -> None:
        """Imports configuration from a JSON file."""
        file_path = ctk.filedialog.askopenfilename(
            title="Import Configuration",
            filetypes=[("JSON files", "*.json")]
        )
        if not file_path:
            return

        try:
            configs = ConfigManager.load_configs(file_path)
            
            # Clear existing apps
            while self.current_row > 1:
                self.remove_app()
            
            # Add new apps
            for config in configs:
                if self.current_row >= 8:
                    break
                    
                app_widgets = [
                    ctk.CTkButton(
                        self.windows_frame,
                        text=config.shortcut_path,
                        command=lambda: self.choose_shortcut(app_widgets[0])
                    ),
                    ctk.CTkButton(
                        self.windows_frame,
                        text="Select Position",
                        command=lambda: self.select_position(app_widgets[2], app_widgets[3])
                    ),
                    ctk.CTkEntry(
                        self.windows_frame,
                        width=140,
                        placeholder_text="Position (e.g., 500*300)"
                    ),
                    ctk.CTkEntry(
                        self.windows_frame,
                        width=90,
                        placeholder_text="Size"
                    )
                ]

                for col, widget in enumerate(app_widgets):
                    widget.grid(column=col, row=self.current_row, padx=10, pady=10)
                
                app_widgets[2].insert(0, f"{config.position[0]}*{config.position[1]}")
                app_widgets[3].insert(0, f"{config.size[0]}*{config.size[1]}")
                
                self.apps.append(app_widgets)
                self.current_row += 1

        except Exception as e:
            logger.error(f"Failed to import configuration: {e}")

    def export_config(self) -> None:
        """Exports current configuration to a JSON file."""
        file_path = ctk.filedialog.asksaveasfilename(
            title="Export Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if not file_path:
            return

        try:
            configs = self.get_app_configs()
            ConfigManager.save_configs(configs, file_path)
        except Exception as e:
            logger.error(f"Failed to export configuration: {e}")

    def run(self) -> None:
        """Starts the main application loop."""
        self.root.mainloop() 