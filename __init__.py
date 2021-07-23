#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import pygame
import characters, menus, sprites
from pygame.locals import *
pygame.init()


# --- Variables --- #

BLACK = (0,)*3
RED = (200,0,0)
WHITE = (255,)*3


# --- App Class --- #

class App(object):
	
	__version__ = "IU 0.2.1 Gamma: Minor updates (Jul 23 2021, 16:05 CST)"
	#"FU 0.2.0 Gamma: Added characters, sprites, and menus modules (Jul 23 2021, 11:50 CST)"
	#"FU 0.1.0 Gamma: Added window and basic internals (Jul 23 2021, 9:40 CST)"
	FPS = 60
	
	def __init__(self):

		pygame.register_quit(self.save)
		self.__clock = pygame.time.Clock()
		pygame.display.set_caption("Townlands: Remastered")
		pygame.display.set_icon(pygame.image.load("./Images/Icon.png"))
		self.__display = pygame.display.set_mode((1284,720), pygame.RESIZABLE)
		self.__font = pygame.font.SysFont("comicsansms", 20)
		
		self.__quit = False
		self.__paused = False
		self.__firstTime = True
		self.__day = 1
		self.__eventTime = 3
		self.__coins = 10
		self.__instructions_list = ["Click the Left/Right Arrow Keys to move", "Click the Down Arrow to upgrade buildings", "Click the F6 key to get extra help and to pause"]
		
		self.bg = pygame.sprite.GroupSingle()
		self.fg = pygame.sprite.Group()
		self.paused = pygame.sprite.Group()
		self.__instructions = pygame.sprite.GroupSingle()
		self.player = pygame.sprite.GroupSingle()
		
		# --- Background Additions --- #
		
		self.bg.add(sprites.Background())
		
		# --- Foreground Additions --- #
		
		self.fg.add(sprites.TownHall())
		
		# --- Paused Additions --- #
		
		self.paused.add(menus.Paused((self.__display.get_width()//3, self.__display.get_height())))
		
		# --- Instructions Additions ---- #
		
		self.__instructions.add(pygame.sprite.Sprite())
		self.__instructions.sprite.image =  self.__font_render(self.__instructions_list[0])
		self.__instructions.sprite.rect = self.__instructions.sprite.image.get_rect()
		
		# --- Character Additions --- #
		
		self.player.add(characters.Character())
		
		# --- Load Save --- #
		
		self.load()
		
	def load(self):
		
		self.__firstTime = False
		# with open("./Saves/Save1.sgf", "rb") as file:
			# file.read()
			
	def save(self):
		pass
		
		# with open("./Saves/Save1.sgf", "wb") as file:
			# file.write("\n".join((self.__firstTime,)))
			
	def __font_render(self, string):
		return self.__font.render(string, True, BLACK)
			
	def instruct(self):
		
		instructions = self.__instructions_list.copy()
		while len(instructions) > 0:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					instructions.pop(0)
					if len(instructions) > 0:
						self.__instructions.sprite.image = self.__font_render(instructions[0])
					else:
						self.__firstTime = False
						return
					
			self.draw()

	def events(self):
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.__quit = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.__paused = not self.__paused
				elif event.key == pygame.K_LEFT:
					self.player.sprite.change_direction('L')
					if event.mod in (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT, pygame.KMOD_SHIFT):
						self.player.sprite.rect.x -= 10
					self.player.sprite.rect.x -= 5
				elif event.key == pygame.K_RIGHT:
					self.player.sprite.change_direction('R')
					if event.mod in (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT, pygame.KMOD_SHIFT):
						self.player.sprite.rect.x += 10
					self.player.sprite.rect.x += 5
				elif event.key == pygame.K_DOWN:
					if (collision := pygame.sprite.spritecollide(self.player.sprite, self.fg, False)) != []: #Create variable 'collision', if 'collision 'is not equal to an empty list
						collision[-1].upgrade()
	
	def draw(self):
		
		self.__display.fill(BLACK)
		self.bg.draw(self.__display)
		self.fg.draw(self.__display)
		self.player.draw(self.__display)
		
		if self.__firstTime:
			self.__instructions.draw(self.__display)
		elif self.__paused:
			self.paused.draw(self.__display)
			
		pygame.display.flip()
			
	def __main__(self):
		
		if self.__firstTime:
			self.instruct()
		
		while not self.__quit:
			self.events()
			self.draw()
			self.__clock.tick(self.FPS)
			
		pygame.quit()
		
		
if __name__ == "__main__":
	App().__main__()
else:
	raise ImportError