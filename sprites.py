#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import pygame.draw
import pygame.image
import pygame.sprite
import local


# --- Sprite Class --- #

class Sprite(pygame.sprite.Sprite):
	def __init__(self, path : str = "", x=0):

		super().__init__()
		self.update(path)
		self.rect.x = x

	def flip(self):
		self.image = pygame.transform.flip(self.image, True, False)

	def update(self, path : str | tuple | list | pygame.Surface = "") -> None:

		if isinstance(path, str):
			self.image = pygame.image.load(f"{local.IMAGE_PATH}/{path}.png").convert_alpha()
		elif isinstance(path, pygame.Surface):
			self.image = path
		else: #path = size
			self.image = pygame.Surface(path).convert_alpha()
		self.rect = self.image.get_rect()


# --- Planet Class --- #

class Planet(Sprite):
	def __init__(self, type=0):

		if type == 0:
			super().__init__((200,)*2)
			self.image.fill((0,)*4)
			pygame.draw.circle(self.image, local.YELLOW, (self.rect.w//2,)*2, self.rect.w//2)
		elif type == 1:
			super().__init__("Moon/Moon")
		else:
			super().__init__("Moon/RedMoon")

		self.rect.topleft = local.DISPLAYW-self.rect.w,0


# --- Flag Class --- #

class Flag(Sprite):
	def __init__(self, banner : pygame.Surface | pygame.sprite.Sprite, offsetx=0):

		super().__init__((225,550))

		self.OFFSETX = offsetx
		self.rect.topleft = (offsetx, local.LANDHEIGHT-self.rect.h)

		self.image.fill((0,)*4)
		pygame.draw.rect(self.image, local.BROWN, (10,0,10,self.rect.h))
		pygame.draw.circle(self.image, local.GOLD, (15,10), 10)
		if isinstance(banner, pygame.Surface):
			self.image.blit(pygame.transform.rotate(banner.copy(), 90), (20,0))
		else:
			self.image.blit(pygame.transform.rotate(banner.image.copy(), 90), (20,0))


# --- Shop Class --- #

class Shop(Sprite):
	def __init__(self, offsetx=0):

		super().__init__("Shop/1")

		self.OFFSETX = offsetx
		self.rect.topleft = (0, local.LANDHEIGHT-self.rect.h)

		self._health = -1


# --- Bound Class --- #

class Bound(pygame.sprite.Sprite):
	def __init__(self, x):

		super().__init__()

		self.image = pygame.Surface((3,local.DISPLAYH))
		self.image.fill(local.RED)
		self.rect = self.image.get_rect()
		self.rect.x = x

	def setX(self, x):
		self.rect.x = x
