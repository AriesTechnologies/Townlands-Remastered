#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import os, pygame, sys
import characters, menus, sprites, local, upgradeable
from pygame.locals import *
pygame.init()


# --- Variables --- #

SHIFTS = (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT)
MOVEMENT = 5
RUN_MOVEMENT = 8

SAVE_PATH = f"{sys.path[0]}/Saves/{os.getlogin()}.sgf"


# --- App Class --- #

class App(object):

	__app__ = "Townlands: Remastered"
	__version__ = """FU 0.5.0 Gamma: Added banner to Pause Menu,
								added all menus (so far),
								added audio menu (replaced brightness), added flag,
								added upgradeable and local modules,
								add some testing objects,
								add save file loading and saving (automatically loads and saves),
								improved instructions function,
								 (Dec 27 2021, 19:04 CST)"""
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
		pygame.display.set_icon(pygame.image.load(f"{sprites.IMAGE_PATH}/Icon.png"))
		self.__display = pygame.display.set_mode((1280,720), pygame.FULLSCREEN | pygame.DOUBLEBUF)
		self.__font = pygame.font.SysFont("comicsansms", 20)

		self.__path : list
		self.__quit = False
		self.__inGame = False
		self.__isPaused = False
		self.__firstTime = True
		self.__audio = True
		self.__dyslexic = False
		self.__debug = True
		self.__day = 1
		self.__difficulty = 3 #Beginner: 5, Easy: 4, Medium: 3, Hard: 2, Master: 1, Hell: 0
		self.__coins = 10

		self.load()

		# --- Menus --- #

		self.bg = pygame.sprite.Group(sprites.Background())
		self.fg = pygame.sprite.Group()
		self.titleMenu = menus.Menu((self.__display.get_width()//3, self.__display.get_height()))
		self.paused = menus.Menu((self.__display.get_width()//3, self.__display.get_height()))
		self.options = menus.Menu(self.__display.get_size())
		self.controls = menus.Menu(self.__display.get_size())
		self.credits = menus.Menu(self.__display.get_size())
		self.__instructions = pygame.sprite.GroupSingle()

		self.player =  pygame.sprite.GroupSingle(characters.Character())

		# --- Foreground Additions --- #

		self.fg.add(upgradeable.TownHall(self.__temp.pop(0)))
		self.fg.add(upgradeable.Wall(self.__temp.pop(0)))
		self.fg.sprites()[-1].rect.topleft = (self.__display.get_width()-self.fg.sprites()[-1].rect.w,self.fg.sprites()[0].rect.h-self.fg.sprites()[-1].rect.h)

		# --- Title Menu Menu --- #

		self.__title_list = ("Play", "New Game", "Options", "Quit")

		for button in self.__title_list:
			self.titleMenu.add_button((self.__display.get_width()//4, self.__display.get_height()//8), button)
		self.titleMenu.center_buttons(self.__display.get_size(), 3)

		# --- Paused Menu --- #

		self.__paused_list = ("Continue", "Options", "Return to Menu")

		self.paused.add(menus.Paused((self.__display.get_width()//4, self.__display.get_height())))
		for button in self.__paused_list:
			self.paused.add_button((self.paused.sprites()[0].rect.w//1.25, self.__display.get_height()//6), button)
		self.paused.center_buttons(self.paused.sprites()[0].rect.size)

		# --- Options Menu --- #

		dyslexic = str(self.__dyslexic).replace("True", "On").replace("False", "Off")
		debug = str(self.__debug).replace("True", "On").replace("False", "Off")
		audio = str(self.__audio).replace("True", "On").replace("False", "Off")
		self.__options_list = ("Controls", f"Audio: {audio}", f"Dyslexia: {dyslexic}", f"Debug: {debug}", "Credits")

		for button in self.__options_list:
			self.options.add_button((self.__display.get_width()//4, self.__display.get_height()//8), button)
		self.options.center_buttons(self.__display.get_size(), 2)

		# --- Controls Menu --- #

		self.__controls_list = ("Left: Left Arrow", "Right : Right Arrow","Run: Shift+Arrow Key","Upgrade: Down Arrow", "Pause: Escape",
		"Back: Backspace or Left Arrow")

		for button in self.__controls_list:
			self.controls.add_button((self.__display.get_width()//4, self.__display.get_height()//8), button)
		self.controls.center_buttons(self.__display.get_size(), 1)

		# --- Credits Additions --- #

		version = App.__version__.split(":")[0]
		self.__credits_list = (f"Version: {version}","Programmer: Brendan Beard", "Published By: AtlasCorporations")

		for i,button in enumerate(self.__credits_list, 1):
			menu = sprites.Sprite(self.__font_render(button))
			self.credits.add(menu)
			menu.rect.topleft = self.__display.get_width()//2-menu.rect.w//2, 35*i

		# --- Instructions Additions ---- #

		self.__instructions_list = ["Click the Left/Right Arrow Keys to move", "Click the Down Arrow to upgrade buildings",
		"Click the Esc Key to get extra help and to pause"]
		self.__instructions_copy = self.__instructions_list.copy()

		self.__instructions.add(pygame.sprite.Sprite())
		self.__instructions.sprite.image =  self.__font_render(self.__instructions_copy.pop(0))
		self.__instructions.sprite.rect = self.__instructions.sprite.image.get_rect()

		# --- Add Path Variable --- #

		self.__path = [self.titleMenu]

		# --- Load Save --- #

		self.__clanBanner = sprites.Sprite("Banners/BlueBanner")
		self.__clanFlag = sprites.Flag(self.__clanBanner)
		self.__clanFlag.rect.topleft = (50, self.fg.sprites()[0].rect.h-self.__clanFlag.rect.h)
		self.fg.add(self.__clanFlag)
		# self.load()

	@property
	def audio(self):
		return self.__audio

	@audio.setter
	def audio(self, audio):
		self.__audio = audio

	@property
	def dyslexic(self):
		return self.__dyslexic

	@dyslexic.setter
	def dyslexic(self, dyslexic):

		self.__dyslexic = dyslexic
		if self.__dyslexic:
			self.__font = pygame.font.Font(f"{sys.path[0]}/Fonts/OpenDyslexic.otf", 20)
		else:
			self.__font = pygame.font.SysFont("comicsansms", 20)

	@property
	def debug(self):
		return self.__debug

	@debug.setter
	def debug(self, debug):
		self.__debug = debug

	def load(self) -> None:
		"""Load in a previous save game file"""

		try:
			with open(SAVE_PATH, "r") as file:
				temp = list((eval(i) for i in file.read().splitlines()))

			self.__firstTime = temp.pop(0)
			self.audio = temp.pop(0)
			self.dyslexic = temp.pop(0)
			self.debug = temp.pop(0)
			self.__day = temp.pop(0)
			self.__difficulty = temp.pop(0)
			self.__coins = temp.pop(0)

			self.__temp = temp

		except Exception as e:
			if isinstance(e, FileNotFoundError):
				self.__temp = [1,]*2
			else:
				with open(f"{sys.path[0]}/Error.log", "w") as file:
					file.write(str(e))
				print(f"Error: {e}")

	def save(self) -> None:
		"""Save the game to file"""

		fg = tuple((i for i in self.fg if isinstance(i, upgradeable.Upgradeable)))
		with open(SAVE_PATH, "w") as file:
			file.write("\n".join((str(self.__firstTime),str(self.__audio), str(self.__dyslexic),
													str(self.__debug), str(self.__day), str(self.__difficulty),
													str(self.__coins), "")))
			file.write("\n".join(tuple((str(i.level) for i in fg))))

	def quit(self) -> None:
		"""Save and quit"""

		self.__quit = True
		self.__path.clear()
		pygame.quit()
		exit(0)

	def __font_render(self, string : str) -> pygame.Surface:
		"""Font render"""
		return self.__font.render(string, True, local.BLACK)

	def instruct(self, event : pygame.event.Event) -> None:
		"""Display instructions loop"""

		if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
			if len(self.__instructions_copy) > 0:
				self.__instructions.sprite.image = self.__font_render(self.__instructions_copy.pop(0))
				self.__instructions.sprite.rect = self.__instructions.sprite.image.get_rect()
			else:
				self.__firstTime = False
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
					self.__audio = not self.__audio
				elif index == 2: #Dyslexia
					self.dyslexic = not self.dyslexic
				elif index == 3: #Debug
					self.__debug = not self.__debug
				elif index == 4: #Credits
					self.__path.append(self.credits)

				if index == 1 or index == 2 or index == 3:
					dyslexic = str(self.__dyslexic).replace("True", "On").replace("False", "Off")
					debug = str(self.__debug).replace("True", "On").replace("False", "Off")
					audio = str(self.__audio).replace("True", "On").replace("False", "Off")
					self.__options_list = ("Controls", f"Audio: {audio}", f"Dyslexia: {dyslexic}", f"Debug: {debug}", "Credits")

					del self.__path[-1]
					self.options._buttons.clear()
					self.options.empty()

					for button in self.__options_list:
						self.options.add_button((self.__display.get_width()//4, self.__display.get_height()//8), button)

					self.options.center_buttons(self.__display.get_size(), 2)
					self.__path.append(self.options)

			elif not self.__inGame and self.__path[-1] == self.titleMenu: #Title Menu
				if index == 0: #Play
					# if self.__noSaves:
					 	self.__firstTime = False
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
		else: #In Game
			if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
				if event.key == pygame.K_LEFT:
					self.player.sprite.direction = -1
				elif event.key == pygame.K_RIGHT:
					self.player.sprite.direction = 1

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
				#Create variable 'collision', if 'collision 'is not equal to an empty list
				fg = (i for i in self.fg if isinstance(i, upgradeable.Upgradeable)) #Valid fg objects
				if (collision := pygame.sprite.spritecollide(self.player.sprite, fg, False)) != []:
					self.__coins = collision[-1].upgrade(self.__coins)
			elif event.key == pygame.K_c:
				self.__coins += 1

	def events(self) -> None:
		"""Main Event Function"""

		event = pygame.event.poll()
		if self.__firstTime and self.__inGame:
			self.instruct(event)
		elif event.type == pygame.QUIT:
			self.quit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.clickEvents(event)
		elif event.type == pygame.KEYDOWN:
			self.keyEvents(event)

	def draw(self) -> None:
		"""Draw menus or game"""

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

		if self.__debug:
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
