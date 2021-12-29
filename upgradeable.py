# --- Imports --- #

import os
import sprites


# --- Upgradeable Class --- #

class Upgradeable(sprites.Sprite):
	def __init__(self, name : str, level=1):
		super().__init__(f"{name}/{level}")

		self.__name = name
		self.__level = level
		self.max_level = len(os.listdir(f"{sprites.local.IMAGE_PATH}/{self.__name}"))

		self.rect.x = sprites.local.DISPLAYW-self.rect.w
		self.rect.y = sprites.local.LANDHEIGHT-self.rect.h

	@property
	def level(self) -> int:
		return self.__level

	def upgrade(self, coins : int) -> None:

		if self.__level < self.max_level and coins >= self._cost:
			self.__level += 1
			self.update(f"{self.__name}/{self.__level}")
			self.rect.x = sprites.local.DISPLAYW-self.rect.w
			self.rect.y = sprites.local.LANDHEIGHT-self.rect.h
			coins -= self._cost
		return coins


# --- Nature Class --- #

class Nature(Upgradeable):
	def __init__(self, name, level=1):

		super().__init__(name, level)

		self._cost = 1

	def upgrade(self, coins : int):

		if self.__level == self.max_level and coins >= self.__cost:
			self.__level = -1
			self.kill()
			coins -= self._cost
		return coins


# --- Town Hall Class --- #

class TownHall(Upgradeable):
	def __init__(self, level=1):

		super().__init__("TownHall", level)

		self._cost = 10


# --- Wall Class --- #

class Wall(Upgradeable):
	def __init__(self, level=1):

		super().__init__("Wall", level)

		self._cost = 3


# --- ArcherTower Class --- #

class ArcherTower(Upgradeable):
	def __init__(self, level=1):

		super().__init__("ArcherTower", level)

		self._cost = 5


# --- Cannon Class --- #

class Cannon(Upgradeable):
	def __init__(self, level=1):

		super().__init__("Cannon", level)

		self._cost = 4


# --- Farm Class --- #

class Farm(Upgradeable):
	def __init__(self, level=1):

		super().__init__("Farm", level)

		self._cost = 5


# --- Statue Class --- #

class Statue(Upgradeable):
	def __init__(self, level=1):

		super().__init__("Statue", level)

		self._cost = 12


# --- Portal Class --- #

class Portal(Upgradeable):
	def __init__(self, level=1):

		super().__init__("Portal", level)

		self._cost = 50
