#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import os, pygame
pygame.init()


# --- Variables --- #

IMAGE_PATH = "./Images"


# --- Sprite Class --- #

class Sprite(pygame.sprite.Sprite):
	def __init__(self, path : str = ""):
		
		super().__init__()
		self.update(path)
		
	def update(self, path : str = "") -> None:
		
		if isinstance(path, str):
			self.image = pygame.image.load(f"{IMAGE_PATH}/{path}.png")
		else: #path = size
			self.image = pygame.Surface(path).convert_alpha()
		self.rect = self.image.get_rect()


# --- Background Class --- #

class Background(Sprite):
	def __init__(self):
		
		super().__init__("World")


# --- Upgradeable Class --- #

class Upgradeable(Sprite):
	def __init__(self, name : str, level=1):
		super().__init__(f"{name}/{level}")
		
		self.__name = name
		self.__level = level
		self.max_level = len(os.listdir(f"{IMAGE_PATH}/{self.__name}"))
		
	@property
	def level(self) -> int:
		return self.__level
		
	def upgrade(self) -> None:
		
		if self.__level < self.max_level:
			self.__level += 1
			self.update(f"{self.__name}/{self.__level}")


# --- Town Hall Class --- #

class TownHall(Upgradeable):
	def __init__(self, level=1):
		
		super().__init__("TownHall", level)
		