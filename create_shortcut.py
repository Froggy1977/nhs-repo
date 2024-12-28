# create_shortcut.py
import os
import sys
import winshell
from win32com.client import Dispatch

def create_shortcut():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the .pyw file
    target = os.path.join(current_dir, 'launch_app.pyw')
    
    # Path to the icon
    icon = os.path.join(current_dir, 'query.png')
    
    # Create shortcut in the current directory
    shortcut_path = os.path.join(current_dir, 'NHS Digital Query.lnk')
    
    # Create the shortcut
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = sys.executable
    shortcut.Arguments = f'"{target}"'
    shortcut.IconLocation = icon
    shortcut.WorkingDirectory = current_dir
    shortcut.save()
    
    print(f"Shortcut created at: {shortcut_path}")

if __name__ == "__main__":
    create_shortcut()