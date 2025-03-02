import pygame
from support import *

WIDTH = 1950
HEIGHT = 1200
FPS      = 60
TILESIZE = 64

register_item(
    name="wood",
    description="simple wood",
    inv_img="../img/wood.png"
)
register_item(
    name="stone",
    description="simple stone",
    inv_img="../img/stone.png"
)
register_item(
    name="sword",
    description="simple sword",
    inv_img="../img/sword.png"
)
register_item(
    name="shield",
    description="simple shield",
    inv_img="../img/shiled.png"
)

"""
Dev-Test Prints
===============

print("----------")
print(get_item_list())
print("----------")
print(get_item("stone"))
print("----------")
print(items)
"""

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