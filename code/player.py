import pygame 
from settings import *
from debug import *
from support import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('../textures/skins/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-10,-26)

		self.direction = pygame.math.Vector2()
		self.player_direction = "down"
		self.idl_direction = "idl_down"
		self.skin_direction= ""

		self.normal_speed = 5
		self.sprint_speed = 8
		self.speed = self.normal_speed
		self.obstacle_sprites = obstacle_sprites
#02556
		self.acceleration = pygame.math.Vector2()


		self.animations_surface = self.import_animation()
		self.animations_frame = 0
		self.animations_speed = 0.2

		self.is_attacking = False
		self.attack_direction = None

	def import_animation(self):
		size = (32, 32)
		scale_faktor = 4
		self.img = import_image('../textures/skins/player/player.png')
		self.animation = [
			["idl_down", [1, 5]], ["idl_right", [2, 5]], ["idl_left", [3, 5]], ["idl_up", [4, 5]], 
			["walk_down", [5, 5]], ["walk_right", [6, 5]], ["walk_left", [7, 5]], ["walk_up", [8, 5]],
			["atk_down", [9, 4]], ["atk_up", [10, 4]], ["atk_left", [11, 4]], ["atk_right", [12, 4]]
		]

		animations = {}

		for animation in self.animation:
			animation_name, (row, frame_count) = animation
			frames = []

			for frame in range(frame_count):
				x = frame * size[0]
				y = (row - 1) * size[1]
				frame_surface = self.img.subsurface((x, y, size[0], size[1]))
				frame_surface = pygame.transform.scale(frame_surface, (size[0]*scale_faktor, size[1]*scale_faktor))
				if animation_name[-4:] == "left":
					frame_surface = pygame.transform.flip(frame_surface, True, False)

				frames.append(frame_surface)

			animations[animation_name] = frames

		return animations


	def input(self):
		keys = pygame.key.get_pressed()
		max_acceleration = self.speed*5

		if not self.is_attacking:
			if keys[pygame.K_UP] or keys[pygame.K_w]:
				self.player_direction = "up"
				self.direction.y = -1

				if self.acceleration.y < max_acceleration:
					self.acceleration.y += 1

			elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
				self.player_direction = "down"
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
				self.direction.x = 1

				if self.acceleration.x > -max_acceleration:
					self.acceleration.x -= 1

			elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
				self.player_direction = "left"
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
				if self.speed < self.sprint_speed:
					self.speed += 1
			else:
				self.speed = self.normal_speed

		debug("Playerdir: " + self.player_direction, 50,10)
		
		
		if keys[pygame.K_f]:
			self.attack_direction = "atk_" + self.player_direction
			debug(self.attack_direction, 70,10)
			self.is_attacking = True

		if keys[pygame.K_f] and keys[pygame.K_LSHIFT]:
			self.is_attacking = False
 
		if self.direction == [0,0]:
			self.skin_direction = "idl_" + self.player_direction
		else:
			self.skin_direction = "walk_" + self.player_direction

		debug(self.direction,30,10)

			

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
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def draw(self):
		self.image = self.animations_surface[self.skin_direction][self.animations_frame%len(self.animations_surface[self.skin_direction])]
		self.rect = self.image.get_rect()
		if cooldown("player_animation", self.animations_speed):
			self.animations_frame += 1

	def update(self):
		self.input()
		self.draw()
		self.move(self.speed)