import pygame 
from settings import *
from debug import *
from support import *
from dialog import *
from audio import *

class Npc(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites, name, dialog, img):
		super().__init__(groups)
		self.name = name
		self.npc_data = npcs[name]
		self.img = img
		self.image_frame = 0
		self.image = self.img["down"][self.image_frame]
		self.image = pygame.transform.scale(self.image, (self.image.get_width()*1, self.image.get_height()*1))
		self.pos = pos
		self.rect = self.image.get_rect(topleft=(self.pos[0], self.pos[1]))
		self.hitbox = self.rect.inflate(-10,-26)
		self.obstacle_sprites = obstacle_sprites

		self.dialog = dialog

		self.player_pos = None
		self.is_inrange = False

		self.ans_keyhandler = None

		self.sound_manager = SoundManager()
		self.sound_manager.set_sfx_volume(1.2)
		self.sound_manager.load_sfx("begrüssung", "begrüssung.mp3")


	def update_player_pos(self, player_pos):
		self.player_pos = player_pos

	def check_distance_to_player(self):
		if self.player_pos:
			distance = pygame.math.Vector2(self.pos).distance_to(self.player_pos)
			if distance < 150:
				self.is_inrange = True
			else:
				self.is_inrange = False

	def talk(self, npc_data):
		pass

	def key_handler(self):
		keys = pygame.key.get_pressed()
		ans = None

		if keys[pygame.K_SPACE]:
			self.dialog.play(self.name, "idl")
			if cooldown("npc_begrüssung", 1):
				self.sound_manager.play_sfx("begrüssung")


		return ans

	def update(self):
		self.check_distance_to_player()

		if self.is_inrange:
			self.ans_keyhandler = self.key_handler()