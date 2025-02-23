# view.py
import tkinter as tk

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.controller = None
        self.root.title("Kursverwaltung")
        self.root.geometry("1000x600")

        # Titel
        tk.Label(root, text="IU Dashboard", fg="darkblue", font=("Arial", 25, "bold"))\
            .grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Eingabefelder und Labels
        tk.Label(root, text="Kurscode:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.kurscode_entry = tk.Entry(root)
        self.kurscode_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Note:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.note_entry = tk.Entry(root)
        self.note_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Status (open/closed):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.status_entry = tk.Entry(root)
        self.status_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(root, text="Prüfungsleistungsdatum (TT.MM.JJJJ):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.pruefungsdatum_entry = tk.Entry(root)
        self.pruefungsdatum_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        self.kurs_button = tk.Button(root, text="Kurs aktualisieren", width=45, fg="white", bg="darkblue")
        self.kurs_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.stats_button = tk.Button(root, text="Statistik anzeigen", width=45)
        self.stats_button.grid(row=6, column=0, columnspan=2, pady=5)
              
        self.modul_info_button = tk.Button(root, text="Moduldaten anzeigen", width=45)
        self.modul_info_button.grid(row=7, column=0, columnspan=2, pady=5)
     
        self.diagramm_button = tk.Button(root, text="Diagramme aktualisieren", width=45, fg="white", bg="darkblue")
        self.diagramm_button.grid(row=8, column=0, columnspan=2, pady=5)


        # Info Label
        self.stats_label = tk.Label(root, text="Statistiken: Noch nicht berechnet", font=("Arial", 10))
        self.stats_label.grid(row=9, column=0, columnspan=2, pady=5)
        
        self.modul_info_label = tk.Label(root, text="Modul-Informationen werden hier angezeigt", font=("Arial", 10))
        self.modul_info_label.grid(row=10, column=0, columnspan=2, pady=5) 

       

        # Canvas für Diagramme
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.grid(row=1, rowspan=10, column=2, columnspan=2, padx=10, pady=5)

    def set_controller(self, controller):
        self.controller = controller
        self.kurs_button.config(command=self.controller.update_kurs)
        self.stats_button.config(command=self.controller.zeige_statistiken)
        self.diagramm_button.config(command=lambda: self.controller.aktualisiere_diagramme(self.canvas_frame))
        self.modul_info_button.config(command=self.controller.zeige_modul_info)

