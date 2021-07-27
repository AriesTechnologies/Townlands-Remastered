#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import pygame
import sprites


# --- Definitions --- #

LIGHTBROWN = (185,122,85)
BROWN = (136,89,63)

FONT = pygame.font.SysFont("comicsansms", 20)


# --- Menu Class --- #

class Menu(pygame.sprite.Group):
	def __init__(self, size : tuple):

		super().__init__()
		
	def add_button(self,size : tuple, text : str) -> None:
		
		self.add(Button(size, text))
		self.sprites()[-1].rect.y = self.sprites()[-1].rect.h*(len(self.sprites())-1)


# --- Button Class --- #

class Button(pygame.sprite.Sprite):
	def __init__(self, size, text):

		super().__init__()
		
		self.image = pygame.Surface(size).convert_alpha()
		self.rect = self.image.get_rect()

		self.update(text)
		
	def update(self, text):
		
		self.text = text
		# pygame.draw.rect(self.image, LIGHTBROWN, self.rect, border_top_right_radius=30, border_bottom_right_radius=30)
		# pygame.draw.rect(self.image, BROWN, self.rect, width=5, border_top_right_radius=30, border_bottom_right_radius=30)
		
		self.image.fill((0,)*4)
		pygame.draw.rect(self.image, BROWN, self.rect, width=5, border_radius=10)
		font = FONT.render(self.text, True, BROWN)
		self.image.blit(font, (self.rect.w//2-font.get_width()//2, self.rect.h//2-font.get_height()//2))
		

# --- Paused Class --- #

class Paused(sprites.Sprite):
	def __init__(self, size : tuple):
		
		super().__init__(size)
		
		self.image = self.image.convert_alpha()
		self.image.fill((0,)*4)
		pygame.draw.rect(self.image, LIGHTBROWN, self.rect, border_top_right_radius=30, border_bottom_right_radius=30)
		pygame.draw.rect(self.image, BROWN, self.rect, width=5, border_top_right_radius=30, border_bottom_right_radius=30)
		
	# def update(self) -> None:
		# pass