from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)
	print(surface_list)
	return surface_list

def import_image(path):
    if type(path) == list:
        return [pygame.image.load(p).convert_alpha() for p in path]
    else:
        return pygame.image.load(path).convert_alpha()

cooldowns = {}
def cooldown(name, duration=1):
    current_time = pygame.time.get_ticks() / 1000

    if name in cooldowns:
        if current_time - cooldowns[name] >= duration:
            cooldowns[name] = current_time
            return True
        return False
    else:
        cooldowns[name] = current_time
        return True

items = {}

def register_item(name="Unknow Item", description="Unknow Item", inv_img="../textures/item/Unknown_Item.png", stack_max=99, group=None, range=3, wear=-1, meta=[]):
    if name in items:
        raise ValueError(f"Item '{name}' ist bereits registriert!")
    
    items[name] = {
        "description": description,
        "inv_img": inv_img,
        "stack_max": stack_max,
        "group": group,
        "range": range,
        "wear": wear,
        "meta": meta
    }

def get_item(name):
    return items.get(name, None)

def get_item_list():
    return list(items.keys())