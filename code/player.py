import pygame 
from settings import *
from debug import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('./textures/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)

		self.direction = pygame.math.Vector2()

		self.normal_speed = 5
		self.sprint_speed = 8
		self.speed = self.normal_speed

		self.obstacle_sprites = obstacle_sprites

		self.acceleration = pygame.math.Vector2()

	def input(self):
		keys = pygame.key.get_pressed()
		max_acceleration = self.speed*5

		if keys[pygame.K_UP] or keys[pygame.K_w]:
			self.direction.y = -1

			if self.acceleration.y < max_acceleration:
				self.acceleration.y += 1

		elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
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
			self.direction.x = 1

			if self.acceleration.x > -max_acceleration:
				self.acceleration.x -= 1

		elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
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

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

		debug(self.speed)
		

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

	def update(self):
		self.input()
		self.move(self.speed)