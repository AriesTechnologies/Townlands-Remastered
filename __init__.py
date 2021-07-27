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
	
	__version__ = "IU 0.3.1 Gamma: Added key repeating, started adding Pause Menu, added top messages (Jul 26 2021, 11:08 CST)"
	#"IU 0.2.1 Gamma: Minor updates (Jul 23 2021, 16:05 CST)"
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
		# self.__isTitleMenu = True
		self.__isPaused = False
		self.__firstTime = True
		self.__day = 1
		self.__eventTime = 3 #Easy: 5, Medium: 3, Hard: 2, Master: 1, Hell: 0
		self.__coins = 10
		self.__instructions_list = ["Click the Left/Right Arrow Keys to move", "Click the Down Arrow to upgrade buildings", "Click the Esc Key to get extra help and to pause"]
		
		self.bg = pygame.sprite.GroupSingle()
		self.fg = pygame.sprite.Group()
		self.paused = menus.Menu((self.__display.get_width()//3, self.__display.get_height()))
		self.__instructions = pygame.sprite.GroupSingle()
		
		self.player = pygame.sprite.GroupSingle()
		
		# --- Background Additions --- #
		
		self.bg.add(sprites.Background())
		
		# --- Foreground Additions --- #
		
		self.fg.add(sprites.TownHall())
		
		# --- Paused Additions --- #
		
		self.paused.add(menus.Paused((self.__display.get_width()//3, self.__display.get_height())))
		self.paused.add_button((self.__display.get_width()//3, self.__display.get_height()//6), "Continue")
		self.paused.add_button((self.__display.get_width()//3, self.__display.get_height()//6), "Options")
		self.paused.add_button((self.__display.get_width()//3, self.__display.get_height()//6), "Save")
		self.paused.add_button((self.__display.get_width()//3, self.__display.get_height()//6), "Quit")
		# self.paused.add(menus.Button((self.__display.get_width()//3, self.__display.get_height()), "New Game"))
		# self.paused.add(menus.Button((self.__display.get_width()//3, self.__display.get_height()), "Credits"))
		
		# --- Instructions Additions ---- #
		
		self.__instructions.add(pygame.sprite.Sprite())
		self.__instructions.sprite.image =  self.__font_render(self.__instructions_list[0])
		self.__instructions.sprite.rect = self.__instructions.sprite.image.get_rect()
		
		# --- Character Additions --- #
		
		self.player.add(characters.Character())
		
		# --- Load Save --- #
		
		self.load()
		
	def load(self) -> None:
		
		self.__firstTime = False
		# with open("./Saves/Save1.sgf", "rb") as file:
			# file.read()
			
	def save(self) -> None:
		pass
		# with open("./Saves/Save1.sgf", "wb") as file:
			# file.write("\n".join((self.__firstTime,)))
			
	def __font_render(self, string : str) -> pygame.Surface:
		return self.__font.render(string, True, BLACK)
			
	def instruct(self) -> None:
		
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

	def events(self) -> None:
		
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			self.__quit = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.__isPaused = not self.__isPaused
			# elif event.key == pygame.K_UP:
				# self.player.sprite.rect.y -= 50
			elif event.key == pygame.K_DOWN:
				if not self.__isPaused:
					if (collision := pygame.sprite.spritecollide(self.player.sprite, self.fg, False)) != []: #Create variable 'collision', if 'collision 'is not equal to an empty list
						self.__coins = collision[-1].upgrade(self.__coins)
					
			while event.type == pygame.KEYDOWN and not self.__isPaused:
				if event.key == pygame.K_LEFT:
					self.player.sprite.change_direction('L')
					if event.mod in (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT, pygame.KMOD_SHIFT):
						self.player.sprite.rect.x -= 5
					self.player.sprite.rect.x -= 3
				elif event.key == pygame.K_RIGHT:
					self.player.sprite.change_direction('R')
					if event.mod in (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT, pygame.KMOD_SHIFT):
						self.player.sprite.rect.x += 5
					self.player.sprite.rect.x += 3
					
				for event in pygame.event.get():
					if event.type == pygame.KEYUP:
						break
						
				self.draw()
					
	def draw(self) -> None:
		
		self.__display.fill(BLACK)
		self.bg.draw(self.__display)
		self.fg.draw(self.__display)
		self.player.draw(self.__display)
		
		if self.__firstTime:
			self.__instructions.draw(self.__display)
		else:
			font = self.__font_render(f"Days: {self.__day}  Coins: {self.__coins}")
			self.__display.blit(font, (self.__display.get_width()//2-font.get_width()//2, 0))
		if self.__isPaused:
			self.paused.draw(self.__display)
			
		pygame.display.flip()
			
	def __main__(self) -> None:
		
		if self.__firstTime:
			self.instruct()
		
		while not self.__quit:
			self.events()
			self.draw()
			# print(round(self.__clock.get_fps(), 0))
			self.__clock.tick(self.FPS)
			
		pygame.quit()
		
		
if __name__ == "__main__":
	App().__main__()
else:
	raise ImportError