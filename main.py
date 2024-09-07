from pywinauto import Application
import subprocess
from time import sleep
# Function to open an app
def open_app(shortcut_path):
    subprocess.Popen(shortcut_path, shell=True)
# Function to move and resize a window by executable name
def move_and_resize_window_by_exe(executable_name, position, size):
    try:
        app = Application(backend='win32').connect(path=executable_name)
        window = app.top_window()
        window.move_window(x=position[0], y=position[1], width=size[0], height=size[1])
    except Exception as e:
        print(f"Error: {e}")

# Example usage
open_app(r"C:\Program Files\XOutPut\XOutput.exe")
sleep(1)
move_and_resize_window_by_exe(r"C:\Program Files\XOutPut\XOutput.exe", (0, 0), (300, 300))