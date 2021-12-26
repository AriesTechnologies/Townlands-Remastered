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

SHIFTS = (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT, pygame.KMOD_SHIFT)
RUN_MOVEMENT = 8
MOVEMENT = 5


# --- App Class --- #

class App(object):

	__app__ = "Townlands: Remastered"

	__version__ = "FU 0.4.0 Gamma: New menu internals, improved lag (forgot to convert images), fixed bug with instructions (Dec 25 2021, 23:02 CST)"
	# __version__ = "IU 0.3.5 Gamma: Cleaned up, improved lag in game (Aug 25 2021, 22:00 CST)"
	#"IU 0.3.4 Gamma: Added Pause Menu, Title Menu button functions (Aug 4 2021, 9:47 CST)"
	#"IU 0.3.3 Gamma: Updates to buttons (Jul 27 2021, 13:43 CST)"
	#"IU 0.3.2 Gamma: Started adding title menu (Jul 27 2021, 11:37 CST)"
	#"IU 0.3.1 Gamma: Added key repeating, started adding Pause Menu, added top messages (Jul 26 2021, 11:08 CST)"
	#"IU 0.2.1 Gamma: Minor updates (Jul 23 2021, 16:05 CST)"
	#"FU 0.2.0 Gamma: Added characters, sprites, and menus modules (Jul 23 2021, 11:50 CST)"
	#"FU 0.1.0 Gamma: Added window and basic internals (Jul 23 2021, 9:40 CST)"
	FPS = 60

	def __init__(self):

		pygame.register_quit(self.save)
		self.__clock = pygame.time.Clock()
		pygame.display.set_caption(App.__app__)
		pygame.display.set_icon(pygame.image.load(f"{sprites.IMAGE_PATH}/Icon.png"))
		self.__display = pygame.display.set_mode((1280,720), pygame.FULLSCREEN | pygame.DOUBLEBUF)
		self.__font = pygame.font.SysFont("comicsansms", 20)

		self.__quit = False
		self.__debug = True
		self.__inGame = False
		self.__isPaused = False
		self.__firstTime = True

		self.__path = []
		self.__day = 1
		self.__eventTime = 3 #Easy: 5, Medium: 3, Hard: 2, Master: 1, Hell: 0
		self.__coins = 10
		self.__instructions_list = ["Click the Left/Right Arrow Keys to move", "Click the Down Arrow to upgrade buildings", "Click the Esc Key to get extra help and to pause"]

		self.titleMenu = menus.Menu((self.__display.get_width()//3, self.__display.get_height()))
		self.bg = pygame.sprite.Group(sprites.Background())
		self.fg = pygame.sprite.Group()
		self.paused = menus.Menu((self.__display.get_width()//3, self.__display.get_height()))
		self.options = menus.Menu(self.__display.get_size())
		self.controls = menus.Menu(self.__display.get_size())
		self.__instructions = pygame.sprite.GroupSingle()

		self.player =  pygame.sprite.GroupSingle(characters.Character())

		# --- Title Menu Additions --- #

		self.titleMenu.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Play")
		self.titleMenu.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "New Game")
		self.titleMenu.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Options")
		self.titleMenu.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Quit")

		self.titleMenu.center_buttons(self.__display.get_size(), 3)

		# --- Background Additions --- #
		# --- Foreground Additions --- #

		self.fg.add(sprites.TownHall())

		# --- Paused Additions --- #

		self.paused.add(menus.Paused((self.__display.get_width()//4, self.__display.get_height())))
		self.paused.add_button((self.paused.sprites()[0].rect.w//1.25, self.__display.get_height()//6), "Continue")
		self.paused.add_button((self.paused.sprites()[0].rect.w//1.25, self.__display.get_height()//6), "Options")
		self.paused.add_button((self.paused.sprites()[0].rect.w//1.25, self.__display.get_height()//6), "Save")
		self.paused.add_button((self.paused.sprites()[0].rect.w//1.25, self.__display.get_height()//6), "Quit")

		self.paused.center_buttons(self.paused.sprites()[0].rect.size)

		# --- Options Additions --- #

		self.options.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Controls")
		self.options.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Brightness")
		self.options.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Dyslexic")
		self.options.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Credits")

		self.options.center_buttons(self.__display.get_size(), 2)

		# --- Controls Additions --- #

		self.controls.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Left: Left Arrow")
		self.controls.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Right : Right Arrow")
		self.controls.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Run: Shift+Arrow Key")
		self.controls.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Upgrade: Down Arrow")
		self.controls.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Pause: Escape")
		self.controls.add_button((self.__display.get_width()//4, self.__display.get_height()//8), "Back: Backspace or Left Arrow")

		self.controls.center_buttons(self.__display.get_size(), 1)

		# --- Instructions Additions ---- #

		self.__instructions.add(pygame.sprite.Sprite())
		self.__instructions.sprite.image =  self.__font_render(self.__instructions_list[0])
		self.__instructions.sprite.rect = self.__instructions.sprite.image.get_rect()

		# --- Add Path --- #

		self.__path.append(self.titleMenu)

		# --- Load Save --- #

		self.load()

	def load(self) -> None:
		pass
		# self.__firstTime = False
		# with open("./Saves/Save1.sgf", "rb") as file:
			# file.read()

	def save(self) -> None:
		pass
		# with open("./Saves/Save1.sgf", "wb") as file:
			# file.write("\n".join((self.__firstTime,)))

	def __font_render(self, string : str) -> pygame.Surface:
		return self.__font.render(string, True, BLACK)

	def instruct(self) -> None:

		pygame.event.clear()
		instructions = self.__instructions_list.copy()
		while len(instructions) > 0:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				elif event.type == pygame.KEYDOWN:
					instructions.pop(0)
					if len(instructions) > 0:
						self.__instructions.sprite.image = self.__font_render(instructions[0])
					else:
						self.__firstTime = False
						pygame.key.set_repeat(App.FPS*2, App.FPS//2)
						return

			self.draw()

	def clickEvents(self, event):

		if not self.__inGame: #Title Menu
			if self.titleMenu.sprites()[0].rect.collidepoint(event.pos):
				self.__inGame = True
				self.__path.clear()
			elif self.titleMenu.sprites()[1].rect.collidepoint(event.pos):
				pass
			elif self.titleMenu.sprites()[2].rect.collidepoint(event.pos):
				self.__path.append(self.options)
			elif self.titleMenu.sprites()[3].rect.collidepoint(event.pos):
				self.__quit = True
				self.__path.clear()

		elif self.__isPaused: #Pause Menu
			if self.paused.sprites()[1].rect.collidepoint(event.pos): #Continue
				pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"mod": 0, "key": pygame.K_ESCAPE}))
			elif self.paused.sprites()[2].rect.collidepoint(event.pos): #Options
				self.__path.append(self.options)
			elif self.paused.sprites()[3].rect.collidepoint(event.pos): #Save
				self.save()
			elif self.paused.sprites()[4].rect.collidepoint(event.pos): #Save+Quit
				self.__quit = True
				self.__path.clear()

		if len(self.__path) > 0: #Both
			if self.__path[-1] == self.options:
				if self.options._buttons[0].rect.collidepoint(event.pos): #Controls
					self.__path.append(self.controls)

	def keyEvents(self, event):

		if event.mod == pygame.KMOD_LCTRL:
			if event.key == pygame.K_q:
				self.__quit = True
				self.__path.clear()
		elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_LEFT:
			if len(self.__path) > 1:
				del self.__path[-1]

		if not self.__inGame: #In Title
			if event.key == pygame.K_RETURN:
				self.__inGame = True
		elif self.__isPaused: #In Pause Menu
			if event.key == pygame.K_ESCAPE:
				self.__path.clear()
				self.__isPaused = False
		elif self.__firstTime:
			self.instruct()
		else: #In Game
			if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
				if event.key == pygame.K_LEFT:
					self.player.sprite.change_direction(-1)
				elif event.key == pygame.K_RIGHT:
					self.player.sprite.change_direction(1)

				if event.mod in SHIFTS:
					x = RUN_MOVEMENT*self.player.sprite.direction
				else:
					x = MOVEMENT*self.player.sprite.direction
				self.player.sprite.rect.x += x
			# elif event.key == pygame.K_UP:
				# self.player.sprite.rect.y -= 50
			elif event.key == pygame.K_ESCAPE:
				self.__path.append(self.paused)
				self.__isPaused = True
			elif event.key == pygame.K_DOWN:
				if (collision := pygame.sprite.spritecollide(self.player.sprite, self.bg, False)) != []: #Create variable 'collision', if 'collision 'is not equal to an empty list
					self.__coins = collision[-1].upgrade(self.__coins)
			elif event.key == pygame.K_c:
				self.__coins += 1


	def events(self) -> None:

		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			self.__quit = True
			self.__path.clear()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.clickEvents(event)
		elif event.type == pygame.KEYDOWN:
			self.keyEvents(event)

	def draw(self) -> None:

		self.bg.draw(self.__display)
		if self.__inGame:
			self.fg.draw(self.__display)
			self.player.draw(self.__display)

			if self.__firstTime:
				self.__instructions.draw(self.__display)
			else:
				font = self.__font_render(f"Days: {self.__day}  Coins: {self.__coins}")
				self.__display.blit(font, (self.__display.get_width()//2-font.get_width()//2, 0))

				if self.__isPaused:
					self.paused.draw(self.__display)
		else:
			font = self.__font_render(App.__app__)
			self.__display.blit(font, (self.__display.get_width()//2-font.get_width()//2, 0))

		if len(self.__path) > 0:
			self.__path[-1].draw(self.__display)

		if self.__debug:
			font = self.__font_render("FPS: {}".format(round(self.__clock.get_fps())))
			self.__display.blit(font, (self.__display.get_width()-font.get_width(), 0))

		pygame.display.flip()

	def __main__(self) -> None:

		while not self.__quit:
			self.events()
			self.draw()
			# print(round(self.__clock.get_fps()))
			self.__clock.tick(self.FPS)

		pygame.quit()


if __name__ == "__main__":
	App().__main__()
else:
	raise ImportError()
