# Debug script from https://github.com/clear-code-projects

import pygame
import datetime

pygame.init()
font = pygame.font.Font(None,30)

def debug(info,y = 10, x = 10):
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'White')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(display_surface,'Black',debug_rect)
	display_surface.blit(debug_surf,debug_rect)

def debug_log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"debug_{timestamp}.txt"

    with open(filename, "a", encoding="utf-8") as file:
        file.write(str(message))
        file.write("\n")
        file.write("\n")