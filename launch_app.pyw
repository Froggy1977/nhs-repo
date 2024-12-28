# launch_app.pyw
import tkinter as tk
from nhs_gui import NHSDigitalGUI

def main():
    root = tk.Tk()
    app = NHSDigitalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()    