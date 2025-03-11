from debug import *
from random import randint, choice
from support import *
from settings import *
from audio import *

class Menu(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.font = pygame.font.SysFont("mongolianbaiti", 50)

		self.fade = FadeEffect()
		self.soundmanager = SoundManager()

		self.images = self.load_images()

		self.input_ans = None
		self.status = "close"
		self.draw_frame = 0

		self.soundmanager.load_sfx("menu", "menu.mp3")

	def load_images(self):
		textures = {
			"menu" : import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/2 Brown Book/1 Sprites/Content/4 Buttons"),
		}
		return textures
	
	def input(self):
		keys = pygame.key.get_pressed()
		ans = ""

		if keys[pygame.K_1]:
			ans = "1"
		if keys[pygame.K_2]:
			ans = "2"
		if keys[pygame.K_3]:
			ans = "3"
		if keys[pygame.K_4]:
			ans = "4"

		if keys[pygame.K_ESCAPE]:
			if self.status == "idl":
				if cooldown("menu_close", 0.5):
					self.status = "close"

		return ans


	def draw(self):
		size = 150
		pos = [100, 400]
		y_ofset = size

		menu = [
			{
				"name": "Spiel Fortsetzen",
				"img" : [
					[18, [pos[0] + size * 0, pos[1] + y_ofset * 0], [size, size]],
					[19, [pos[0] + size * 1, pos[1] + y_ofset * 0], [size*3, size]],
					[20, [pos[0] + size * 4, pos[1] + y_ofset * 0], [size, size]]
				],
				"img_klick": [
					[18, [pos[0] + size * 0, pos[1] + y_ofset * 0], [size, size]],
					[19, [pos[0] + size * 1, pos[1] + y_ofset * 0], [size*3, size]],
					[20, [pos[0] + size * 4, pos[1] + y_ofset * 0], [size, size]]
				],
			},{
				"name": "Einstellungen",
				"img" : [
					[18, [pos[0] + size * 0, pos[1] + y_ofset * 1], [size, size]],
					[19, [pos[0] + size * 1, pos[1] + y_ofset * 1], [size*3, size]],
					[20, [pos[0] + size * 4, pos[1] + y_ofset * 1], [size, size]]
				],
				"img_klick": [
					[18, [pos[0] + size * 0, pos[1] + y_ofset * 1], [size, size]],
					[19, [pos[0] + size * 1, pos[1] + y_ofset * 1], [size*3, size]],
					[20, [pos[0] + size * 4, pos[1] + y_ofset * 1], [size, size]]
				],
			},{
				"name": "Speichern & Laden",
				"img" : [
					[18, [pos[0] + size * 0, pos[1] + y_ofset * 2], [size, size]],
					[19, [pos[0] + size * 1, pos[1] + y_ofset * 2], [size*3, size]],
					[20, [pos[0] + size * 4, pos[1] + y_ofset * 2], [size, size]]
				],
				"img_klick": [
					[18, [pos[0] + size * 0, pos[1] + y_ofset * 2], [size, size]],
					[19, [pos[0] + size * 1, pos[1] + y_ofset * 2], [size*3, size]],
					[20, [pos[0] + size * 4, pos[1] + y_ofset * 2], [size, size]]
				],
			},{
				"name": "Spiel Beenden",
				"img" : [
					[18, [pos[0] + size * 0, pos[1] + y_ofset * 3], [size, size]],
					[19, [pos[0] + size * 1, pos[1] + y_ofset * 3], [size*3, size]],
					[20, [pos[0] + size * 4, pos[1] + y_ofset * 3], [size, size]]
				],
				"img_klick": [
					[18, [pos[0] + size * 0, pos[1] + y_ofset * 3], [size, size]],
					[19, [pos[0] + size * 1, pos[1] + y_ofset * 3], [size*3, size]],
					[20, [pos[0] + size * 4, pos[1] + y_ofset * 3], [size, size]]
				],
			}
		]
		
		if self.status == "open":
			for i in range(self.draw_frame + 1):
				element = menu[i]
				for n in range(len(element["img"])):
					img = pygame.transform.scale(self.images["menu"][element["img"][n][0]], element["img"][n][2])
					self.screen.blit(img, element["img"][n][1])

				numb = self.font.render(str(i + 1), True, "black")
				self.screen.blit(numb, (element["img"][0][1][0] + 25, element["img"][0][1][1] + 65))

				text = self.font.render(element["name"], True, "black")
				self.screen.blit(text, (element["img"][0][1][0] + 100 , element["img"][0][1][1] + 65))
			

			if cooldown("menu_frame", 0.15):
				self.soundmanager.play_sfx("menu")
				self.draw_frame += 1
				if self.draw_frame >= len(menu):
					self.draw_frame = 0
					self.status = "idl"
					return "idl"
			
			return "open"

		if self.status == "close":
			if self.draw_frame == 0:
				self.draw_frame = len(menu)

			for i in range(self.draw_frame):
				element = menu[i]
				for n in range(len(element["img"])):
					img = pygame.transform.scale(self.images["menu"][element["img"][n][0]], element["img"][n][2])
					self.screen.blit(img, element["img"][n][1])

				numb = self.font.render(str(i + 1), True, "black")
				self.screen.blit(numb, (element["img"][0][1][0] + 25, element["img"][0][1][1] + 65))

				text = self.font.render(element["name"], True, "black")
				self.screen.blit(text, (element["img"][0][1][0] + 100 , element["img"][0][1][1] + 65))

			if cooldown("menu_frame", 0.15):
				self.soundmanager.play_sfx("menu")
				self.draw_frame -= 1
				if self.draw_frame <= 0:
					self.draw_frame = 0
					self.status = "closed"
					return "closed"

			return "close"


		if self.status == "idl":
			for element in menu:
				for n in range(len(element["img"])):
					img = pygame.transform.scale(self.images["menu"][element["img"][n][0]], element["img"][n][2])
					self.screen.blit(img, element["img"][n][1])

				numb = self.font.render(str(menu.index(element) + 1), True, "black")
				self.screen.blit(numb, (element["img"][0][1][0] + 25, element["img"][0][1][1] + 65))

				text = self.font.render(element["name"], True, "black")
				self.screen.blit(text, (element["img"][0][1][0] + 100, element["img"][0][1][1] + 65))

			return "idl"



	def update(self, input_status):
		if input_status == "open" :
			self.status = "open"

		self.input_ans = self.input()
		self.fade.update()

		draw_ans = self.draw()
		self.status = draw_ans

		if self.status == "open":
			self.fade.set_fade(50, 0.5)
		if self.status == "close":
			self.fade.set_fade(0, 0.4)

		return {"input_ans": self.input_ans, "status": self.status}
	

class Inventar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.fade = FadeEffect()
		self.soundmanager = SoundManager()
		self.font_big = pygame.font.Font("../font/BLACC___.TTF", 100)
		self.font_smal = pygame.font.Font("../font/BLACC___.TTF", 40)

		self.status = None
		self.season = "spring"
		self.player_pos = (0,0)

		self.textures = self.load_images()
		self.inv_open_frame = 0
		self.inv_close_frame = 0

		self.input_ans = None
		self.draw_open_ans = None
		self.draw_close_ans = None

		self.inv_pos = (-70, -330)
		self.inv_scale = 2.3

		self.scroll_dir = "Left"
		self.scroll_frame = 0
		self.rand_style = 0
		self.tab_frame = 0
		self.tab_selectet = 1

		self.content_left_pos = pygame.Rect(280, 170, 600, 750)
		self.content_right_pos = pygame.Rect(1040, 170, 600, 750)

		self.inventar = []
		self.inventar_wight = 6


		# Hotbar
		self.hotbar_slots = 9
		self.hotbar = [["", 0] for i in range(self.hotbar_slots)]
		self.hotbar_index = 1
		self.hotbar_seleced = self.hotbar[self.hotbar_index+1]

		self.all_items = []

		self.soundmanager.load_sfx("book_open", "book_open.mp3")
		self.soundmanager.load_sfx("book_close", "book_close.mp3")
		self.soundmanager.load_sfx("flippage1", "flippage1.mp3")
		self.soundmanager.load_sfx("flippage2", "flippage2.mp3")
		self.soundmanager.load_sfx("flippage3", "flippage3.mp3")

	def add_item(self, item, amount):
		
		for slot in self.hotbar:
			if slot[0] == "":
				slot[0] = item
				slot[1] = amount
				break
			elif slot[0] == item:
				slot[1] += amount
				break

	def key_handler(self, kind):
		keys = pygame.key.get_pressed()

		if kind == "hotbar":
			for num_key in range(1, self.hotbar_slots + 1):
				if keys[getattr(pygame, f'K_{num_key}')]:
					self.hotbar_index = num_key

			if keys[pygame.K_g]:
				if cooldown("give_status", 0.5):
					self.add_item(choice(get_item_list()), randint(1,10))

		if kind == "inv":
			if keys[pygame.K_ESCAPE] or keys[pygame.K_e]:
				if cooldown("inv_close", 0.5):
					self.status = "close"

			if keys[pygame.K_LEFT]:
				if cooldown("inv_scroll", 0.5):	
					self.scroll_dir = "Left"
					self.status = "scroll"
			if keys[pygame.K_RIGHT]:
				if cooldown("inv_scroll", 0.5):	
					self.scroll_dir = "Right"
					self.status = "scroll"

			if keys[pygame.K_DOWN]:
				if cooldown("inv_tabs", 0.5):
					if self.status == "idl":
						self.status = "apear_tabs"

			if keys[pygame.K_UP]:
				if cooldown("inv_tabs", 0.5):
					if self.status == "idl":
						self.status = "disapear_tabs"


			for num_key in range(1, 7):
				if keys[getattr(pygame, f"K_{num_key}")]:
					if cooldown("tab_select", 0.1) and self.status == "idl":
						self.tab_selectet = num_key
						self.status = "disapear_tabs"


	def load_images(self):
		textures = {
			"inv_open" : import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Open and Close/Style 2/Open"),
			"inv_close" : import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Open and Close/Style 2/Close"),
			"hotbar_paper": import_image("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Paper UI Pack/Paper UI/Plain/3 Item Holder/1.png"),
			"hotbar_slot": import_image("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Content/5 Holders/6.png"),
			"hotbar_slot_highlight": import_image("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Content/6 High lighter/5.png"),
			"inv_scroll": {
				"left": [
					import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Page Flip/Style 1/Flip Left/"),
					import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Page Flip/Style 2/Flip Left/"),
					import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Page Flip/Style 3/Flip Left/"),
				],
				"right": [
					import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Page Flip/Style 1/Flip Right/"),
					import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Page Flip/Style 2/Flip Right/"),
					import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Page Flip/Style 3/Flip Right/"),
				]
			},
			"apear_tabs": import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Side Tabs/Appear/Without icons/"),
			"disapear_tabs": import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Side Tabs/Disappear/Without icons/"),
			"selected_tab": import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Side Tabs/Tabs/Without icons/"),
			"tabs": import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Content/tabs/"),
			"content_map": import_image(["../textures/inv_maps/spring.png", "../textures/inv_maps/summer.png", "../textures/inv_maps/autom.png", "../textures/inv_maps/winter.png"]),
			"content_map_frame": import_image("../textures/inv_maps/frame.png"),
			"content_map_marker": import_image("../textures/inv_maps/marker.png")
		}
		return textures

			
	def draw(self, kind):
		if kind == "inv":
			if self.status == "open":
				surface = self.textures["inv_open"][self.inv_open_frame]
				size = surface.get_size()
				img = pygame.transform.scale(surface, (int(size[0] * self.inv_scale), int(size[1] * self.inv_scale)))
				self.screen.blit(img, self.inv_pos)

				if cooldown("open_sound", 1):
					self.soundmanager.play_sfx("book_open")

				if cooldown("inv_open", 0.1):
					self.inv_open_frame += 1
					if self.inv_open_frame >= len(self.textures["inv_open"]):
						self.inv_open_frame = 0
						self.status = "idl"
				else:
					self.status = "open"
			
			elif self.status == "close":
				surface = self.textures["inv_close"][self.inv_close_frame]
				size = surface.get_size()
				img = pygame.transform.scale(surface, (int(size[0] * self.inv_scale), int(size[1] * self.inv_scale)))
				self.screen.blit(img, self.inv_pos)

				if cooldown("close_delay", 1.5):
					if cooldown("close_sound", 1):
						self.soundmanager.play_sfx("book_close")

				if cooldown("inv_close", 0.1):
					self.inv_close_frame += 1
					if self.inv_close_frame >= len(self.textures["inv_close"]):
						self.inv_close_frame = 0
						self.status = "closed"
				else:
					self.status = "close"


			elif self.status == "idl":
				surface = self.textures["selected_tab"][self.tab_selectet]
				size = surface.get_size()
				img = pygame.transform.scale(surface, (int(size[0] * self.inv_scale), int(size[1] * self.inv_scale)))
				self.screen.blit(img, self.inv_pos)
				self.status = "idl"
			
			
			elif self.status == "scroll":
				if self.scroll_frame == 0:
					self.rand_style = randint(0, 2)

				if self.scroll_dir == "Left":
					surface = self.textures["inv_scroll"]["left"][self.rand_style][self.scroll_frame]

				elif self.scroll_dir == "Right":
					surface = self.textures["inv_scroll"]["right"][self.rand_style][self.scroll_frame]

				size = surface.get_size()
				img = pygame.transform.scale(surface, (int(size[0] * self.inv_scale), int(size[1] * self.inv_scale)))
				self.screen.blit(img, self.inv_pos)

				if cooldown("flippage_sound", 1):
					self.soundmanager.play_sfx(f"flippage{randint(1,3)}")

				if cooldown("inv_scroll", 0.08):
					self.scroll_frame += 1
					if self.scroll_frame >= len(self.textures["inv_scroll"]["left"][self.rand_style]):
						self.scroll_frame = 0
						self.status = "apear_tabs"
					else:
						self.status = "scroll"

			
			elif self.status == "apear_tabs":
				surface = self.textures["apear_tabs"][self.tab_frame]
				size = surface.get_size()
				img = pygame.transform.scale(surface, (int(size[0] * self.inv_scale), int(size[1] * self.inv_scale)))
				self.screen.blit(img, self.inv_pos)

				if cooldown("inv_tabs", 0.1):
					self.tab_frame += 1
					if self.tab_frame >= len(self.textures["apear_tabs"]):
						self.tab_frame = 0
					self.status = "idl"
				else:
					self.status = "apear_tabs"


			elif self.status == "disapear_tabs":
				surface = self.textures["disapear_tabs"][self.tab_frame]
				size = surface.get_size()
				img = pygame.transform.scale(surface, (int(size[0] * self.inv_scale), int(size[1] * self.inv_scale)))
				self.screen.blit(img, self.inv_pos)

				if cooldown("inv_tabs", 0.1):
					self.tab_frame += 1
					if self.tab_frame >= len(self.textures["disapear_tabs"]):
						self.tab_frame = 0
						self.status = "scroll"
				else:
					self.status = "disapear_tabs"

			"""
			rect_left_surface = pygame.Surface(self.content_left_pos.size, pygame.SRCALPHA)
			rect_left_surface.fill((255, 0, 0, 128))  # 50% transparentes Rot
			self.screen.blit(rect_left_surface, self.content_left_pos.topleft)

			rect_right_surface = pygame.Surface(self.content_right_pos.size, pygame.SRCALPHA)
			rect_right_surface.fill((0, 255, 0, 128))  # 50% transparentes Grün
			self.screen.blit(rect_right_surface, self.content_right_pos.topleft)
			"""
			

			if self.status in ["idl"]:
				tab_pos = [1700, 230]
				tab_scale = 2.3
				tab_ofset = 20
				for i in range(len(self.textures["tabs"])):
					surface = self.textures["tabs"][i]
					size = surface.get_size()
					img = pygame.transform.scale(surface, (int(size[0] * tab_scale), int(size[1] * tab_scale)))
					
					if i+1 == self.tab_selectet:
						self.screen.blit(img, (tab_pos[0] + tab_ofset, tab_pos[1] + i * 88))
					else:
						self.screen.blit(img, (tab_pos[0], tab_pos[1] + i * 88))
				
				"""
				Tabs
				-----
				- Map -> key m
				- Inventar (Items) -> key e
				- Quest -> key j
				- Settings -> über menu
				- Save
				- Credits
				"""
				
				if self.tab_selectet == 1:
					seasons = {"spring": 0, "summer": 1, "autom": 2, "winter": 3}

					text = self.font_big.render("Map", True, (0, 0, 0))
					text_rect = text.get_rect(center=(self.content_left_pos.centerx, self.content_left_pos.y + 20))

					surface_map = self.textures["content_map"][seasons.get(self.season, -1)]
					surface_frame = self.textures["content_map_frame"]
					surface_marker = self.textures["content_map_marker"]
					img_map = pygame.transform.scale(surface_map, (500,500))
					img_frame = pygame.transform.scale(surface_frame, (500,500))
					img_marker = pygame.transform.scale(surface_marker, (13,13))

					p = get_minimap_position(self.player_pos[0], self.player_pos[1])
					img_map_rect = img_map.get_rect(center=(self.content_left_pos.centerx, self.content_left_pos.centery))
					img_frame_rect = img_frame.get_rect(center=(self.content_left_pos.centerx, self.content_left_pos.centery))
					img_marker_rect = img_marker.get_rect(center=(img_map_rect.topleft[0] + p[0], img_map_rect.topleft[1] + p[1]))
					
					
					self.screen.blit(text, text_rect)
					self.screen.blit(img_map, img_map_rect)
					self.screen.blit(img_frame, img_frame_rect)
					self.screen.blit(img_marker, img_marker_rect)

				elif self.tab_selectet == 2:
					text = self.font_big.render("Inventar", True, (0, 0, 0))
					text_rect = text.get_rect(center=(self.content_left_pos.centerx, self.content_left_pos.y + 20))
					
					self.screen.blit(text, text_rect)

				elif self.tab_selectet == 3:
					text = self.font_big.render("Quest", True, (0, 0, 0))
					text_rect = text.get_rect(center=(self.content_left_pos.centerx, self.content_left_pos.y + 20))

					text1 = self.font_smal.render("Quest noch nicht verfügbar.", True, (0,0,0))
					text2 = self.font_smal.render("Entdecke bis dann die Welt.", True, (0,0,0))
					text1_rect = text1.get_rect(topleft=(self.content_left_pos.topleft[0], self.content_left_pos.y + 120))
					text2_rect = text2.get_rect(topleft=(self.content_left_pos.topleft[0], self.content_left_pos.y + 170))
					
					self.screen.blit(text, text_rect)
					self.screen.blit(text1, text1_rect)
					self.screen.blit(text2, text2_rect)

				elif self.tab_selectet == 4:
					text = self.font_big.render("Settings", True, (0, 0, 0))
					text_rect = text.get_rect(center=(self.content_left_pos.centerx, self.content_left_pos.y + 20))

					self.screen.blit(text, text_rect)

				elif self.tab_selectet == 5:
					text = self.font_big.render("Save", True, (0, 0, 0))
					text_rect = text.get_rect(center=(self.content_left_pos.centerx, self.content_left_pos.y + 20))
					
					self.screen.blit(text, text_rect)

				elif self.tab_selectet == 6:
					text = self.font_big.render("Credits", True, (0, 0, 0))
					text_rect = text.get_rect(center=(self.content_left_pos.centerx, self.content_left_pos.y + 20))

					hole_text = [
						"Vielen Dank für die Unterstützung:",
						"- Emanuelle Costa [Texture]",
						"- Humblepixel [Texture]",
						"- Clear Code [Tutorial/Grundlagen]",
						"- Andrin & Jonas [Code & Moral]",
						"- Copilot und ChatGPT [Code]"
					]

					start_y = self.content_left_pos.y + 100

					for i, line in enumerate(hole_text):
						text1 = self.font_smal.render(line, True, (0, 0, 0))
						text1_rect = text1.get_rect(topleft=(self.content_left_pos.topleft[0], start_y + i * 50))
						self.screen.blit(text1, text1_rect)

					self.screen.blit(text, text_rect)

			return self.status


					
		if kind == "hotbar":
			hotbar_paper_scale = 1
			hotbar_slot_scale = 1
			pos = [460 , 900]

			self.textures["hotbar_paper"] = pygame.transform.scale(self.textures["hotbar_paper"], (int(self.textures["hotbar_paper"].get_width() * hotbar_paper_scale), int(self.textures["hotbar_paper"].get_height() * hotbar_paper_scale)))
			self.textures["hotbar_slot"] = pygame.transform.scale(self.textures["hotbar_slot"], (self.textures["hotbar_slot"].get_width() * hotbar_slot_scale, self.textures["hotbar_slot"].get_height() * hotbar_slot_scale))

			self.screen.blit(self.textures["hotbar_paper"], pos)
			for i in range(9):
				self.screen.blit(self.textures["hotbar_slot"], (pos[0] + 80 + i * 95, pos[1] + 60))
			self.screen.blit(self.textures["hotbar_slot_highlight"], (pos[0] + 80 + (self.hotbar_index-1) * 95, pos[1] + 60))


	def update(self, kind, input_status, season, playerpos):
		self.season = season
		self.player_pos = playerpos
		self.fade.update()
		if input_status == "open" :
			self.status = "open"
			
		key_ans = self.key_handler(kind)


		if kind == "inv":
			draw_ans = self.draw(kind)
			self.status = draw_ans

			if self.status == "open":
				self.fade.set_fade(50, 0.5)
			if self.status == "close":
				self.fade.set_fade(0, 0.4)
			
			return {"input_ans": self.input_ans, "status": self.status}

		elif kind == "hotbar":
			self.draw(kind)

			self.hotbar_seleced = self.hotbar[self.hotbar_index-1]
			#debug(self.hotbar, 130,10)
			#debug(self.hotbar_seleced, 150,10)

			return {}



class Item(pygame.sprite.Sprite):
	def __init__(self, name, description, path, stack_max, group = None, range = 3, wear = -1, meta = []):
		super().__init__(group)
		self.name = name
		self.type = description
		self.inv_img = import_image(path)
		self.stack_max = stack_max
		self.group = group
		self.range = range
		self.wear = wear
		self.meta = meta