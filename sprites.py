#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import os, pygame


# --- Variables --- #

IMAGE_PATH = "./Images"


# --- Sprite Class --- #

class Sprite(pygame.sprite.Sprite):
	def __init__(self, path):
		
		super().__init__()
		self.update(path)
		
	def update(self, path):
		
		self.image = pygame.image.load(f"{IMAGE_PATH}/{path}.png")
		self.rect = self.image.get_rect()


# --- Background Class --- #

class Background(Sprite):
	def __init__(self):
		
		super().__init__("World")


# --- Upgradeable Class --- #

class Upgradeable(Sprite):
	def __init__(self, name, level=1):
		super().__init__(f"{name}/{level}")
		
		self.__name = name
		self.__level = level
		self.max_level = len(os.listdir(f"{IMAGE_PATH}/{self.__name}"))
		
	@property
	def level(self):
		return self.__level
		
	def upgrade(self):
		
		if self.__level < self.max_level:
			self.__level += 1
			self.update(f"{self.__name}/{self.__level}")


# --- Town Hall Class --- #

class TownHall(Upgradeable):
	def __init__(self, level=1):
		
		super().__init__("TownHall", level)
		