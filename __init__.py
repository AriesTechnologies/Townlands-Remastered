#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import pygame
import enemies, characters, maps, menus, sprites, local, upgradeable
from pygame.locals import *


# --- Definitions --- #

def collide_with_bounds(sprite, group):

	hits = pygame.sprite.spritecollide(sprite, group, False)
	if hits: #If non-empty list
		group = hits[0]
		if group.rect.centerx > sprite.rect.centerx:
			sprite.rect.x = group.rect.left-sprite.rect.w
		if group.rect.centerx < sprite.rect.centerx:
			sprite.rect.x = group.rect.right

def collide_with_building(sprite, group):
	"""If touching building with more than 0 health"""

	hits = tuple((i for i in pygame.sprite.spritecollide(sprite, group, False)
							if isinstance(i, upgradeable.Upgradeable) and i._health > 0 and i.level > 1))
	if hits:
		if len(hits) > 1:
			hits = tuple((i for i in hits if isinstance(i, upgradeable.Wall)))
		hits = hits[-1]
		return hits
	return False

def collide_with_player(sprite, group):
	return pygame.sprite.spritecollide(sprite, group, False)


# --- App Class --- #

class App(object):

	__app__ = "Townlands: Remastered"
	__version__ = """IU 1.2.0 Alpha: Added copyright, removed New Game button (Dec 31 2021, 23:38 CST)"""
	#"""IU 1.1.0 Alpha: Added game over (Dec 31 2021, 23:12 CST)"""
	# """FU 1.0.0 Alpha: Added all buildings,
	# 								added "camera",
	# 								added enemies,
	# 								released
	# 								(Dec 31 2021, 16:32 CST)"""
	# """IU 0.5.1 Gamma: Added day/night cycle,
	# 								added gaining coins after every night,
	# 								added all updated graphics (Dec 29 2021, 16:38)"""
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
		self.__difficulty = 2 #Beginner: 0, Easy: 1, Medium: 2, Hard: 3, Master: 4, Hell: 5 (not added fully)
		self.__coins = 10

		self.load()

		# --- Background/Foreground --- #

		self.bg = pygame.sprite.Group(maps.TiledMap(self.__day))
		self.fg, self.fg2 = pygame.sprite.Group(), pygame.sprite.Group() #Create fg groups
		self.player =  pygame.sprite.GroupSingle(characters.Character())
		self.__monsters = pygame.sprite.Group()
		self.camera = maps.Camera(self.bg.sprites()[0].rect.size)

		self.boundaries = pygame.sprite.Group()
		self.boundaries.add(sprites.Bound(0))
		self.boundaries.add(sprites.Bound(self.bg.sprites()[0].rect.w-3))

		# --- Background Additions --- #

		self.bg.add(sprites.Planet(self.bg.sprites()[0].type))

		# --- Foreground Additions --- #

		#TownHall
		self.fg.add(upgradeable.TownHall(self.__temp.pop(0)))

		#Flag, Shop, Statue
		self.__clanBanner = sprites.Sprite("Banners/BlueStar")
		self.fg.add(sprites.Flag(self.__clanBanner, self.fg.sprites()[-1].OFFSETX+self.fg.sprites()[-1].rect.w//20))
		self.fg.add(sprites.Shop(self.fg.sprites()[0].OFFSETX))
		self.fg.add(upgradeable.Statue(self.__temp.pop(0), self.bg.sprites()[0].rect.w))

		#ArcherTowers
		self.fg.add(upgradeable.ArcherTower(self.__temp.pop(0), self.fg.sprites()[0].OFFSETX-self.fg.sprites()[0].rect.w))
		self.fg.add(upgradeable.ArcherTower(self.__temp.pop(0), self.fg.sprites()[0].OFFSETX+self.fg.sprites()[0].rect.w*2))

		#Farm
		self.fg.add(upgradeable.Farm(self.__temp.pop(0), 2300))
		self.fg.add(upgradeable.Farm(self.__temp.pop(0), 4700))

		#Cannons
		self.fg.add(upgradeable.Cannon(self.__temp.pop(0), 1000))
		self.fg.add(upgradeable.Cannon(self.__temp.pop(0), 6600))
		self.fg.sprites()[-1].flip()

		#Portal
		if self.__temp[0] == 1:
			self.fg.add(upgradeable.Portal(self.__temp.pop(0), 0))

		#Walls
		archerw = self.fg.sprites()[4].rect.w
		cannonw = self.fg.sprites()[-3].rect.w

		self.fg2.add(upgradeable.Wall(self.__temp.pop(0), self.fg.sprites()[-3].OFFSETX-cannonw//8)) #Left Cannon
		self.fg2.add(upgradeable.Wall(self.__temp.pop(0), self.fg.sprites()[4].OFFSETX-archerw//8)) #Left ArcherTower
		self.fg2.add(upgradeable.Wall(self.__temp.pop(0), self.fg.sprites()[0].OFFSETX-self.fg.sprites()[0].rect.w//32)) #Left TownHall
		self.fg2.add(upgradeable.Wall(self.__temp.pop(0), self.fg.sprites()[0].OFFSETX+self.fg.sprites()[0].rect.w)) #Right TownHall
		self.fg2.add(upgradeable.Wall(self.__temp.pop(0), self.fg.sprites()[5].OFFSETX+archerw+archerw//8)) #Right ArcherTower
		self.fg2.add(upgradeable.Wall(self.__temp.pop(0), self.fg.sprites()[-2].OFFSETX+cannonw+cannonw//8)) #Right Cannon


		# --- Menu Buttons --- #

		# self.__title_list = ("Play", "New Game", "Options", "Quit")
		self.__title_list = ("Play", "Options", "Quit")
		self.__paused_list = ("Continue", "Options", "Return to Menu")
		self.__controls_list = ("Left: Left Arrow", "Right : Right Arrow","Run: Shift+Arrow Key","Upgrade: Down Arrow", "Pause: Escape",
		"Back: Left Arrow (in menus)")

		version = App.__version__.split(":")[0]
		self.__credits_list = (f"Version: {version}","Programmer: Brendan Beard", "Published By: AtlasCorporations")

		self.__instructions_list = ["Click the Left/Right Arrow Keys to move", "Click the Down Arrow to upgrade buildings",
		"Click the Esc Key to get extra help and to pause"]

		self.createMenus()
		self.__path = [self.titleMenu]
		self.__all_sprites = self.fg.sprites()+self.fg2.sprites()

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
		return self.bg.sprites()[0].type == 0

	@property
	def isGameOver(self):
		return self.player.sprite._health == 0

	def load(self) -> None:
		"""Load in a previous save game file"""

		temp = []

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
		except Exception as e:
			if isinstance(e, FileNotFoundError):
				temp = [1,]*25 #Should be plenty of 1's for the save
			else:
				with open(local.ERROR_PATH, "w") as file:
					file.write(str(e))
				# print(f"Error: {e}")
		finally:
			self.__temp = temp

	def save(self) -> None:
		"""Save the game to file"""

		fg = self.fg.sprites()+self.fg2.sprites()
		fg = tuple((i for i in fg if isinstance(i, upgradeable.Upgradeable)))
		with open(local.SAVE_PATH, "w") as file:
			file.write("\n".join((str(i) for i in self.__settings)))
			file.write("\n")
			file.write("\n".join((str(self.__day), str(self.__difficulty), str(self.__coins))))
			file.write("\n")
			file.write("\n".join(tuple((str(i.level) for i in fg))))
			file.write("\n")

	def quit(self) -> None:
		"""Save and quit"""

		self.__quit = True
		self.__path.clear()
		pygame.quit()
		exit(0)

	def __font_render(self, string : str, color : tuple | pygame.Color = None) -> pygame.Surface:
		"""Font render"""
		if color == None:
			if self.bg.sprites()[0].type == 0:
				return self.__font.render(string, True, local.BLACK)
			else:
				return self.__font.render(string, True, local.WHITE)
		else:
			return self.__font.render(string, True, color)

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
		# audio = str(self.audio).replace("True", "On").replace("False", "Off")
		self.__options_list = (f"Dyslexia: {dyslexic}", f"Debug: {debug}", "Credits")
		# self.__options_list = ("Controls", f"Audio: {audio}", f"Dyslexia: {dyslexic}", f"Debug: {debug}", "Credits")

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

	def __instruct(self, event : pygame.event.Event) -> None:
		"""Display instructions loop"""

		if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
			if len(self.__instructions_copy) > 0:
				self.__instructions.sprite.image = self.__font_render(self.__instructions_copy.pop(0))
				self.__instructions.sprite.rect = self.__instructions.sprite.image.get_rect()
			else:
				self.__settings[0] = False
				pygame.key.set_repeat(App.FPS*2, App.FPS//2)

	def gameOver(self):
		"""Game Over"""

		self.bg.sprites()[-1].rect.x = 0
		while self.__inGame:
			event = pygame.event.poll()
			if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
				self.__inGame = False
				self.__quit = True
				# self.__path = [self.titleMenu]
				return

			font = self.__font_render("Game Over!", local.RED)
			self.__display.blit(font, (self.__display.get_width()//2-font.get_width()//2, 50))
			pygame.display.flip()

	def spawnMonsters(self, amount=1, remove=False):
		"""Spawn monsters or remove monsters"""

		if remove:
			self.fg.remove(self.__monsters)
			if len(self.__monsters.sprites()) == 0:
				self.__coins += 10
			self.__monsters.empty()
		else:
			for i in range(amount):
				self.__monsters.add(enemies.Monster(self.__day))
			self.fg.add(self.__monsters)

	def __clickEvents(self, event : pygame.event.Event) -> None:
		"""Mousebuttondown Events"""

		if len(self.__path) > 0: #Both
			index = tuple((self.__path[-1]._buttons.index(sprite) for sprite in self.__path[-1]._buttons if sprite.rect.collidepoint(event.pos)))
			if index != ():
				index = index[-1]

			if self.__path[-1] == self.options:
				# if index == 0: #Controls
				# 	self.__path.append(self.controls)
				# if index == 1: #Audio
				# 	self.audio = not self.audio
				if index == 0: #Dyslexia
					self.dyslexic = not self.dyslexic
				elif index == 1: #Debug
					self.debug = not self.debug
				elif index == 2: #Credits
					self.__path.append(self.credits)

				# if index == 1 or index == 2 or index == 3:
				if index == 0 or index == 1:
					del self.__path[-1]
					self.createMenus() #Recreate Menus with new font or updated stats

			elif not self.__inGame and self.__path[-1] == self.titleMenu: #Title Menu
				if index == 0: #Play
					self.__settings[0] = False
					pygame.time.set_timer(local.DAYNIGHTEVENT, local.DAYCYCLETIME, 0)
					pygame.time.set_timer(local.ATTACKEVENT, local.ATTACKTIME, 0)
					pygame.key.set_repeat(App.FPS*2, App.FPS//2)
				#elif index == 2: #Options
				elif index == 1: #Options
					self.__path.append(self.options)
				# elif index == 3: #Quit
				elif index == 2: #Quit
					self.quit()

				if index == 0:# or index == 1:
					self.__inGame = True
					# pygame.time.set_timer(local.DAYNIGHTEVENT, local.DAYCYCLETIME, 0)
					# pygame.key.set_repeat(App.FPS*2, App.FPS//2)
					self.__path.clear()

			elif self.__isPaused and self.__path[-1] == self.paused: #Pause Menu
				if index == 0: #Continue
					pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"mod": 0, "key": pygame.K_ESCAPE}))
				elif index == 1: #Options
					self.__path.append(self.options)
				elif index == 2: #Return to Menu
					self.bg.sprites()[-1].rect.x = 0
					self.__inGame = False
					self.__path = [self.titleMenu]

	def __keyEvents(self, event : pygame.event.Event) -> None:
		"""Key Events"""

		if event.mod == pygame.KMOD_LCTRL:
			if event.key == pygame.K_q:
				self.__quit = True
				self.__path.clear()
			elif event.key == pygame.K_d:
				self.debug = not self.debug
			elif event.key == pygame.K_n:
				pygame.event.post(local.DAYNIGHTEVENT)
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

				if event.mod in local.SHIFTS:
					x = local.RUN_MOVEMENT
				else:
					x = local.MOVEMENT
				self.player.sprite.rect.x += x*self.player.sprite.direction
				collide_with_bounds(self.player.sprite, self.boundaries)
			elif event.key == pygame.K_ESCAPE:
				self.__path.append(self.paused)
				self.__isPaused = True
			elif event.key == pygame.K_DOWN:
				#Create variable 'collision', if 'collision 'is not equal to an empty list
				fg = self.fg.sprites()+self.fg2.sprites()
				fg = (i for i in fg if isinstance(i, upgradeable.Upgradeable)) #Valid fg objects
				if (collision := pygame.sprite.spritecollide(self.player.sprite, fg, False)) != []:
					self.__coins = collision[-1].upgrade(self.__coins)
			# elif event.key == pygame.K_c:
			# 	self.__coins += 1

	def events(self) -> None:
		"""Main Event Function"""

		event = pygame.event.poll()
		if self.__settings[0] and self.__inGame:
			self.__instruct(event)
		elif event.type == pygame.QUIT:
			self.quit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.__clickEvents(event)
		elif event.type == pygame.KEYDOWN:
			self.__keyEvents(event)
		elif event.type == local.DAYNIGHT:
			if not self.__isPaused and self.__inGame:
				self.__day += 0.5
				if self.__day % 1 == 0:
					pygame.time.set_timer(local.ATTACKEVENT, 0, 0)
					self.spawnMonsters(1, True)
					self.bg.sprites()[0].type = 0
					self.__coins += 10
				else:
					pygame.time.set_timer(local.ATTACKEVENT, local.ATTACKTIME, 0)
					self.spawnMonsters(1)
					if int(self.__day) % 5 == 0:
						self.bg.sprites()[0].type = 2
					else:
						self.bg.sprites()[0].type = 1

				self.bg.remove(self.bg.sprites()[-1])
				self.bg.add(sprites.Planet(self.bg.sprites()[0].type))

		elif event.type == local.ATTACK:
			for i in self.__monsters.sprites():
				if (build := collide_with_building(i, self.__all_sprites)):
					i.attack(build)

			if collide_with_player(self.player.sprite, self.__monsters):
				i.attack(self.player.sprite)

	def update(self) -> None:
		"""Updates positions"""

		if collide_with_player(self.player.sprite, self.__monsters):
			self.player.sprite._health -= 1

		#Move monsters if not colliding_with_building and building health > 0 and build level > 1
		for i in self.__monsters.sprites():
			if not (build := collide_with_building(i, self.__all_sprites)):
				i.move()

		#Move objects
		for i in self.fg.sprites()+self.fg2.sprites():
			i.rect.x = self.bg.sprites()[0].rect.x+i.OFFSETX

		#Apply the camera
		sprites =  [self.bg.sprites()[0]]+self.boundaries.sprites()
		for i in sprites:
			i.rect = self.camera.apply(i)

		self.camera.update(self.player.sprite)
		self.player.sprite.rect = self.camera.apply(self.player.sprite)

	def draw(self) -> None:
		"""Draw menus or game"""

		#Cover up issue with camera
		if self.isDay:
			colors = iter((local.LIGHTBLUE, local.BLUE, local.LIGHTBROWN, local.GREEN))
		else:
			if self.bg.sprites()[0].type == 1:
				colors = iter((local.DARK, local.DARKBLUE, local.DARKBROWN, local.DARKGREEN))
			else:
				colors = iter((local.DARKRED, local.DARKBLUE, local.DARKBROWN, local.DARKGREEN))

		self.__display.fill(next(colors))
		pygame.draw.rect(self.__display, next(colors), (0,local.LANDHEIGHT,local.DISPLAYW,local.LANDHEIGHT))
		pygame.draw.rect(self.__display, next(colors), (0,local.LANDHEIGHT,local.DISPLAYW,60))
		pygame.draw.rect(self.__display, next(colors), (0,local.LANDHEIGHT,local.DISPLAYW,30))

		#Draw game
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
			font = self.__font_render("Copyright: AtlasCorporations (2022)")
			self.__display.blit(font, (self.__display.get_width()//2-font.get_width()//2, local.DISPLAYH-font.get_height()-5))

		#Draw menu
		if len(self.__path) > 0:
			self.__path[-1].draw(self.__display)

		#Write debug stuff
		if self.debug:
			for i,x in enumerate(("FPS: {}".format(round(self.__clock.get_fps())), f"Exact Day: {self.__day}", f"Bg Rect: {self.bg.sprites()[0].rect.topleft}")):
				font = self.__font_render(x)
				self.__display.blit(font, (self.__display.get_width()-font.get_width()-5, 20*i))
			if self.__inGame and not self.__isPaused:
				self.boundaries.draw(self.__display)

		pygame.display.flip()

	def __main__(self) -> None:
		"""Main"""

		while not self.__quit:
			self.events()
			self.update()
			self.draw()
			if self.isGameOver:
				self.gameOver()
			# print(round(self.__clock.get_fps()))
			self.__clock.tick(self.FPS)

		pygame.quit()


if __name__ == "__main__":
	App().__main__()
else:
	raise ImportError()
