import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.groups = groups
        
        if "background" in sprite_type:
            self.type = "background"
        
        if "boundary" in sprite_type:
            self.boundary_type = sprite_type[2]
            if self.boundary_type == 0:
                # wasser
                for group in self.groups:
                    if isinstance(group, pygame.sprite.Group) and group == groups[0]:
                        group.remove(self)
                        
            if self.boundary_type == 12:
                # border
                pass
        
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)