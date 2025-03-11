import pygame
from support import *

WIDTH = 1950
HEIGHT = 1200
FPS	  = 60
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
				{"text": "Guten Tag fremder Wanderer.", "time": 2, "root": 0},
				{"text": "Wohin des Weges Fremder? Hast du die Insel schon besucht?", "time": 2, "root": 0},
				{"text": "Das wandern ist des Müllers Lust, das wandern ist das Müllers Lust- Lalala la la...", "time": 2, "root": 0},
				{"text": "Mein Name ist Josh. Jeden Tag schaue ich bei meinen Feldern vorbei und giesse sie. Hast du gewusst, das im Sommer alle Pflanzen welken?", "time": 2, "root": 0},
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
	
texture_path = {
	"spring": "../textures/farm crops/spring crops.png",
	"summer": "../textures/farm crops/summer crops.png",
	"autom": "../textures/farm crops/autom crops.png"
}
plant_list = {
	"spring": [
		{
			"name": "strawberry",
			"info": "Erdbeere - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 6, (16,16), 4.5, (0,0)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,0)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,0)),
			},
			"grow_stats": 6
		},{
			"name": "spring onion",
			"info": "Frühlingszwiebel - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 6, (16,16), 4.5, (0,1)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,1)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,1)),
			},
			"grow_stats": 6
		},{
			"name": "potato",
			"info": "Kartoffel - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 6, (16,16), 4.5, (0,2)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,2)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,2)),
			},
			"grow_stats": 6
		},{
			"name": "onion",
			"info": "Zwiebel - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 6, (16,16), 4.5, (0,3)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,3)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,3)),
			},
			"grow_stats": 6
		},{
			"name": "carrot",
			"info": "Karotte - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 6, (16,16), 4.5, (0,4)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,4)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,4)),
			},
			"grow_stats": 6
		},{
			"name": "blueberry",
			"info": "Heidelbeere - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 6, (16,16), 4.5, (0,5)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,5)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,5)),
			},
			"grow_stats": 6
		},{
			"name": "parsnip",
			"info": "Pastinake - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 5, (16,16), 4.5, (0,6)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,6)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,6)),
			},
			"grow_stats": 5
		},{
			"name": "salad",
			"info": "Salat - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 7, (16,16), 4.5, (0,7)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,7)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,7)),
			},
			"grow_stats": 7
		},{
			"name": "cauliflower",
			"info": "Blumenkohl - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 6, (16,16), 4.5, (0,8)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,8)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,8)),
			},
			"grow_stats": 6
		},{
			"name": "barley",
			"info": "Gerste - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 6, (16,16), 4.5, (0,9)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,9)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,9)),
			},
			"grow_stats": 6
		},{
			"name": "broccoli",
			"info": "Brokkoli - Frühling",
			"texture": {
				"planted": import_tileset("plants", texture_path["spring"], 5, (16,16), 4.5, (0,10)),
				"inv": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (7,10)),
				"seeds": import_tileset("plants", texture_path["spring"], 1, (16,16), 4.5, (8,10)),
			},
			"grow_stats": 5
		}
	],
	"summer": [
		{
			"name": "tomato",
			"info": "Tomate - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 7, (16,16), 4.5, (0,0)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,0)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,0)),
			},
			"grow_stats": 7
		},{
			"name": "sunflower",
			"info": "Sonnenblume - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 6, (16,16), 4.5, (0,1)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,1)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,1)),
			},
			"grow_stats": 6
		},{
			"name": "chili",
			"info": "Chili - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 7, (16,16), 4.5, (0,2)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,2)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,2)),
			},
			"grow_stats": 7
		},{
			"name": "corn",
			"info": "Mais - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 8, (16,16), 4.5, (0,3)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,3)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,3)),
			},
			"grow_stats": 8
		},{
			"name": "peppers",
			"info": "Paprika - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 6, (16,16), 4.5, (0,4)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (8,4)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,4)),
			},
			"grow_stats": 6
		},{
			"name": "tomate2",
			"info": "Tomate - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 6, (16,16), 4.5, (0,5)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,5)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,5)),
			},
			"grow_stats": 6
		},{
			"name": "melon",
			"info": "Melone - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 8, (16,16), 4.5, (0,6)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,6)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,6)),
			},
			"grow_stats": 8
		},{
			"name": "cucumber",
			"info": "Gurke - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 6, (16,16), 4.5, (0,7)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,7)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,7)),
			},
			"grow_stats": 6
		},{
			"name": "aubergine",
			"info": "Aubergine - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 6, (16,16), 4.5, (0,8)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,8)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,8)),
			},
			"grow_stats": 6
		},{
			"name": "pineapple",
			"info": "Ananas - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 6, (16,16), 4.5, (0,9)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,9)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,9)),
			},
			"grow_stats": 6
		},{
			"name": "bean",
			"info": "Bohne - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 7, (16,16), 4.5, (0,10)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,10)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,10)),
			},
			"grow_stats": 7
		},{
			"name": "blueberry",
			"info": "Heidelbeere - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 7, (16,16), 4.5, (0,11)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,11)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (10,11)),
			},
			"grow_stats": 7
		},{
			"name": "wheat",
			"info": "Weizen - Sommer",
			"texture": {
				"planted": import_tileset("plants", texture_path["summer"], 6, (16,16), 4.5, (0,12)),
				"inv": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (8,12)),
				"seeds": import_tileset("plants", texture_path["summer"], 1, (16,16), 4.5, (9,12)),
			},
			"grow_stats": 6
		}
	],
	"autom": [
		{
			"name": "root beet",
			"info": "Rote Beete - Herbst",
			"texture": {
				"planted": import_tileset("plants", texture_path["autom"], 6, (16,16), 4.5, (0,0)),
				"inv": import_tileset("plants", texture_path["autom"], 1, (16,16), 4.5, (7,0)),
				"seeds": import_tileset("plants", texture_path["autom"], 1, (16,16), 4.5, (8,0)),
			},
			"grow_stats": 6
		},{
			"name": "pumpkin",
			"info": "Kürbis - Herbst",
			"texture": {
				"planted": import_tileset("plants", texture_path["autom"], 5, (16,16), 4.5, (1,1)),
				"inv": import_tileset("plants", texture_path["autom"], 1, (16,16), 4.5, (7,1)),
				"seeds": import_tileset("plants", texture_path["autom"], 1, (16,16), 4.5, (8,1)),
			},
			"grow_stats": 5
		},{
			"name": "grapes",
			"info": "Trauben - Herbst",
			"texture": {
				"planted": import_tileset("plants", texture_path["autom"], 5, (16,16), 4.5, (1,2)),
				"inv": import_tileset("plants", texture_path["autom"], 1, (16,16), 4.5, (7,2)),
				"seeds": import_tileset("plants", texture_path["autom"], 1, (16,16), 4.5, (8,2)),
			},
		}
	],
    "rotten": import_image("../textures/farm crops/rotten_plant.png")
}