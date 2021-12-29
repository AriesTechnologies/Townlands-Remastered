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
	def __init__(self, path : str = ""):

		super().__init__()
		self.update(path)

	def update(self, path : str | tuple | list | pygame.Surface = "") -> None:

		if isinstance(path, str):
			self.image = pygame.image.load(f"{local.IMAGE_PATH}/{path}.png").convert_alpha()
		elif isinstance(path, pygame.Surface):
			self.image = path
		else: #path = size
			self.image = pygame.Surface(path).convert_alpha()
		self.rect = self.image.get_rect()


# --- Background Class --- #

class Background(Sprite):
	def __init__(self, type=0):

		super().__init__((local.DISPLAYW, 138))

		self.type = type
		self.rect.y = local.LANDHEIGHT

	@property
	def type(self):
		return self.__type

	@type.setter
	def type(self, type):

		self.__type = type
		if self.__type == 0:
			colors = iter((local.BLUE, local.LIGHTBROWN, local.GREEN))
		else:
			colors = iter((local.DARKBLUE, local.DARKBROWN, local.DARKGREEN))

		self.image.fill(next(colors))
		pygame.draw.rect(self.image, next(colors), (0,0,self.rect.w,69))
		pygame.draw.rect(self.image, next(colors), (0,0,self.rect.w,16))


# --- Planet Class --- #

class Planet(Sprite):
	def __init__(self, type=0):

		self.__type = type

		if self.__type == 0:
			super().__init__((200,)*2)
			self.image.fill((0,)*4)
			pygame.draw.circle(self.image, local.YELLOW, (self.rect.w//2,)*2, self.rect.w//2)
		elif self.__type == 1:
			super().__init__("Moon/Moon")
		else:
			super().__init__("Moon/RedMoon")

		self.rect.topleft = local.DISPLAYW-self.rect.w,0

	@property
	def type(self):
		return self.__type

	@type.setter
	def type(self, type):
		self.__type = type
		self = self.__init__(self.__type)


# --- Flag Class --- #

class Flag(Sprite):
	def __init__(self, banner : pygame.Surface | pygame.sprite.Sprite):

		super().__init__((225,550))

		self.rect.topleft = (30, local.LANDHEIGHT-self.rect.h)

		self.image.fill((0,)*4)
		pygame.draw.rect(self.image, local.BROWN, (10,0,10,self.rect.h))
		pygame.draw.circle(self.image, local.GOLD, (15,10), 10)
		if isinstance(banner, pygame.Surface):
			self.image.blit(pygame.transform.rotate(banner.copy(), 90), (20,0))
		else:
			self.image.blit(pygame.transform.rotate(banner.image.copy(), 90), (20,0))


# --- Shop Class --- #

class Shop(Sprite):
	def __init__(self):

		super().__init__("Shop/1")

		self.rect.topleft = (0, local.LANDHEIGHT-self.rect.h)
