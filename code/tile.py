import pygame
from settings import *
from random import *
from debug import *

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

class Plants(pygame.sprite.Sprite):
    def __init__(self, pos, groups, data):
        super().__init__(groups)
        self.pos = pos
        self.data = data

        self.grow_count = 0
        self.grow_level = 0

        self.style = data["style"]
        self.col = data["col"]
        self.pos = data["pos"]

        self.season = "spring"
        self.season_set = False

        self.rand_type = randint(0, len(plant_list[self.season])-1)

        self.image = plant_list[self.season][self.rand_type]["texture"]["planted"][self.grow_count]

        self.rect = self.image.get_rect(topleft=self.pos)
        self.rect.y -= 25

    def grow_update(self, season):
        self.current_season = season      

        if self.current_season != self.season:
            self.image = plant_list["rotten"]
            self.rect = self.image.get_rect(topleft=self.pos)
            self.rect.y -= 0

        else:
            if plant_list[self.season][self.rand_type]["grow_stats"]-1 > self.grow_count:
                self.grow_count += 1
            self.image = plant_list[self.season][self.rand_type]["texture"]["planted"][self.grow_count]
            self.rect = self.image.get_rect(topleft=self.pos)
            self.rect.y -= 25

    def update(self):
        pass