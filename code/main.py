import pygame, sys
from settings import *
from level import Level
from debug import *
from support import *

class Game: 
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.clock = pygame.time.Clock()
		pygame.mouse.set_visible(True)

		self.game_running = True
		self.cursor_image = import_image("../textures/ui/cursor.png")
		self.cursor_pressed_image = import_image("../textures/ui/cursor_pressed.png")

		self.level = Level()
	def run(self):
		while self.game_running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			game.key_handler()
			self.cursor()

			self.screen.fill('black')
			self.level.run()
			debug(round(self.clock.get_fps()), 600, 10)

			pygame.display.update()
			self.clock.tick(FPS)
			#print(round(self.clock.get_fps()))

	def key_handler(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_DELETE]:
			self.game_running = False

	def cursor(self):
		self.mouse = pygame.mouse.get_pressed()

		if self.mouse[0]==True or self.mouse[2]==True:
			cursor_image = self.cursor_pressed_image
		else:
			cursor_image = self.cursor_image

		cursor = pygame.cursors.Cursor((0, 0),cursor_image)
		pygame.mouse.set_cursor(cursor)

if __name__ == '__main__':
	game = Game()
	game.run()