import subprocess
import pyautogui
import time

# Define the shortcuts and the coordinates
apps = [
    {"shortcut": "C:\\Users\\Vic\\Desktop\\PROGRAMS\\FrameView.lnk", "position": (100, 100)},
    {"shortcut": "C:\\Users\\Vic\\Desktop\\PROGRAMS\\XOutput.lnk", "position": (300, 100)},
]

# Function to open an app
def open_app(shortcut_path):
    subprocess.Popen(shortcut_path, shell=True)

# Function to position an app window
def move_window(position):
    time.sleep(2)  # Wait for the app to open
    pyautogui.hotkey('alt', 'space')  # Open window control menu
    pyautogui.press('m')  # Select move
    pyautogui.moveTo(position)  # Move the window to the desired position
    pyautogui.click()  # Confirm the move

# Open and position each app
for app in apps:
    open_app(app["shortcut"])
    move_window(app["position"])
