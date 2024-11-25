import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()
		self.game_running = True

		self.level = Level()
	
	def run(self):
		while self.game_running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			game.key_handler()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

	def key_handler(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_ESCAPE]:
			self.game_running = False

if __name__ == '__main__':
	game = Game()
	game.run()