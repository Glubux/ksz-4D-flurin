from debug import *
from register import *
from random import randint, choice

class Inventar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		
		self.hotbar_slots = 5
		self.hotbar = [["", 0] for i in range(self.hotbar_slots)]
		self.hotbar_index = 1
		self.hotbar_seleced = self.hotbar[self.hotbar_index+1]

		self.all_items = []

		self.give_status = False
		self.give_countdown = 300
		self.give_time = 0
		
	def input(self):
		keys = pygame.key.get_pressed()

		for num_key in range(self.hotbar_slots+1):
			if keys[getattr(pygame, f'K_{num_key}')]:
				self.hotbar_index = num_key
		
		if keys[pygame.K_g]:
			if self.give_status:
				if self.give_time + self.give_countdown <= pygame.time.get_ticks():
					self.give_status = False
			else:
				self.add_item(choice(get_item_list()), randint(1,10))
				self.give_status = True
				self.give_time = pygame.time.get_ticks()


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

		debug(self.hotbar_index, 30, 10)
		debug(self.hotbar, 50,10)
		debug(self.hotbar_seleced, 70,10)

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