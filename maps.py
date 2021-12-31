# --- Imports --- #

import pytmx
import pygame
import sprites, local


# --- TiledMap Class --- #

class TiledMap(sprites.Sprite):
    def __init__(self, day=1, x=0):

        if day % 1 == 0:
            self.type = 0
        else:
            if int(day) % 5 == 0:
                self.type = 2
            else:
                self.type = 1

    @property
    def type(self):
    	return self.__type

    @type.setter
    def type(self, type):

        self.__type = type
        if self.__type == 1 or self.__type == 2:
            type = 1
        else:
            type = 0

        self.__tmxdata = pytmx.load_pygame(f"{local.IMAGE_PATH}/{type}.tmx", pixelalpha=True)
        self.width = self.__tmxdata.width * self.__tmxdata.tilewidth
        self.height = self.__tmxdata.height * self.__tmxdata.tileheight

        if hasattr(self, "rect"):
            x = self.rect.x
            self.update((self.width, self.height))
            self.rect.x = x
        else:
            super().__init__((self.width, self.height))
        self.render()

    def render(self):

        self.image.fill((0,)*4)
        for layer in self.__tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = self.__tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        self.image.blit(tile, (x * self.__tmxdata.tilewidth, y * self.__tmxdata.tileheight))


# --- Camera Class --- #

class Camera:
    def __init__(self, size):
        self.rect = pygame.rect.Rect((0,)*2, size)
        self.width = size[0]
        self.height = size[1]

    def apply(self, entity):

        if isinstance(entity, pygame.rect.Rect):
            return rect.move(self.rect.topleft)
        else:
            return entity.rect.move(self.rect.topleft)

    def update(self, target):
        # limit scrolling to map size

        x = -target.rect.x + local.DISPLAYW // 2
        # y = -target.rect.y + local.DISPLAYH // 2

        # x = min(0,x)
        # x = min(0, x)
        # x = max(-(self.weight - local.DISPLAYW), min(0, x))  # left/right
        # y = max(-(self.height - local.DISPLAYH), min(0, y))  # top/bottom
        self.rect = pygame.rect.Rect(x, 0, self.width, local.DISPLAYH)#self.height)
