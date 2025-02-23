# speicher_manager.py
import csv
from tkinter import messagebox

class SpeicherManager:
    def __init__(self, csv_datei):
        self.csv_datei = csv_datei
    
    def lade_csv(self):
        daten = []
        try:
            with open(self.csv_datei, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=";")
                header = next(reader, None)
                if header:
                    daten.append(header)
                daten.extend([row for row in reader])
        except FileNotFoundError:
            messagebox.showerror("Fehler", "CSV-Datei nicht gefunden!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Datei: {e}")
        return daten
    
    def speichere_csv(self, daten):
        try:
            with open(self.csv_datei, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerows(daten)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Datei: {e}")
