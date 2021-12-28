#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import os, pygame, sys
import local
pygame.init()


# --- Variables --- #

IMAGE_PATH = f"{sys.path[0]}/Images"


# --- Sprite Class --- #

class Sprite(pygame.sprite.Sprite):
	def __init__(self, path : str = ""):

		super().__init__()
		self.update(path)

	def update(self, path : str | tuple | list | pygame.Surface = "") -> None:

		if isinstance(path, str):
			self.image = pygame.image.load(f"{IMAGE_PATH}/{path}.png").convert_alpha()
		elif isinstance(path, pygame.Surface):
			self.image = path
		else: #path = size
			self.image = pygame.Surface(path).convert_alpha()
		self.rect = self.image.get_rect()


# --- Background Class --- #

class Background(Sprite):
	def __init__(self):

		super().__init__("World")


# --- Flag Class --- #

class Flag(Sprite):
	def __init__(self, banner : pygame.Surface | pygame.sprite.Sprite):

		super().__init__((225,550))

		self.image.fill((0,)*4)
		pygame.draw.rect(self.image, local.BROWN, (10,0,10,self.rect.h))
		pygame.draw.circle(self.image, local.GOLD, (15,10), 10)
		if isinstance(banner, pygame.Surface):
			self.image.blit(pygame.transform.rotate(banner.copy(), 90), (20,0))
		else:
			self.image.blit(pygame.transform.rotate(banner.image.copy(), 90), (20,0))
