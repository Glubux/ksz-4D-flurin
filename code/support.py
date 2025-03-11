from csv import reader
from os import walk
import re
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

def numeric_sort_key(filename):
    # für alphabetische und numerische sortierung
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', filename)]

def import_folder(path):
    surface_list = []

    for _, _, img_files in walk(path):
        img_files.sort(key=numeric_sort_key)

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
	
	if anymation_type == "plants":
		# meta -> position des ersten Tiles
		surfaces = []

		for x in range(amount_frames):
			surface = img.subsurface((meta[0] + x)*size[0], ((meta[1]*2 + 1)) * size[1], size[0], size[1])
			surface = pygame.transform.scale(surface, (size[0]*scale_faktor, size[1]*scale_faktor))
			surfaces.append(surface)

		return surfaces
	
		

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



class FadeEffect:
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.target_alpha = 0
		self.current_alpha = 0
		self.fade_speed = 0
		self.surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
		self.surface.fill((0, 0, 0))
		self.surface.set_alpha(self.current_alpha)
		self.fade_start_time = 0
		self.fade_duration = 0
		self.is_fading = False
		self.start_alpha = 0

	def set_fade(self, target_percent, time_seconds, instant=False):
		self.target_alpha = int(target_percent * 255 / 100)

		if instant:
			self.current_alpha = self.target_alpha
			self.surface.set_alpha(self.current_alpha)
			self.is_fading = False
		else:
			self.start_alpha = self.current_alpha
			self.fade_duration = time_seconds
			self.fade_start_time = pygame.time.get_ticks()
			self.is_fading = True

	def update(self):
		if self.is_fading:
			elapsed_time = (pygame.time.get_ticks() - self.fade_start_time) / 1000.0

			if elapsed_time >= self.fade_duration:
				self.current_alpha = self.target_alpha
				self.is_fading = False
			else:
				progress = elapsed_time / self.fade_duration
				self.current_alpha = int(self.start_alpha + (self.target_alpha - self.start_alpha) * progress)

			self.surface.set_alpha(self.current_alpha)

		self.screen.blit(self.surface, (0, 0))
		return not self.is_fading


def get_minimap_position(player_x, player_y, map_width=5000, map_height=5000, mini_width=500, mini_height=500):
    mini_x = round((player_x / map_width) * mini_width)
    mini_y = round((player_y / map_height) * mini_height)
    return mini_x, mini_y