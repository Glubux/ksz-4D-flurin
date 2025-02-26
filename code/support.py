from csv import reader
from os import walk
import pygame

pygame.init()
pygame.display.set_mode((1, 1))

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
	return surface_list

def import_image(path):
	if type(path) == list:
		if len(path) == 1:
			return pygame.image.load(path[0]).convert_alpha()
		else:
			return [pygame.image.load(p).convert_alpha() for p in path]
	else:
		return pygame.image.load(path).convert_alpha()
	
def import_tileset(anymation_type, path, amount_frames, size=(32,32), scale_faktor=4.5, meta=None):
	img = import_image(path)
	if anymation_type == "character":
		direction = ["down", "up", "right", "left"]
		animation = {}
		flip = False
		
		for y in range(amount_frames[1]):
			frames = []

			for x in range(amount_frames[0]):
				if direction[y] == "left":
					flip = True
					y -= 1
	
				frame_surface = img.subsurface((x*size[0], y*size[1], size[0], size[1]))
				frame_surface = pygame.transform.scale(frame_surface, (size[0]*scale_faktor, size[1]*scale_faktor))
				
				if flip:
					frame_surface = pygame.transform.flip(frame_surface, True, False)
					y += 1
					
				frames.append(frame_surface)
			animation[direction[y]] = frames
		return animation
	
	if anymation_type == "tileset":
		sub_surfaces = []

		for y in range(amount_frames[1]):
			for x in range(amount_frames[0]):
				sub_surface = img.subsurface((x*size[0], y*size[1], size[0], size[1]))
				sub_surface = pygame.transform.scale(sub_surface, (size[0]*scale_faktor, size[1]*scale_faktor))
				sub_surfaces.append(sub_surface)

		return sub_surfaces
	
		

cooldowns = {}
def cooldown(name: str, duration=1):
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