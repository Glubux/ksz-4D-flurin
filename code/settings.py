import pygame

# game setup
WIDTH    = 1550
HEIGTH   = 880
FPS      = 60
TILESIZE = 64



npcs = {
    "schrödinger": {
        "img": ["../textures/skins/schrödinger/schrödinger.png"],
        "talk": {
            "idl": [
                {"text": "Schönes Wetter heute, nicht wahr?", "time": 2, "root": 0},
                {"text": "Wo ist meine Katze? Lebt sie noch?", "time": 2, "root": 0},
                {"text": "Schröööödinger, Schröööödiiinger!", "time": 2, "root": 0},
                {"text": "Hallo Mein Name ist Schrödinger. Ich bin ein Mensch. Oder Nicht? Bitte hilf mir, ich bin in gefahrt.", "time": 2, "root": 0},
            ],
            "begrüssung": [
                {"text": "Hallo mein Name ist Schrödinger.", "time": 1, "root": 0},
                {"text": "Es freut mich dich kennen zu lernen.", "time": 1, "root": 0},
                {"text": "Früher antwortete man noch..." , "time": 1, "root": 0},
                {"text": "Früher antwortete man noch... Tschau" , "time": 1, "root": 0},
            ]
        }
    }
}