#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import pygame
import characters, menus, sprites, local, upgradeable
from pygame.locals import *


# --- Variables --- #

SHIFTS = (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT)
DAYNIGHTEVENT = pygame.event.Event(local.DAYNIGHT)


# --- App Class --- #

class App(object):

	__app__ = "Townlands: Remastered"
	__version__ = """IU 0.5.1 Gamma: Added day/night cycle,
									added gaining coins after every night,
									added all updated graphics (Dec 29 2021, 16:38)"""
	# """FU 0.5.0 Gamma: Added banner to Pause Menu,
	# 							added all menus (so far),
	# 							added audio menu (replaced brightness), added flag,
	# 							added upgradeable and local modules,
	# 							add some testing objects,
	# 							add save file loading and saving (automatically loads and saves),
	# 							improved instructions function,
	# 							 (Dec 27 2021, 19:04 CST)"""
	#"FU 0.4.0 Gamma: New menu internals, improved lag (forgot to convert images), fixed bug with instructions (Dec 25 2021, 23:02 CST)"
	#"IU 0.3.5 Gamma: Cleaned up, improved lag in game (Aug 25 2021, 22:00 CST)"
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
		pygame.display.set_icon(pygame.image.load(f"{local.IMAGE_PATH}/Icon.png"))
		self.__display = pygame.display.set_mode((1280,720), pygame.FULLSCREEN | pygame.DOUBLEBUF)
		self.__font = pygame.font.SysFont("comicsansms", 20)

		self.__path : list

		self.__quit = False
		self.__inGame = False
		self.__isPaused = False
		self.__settings = [True, True, False, True]
		self.__day = 1
		self.__difficulty = 3 #Beginner: 5, Easy: 4, Medium: 3, Hard: 2, Master: 1, Hell: 0
		self.__coins = 10

		self.load()

		# --- Background/Foreground --- #

		if self.__temp[0] == 0:
			self.bg = pygame.sprite.Group(sprites.Background(0))
		else:
			self.bg = pygame.sprite.Group(sprites.Background(1))

		self.fg = pygame.sprite.Group()
		self.player =  pygame.sprite.GroupSingle(characters.Character())
		self.fg2 = pygame.sprite.Group()

		# --- Background Additions --- #

		self.bg.add(sprites.Planet(self.__temp.pop(0)))

		# --- Foreground Additions --- #

		self.__clanBanner = sprites.Sprite("Banners/BlueStar")
		self.fg.add(sprites.Flag(self.__clanBanner))

		self.fg.add(upgradeable.TownHall(self.__temp.pop(0)))
		self.fg.add(sprites.Shop())
		self.fg.add(upgradeable.Statue(self.__temp.pop(0)))

		# --- Foreground 2 Additions --- #

		self.fg2.add(upgradeable.Wall(self.__temp.pop(0)))

		# --- Menu Buttons --- #

		self.__title_list = ("Play", "New Game", "Options", "Quit")
		self.__paused_list = ("Continue", "Options", "Return to Menu")
		self.__controls_list = ("Left: Left Arrow", "Right : Right Arrow","Run: Shift+Arrow Key","Upgrade: Down Arrow", "Pause: Escape",
		"Back: Left Arrow (in menus)")

		version = App.__version__.split(":")[0]
		self.__credits_list = (f"Version: {version}","Programmer: Brendan Beard", "Published By: AtlasCorporations")

		self.__instructions_list = ["Click the Left/Right Arrow Keys to move", "Click the Down Arrow to upgrade buildings",
		"Click the Esc Key to get extra help and to pause"]

		self.createMenus()
		self.__path = [self.titleMenu]

	@property
	def audio(self):
		return self.__settings[1]

	@audio.setter
	def audio(self, audio):
		self.__settings[1] = audio

	@property
	def dyslexic(self):
		return self.__settings[2]

	@dyslexic.setter
	def dyslexic(self, dyslexic):

		self.__settings[2] = dyslexic
		if self.__settings[2]:
			self.__font = local.FONT = local.OPENDYSLEXIC
		else:
			self.__font = local.FONT = local.COMICSANS

	@property
	def debug(self):
		return self.__settings[3]

	@debug.setter
	def debug(self, debug):
		self.__settings[3] = debug

	@property
	def isDay(self):
		return self.bg.sprites()[-1].type == 0

	def load(self) -> None:
		"""Load in a previous save game file"""

		try:
			with open(local.SAVE_PATH, "r") as file:
				temp = list((eval(i) for i in file.read().splitlines()))

			self.__settings[0] = temp.pop(0)
			self.audio = temp.pop(0)
			self.dyslexic =  temp.pop(0)
			self.debug = temp.pop(0)
			self.__day = temp.pop(0)
			self.__difficulty = temp.pop(0)
			self.__coins = temp.pop(0)

			self.__temp = temp

		except Exception as e:
			if isinstance(e, FileNotFoundError):
				self.__temp = [1,]*2
			else:
				with open(local.ERROR_PATH, "w") as file:
					file.write(str(e))
				print(f"Error: {e}")

	def save(self) -> None:
		"""Save the game to file"""

		fg = self.fg.sprites()+self.fg2.sprites()
		fg = tuple((i for i in fg if isinstance(i, upgradeable.Upgradeable)))
		with open(local.SAVE_PATH, "w") as file:
			file.write("\n".join((str(i) for i in self.__settings)))
			file.write("\n")
			file.write("\n".join((str(self.__day), str(self.__difficulty), str(self.__coins),
													str(self.bg.sprites()[-1].type))))
			file.write("\n")
			file.write("\n".join(tuple((str(i.level) for i in fg))))
			file.write("\n")

	def quit(self) -> None:
		"""Save and quit"""

		self.__quit = True
		self.__path.clear()
		pygame.quit()
		exit(0)

	def __font_render(self, string : str) -> pygame.Surface:
		"""Font render"""
		return self.__font.render(string, True, local.BLACK)

	def createMenus(self):
		"""Create the menus"""

		self.titleMenu = menus.Menu((self.__display.get_width()//3, self.__display.get_height()))
		self.paused = menus.Menu((self.__display.get_width()//3, self.__display.get_height()))
		self.options = menus.Menu(self.__display.get_size())
		self.controls = menus.Menu(self.__display.get_size())
		self.credits = menus.Menu(self.__display.get_size())
		self.__instructions = pygame.sprite.GroupSingle()

		# --- Title Menu Menu --- #

		for button in self.__title_list:
			self.titleMenu.add_button((self.__display.get_width()//4, self.__display.get_height()//8), button)
		self.titleMenu.center_buttons(self.__display.get_size(), 3)

		# --- Paused Menu --- #

		self.paused.add(menus.Paused((self.__display.get_width()//4, self.__display.get_height())))
		for button in self.__paused_list:
			self.paused.add_button((self.paused.sprites()[0].rect.w//1.25, self.__display.get_height()//6), button)
		self.paused.center_buttons(self.paused.sprites()[0].rect.size)

		# --- Options Menu --- #

		dyslexic = str(self.dyslexic).replace("True", "On").replace("False", "Off")
		debug = str(self.debug).replace("True", "On").replace("False", "Off")
		audio = str(self.audio).replace("True", "On").replace("False", "Off")
		self.__options_list = ("Controls", f"Audio: {audio}", f"Dyslexia: {dyslexic}", f"Debug: {debug}", "Credits")

		for button in self.__options_list:
			self.options.add_button((self.__display.get_width()//4, self.__display.get_height()//8), button)
		self.options.center_buttons(self.__display.get_size(), 2)

		# --- Controls Menu --- #

		for button in self.__controls_list:
			self.controls.add_button((self.__display.get_width()//4, self.__display.get_height()//8), button)
		self.controls.center_buttons(self.__display.get_size(), 1)

		# --- Credits Additions --- #

		for i,button in enumerate(self.__credits_list, 1):
			menu = sprites.Sprite(self.__font_render(button))
			self.credits.add(menu)
			menu.rect.topleft = self.__display.get_width()//2-menu.rect.w//2, 35*i

		# --- Instructions Additions ---- #

		self.__instructions_copy = self.__instructions_list.copy()

		self.__instructions.add(pygame.sprite.Sprite())
		self.__instructions.sprite.image =  self.__font_render(self.__instructions_copy.pop(0))
		self.__instructions.sprite.rect = self.__instructions.sprite.image.get_rect()

		# --- Set Menu Path --- #

		if self.__isPaused:
			self.__path = [self.paused, self.options]
		else:
			self.__path = [self.titleMenu, self.options]

	def instruct(self, event : pygame.event.Event) -> None:
		"""Display instructions loop"""

		if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
			if len(self.__instructions_copy) > 0:
				self.__instructions.sprite.image = self.__font_render(self.__instructions_copy.pop(0))
				self.__instructions.sprite.rect = self.__instructions.sprite.image.get_rect()
			else:
				self.__settings[0] = False
				pygame.key.set_repeat(App.FPS*2, App.FPS//2)

	def clickEvents(self, event : pygame.event.Event) -> None:
		"""Mousebuttondown Events"""

		if len(self.__path) > 0: #Both
			index = tuple((self.__path[-1]._buttons.index(sprite) for sprite in self.__path[-1]._buttons if sprite.rect.collidepoint(event.pos)))
			if index != ():
				index = index[-1]

			if self.__path[-1] == self.options:
				if index == 0: #Controls
					self.__path.append(self.controls)
				elif index == 1: #Audio
					self.audio = not self.audio
				elif index == 2: #Dyslexia
					self.dyslexic = not self.dyslexic
				elif index == 3: #Debug
					self.debug = not self.debug
				elif index == 4: #Credits
					self.__path.append(self.credits)

				if index == 1 or index == 2 or index == 3:
					del self.__path[-1]
					self.createMenus() #Recreate Menus with new font or updated stats

			elif not self.__inGame and self.__path[-1] == self.titleMenu: #Title Menu
				if index == 0: #Play
					self.__settings[0] = False
					pygame.time.set_timer(DAYNIGHTEVENT, local.DAYCYCLETIME, 0)
					pygame.key.set_repeat(App.FPS*2, App.FPS//2)
				elif index == 2: #Options
					self.__path.append(self.options)
				elif index == 3: #Quit
					self.quit()

				if index == 0 or index == 1:
					self.__inGame = True
					self.__path.clear()

			elif self.__isPaused and self.__path[-1] == self.paused: #Pause Menu
				if index == 0: #Continue
					pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"mod": 0, "key": pygame.K_ESCAPE}))
				elif index == 1: #Options
					self.__path.append(self.options)
				elif index == 2: #Return to Menu
					self.__inGame = False
					self.__path = [self.titleMenu]

	def keyEvents(self, event : pygame.event.Event) -> None:
		"""Key Events"""

		if event.mod == pygame.KMOD_LCTRL:
			if event.key == pygame.K_q:
				self.__quit = True
				self.__path.clear()
			# elif event.key == pygame.K_d:
			# 	pygame.event.post(DAYNIGHTEVENT)
		elif event.key == pygame.K_LEFT:
			if len(self.__path) > 1:
				del self.__path[-1]

		if not self.__inGame: #In Title
			if event.key == pygame.K_RETURN:
				self.__inGame = True
		elif self.__isPaused: #In Pause Menu
			if event.key == pygame.K_ESCAPE:
				self.__path.clear()
				self.__isPaused = False
		else: #In Game
			if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
				if event.key == pygame.K_LEFT:
					self.player.sprite.direction = -1
				elif event.key == pygame.K_RIGHT:
					self.player.sprite.direction = 1

				if event.mod in SHIFTS:
					x = local.RUN_MOVEMENT*self.player.sprite.direction
				else:
					x = local.MOVEMENT*self.player.sprite.direction
				self.player.sprite.rect.x += x
			# elif event.key == pygame.K_UP:
				# self.player.sprite.rect.y -= 50
			elif event.key == pygame.K_ESCAPE:
				self.__path.append(self.paused)
				self.__isPaused = True
			elif event.key == pygame.K_DOWN:
				#Create variable 'collision', if 'collision 'is not equal to an empty list
				fg = self.fg.sprites()+self.fg2.sprites()
				fg = (i for i in fg if isinstance(i, upgradeable.Upgradeable)) #Valid fg objects
				if (collision := pygame.sprite.spritecollide(self.player.sprite, fg, False)) != []:
					self.__coins = collision[-1].upgrade(self.__coins)
			elif event.key == pygame.K_c:
				self.__coins += 1

	def events(self) -> None:
		"""Main Event Function"""

		event = pygame.event.poll()
		if self.__settings[0] and self.__inGame:
			self.instruct(event)
		elif event.type == pygame.QUIT:
			self.quit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.clickEvents(event)
		elif event.type == pygame.KEYDOWN:
			self.keyEvents(event)
		elif event.type == local.DAYNIGHT:
			if not self.__isPaused and self.__inGame:
				self.__day += 0.5
				if self.__day % 1 == 0:
					self.bg.sprites()[0].type = self.bg.sprites()[-1].type = 0
					self.__coins += 10
				else:
					self.bg.sprites()[0].type = 1
					if int(self.__day) % 5 == 0:
						self.bg.sprites()[-1].type = 2
					else:
						self.bg.sprites()[-1].type = 1


	def draw(self) -> None:
		"""Draw menus or game"""

		if self.isDay:
			self.__display.fill(local.LIGHTBLUE)
		else:
			if self.bg.sprites()[-1].type == 1:
				self.__display.fill(local.DARK)
			else:
				self.__display.fill(local.DARKRED)

		self.bg.draw(self.__display)
		if self.__inGame:
			self.fg.draw(self.__display)
			self.player.draw(self.__display)
			self.fg2.draw(self.__display)

			if self.__settings[0]:
				self.__instructions.draw(self.__display)
			else:
				font = self.__font_render("Days: {}  Coins: {}".format(int(self.__day), self.__coins))
				self.__display.blit(font, (self.__display.get_width()//2-font.get_width()//2, 0))

				if self.__isPaused:
					self.paused.draw(self.__display)
					if len(self.__path) == 1: #Only display on first pause menu, no submenus
						rect = pygame.rect.Rect(self.__display.get_width()//2,
																		self.__display.get_height()//4,
																		self.__display.get_width()//8,
																		self.__display.get_height()//2)
						path = ((rect.x, rect.y),
									(rect.x+rect.w, rect.h),
									(rect.x, rect.y+rect.h),
									(rect.x-rect.w, rect.h))

						pygame.draw.polygon(self.__display, local.LIGHTBROWN, path)
						pygame.draw.polygon(self.__display, local.BROWN, path, 3)
						self.__display.blit(self.__clanBanner.image, (rect.x-self.__clanBanner.rect.w//2, rect.h-self.__clanBanner.rect.h//2))
		else:
			font = self.__font_render(App.__app__)
			self.__display.blit(font, (self.__display.get_width()//2-font.get_width()//2, 0))

		if len(self.__path) > 0:
			self.__path[-1].draw(self.__display)

		if self.debug:
			font = self.__font_render("FPS: {}".format(round(self.__clock.get_fps())))
			self.__display.blit(font, (self.__display.get_width()-font.get_width()-5, 0))

		pygame.display.flip()

	def __main__(self) -> None:
		"""Main"""

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
