# --- Imports --- #

import os
from sprites import IMAGE_PATH, Sprite


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

	def upgrade(self, coins : int) -> None:

		if self.__level < self.max_level and coins >= self._cost:
			self.__level += 1
			self.update(f"{self.__name}/{self.__level}")
			coins -= self._cost
		return coins


# --- Town Hall Class --- #

class TownHall(Upgradeable):
	def __init__(self, level=1):

		super().__init__("TownHall", level)

		self._cost = 10

class Wall(Upgradeable):
	def __init__(self, level=1):

		super().__init__("Wall", level)

		self._cost = 3
