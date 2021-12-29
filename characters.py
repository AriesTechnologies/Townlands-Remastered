#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import pygame.transform as pg_transform
from local import LANDHEIGHT
from sprites import Sprite


# --- Character Class --- #

class Character(Sprite):
	def __init__(self):

		super().__init__("Explorer")

		self.rect.y =  LANDHEIGHT-self.rect.h
		self.__direction = 1

	@property
	def direction(self) -> str:
		return self.__direction

	@direction.setter
	def direction(self, direction : int) -> None:

		if direction != self.__direction:
			self.__direction = direction
			self.image = pg_transform.flip(self.image, True, False)
