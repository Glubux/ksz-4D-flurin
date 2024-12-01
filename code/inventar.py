from debug import *

class Inventar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		
		self.hotbar_slots = 5
		self.hotbar = [["", 0] for i in range(self.hotbar_slots)]
		self.hotbar_index = 1
		self.hotbar_seleced = self.hotbar[self.hotbar_index+1]

	def input(self):
		keys = pygame.key.get_pressed()

		for num_key in range(self.hotbar_slots+1):
			if keys[getattr(pygame, f'K_{num_key}')]:
				self.hotbar_index = num_key
		
		if keys[pygame.K_g]:
			self.add_item(input("Item: "), int(input("Amount: ")))
			print("-------")

	def add_item(self, item, amount):
		
		for slot in self.hotbar:
			if slot[0] == "":
				slot[0] = item
				slot[1] = amount
				break
			elif slot[0] == item:
				slot[1] += amount
				break
			else:
				print("Inv Full")

	def update(self):
		self.input()

		self.hotbar_seleced = self.hotbar[self.hotbar_index-1]

		debug(self.hotbar_index, 30, 10)
		debug(self.hotbar, 50,10)
		debug(self.hotbar_seleced, 70,10)

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, type):
        super().__init__(groups)
		
        self.pos = pos
        self.obstacle_sprites =obstacle_sprites
        self.type = type