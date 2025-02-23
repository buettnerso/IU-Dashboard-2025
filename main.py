# main.py
import tkinter as tk
from speicher_manager import SpeicherManager
from model import ModulManager
from view import Dashboard
from controller import Controller

def main():
    speicher_manager = SpeicherManager("modulplan.csv")
    modul_manager = ModulManager(speicher_manager)
    root = tk.Tk()
    dashboard = Dashboard(root)
    controller = Controller(modul_manager, dashboard)
    dashboard.set_controller(controller)
    root.mainloop()

if __name__ == "__main__":
    main()
