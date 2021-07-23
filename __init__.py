#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import pygame
import sprites, characters
from pygame.locals import *

pygame.init()


# --- App Class --- #

class App(object):
	
	__version__ = "FU 0.1.0 Gamma: Added window and basic internals (Jul 23 2021, 9:40 CST)"
	FPS = 60
	
	def __init__(self):

		pygame.register_quit(self.save)
		self.__clock = pygame.time.Clock()
		pygame.display.set_caption("Townlands: Remastered")
		pygame.display.set_icon(pygame.image.load("./Images/Icon.png"))
		self.__display = pygame.display.set_mode((1284,720), pygame.RESIZABLE)
		
		self.__quit = False
		self.__paused = False
		self.bg = pygame.sprite.GroupSingle()
		self.fg = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		
		self.bg.add(sprites.Background())
		self.fg.add(sprites.TownHall())
		
	def load(self):
		pass
		# with open("./Saves/Save1.sgf", "rb") as file:
			# file.read()
			
	def save(self):
		pass
		# with open("./Saves/Save1.sgf", "wb") as file:
			# file.write("\n".join())
			
	def events(self):
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.__quit = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.__paused = True
				elif event.key == pygame.K_LEFT:
					if event.mod in (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT, pygame.KMOD_SHIFT):
						pass
					pass
				elif event.key == pygame.K_RIGHT:
					if event.mod in (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT, pygame.KMOD_SHIFT):
						pass
					pass
				elif event.key == pygame.K_DOWN:
					#Check collision
					self.fg.sprites()[-1].upgrade()
	
	def draw(self):
		
		self.bg.draw(self.__display)
		self.fg.draw(self.__display)
		pygame.display.flip()
			
	def __main__(self):
		
		while not self.__quit:
			self.events()
			self.draw()
			self.__clock.tick(self.FPS)
			
		pygame.quit()
		
		
if __name__ == "__main__":
	App().__main__()
else:
	raise ImportError