#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import pygame


lightbrown = (185,122,85)
brown = (136,89,63)


# --- Menu Class --- #

class Menu(pygame.sprite.Sprite):
	def __init__(self, size):

		super().__init__()
		
		self.image = pygame.Surface(size).convert_alpha()
		self.rect = self.image.get_rect()
		

# --- Paused Class --- #

class Paused(Menu):
	def __init__(self, size):
		
		super().__init__(size)
		
		self.image.fill((0,)*4)
		pygame.draw.rect(self.image, lightbrown, self.rect, border_top_right_radius=30, border_bottom_right_radius=30)
		pygame.draw.rect(self.image, brown, self.rect, width=5, border_top_right_radius=30, border_bottom_right_radius=30)
		
	def update(self):
		pass