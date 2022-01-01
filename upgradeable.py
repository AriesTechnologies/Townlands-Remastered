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

		self.OFFSETX = sprites.local.DISPLAYW-self.rect.w
		self.rect.y = sprites.local.LANDHEIGHT-self.rect.h

	@property
	def level(self) -> int:
		return self.__level

	def resetLevel(self):
		self._heath = 0
		self.__level = 0
		self.upgrade(self._cost)

	def upgrade(self, coins : int) -> None:

		if self.__level < self.max_level and coins >= self._cost:
			self.__level += 1
			self._health += self._perUpgrade
			self.update(f"{self.__name}/{self.__level}")
			self.rect.x = sprites.local.DISPLAYW-self.rect.w
			self.rect.y = sprites.local.LANDHEIGHT-self.rect.h
			coins -= self._cost
		return coins


# --- Town Hall Class --- #

class TownHall(Upgradeable):
	def __init__(self, level=1, offsetx=3200):

		super().__init__("TownHall", level)

		self.OFFSETX = offsetx
		self._cost = 10
		self._perUpgrade = 50
		self._health = 150+(self._perUpgrade*(self.level-1))


# --- Wall Class --- #

class Wall(Upgradeable):
	def __init__(self, level=1, offsetx=0):

		super().__init__("Wall", level)

		self.OFFSETX = offsetx-self.rect.w//2
		self._cost = 3
		self._perUpgrade = 50
		self._health = 150+(self._perUpgrade*(self.level-1))


# --- ArcherTower Class --- #

class ArcherTower(Upgradeable):
	def __init__(self, level=1, offsetx=0):

		super().__init__("ArcherTower", level)

		self.OFFSETX = offsetx
		self._cost = 5
		self._perUpgrade = 50
		self._health = 75+(self._perUpgrade*(self.level-1))
		self.damage = 20


# --- Cannon Class --- #

class Cannon(Upgradeable):
	def __init__(self, level=1, offsetx=0):

		super().__init__("Cannon", level)

		self.OFFSETX = offsetx
		self._cost = 4
		self._perUpgrade = 25
		self._health = 75+(self._perUpgrade*(self.level-1))
		self.damage = 30


# --- Farm Class --- #

class Farm(Upgradeable):
	def __init__(self, level=1, offsetx=0):

		super().__init__("Farm", level)

		self.OFFSETX = offsetx
		self._cost = 5
		self._perUpgrade = 25
		self._health = 50+(self._perUpgrade*(self.level-1))


# --- Statue Class --- #

class Statue(Upgradeable):
	def __init__(self, level=1, offsetx=0):

		super().__init__("Statue", level)

		self.OFFSETX = offsetx-self.rect.w
		self._cost = 12
		self._perUpgrade = 0
		self._health = -1


# --- Portal Class --- #

class Portal(Upgradeable):
	def __init__(self, level=1, offsetx=0):

		super().__init__("Portal", level)

		self.OFFSETX = offsetx
		self._cost = 150
		self._perUpgrade = 0
		self._health = -1

	def upgrade(self, coins : int):

		if self.__level == self.max_level and coins >= self.__cost:
			self.__level = -1
			self.kill()
			coins -= self._cost
		return coins
