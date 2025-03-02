import pygame, sys
from settings import *
from tile import Tile
from player import Player
from debug import *
from support import *
from inventar import *
from npc import *

class Level:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.season = "autom"
		self.season_list = ["winter", "spring", "summer", "autom"]

		self.visible_sprites = YSortCameraGroup(self.season)
		self.obstacle_sprites = pygame.sprite.Group()
		self.water_group = pygame.sprite.Group()
		self.npcs = pygame.sprite.Group()

		self.hotbar = Hotbar()
		self.menu = Menu()
		self.inv = Inventar()
		self.dialog = Dialog()
		self.time = Time()
		self.fade = FadeEffect()
		
		self.inv_status = False
		self.menu_status = False
		self.dialog_status = False

		self.menu_data = None
		self.inv_data = None

		self.inv_update_ans = None
		self.dialog_ans = None

		self.map()

	def map(self):
		season_setting = {
			"winter": ["winter_deco", "boundary"],
			"spring": ["spring_deco", "water_spring_summer", "boundary"],
			"summer": ["summer_deco", "water_spring_summer", "boundary"],
			"autom": ["autom_deco", "water_autom", "boundary"],
		}
		csv_data = {
			"boundary": [import_csv_layout("../textures/map/map_obstacle_main.csv"), "None"],
			"water_spring_summer": [import_csv_layout("../textures/map/map_Animation_water_spring_summer.csv"), "summer"],
			"water_autom": [import_csv_layout("../textures/map/map_Animation_water_autom.csv"), "autom"],
			
			"spring_deco": [import_csv_layout("../textures/map/map_Spring_decoration.csv"), "spring"],
			"summer_deco": [import_csv_layout("../textures/map/map_Summer_decoration.csv"), "summer"],
			"autom_deco": [import_csv_layout("../textures/map/map_Autom_decoration.csv"), "autom"],
			"winter_deco": [import_csv_layout("../textures/map/map_Winter_decoration.csv"), "winter"],

		}
		textures = {
			"winter": import_tileset("tileset", "../textures/farm/Tileset/Tileset Winter.png", [15,14], (16,16), 4),
			"summer": import_tileset("tileset", "../textures/farm/Tileset/Tileset Grass Summer.png", [25,22], (16,16), 4),
			"spring": import_tileset("tileset", "../textures/farm/Tileset/Tileset Grass Spring.png", [25,27], (16,16), 4),
			"autom": import_tileset("tileset", "../textures/farm/Tileset/Tileset Grass Fall.png", [25,22], (16,16), 4),
			"boundary": import_tileset("tileset", "../textures/tiled/color_tiledset.png", [4,4], (16,16), 4)
		}
		
		for style in season_setting[self.season]: # needed csv_data
			layout = csv_data[style][0] # -> [surfacelist, textur_verweis]
			
			for row_index, row in enumerate(layout):
				for coll_index, col in enumerate(row):
					x = coll_index * TILESIZE
					y = row_index * TILESIZE
					col = int(col)

					if col != -1:
						if style == "boundary":
							if col == 0: # wasser
								Tile((x,y),[self.visible_sprites, self.water_group], [style, "background", col] ,textures["boundary"][col])
							elif col == 12: # border
								Tile((x,y),[self.obstacle_sprites, self.visible_sprites], [style, "background", col] ,textures["boundary"][col])
						
						elif style == "water_spring_summer":
							Tile((x,y),[self.visible_sprites], [style, "background"] ,textures["spring"][col])
						elif style == "water_autom":
							Tile((x,y),[self.visible_sprites], [style, "background"] ,textures["autom"][col])
							
						else:
							Tile((x,y),[self.visible_sprites], [style, "backgorund"], textures[self.season][col])

						if style == "npc":
							npc = Npc((x, y), [self.visible_sprites, self.npcs], self.obstacle_sprites, "schrödinger", self.dialog)
							self.npcs.add(npc)
							pass

		self.player = Player((1000,500),[self.visible_sprites],self.obstacle_sprites,"Alex")


	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_e]:
			if cooldown("open_inv", 0.5):
				if not self.inv_status:
					if self.menu_status:
						pass
					else:
						self.inv_status = True
						self.inv.open_inv()
						self.fade.set_fade(50, 0.5)

				else:
					self.inv.close_inv()
					self.fade.set_fade(0, 0.7)
					

		if keys[pygame.K_ESCAPE]:
			if cooldown("open_menu", 0.5):
				if not self.menu_status:
					if self.inv_status:
						self.inv.close_inv()
						self.fade.set_fade(0, 0.7)

					else:
						self.menu_status = True
						self.menu.open_menu()
						self.fade.set_fade(50, 0.5)
				
				else:
					self.menu_status = False
					self.menu.close_menu()
					self.fade.set_fade(0, 1, True)

		
	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.input()
		self.time.update()
		self.fade.update()

		self.dialog_ans = self.dialog.update()

		if self.menu_status:
			self.menu_data = self.menu.update()

			if self.menu_data == "1":
				self.menu.close_menu()
				self.menu_status = False
			if self.menu_data == "2":
				print("Einstellungen")
			if self.menu_data == "3":
				print("Speichern & Laden")
			if self.menu_data == "4":
				pygame.quit()
				sys.exit()
			
		elif self.inv_status:
			self.inv_update_ans = self.inv.update()
			print(self.inv_update_ans)
			if self.inv_update_ans["status"] == "closed":
				self.inv_status = False
				self.inv.status = ""
		
		else:
			self.hotbar.update()

			self.visible_sprites.update()

			for npc in self.npcs:
				npc.update_player_pos(self.player.rect.center)

		if self.colide():
			#print("water")
			pass

	def colide(self):
		return pygame.sprite.spritecollideany(self.player, self.water_group, pygame.sprite.collide_rect)

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self, season):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		self.season = season

		self.floor_surf = import_image(f'../textures/tiled/map_{self.season}.png')
		self.floor_surf = pygame.transform.scale(self.floor_surf, (self.floor_surf.get_width()*4, self.floor_surf.get_height()*4))
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))


	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - self.half_width + player.acceleration.x
		self.offset.y = player.rect.centery - self.half_height + player.acceleration.y

		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)

		# auftrennen von Y-sored und background
		background_sprites = [sprite for sprite in self.sprites() if getattr(sprite, "type", None) == "background"]
		normal_sprites = [sprite for sprite in self.sprites() if getattr(sprite, "type", None) != "background"]

		# ohne Y-Wert sortieren 
		for sprite in background_sprites:
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)

		# mit Y-Wert sortieren
		for sprite in sorted(normal_sprites, key=lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)



