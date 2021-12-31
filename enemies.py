# --- Imports --- #

from sprites import Sprite
import local


# --- Monster Class --- #

class Monster(Sprite):
    def __init__(self, day=1):

        super().__init__("Monsters/Monster")

        self._health = 100
        self.__damage = 20*(day//5)
        self.OFFSETX = 0
        self.rect.y = local.LANDHEIGHT-self.rect.h

    def move(self):
        self.OFFSETX += 8

    def attack(self, building):
        building._health -= self.__damage
        if building._health <= 0:
            building.resetLevel()

        if hasattr(building, "damage"):
            self._health -= building.damage
            if self._health <= 0:
                self.kill()
