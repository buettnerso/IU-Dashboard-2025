# model.py
from datetime import datetime, timezone
from speicher_manager import SpeicherManager

class Pruefungsleistung:
    def __init__(self, kursnote=None, bestandenstatus=False, datum=None):
        self.kursnote = kursnote
        self.bestandenstatus = bestandenstatus
        # Falls kein Datum übergeben wird, wird das aktuelle Datum verwendet
        self.datum = datum if datum else datetime.now(timezone.utc)

class Modul:
    def __init__(self, speicher_manager, kurscode, modulbezeichnung, semesternummer, status, credits=5, pruefungsleistung=None):
        self.speicher_manager = speicher_manager
        self.kurscode = kurscode
        self.modulbezeichnung = modulbezeichnung
        self.credits = credits  # fest auf 5
        self.semesternummer = semesternummer
        self.status = status.lower()
        if pruefungsleistung is None:
            self.pruefungsleistung = Pruefungsleistung()
        else:
            self.pruefungsleistung = pruefungsleistung

    def update(self, neue_note, neuer_status, pruefungsdatum=None):
        self.pruefungsleistung.kursnote = neue_note
        self.status = neuer_status.lower()
        self.pruefungsleistung.bestandenstatus = (self.status == "closed")
        if pruefungsdatum:
            self.pruefungsleistung.datum = pruefungsdatum
        else:
            self.pruefungsleistung.datum = datetime.now(timezone.utc)

class ModulManager:
    def __init__(self, speicher_manager):
        self.speicher_manager = speicher_manager
        self.kurse = {}  # kurscode -> Modul Objekt
        self.lade_kurse()

    def lade_kurse(self):
        daten = self.speicher_manager.lade_csv()
        if not daten:
            return
        header = daten[0]
        daten = daten[1:]
        # CSV-Spalten: Semester, Modulbezeichnung, Kurscode, Note, Status, Credits, Prüfungsdatum
        for row in daten:
            if len(row) >= 7:
                semesternummer = row[0].strip()
                modulbezeichnung = row[1].strip()
                kurscode = row[2].strip()
                try:
                    note = float(row[3].replace(",", ".")) if row[3].strip() else None
                except ValueError:
                    note = None
                status = row[4].strip().lower()
                credits = 5
                try:
                    datum = datetime.strptime(row[6].strip(), "%d.%m.%Y") if row[6].strip() else datetime.now(timezone.utc)
                except ValueError:
                    datum = datetime.now(timezone.utc)
                pruefungsleistung = Pruefungsleistung(
                    kursnote=note,
                    bestandenstatus=(status == "closed"),
                    datum=datum
                )
                modul = Modul(self.speicher_manager, kurscode, modulbezeichnung, semesternummer, status, credits, pruefungsleistung)
                self.kurse[kurscode] = modul

    def update_kurs(self, kurscode, neue_note, neuer_status, pruefungsdatum):
        if kurscode in self.kurse:
            modul = self.kurse[kurscode]
            modul.update(neue_note, neuer_status, pruefungsdatum)
            self.speichere_kurse()
            return True
        return False

    def speichere_kurse(self):
        daten = []
        header = ["Semester", "Modulbezeichnung", "Kurscode", "Note", "Status", "Credits", "Prüfungsdatum"]
        daten.append(header)
        for modul in self.kurse.values():
            note_str = str(modul.pruefungsleistung.kursnote) if modul.pruefungsleistung.kursnote is not None else ""
            datum_str = modul.pruefungsleistung.datum.strftime("%d.%m.%Y")
            row = [
                modul.semesternummer,
                modul.modulbezeichnung,
                modul.kurscode,
                note_str,
                modul.status,
                str(modul.credits),
                datum_str
            ]
            daten.append(row)
        self.speicher_manager.speichere_csv(daten)

    def berechne_durchschnitt(self):
        noten = [modul.pruefungsleistung.kursnote for modul in self.kurse.values()
                 if modul.pruefungsleistung.kursnote is not None and modul.pruefungsleistung.kursnote > 0]
        return sum(noten) / len(noten) if noten else None

    def zaehle_module(self):
        abgeschlossen = sum(1 for modul in self.kurse.values() if modul.status == "closed")
        offen = sum(1 for modul in self.kurse.values() if modul.status == "open")
        return abgeschlossen, offen

    def sum_credits(self):
        return sum(modul.credits for modul in self.kurse.values() if modul.status == "closed")
