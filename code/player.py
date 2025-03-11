import pygame 
from settings import *
from debug import *
from support import *
from audio import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites,skin_name):
		super().__init__(groups)
		self.skin_name = skin_name
		self.image = pygame.image.load('../textures/character and portrait/Character/Pre-made/'+self.skin_name+'/Idle.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-70,-50)

		self.sound_manager = SoundManager()
		self.acceleration = pygame.math.Vector2()
		self.direction = pygame.math.Vector2()
		self.player_direction = "down"
		self.player_action = "idle"

		self.normal_speed = 4
		self.sprint_speed = 6
		self.speed = self.normal_speed
		self.obstacle_sprites = obstacle_sprites

		self.animations_surface = self.load_textures()
		self.animations_frame = 0
		self.animations_speed = 0.2

		self.is_attacking = False 
		self.attacking_frame = 0
		self.attacking_radius = 5 * TILESIZE

		# sounds
		self.sound_manager.load_sfx("walk", "walk.mp3")
		self.sound_manager.load_sfx("run", "run.mp3")

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)



	def load_textures(self):
		textures = {
			"walk": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Walk.png", [6,4]),
			"run": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Run.png", [8,4]),
			"idl": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Idle.png", [4,4]),
			"damage": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Damage.png", [4,4]),
			"dead": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Dead.png", [4,4]),
			"axe": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Axe.png", [6,4]),
			"bow": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Bow and Arrow.png", [7,4]),
			"sword": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Sword.png", [10,4]),
			"shovel": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Shovel.png", [5,4]),
			"pickaxe": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Pickaxe.png", [6,4]),
			"sickle": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Sickle.png", [6,4]),
			"hoe": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Hoe.png", [6,4]),
			"watering": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Watering.png", [6,4]),
			"sitting": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Sitting.png", [3,1]),
			"sleep": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Sleep.png", [2,1]),
			"climbing": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Climbing.png", [5,1]),
			"petting": import_tileset("character", "../textures/character and portrait/Character/Pre-made/"+self.skin_name+"/Petting.png", [4,1]),
		}
		return textures
	
	def input(self):
		keys = pygame.key.get_pressed()
		mouse_x, mouse_y = pygame.mouse.get_pos()
		max_acceleration = self.speed*5

		if self.direction == [0,0]:
			self.player_action = "idl"

		if not self.is_attacking:
			if keys[pygame.K_UP] or keys[pygame.K_w]:
				self.player_direction = "up"
				self.player_action = "walk"
				self.direction.y = -1
				
				if self.acceleration.y < max_acceleration:
					self.acceleration.y += 1

			elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
				self.player_direction = "down"
				self.player_action = "walk"
				self.direction.y = 1

				if self.acceleration.y > -max_acceleration:
					self.acceleration.y -= 1
			else:
				self.direction.y = 0

				if self.acceleration.y < 0:
					self.acceleration.y += 1
				if self.acceleration.y > 0:
					self.acceleration.y -= 1

			if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
				self.player_direction = "right"
				self.player_action = "walk"
				self.direction.x = 1

				if self.acceleration.x > -max_acceleration:
					self.acceleration.x -= 1

			elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
				self.player_direction = "left"
				self.player_action = "walk"
				self.direction.x = -1

				if self.acceleration.x < max_acceleration:
					self.acceleration.x += 1
			else:
				self.direction.x = 0

				if self.acceleration.x < 0:
					self.acceleration.x += 1
				if self.acceleration.x > 0:
					self.acceleration.x -= 1

			if keys[pygame.K_LSHIFT]:
				if self.direction != [0,0]:	
					self.player_action = "run"

				if self.speed < self.sprint_speed:
					self.speed += 1
			else:
				self.speed = self.normal_speed
		
		if keys[pygame.K_f] or self.is_attacking:
			self.is_attacking = True
			self.player_action = "sword"

		if keys[pygame.K_g]:
			dx = mouse_x - self.rect.x
			dy = mouse_y - self.rect.y
			distance = (dx**2 + dy**2) ** 0.5

			if distance <= self.attacking_radius:
				debug("Selected", 600, 20)
			

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		if not self.is_attacking:
			self.hitbox.x += self.direction.x * speed
			self.collision('horizontal')
			self.hitbox.y += self.direction.y * speed
			self.collision('vertical')

		self.rect.center = self.hitbox.center
		

	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom


	def draw(self):
		if self.is_attacking:
			self.image = self.animations_surface[self.player_action][self.player_direction][self.attacking_frame%len(self.animations_surface[self.player_action][self.player_direction])]
			self.rect = self.image.get_rect()

			if cooldown("player_animation", self.animations_speed/2):
				self.attacking_frame += 1
				if self.attacking_frame == len(self.animations_surface[self.player_action][self.player_direction]):
					self.is_attacking = False
					self.attacking_frame = 0

		else:
			self.image = self.animations_surface[self.player_action][self.player_direction][self.animations_frame%len(self.animations_surface[self.player_action][self.player_direction])]
			self.rect = self.image.get_rect()
			if cooldown("player_animation", self.animations_speed):
				self.animations_frame += 1

	def update(self):
		self.input()
		self.draw()
		self.move(self.speed)

		if self.player_action == "walk":
			if cooldown("sound_walk", 0.4):
				self.sound_manager.set_sfx_volume(0.3)
				self.sound_manager.play_sfx(self.player_action)
		if self.player_action == "run":
			if cooldown("sound_run", 0.3):
				self.sound_manager.set_sfx_volume(0.3)
				self.sound_manager.play_sfx(self.player_action)


		mouse_x, mouse_y = pygame.mouse.get_pos()
		dx = mouse_x - self.rect.x
		dy = mouse_y - self.rect.y
		distance = (dx**2 + dy**2) ** 0.5

		if distance <= self.attacking_radius:
			grid_x = (mouse_x // TILESIZE) * TILESIZE
			grid_y = (mouse_y // TILESIZE) * TILESIZE
			pygame.draw.rect(self.screen, (255,0,0), (grid_x, grid_y, TILESIZE, TILESIZE), 3)

