#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import pygame
from sprites import IMAGE_PATH


# --- Character Class --- #

class Character(pygame.sprite.Sprite):
	def __init__(self):
	
		super().__init__()
		
		self.image = pygame.image.load(f"{IMAGE_PATH}/Prince/Prince.png")
		self.rect.topleft = 0,0
	