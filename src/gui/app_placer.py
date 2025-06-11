import customtkinter as ctk
from typing import List, Tuple, Union
import logging
from time import sleep
import json
from ..utils.window_manager import WindowManager
from ..utils.config_manager import AppConfig, ConfigManager
from ..utils.screen_manager import PositionSelector, ScreenManager

logger = logging.getLogger(__name__)

# Define a type for customtkinter widgets
CTkWidgetType = Union[ctk.CTkButton, ctk.CTkEntry, ctk.CTkFrame]

class AppPlacerGUI:
    """Main GUI application for the Auto-Placer."""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AUTO-PLACER")
        self.root.iconbitmap("src/assets/aap.ico")
        self.apps: List[List[CTkWidgetType]] = []
        self.current_row = 0
        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the main UI components."""
        # Title
        title_label = ctk.CTkLabel(self.root, text="AUTO-PLACER", font=("", 30))
        title_label.pack(padx=20, pady=10)

        # Main buttons frame
        buttons_frame = ctk.CTkFrame(self.root)
        buttons_frame.pack(pady=10, padx=20, fill="x")

        # Left side buttons (Add, Import, Export)
        left_buttons = ctk.CTkFrame(buttons_frame)
        left_buttons.pack(side=ctk.LEFT, padx=10, pady=5)

        self.add_button = ctk.CTkButton(left_buttons, text="ADD APP", command=self.add_app)
        self.add_button.pack(side=ctk.LEFT, padx=5)

        self.import_button = ctk.CTkButton(left_buttons, text="IMPORT", command=self.import_config)
        self.import_button.pack(side=ctk.LEFT, padx=5)

        self.export_button = ctk.CTkButton(left_buttons, text="EXPORT", command=self.export_config)
        self.export_button.pack(side=ctk.LEFT, padx=5)

        # Right side button (Open)
        self.open_button = ctk.CTkButton(buttons_frame, text="OPEN ALL", command=self.open_apps)
        self.open_button.pack(side=ctk.RIGHT, padx=10, pady=5)

        # Windows frame with scrollbar
        self.windows_frame = ctk.CTkScrollableFrame(self.root, width=600, height=400)
        self.windows_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Add initial app row
        self.add_app()

    def add_app(self) -> None:
        """Adds a new app configuration row."""
        if self.current_row >= 8:
            return

        # Create a frame for this app's widgets
        app_frame = ctk.CTkFrame(self.windows_frame)
        app_frame.pack(pady=5, padx=5, fill="x")

        # App selection button
        app_button = ctk.CTkButton(
            app_frame,
            text="Click to choose an app!",
            command=lambda: self.choose_shortcut(app_button),
            width=200
        )
        app_button.pack(side=ctk.LEFT, padx=5, pady=5)

        # Position selection button
        pos_button = ctk.CTkButton(
            app_frame,
            text="Select Position",
            command=lambda: self.select_position(pos_entry, size_entry),
            width=120
        )
        pos_button.pack(side=ctk.LEFT, padx=5, pady=5)

        # Position entry
        pos_entry = ctk.CTkEntry(
            app_frame,
            width=140,
            placeholder_text="Position (e.g., 500*300)"
        )
        pos_entry.pack(side=ctk.LEFT, padx=5, pady=5)

        # Size entry
        size_entry = ctk.CTkEntry(
            app_frame,
            width=90,
            placeholder_text="Size"
        )
        size_entry.pack(side=ctk.LEFT, padx=5, pady=5)

        # Remove button for this specific app
        remove_button = ctk.CTkButton(
            app_frame,
            text="×",
            width=30,
            command=lambda: self.remove_specific_app(app_frame, app_widgets)
        )
        remove_button.pack(side=ctk.LEFT, padx=5, pady=5)

        app_widgets = [app_button, pos_button, pos_entry, size_entry]
        self.apps.append(app_widgets)
        self.current_row += 1

    def remove_specific_app(self, app_frame: ctk.CTkFrame, app_widgets: List[CTkWidgetType]) -> None:
        """Removes a specific app configuration."""
        if self.current_row <= 1:
            return

        app_frame.destroy()
        self.apps.remove(app_widgets)
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
        self.import_button.configure(state=state)
        self.export_button.configure(state=state)
        self.open_button.configure(state=state)

    def open_apps(self) -> None:
        """Opens and positions all configured applications."""
        self.toggle_widgets("disabled")
        
        try:
            configs = self.get_app_configs()
            total_windows = len(configs)
            
            # Create progress window
            progress_window = ctk.CTkToplevel(self.root)
            progress_window.title("Processing Windows")
            progress_window.geometry("300x150")
            progress_window.attributes('-topmost', True)
            
            # Add progress label
            progress_label = ctk.CTkLabel(
                progress_window,
                text=f"Opening windows...\n0/{total_windows}",
                font=("", 14)
            )
            progress_label.pack(pady=20)
            
            # Add progress bar
            progress_bar = ctk.CTkProgressBar(progress_window)
            progress_bar.pack(pady=10, padx=20, fill="x")
            progress_bar.set(0)
            
            # Open all apps first
            for i, config in enumerate(configs, 1):
                WindowManager.open_app(config.shortcut_path)
                progress_label.configure(text=f"Opening windows...\n{i}/{total_windows}")
                progress_bar.set(i / total_windows)
                progress_window.update()
            
            # Wait for apps to open
            progress_label.configure(text="Waiting for windows to open...")
            progress_window.update()
            sleep(2)
            
            # Position all windows
            for i, config in enumerate(configs, 1):
                WindowManager.move_and_resize_window(
                    config.shortcut_path,
                    config.position,
                    config.size
                )
                progress_label.configure(text=f"Positioning windows...\n{i}/{total_windows}")
                progress_bar.set(i / total_windows)
                progress_window.update()
            
            # Show completion message
            progress_label.configure(text="All windows processed!")
            progress_window.update()
            sleep(1)
            progress_window.destroy()
            
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
            for app_widgets in self.apps[:]:
                app_frame = app_widgets[0].master
                self.remove_specific_app(app_frame, app_widgets)
            
            # Add new apps
            for config in configs:
                if self.current_row >= 8:
                    break
                    
                # Create a frame for this app's widgets
                app_frame = ctk.CTkFrame(self.windows_frame)
                app_frame.pack(pady=5, padx=5, fill="x")

                # App selection button
                app_button = ctk.CTkButton(
                    app_frame,
                    text=config.shortcut_path,
                    command=lambda: self.choose_shortcut(app_button),
                    width=200
                )
                app_button.pack(side=ctk.LEFT, padx=5, pady=5)

                # Position selection button
                pos_button = ctk.CTkButton(
                    app_frame,
                    text="Select Position",
                    command=lambda: self.select_position(pos_entry, size_entry),
                    width=120
                )
                pos_button.pack(side=ctk.LEFT, padx=5, pady=5)

                # Position entry
                pos_entry = ctk.CTkEntry(
                    app_frame,
                    width=140,
                    placeholder_text="Position (e.g., 500*300)"
                )
                pos_entry.pack(side=ctk.LEFT, padx=5, pady=5)
                pos_entry.insert(0, f"{config.position[0]}*{config.position[1]}")

                # Size entry
                size_entry = ctk.CTkEntry(
                    app_frame,
                    width=90,
                    placeholder_text="Size"
                )
                size_entry.pack(side=ctk.LEFT, padx=5, pady=5)
                size_entry.insert(0, f"{config.size[0]}*{config.size[1]}")

                # Remove button for this specific app
                remove_button = ctk.CTkButton(
                    app_frame,
                    text="×",
                    width=30,
                    command=lambda: self.remove_specific_app(app_frame, app_widgets)
                )
                remove_button.pack(side=ctk.LEFT, padx=5, pady=5)

                app_widgets = [app_button, pos_button, pos_entry, size_entry]
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