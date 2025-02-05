import pygame, sys
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from inventar import *
from npc import *

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.npcs = pygame.sprite.Group()

		
		self.inv_status = False
		self.menu_status = False
		self.dialog_status = False

		self.hotbar = Hotbar()
		self.menu = Menu()
		self.inv = Inventar()
		self.dialog = Dialog()

		self.menu_data = None
		self.inv_data = None

		self.inv_update_ans = None

		self.dialog_ans = None

		# sprite setup
		self.create_map()


	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../map/map1_border.csv'),
			'grass': import_csv_layout('../map/map1_grass.csv'),
			"npc": import_csv_layout("../textures/Tiled_work/npc.csv")
		}
		textures = {
			'grass': import_folder('../textures/grass'),
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')

						if style == 'grass':
							grass_img = textures['grass'][int(col)-64]
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'grass',grass_img)

						if style == "npc":
							npc = Npc((x, y), [self.visible_sprites, self.npcs], self.obstacle_sprites, "schrödinger", self.dialog)
							self.npcs.add(npc)


		self.player = Player((1000,500),[self.visible_sprites],self.obstacle_sprites)


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

				else:
					self.inv.close_inv()
					pass

		if keys[pygame.K_ESCAPE]:
			if cooldown("open_menu", 0.5):
				if not self.menu_status:
					if self.inv_status:
						self.inv.close_inv()
					else:
						self.menu_status = True
						self.menu.open_menu()
				
				else:
					self.menu.close_menu()
					self.menu_status = False
		
	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.input()

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


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load('../textures/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width + player.acceleration.x
		self.offset.y = player.rect.centery - self.half_height + player.acceleration.y
		self.offset.normalize()

		# drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
