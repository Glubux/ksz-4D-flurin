import pygame
from settings import *
from support import *
from debug import *
from random import randint
import re

class Dialog(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.textures = self.load_grafics()

		self.status = False
		self.player = None
		self.dialog = None

		self.dialog_count = 0
		self.dialog_speed = 0.1
		self.dialog_words = ""

		self.font = pygame.font.SysFont("mongolianbaiti", 30)


	def load_grafics(self):
		textures = {
			"background": import_image("../textures/Premium Pack v1.0/Premium Pack v1.0/1 Green Book/1 Sprites/Paper UI Pack/Paper UI/Plain/7 Dialogue Box/1.png"),
		}
		return textures

	def key_handler(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RETURN]:
			if self.dialog_count+1 >= len(self.dialog_words):
				self.status = False

	def draw(self, dialog_words, dialog_count):
		pos = (300, HEIGHT - 550)
		scale = 1.5
		max_width = 656 * 2 - 40
		line_height = 30 * scale

		self.screen.blit(pygame.transform.scale(self.textures["background"], (656 * 2, 224 * 1.5)), pos)

		initial_x = pos[0] + 100 
		x, y = initial_x, pos[1] + 100

		for i in range(dialog_count + 1):
			text = dialog_words[i]
			text_surface = self.font.render(text, True, (0, 0, 0))
			text_surface = pygame.transform.scale(text_surface, (text_surface.get_width() * scale, text_surface.get_height() * scale))

			if x + text_surface.get_width() > pos[0] + max_width:
				x = initial_x
				y += line_height

			self.screen.blit(text_surface, (x, y))
			x += text_surface.get_width()
			
			if y + line_height > pos[1] + 224 * 1.5:
				break

	def play(self, name, dialog):
		if not self.status:
			self.status = True
			self.name = name
			self.dialog_count = 0
			self.dialog = npcs[self.name]["talk"][dialog][randint(0, len(npcs[self.name]["talk"][dialog])-1)]

			self.dialog_words = re.findall(r'\S+\s*', self.dialog["text"])

	def update(self):
		if self.status:
			if cooldown("dialog_speed", self.dialog_speed) and self.dialog_count+1 < len(self.dialog_words):
				self.dialog_count += 1
			
			self.draw(self.dialog_words, self.dialog_count)

		self.key_handler()
		return self.status