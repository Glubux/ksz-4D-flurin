from debug import *
from random import randint, choice
from support import *
from settings import *

class Hotbar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		
		self.hotbar_slots = 5
		self.hotbar = [["", 0] for i in range(self.hotbar_slots)]
		self.hotbar_index = 1
		self.hotbar_seleced = self.hotbar[self.hotbar_index+1]

		self.all_items = []

		
	def input(self):
		keys = pygame.key.get_pressed()

		for num_key in range(self.hotbar_slots+1):
			if keys[getattr(pygame, f'K_{num_key}')]:
				self.hotbar_index = num_key

		if keys[pygame.K_g]:
			if cooldown("give_status", 0.5):
				self.add_item(choice(get_item_list()), randint(1,10))				
		
		
	def add_item(self, item, amount):
		
		for slot in self.hotbar:
			if slot[0] == "":
				slot[0] = item
				slot[1] = amount
				break
			elif slot[0] == item:
				slot[1] += amount
				break

	def update(self):
		self.input()

		self.hotbar_seleced = self.hotbar[self.hotbar_index-1]

		debug(self.hotbar, 130,10)
		debug(self.hotbar_seleced, 150,10)

class Item(pygame.sprite.Sprite):
	def __init__(self, name = "Unknow Item", description = "Unknow Item", inv_img = "./textures/item/Unknown_Item.png", stack_max = 99, group = None, range = 3, wear = -1, meta = []):
		super().__init__()
		self.name = name
		self.type = description
		self.inv_img = inv_img
		self.stack_max = stack_max
		self.group = group
		self.range = range
		self.wear = wear
		self.meta = meta


