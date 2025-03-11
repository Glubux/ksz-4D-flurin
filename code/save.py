import json
import pickle


spielstand = {
    "spieler": {
        "position": [5, 10],
        "leben": 3,
        "inventar": ["Axt", "Samen"]
    },
    "welt": {
        "zeit": 120,
        "tiles": {
            "5_10": "Farmland",
            "6_10": "Pflanze_Stufe_2"
        }
    }
}

""" def speichere_spielstand(datei, daten):
    with open(datei, "w") as f:
        json.dump(daten, f, indent=4)  # `indent=4` für bessere Lesbarkeit

speichere_spielstand("spielstand.json", spielstand)


def lade_spielstand(datei):
    try:
        with open(datei, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Kein Spielstand gefunden, starte neues Spiel.")
        return {}  # Falls keine Datei existiert, wird ein leeres Dict zurückgegeben
    

spielstand = lade_spielstand("spielstand.json") """


def speichere_spielstand_binär(datei, daten):
    with open(datei, "wb") as f:
        pickle.dump(daten, f)

def lade_spielstand_binär(datei):
    try:
        with open(datei, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("Kein Spielstand gefunden.")
        return {}
    
# speichere_spielstand_binär("./text.txt", spielstand)
new = None
while True:
    eingabe = input("> ")

    try:
        if eingabe == "save":
            speichere_spielstand_binär("./text", spielstand)

        elif eingabe == "load":
            new = lade_spielstand_binär("./text")
        
        elif eingabe == "print":
            print(new)

        elif eingabe == "data":
            print(spielstand)

    except:
        print(f"*** Ungültige Eingabe: {eingabe} ***")
