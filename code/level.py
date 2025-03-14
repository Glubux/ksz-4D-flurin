import pygame, sys
from settings import *
from tile import *
from player import Player
from debug import *
from support import *
from inventar import *
from npc import *
from audio import *

class Level:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.menu = Menu()
		self.inv = Inventar()
		self.dialog = Dialog()
		self.time = Time()
		self.fade = FadeEffect()
		self.sound_manager = SoundManager()

		self.ingametime = self.time.update()

		self.season = self.ingametime["season"]
		self.season_current = self.season
		self.day_current = self.ingametime["day"]
		self.season_list = ["winter", "spring", "summer", "autom"]

		self.visible_sprites = YSortCameraGroup(self.season)
		self.obstacle_sprites = pygame.sprite.Group()
		self.water_group = pygame.sprite.Group()
		self.npcs = pygame.sprite.Group()
		self.plants = pygame.sprite.Group()


		self.inv_status = "closed"
		self.menu_status = "closed"
		self.dialog_status = False

		self.inv_update_ans = None
		self.menu_update_ans = None
		self.dialog_ans = None

		# sounds
		self.sound_manager.load_sfx("faucet", "/mornign_faucet.mp3")
		self.sound_manager.load_sfx("ernte", "ernte.mp3")
		self.sound_manager.load_sfx("attack", "attack.mp3")


		self.music_list = [
			"whispers_in_the_rain.mp3",
			"the_old_windmill.mp3",
			"echoes_in_the_glen.mp3",
			"after work.mp3",
			"autumn vibes.mp3",
			"dance of the trees.mp3",
			"hot springs.mp3",
			"life of sense.mp3",
			"like the wind.mp3",
			"the lighthouse.mp3",
			"the watermill.mp3",
		]
		self.season_changed = False
		self.map(self.season)

	def map(self, season):
		self.season_setting = {
			"winter": ["winter_deco", "boundary", "npc"],
			"spring": ["spring_deco", "water_spring_summer", "boundary", "plants", "npc"],
			"summer": ["summer_deco", "water_spring_summer", "boundary", "plants", "npc"],
			"autom": ["autom_deco", "water_autom", "boundary", "plants", "npc"],
		}
		self.csv_data = {
			"boundary": [import_csv_layout("../textures/map/map_obstacle_main.csv"), "None"],
			"plants": [import_csv_layout("../textures/map/map_obstacle_plants.csv"), "None"],
			"water_spring_summer": [import_csv_layout("../textures/map/map_Animation_water_spring_summer.csv"), "summer"],
			"water_autom": [import_csv_layout("../textures/map/map_Animation_water_autom.csv"), "autom"],
			
			"spring_deco": [import_csv_layout("../textures/map/map_Spring_decoration.csv"), "spring"],
			"summer_deco": [import_csv_layout("../textures/map/map_Summer_decoration.csv"), "summer"],
			"autom_deco": [import_csv_layout("../textures/map/map_Autom_decoration.csv"), "autom"],
			"winter_deco": [import_csv_layout("../textures/map/map_Winter_decoration.csv"), "winter"],
			"npc": [import_csv_layout("../textures/map/map_npc.csv"), None]
		}
		self.textures = {
			"winter": import_tileset("tileset", "../textures/farm/Tileset/Tileset Winter.png", [15,14], (16,16), 4),
			"summer": import_tileset("tileset", "../textures/farm/Tileset/Tileset Grass Summer.png", [25,22], (16,16), 4),
			"spring": import_tileset("tileset", "../textures/farm/Tileset/Tileset Grass Spring.png", [25,27], (16,16), 4),
			"autom": import_tileset("tileset", "../textures/farm/Tileset/Tileset Grass Fall.png", [25,22], (16,16), 4),
			"boundary": import_tileset("tileset", "../textures/tiled/color_tiledset.png", [4,4], (16,16), 4),
			#"plants": import_tileset("tileset", "../textures/tiled/color_tiledset.png", [4,4], (16,16), 4),
			"plants": import_image("../textures/farm/farmland.png"),
			"npc": import_tileset("character", "../textures/character and portrait/Character/Pre-made/Josh/Idle.png", [4,4]),
		}
		
		for style in self.season_setting[season]: # needed self.csv_data
			layout = self.csv_data[style][0] # -> [surfacelist, textur_verweis]
			
			for row_index, row in enumerate(layout):
				for coll_index, col in enumerate(row):
					x = coll_index * TILESIZE
					y = row_index * TILESIZE
					col = int(col)

					if col != -1:
						if style == "boundary":
							if col == 0: # wasser
								Tile((x,y),[self.water_group], [style, "background", col] ,self.textures["boundary"][col])
							elif col == 12: # border
								Tile((x,y),[self.obstacle_sprites], [style, "background", col] ,self.textures["boundary"][col])
						
						elif style == "water_spring_summer":
							Tile((x,y),[self.visible_sprites], [style, "background"] ,self.textures["spring"][col])
						elif style == "water_autom":
							Tile((x,y),[self.visible_sprites], [style, "background"] ,self.textures["autom"][col])

						elif style == "plants":
							Tile((x,y),[self.visible_sprites], [style, "background"], self.textures["plants"])
							Plants((x,y),[self.visible_sprites, self.plants], {"style": style, "col": col, "pos": (x,y)})

						elif style == "npc":
							npc = Npc((x, y), [self.visible_sprites, self.npcs], self.obstacle_sprites, "schrödinger", self.dialog, self.textures["npc"])
							self.npcs.add(npc)
							
						else:
							Tile((x,y),[self.visible_sprites], [style, "backgorund"], self.textures[self.season][col])

		if self.season_changed:
			self.player = Player((self.player.rect.x,self.player.rect.y),[self.visible_sprites],self.obstacle_sprites,"Alex")
		else:
			self.player = Player((1500,500),[self.visible_sprites],self.obstacle_sprites,"Alex")


	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_e]:
			if cooldown("open_inv", 0.5):
				if self.inv_status == "closed" and self.menu_status == "closed":
					self.inv_status = "open"

		if keys[pygame.K_ESCAPE]:
			if cooldown("open_menu", 0.5):
				if self.menu_status == "closed" and self.inv_status == "closed":
					self.menu_status = "open"
					#self.fade.set_fade(50, 0.5)

					#self.fade.set_fade(0, 1, True)

		elif keys[pygame.K_f]:
			if cooldown("ernte", 0.3):
				colided = pygame.sprite.spritecollide(self.player, self.plants, True, pygame.sprite.collide_mask)
				if colided:
					self.sound_manager.play_sfx("ernte")
				else:
					self.sound_manager.play_sfx("attack")


		if keys[pygame.K_c]:
			x = self.player.rect.centerx
			y = self.player.rect.centery
			Tile((x,y),[self.visible_sprites], ["style", "background"], self.textures["boundary"][0])

		if keys[pygame.K_m]:
			self.sound_manager.stop_music()
		
		if keys[pygame.K_LALT]:
			self.sound_manager.set_music_volume(0.05)
		if keys[pygame.K_RALT]:
			self.sound_manager.set_music_volume(0.2)


		
	def run(self):
		if self.season_changed == False:
			self.season_changed = True

		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.input()
		self.ingametime = self.time.update()
		if self.ingametime["season"] != self.season_current:
			self.season_current = self.ingametime["season"]
			self.season = self.season_current
			self.visible_sprites.empty()
			self.visible_sprites.__init__(self.season)
			self.map(self.season)

		if self.ingametime["day"] != self.day_current:
			self.day_current = self.ingametime["day"]
			for plant in self.plants:
				plant.grow_update(self.season)

		if self.ingametime["hour"] == 6 and self.ingametime["minute"] == 6:
			self.sound_manager.set_sfx_volume(0.1)
			self.sound_manager.play_sfx("faucet")

		self.fade.update()

		self.dialog_ans = self.dialog.update()

		self.play_music()
		#self.sound_manager.stop_music()

		if self.menu_status in ["open", "opened"]:
			self.menu_update_ans = self.menu.update(self.menu_status)

			if self.menu_update_ans["input_ans"] == "1":
				self.menu.status = "close"
				self.menu_status = False
			if self.menu_update_ans["input_ans"] == "2":
				print("Einstellungen")
			if self.menu_update_ans["input_ans"] == "3":
				print("Speichern & Laden")
			if self.menu_update_ans["input_ans"] == "4":
				pygame.quit()
				sys.exit()

			if self.menu_update_ans["status"] == "closed":
				self.menu_status = "closed"
			elif self.menu_update_ans["status"] == "idl":
				self.menu_status = "opened"
			
			
		elif self.inv_status in ["open", "opened"]:
			self.inv_update_ans = self.inv.update("inv", self.inv_status, self.season, self.player.rect)
		
			if self.inv_update_ans["status"] == "closed":
				self.inv_status = "closed"
				self.inv.status = None
			elif self.inv_update_ans["status"] == "idl":
				self.inv_status = "opened"
		
		else:
			self.inv_update_ans = self.inv.update("hotbar", "", "", "")
			self.time.draw()

			self.visible_sprites.update()

			for npc in self.npcs:
				npc.update_player_pos(self.player.rect.center)

		if self.colide():
			#print("water")
			pass


		
	def colide(self):
		return pygame.sprite.spritecollideany(self.player, self.water_group, pygame.sprite.collide_rect)
	
	def play_music(self):
		if not self.sound_manager.is_music_playing():
			self.sound_manager.play_music(self.music_list[randint(0, len(self.music_list)-1)],1)

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
		self.screen = pygame.display.get_surface()
		self.font = pygame.font.SysFont("mongolianbaiti", 50)
		self.season_list = ["spring", "summer", "autom", "winter"]
		self.weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
		self.time = {
			"year": 1,
			"season": "spring",
			"day": 1,
			"hour": 5,
			"minute": 45,
			"weekday": self.weekdays[0]
		}
		self.images = self.load_images()
		self.rect = self.images["morning"][0].get_rect()
		self.images_count = 0
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
				self.time["weekday"] = self.weekdays[(self.weekdays.index(self.time["weekday"]) + 1) % 7]
			if self.time["day"] > 28:
				self.time["day"] = 1
				self.time["season"] = self.season_list[(self.season_list.index(self.time["season"]) + 1) % 4]
			if self.time["season"] == "spring":
				self.time["year"] += 1
	
	def key_handler(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_o]:
			if cooldown("time_speed_input", 0.2):
				self.time_sprint -= 0.2

		elif keys[pygame.K_l]:
			if cooldown("test", 0.2):
				self.time["day"] += 1
		
		elif keys[pygame.K_p]:
			self.time_sprint = 0.8


	def load_images(self):
		self.scale_faktor = 1.5
		self.background_scale = 1.8

		raw_images = {
			"morning": import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Day & Night Cycle/Inventory Book/1 Dawn/"),
			"day": import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Day & Night Cycle/Inventory Book/2 Day/"),
			"evening": import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Day & Night Cycle/Inventory Book/3 Noon/"),
			"night": import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Day & Night Cycle/Inventory Book/4 Night/"),
			"time_background": import_image("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Paper UI Pack/Paper UI/Plain/6 Player HUD/1.png")
		}

		scaled_images = {}

		for key in ["morning", "day", "evening", "night"]:
			scaled_images[key] = [pygame.transform.scale(img, (int(img.get_width() * self.scale_faktor), int(img.get_height() * self.scale_faktor))) for img in raw_images[key]]

		time_background_image = raw_images["time_background"]
		scaled_images["time_background"] = pygame.transform.scale(time_background_image, (int(time_background_image.get_width() * self.background_scale), int(time_background_image.get_height() * self.background_scale)))

		return scaled_images


	def draw(self):
		if 20 <= self.time["hour"] < 23:
			image_list = self.images["evening"]
		elif 22 <= self.time["hour"] or self.time["hour"] < 5:
			image_list = self.images["night"]
		elif 5 <= self.time["hour"] < 8:
			image_list = self.images["morning"]
		elif 8 <= self.time["hour"] < 20:
			image_list = self.images["day"]
		
		if cooldown("draw_time_image", 0.1):
			self.images_count = (self.images_count + 1) % len(image_list)

		pos = [WIDTH - self.images["time_background"].get_width()-50 ,0]


		time_text_1 = self.font.render(f"{self.time["weekday"]} | {self.time["day"]}", True, "black")
		time_text_2 = self.font.render(f"{self.time["hour"]}:{self.time["minute"]-self.time["minute"]%5} ", True, "black")
		
		self.screen.blit(self.images["time_background"], pos)
		self.screen.blit(image_list[self.images_count], [pos[0] + 280, pos[1] + 70])
		self.screen.blit(time_text_1, [pos[0] + 100, pos[1] + 100])
		self.screen.blit(time_text_2, [pos[0] + 100, pos[1] + 150])

		
	def update(self):
		self.day_night_cycle.update(self.time["hour"], self.time["minute"])
		self.day_night_cycle.draw()
		self.calculate_time()
		self.key_handler()

		return self.time
