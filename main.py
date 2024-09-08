import customtkinter as ctk
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
def add_app(window): # Function for adding apps 
    global i,j,apps
    if i < 8 :
        app = [
            ctk.CTkButton(window,text="Click to choose an app ! ",command=lambda:choose_shortcut(app[0])),
            ctk.CTkEntry(window,width=140,placeholder_text="Place (exp: 500*300 )"),
            ctk.CTkEntry(window,width=90,placeholder_text="Size"),
        ]
        for a in app:
            a.grid(column=j , row=i,padx = 10,pady = 10)
            j+=1
        j = 0
        i+=1
        apps.append(app)

def delete_app(): # Function for removing apps
    global i,apps
    if i > 1 :
        for a in apps[-1]:
            a.grid_forget()
        apps.pop()
        i = i-1
i = 0 ; j = 0

def choose_shortcut(btn): # for choosing shortcuts
    f = ctk.filedialog.askopenfilename(
        title=" Choose a shortcut file ",
        filetypes=(("Executables", "*.exe"),("Shortcuts", "*.lnk"))
        )
    btn.configure(text = f)

def disable_all(): # disable all widgets
    for i in apps:
        for j in i:
            j.configure(state = "disabled")
    button_add.configure(state = "disabled")
    button_rem.configure(state = "disabled")
    button_opn.configure(state = "disabled")
    
def enable_all(): # enable all widgets
    for i in apps:
        for j in i:
            j.configure(state = "normal")
    button_add.configure(state = "normal")
    button_rem.configure(state = "normal")
    button_opn.configure(state = "normal")
def get_from_str(ch):
    ch = ch.split("*")
    return (int(ch[0]),int(ch[1]))
def open_apps():
    disable_all()
    for i in apps :
        open_app(i[0].cget("text"))
    sleep(2)
    for i in apps :
        move_and_resize_window_by_exe(i[0].cget("text"),get_from_str(i[1].get()),get_from_str(i[2].get()))
    enable_all()
apps = []
root = ctk.CTk()
root.title("AUTO-PLACER")
lab_title = ctk.CTkLabel(root,text="AUTO - PLACER",font=("",30)) # Title Label
lab_title.pack(padx = 20 , pady = 10)
frame_buttons = ctk.CTkFrame(root) # Frame to contain main buttons
frame_buttons.pack(pady = 10,padx = 20)
button_add = ctk.CTkButton(frame_buttons,text="ADD",command=lambda : add_app(frame_windows))
button_add.pack(side = ctk.LEFT,padx = 10,pady = 5)
button_rem = ctk.CTkButton(frame_buttons,text="REMOVE",command=delete_app)
button_rem.pack(side = ctk.LEFT,padx = 10,pady = 10)
button_opn = ctk.CTkButton(frame_buttons,text="OPEN",command=open_apps)
button_opn.pack(side = ctk.LEFT,padx = 10,pady = 5)
frame_windows = ctk.CTkFrame(root) # Frame to contain windows
frame_windows.pack(pady = 10,padx = 20)
add_app(frame_windows)
root.mainloop()