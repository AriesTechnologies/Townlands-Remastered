#Author: AtlasCorporations
#Published: AtlasCorporations
#Copyright: 2022

# --- Imports --- #

import pygame.transform as pg_transform
from sprites import Sprite


# --- Character Class --- #

class Character(Sprite):
	def __init__(self):
	
		super().__init__("Prince")
		
		self.rect.y =  300
		self.facing = "R"
		
	def change_direction(self, direction : chr) -> None:
		
		if direction != self.facing:
			self.facing = direction
			self.image = pg_transform.flip(self.image, True, False)
			if self.facing == 'R':
				self.rect.x += 50 #Temp
			else:
				self.rect.x -= 50 #Temp