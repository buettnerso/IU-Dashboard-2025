# controller.py
from tkinter import messagebox
from datetime import datetime, timezone
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Controller:
    def __init__(self, modul_manager, dashboard):
        self.modul_manager = modul_manager
        self.dashboard = dashboard

    def update_kurs(self):
        kurscode = self.dashboard.kurscode_entry.get().strip()
        note = self.dashboard.note_entry.get().strip()
        status = self.dashboard.status_entry.get().strip()
        pruefungsdatum_str = self.dashboard.pruefungsdatum_entry.get().strip()

        try:
            neue_note = float(note.replace(",", "."))
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Note eingeben!")
            return

        if status.lower() not in ["open", "closed"]:
            messagebox.showerror("Fehler", "Status muss 'open' oder 'closed' sein!")
            return

        # Parse das Prüfungsdatum (Format: TT.MM.JJJJ)
        try:
            pruefungsdatum = datetime.strptime(pruefungsdatum_str, "%d.%m.%Y")
            pruefungsdatum = pruefungsdatum.replace(tzinfo=timezone.utc)
        except ValueError:
            messagebox.showerror("Fehler", "Bitte ein gültiges Prüfungsdatum im Format TT.MM.JJJJ eingeben!")
            return

        if self.modul_manager.update_kurs(kurscode, neue_note, status.lower(), pruefungsdatum):
            messagebox.showinfo("Erfolg", f"Kurs {kurscode} wurde aktualisiert!")
            self.zeige_statistiken()
            self.zeige_modul_info()
        else:
            messagebox.showwarning("Nicht gefunden", f"Kurs {kurscode} existiert nicht!")

    def hole_statistiken(self):
        durchschnitt = self.modul_manager.berechne_durchschnitt()
        abgeschlossen, offen = self.modul_manager.zaehle_module()
        credits = self.modul_manager.sum_credits()
        return {
            "durchschnitt": f"{durchschnitt:.2f}" if durchschnitt is not None else "Keine Noten",
            "abgeschlossen": abgeschlossen,
            "offen": offen,
            "credits": credits
        }

    def zeige_statistiken(self):
        stats = self.hole_statistiken()
        self.dashboard.stats_label.config(
            text=f"Aktueller Notendurchschnitt: {stats["durchschnitt"]}\n"
                 f"Anzahl abgeschlossener Module: {stats["abgeschlossen"]}\n"
                 f"Anzahl offener Module: {stats["offen"]}\n"
                 f"Bisher erworbene Credits: {stats["credits"]}"
       )

    def aktualisiere_diagramme(self, canvas_frame):
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        # Diagramm 1: Balkendiagramm für Module (abgeschlossen vs. offen)
        fig, ax = plt.subplots(figsize=(6, 2))
        abgeschlossen, offen = self.modul_manager.zaehle_module()
        ax.bar(["Abgeschlossen", "Offen"], [abgeschlossen, offen], color=["darkblue", "orange"])
        ax.set_title("Modulübersicht")

        self.canvas1 = FigureCanvasTkAgg(fig, master=canvas_frame)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=0, column=0)

        # Diagramm 2: Studienzeit-Diagramm über 42 Monate
        total_months = 42
        study_start = datetime(2024, 3, 1, tzinfo=timezone.utc)
        jetzt = datetime.utcnow().replace(tzinfo=timezone.utc)

        vergangene_monate = int((jetzt - study_start).days // 30)  # Explizit als int casten
        vergangene_monate = max(0, min(vergangene_monate, total_months))  # Begrenzung zwischen 0 und 42
        verbleibende_monate = total_months - vergangene_monate
        
        fig2, ax2 = plt.subplots(figsize=(6, 2))
        ax2.barh(["Studienzeit"], [vergangene_monate], color="darkblue", label="Vergangene Zeit", height=0.2)
        ax2.barh(["Studienzeit"], [verbleibende_monate], left=vergangene_monate, color="orange", label="Verbleibende Zeit", height=0.2)
        
        ax2.set_title("Studienzeit (42 Monate)")
        fig2.subplots_adjust(left=0.2)
        ax2.set_xlabel("Monate")
        ax2.legend()
        ax2.grid(axis="x")
        ax2.set_xticks(range(0, total_months + 1, 6))

        self.canvas2 = FigureCanvasTkAgg(fig2, master=canvas_frame)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=1, column=0)

    def zeige_modul_info(self):
        kurscode = self.dashboard.kurscode_entry.get().strip()
        if kurscode in self.modul_manager.kurse:
            modul = self.modul_manager.kurse[kurscode]
            pruefung = modul.pruefungsleistung
            note = pruefung.kursnote if pruefung.kursnote is not None else "keine Note"
            datum_str = pruefung.datum.strftime("%d.%m.%Y")
            info = (
                f"Kurscode: {modul.kurscode}\n"
                f"Modulbezeichnung: {modul.modulbezeichnung}\n"
                f"Credits: {modul.credits}\n"
                f"Status: {modul.status}\n"
                f"Kursnote: {note}\n"
                f"Prüfungsdatum: {datum_str}"
            )
            self.dashboard.modul_info_label.config(text=info)
        else:
            self.dashboard.modul_info_label.config(text=f"Kein Modul mit Kurscode '{kurscode}' gefunden.")