class DayNightCycle:
	"""Die DayNightCycle Funktion ist mit starken Unterstützung von ChatGPT geschrieben worden"""

	def __init__(self):
		self.screen = pygame.display.get_surface()

		self.day_color = pygame.Color(0, 0, 0, 0)
		self.night_color = pygame.Color(0, 0, 10, 180)

	def get_time_factor(self, hour, minute):
		if 21 <= hour < 22:
			return (hour - 21) + (minute / 60)
		elif 6 <= hour < 7:
			return 1 - ((hour - 6) + (minute / 60))
		elif 22 <= hour or hour < 6:
			return 1.0
		else:
			return 0.0

	def update(self, hour, minute):
		factor = self.get_time_factor(hour, minute)
		self.current_color = self.smooth_transition(self.day_color, self.night_color, factor)

	def smooth_transition(self, start_color, end_color, factor):
		r = int(start_color.r + (end_color.r - start_color.r) * factor)
		g = int(start_color.g + (end_color.g - start_color.g) * factor)
		b = int(start_color.b + (end_color.b - start_color.b) * factor)
		a = int(start_color.a + (end_color.a - start_color.a) * factor)
		return pygame.Color(r, g, b, a)

	def draw(self):
		overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
		overlay.fill(self.current_color)
		self.screen.blit(overlay, (0, 0))



class Time():
	def __init__(self):
		self.season_list = ["spring", "summer", "autumn", "winter"]
		self.time = {
			"year": 1,
			"season": "spring",
			"day": 1,
			"hour": 12,
			"minute": 0
		}
		self.gameminute_in_seconds = 0.8
		self.time_sprint = 1

		self.day_night_cycle = DayNightCycle()

	def calculate_time(self):
		if cooldown("gameminute", self.gameminute_in_seconds * self.time_sprint):
			self.time["minute"] += 1
			if self.time["minute"] >= 60:
				self.time["minute"] = 0
				self.time["hour"] += 1
				if self.time["hour"] >= 24:
					self.time["hour"] = 0
					self.time["day"] += 1
					if self.time["day"] > 28:
						self.time["day"] = 1
						self.time["season"] = self.season_list[(self.season_list.index(self.time["season"]) + 1) % 4]
						if self.time["season"] == "spring":
							self.time["year"] += 1
	
	def key_handler(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_i]:
			if cooldown("time_speed_input", 0.2):
				self.time_sprint += 0.2
		elif keys[pygame.K_o]:
			if cooldown("time_speed_input", 0.2):
				self.time_sprint -= 0.2
		elif keys[pygame.K_p]:
			self.time_sprint = 0.8

	def update(self):
		self.day_night_cycle.update(self.time["hour"], self.time["minute"])
		self.day_night_cycle.draw()
		self.calculate_time()
		self.key_handler()
		
		debug(f"{self.time["season"]} {self.time["day"]}. {self.time["hour"]}:{self.time["minute"]}", 200, 10)

		return self.time