class Menu(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.font = pygame.font.SysFont("mongolianbaiti", 50)

		self.images = self.load_images()

		self.status = False
		self.draw_frame = 0

	def load_images(self):
		textures = {
			"menu" : import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Content/4 Buttons"),
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

		return ans

	def open_menu(self):
		self.status = True
		self.draw_frame = 0

	def close_menu(self):
		self.status = False


	def draw(self):
		size = 150
		pos = [100, 400]
		y_ofset = size

		menu = [
			{
				"name": "Spiel Fortsetzen",
				"img" : [
					[14, [pos[0] + size * 0, pos[1] + y_ofset * 0], [size, size]],
					[15, [pos[0] + size * 1, pos[1] + y_ofset * 0], [size*3, size]],
					[16, [pos[0] + size * 4, pos[1] + y_ofset * 0], [size, size]]
				],
				"img_klick": [
					[17, [pos[0] + size * 0, pos[1] + y_ofset * 0], [size, size]],
					[18, [pos[0] + size * 1, pos[1] + y_ofset * 0], [size*3, size]],
					[19, [pos[0] + size * 4, pos[1] + y_ofset * 0], [size, size]]
				],
			},{
				"name": "Einstellungen",
				"img" : [
					[14, [pos[0] + size * 0, pos[1] + y_ofset * 1], [size, size]],
					[15, [pos[0] + size * 1, pos[1] + y_ofset * 1], [size*3, size]],
					[16, [pos[0] + size * 4, pos[1] + y_ofset * 1], [size, size]]
				],
				"img_klick": [
					[17, [pos[0] + size * 0, pos[1] + y_ofset * 1], [size, size]],
					[18, [pos[0] + size * 1, pos[1] + y_ofset * 1], [size*3, size]],
					[19, [pos[0] + size * 4, pos[1] + y_ofset * 1], [size, size]]
				],
			},{
				"name": "Speichern & Laden",
				"img" : [
					[14, [pos[0] + size * 0, pos[1] + y_ofset * 2], [size, size]],
					[15, [pos[0] + size * 1, pos[1] + y_ofset * 2], [size*3, size]],
					[16, [pos[0] + size * 4, pos[1] + y_ofset * 2], [size, size]]
				],
				"img_klick": [
					[17, [pos[0] + size * 0, pos[1] + y_ofset * 2], [size, size]],
					[18, [pos[0] + size * 1, pos[1] + y_ofset * 2], [size*3, size]],
					[19, [pos[0] + size * 4, pos[1] + y_ofset * 2], [size, size]]
				],
			},{
				"name": "Spiel Beenden",
				"img" : [
					[14, [pos[0] + size * 0, pos[1] + y_ofset * 3], [size, size]],
					[15, [pos[0] + size * 1, pos[1] + y_ofset * 3], [size*3, size]],
					[16, [pos[0] + size * 4, pos[1] + y_ofset * 3], [size, size]]
				],
				"img_klick": [
					[17, [pos[0] + size * 0, pos[1] + y_ofset * 3], [size, size]],
					[18, [pos[0] + size * 1, pos[1] + y_ofset * 3], [size*3, size]],
					[19, [pos[0] + size * 4, pos[1] + y_ofset * 3], [size, size]]
				],
			}
		]
		
		
		for i in range(self.draw_frame + 1):
			element = menu[i]
			for n in range(len(element["img"])):
				img = pygame.transform.scale(self.images["menu"][element["img"][n][0]], element["img"][n][2])
				self.screen.blit(img, element["img"][n][1])

			numb = self.font.render(str(i + 1), True, "black")
			self.screen.blit(numb, (element["img"][0][1][0] + 25, element["img"][0][1][1] + 50))

			text = self.font.render(element["name"], True, "black")
			self.screen.blit(text, (element["img"][0][1][0] + 100 , element["img"][0][1][1] + 50))

		if cooldown("menu_frame", 0.15):
			self.draw_frame += 1
			if self.draw_frame >= len(menu):
				self.draw_frame -= 1

	def update(self):
		self.draw()
		ans = self.input()
		return ans
	
class Inventar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()

		self.status = None

		self.textures = self.load_images()
		self.inv_open_frame = 0
		self.inv_close_frame = 0

		self.input_ans = None
		self.draw_open_ans = None
		self.draw_close_ans = None

		self.inv_pos = (-70, -330)
		self.inv_scale = 2.3

	def open_inv(self):
		self.status = "open"
		self.draw_open()


	def close_inv(self):
		self.status = "close"
		self.draw_close()

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_ESCAPE] or keys[pygame.K_e]:
			if cooldown("inv_close", 0.5):
				self.status = "close"

	def load_images(self):
		textures = {
			"inv_open" : import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Open and Close/Style 2/Open"),
			"inv_close" : import_folder("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Open and Close/Style 2/Close"),
			"inv_book" : import_image("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Inventory Book/Book Idle/1.png")
		}
		return textures

	def draw_open(self):
		for i in range(len(self.textures["inv_open"])):
			surface = self.textures["inv_open"][self.inv_open_frame]
			size = surface.get_size()
			img = pygame.transform.scale(surface, (int(size[0] * self.inv_scale), int(size[1] * self.inv_scale)))
			self.screen.blit(img, self.inv_pos)

		if cooldown("inv_open", 0.1):
			self.inv_open_frame += 1
			if self.inv_open_frame >= len(self.textures["inv_open"]):
				self.inv_open_frame = 0
				return "open_finish"

	def draw_close(self):
		for i in range(len(self.textures["inv_close"])):
			surface = self.textures["inv_close"][self.inv_close_frame]
			size = surface.get_size()
			img = pygame.transform.scale(surface, (int(size[0] * self.inv_scale), int(size[1] * self.inv_scale)))
			self.screen.blit(img, self.inv_pos)

		if cooldown("inv_close", 0.1):
			self.inv_close_frame += 1
			if self.inv_close_frame >= len(self.textures["inv_close"]):
				self.inv_close_frame = 0
				return "close_finish"
			
	def draw(self):
		size = self.textures["inv_book"].get_size()
		img = pygame.transform.scale(self.textures["inv_book"], (int(size[0] * self.inv_scale), int(size[1] * self.inv_scale)))
		self.screen.blit(img, self.inv_pos)
			

	def update(self):
		if self.status == "open":
			self.draw_open_ans = self.draw_open()
			if self.draw_open_ans == "open_finish":
				self.status = "working"

		elif self.status == "close":
			self.draw_close_ans = self.draw_close()
			if self.draw_close_ans == "close_finish":
				self.status = "closed"

		elif self.status == "working":
			self.input_ans = self.input()
			self.draw()

		return {"input_ans": self.input_ans, "status": self.status}

class Inventory_Image(pygame.sprite.Sprite):
	def __init__(self, pos, groups, type = "visible", surface = pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__()

		self.image = None
		self.rect = self.image.get_rect()