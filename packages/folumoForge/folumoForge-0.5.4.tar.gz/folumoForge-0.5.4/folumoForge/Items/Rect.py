import pygame
from pygame import Surface

from .. import itemBase, Screen


class Rect(itemBase):
    def __init__(self, screen: Screen, xy=(0, 0), wh=(50, 50), color="white", opacity=0):
        super().__init__("Rect")
        self.screen = screen
        screen.Items.append(self)

        self.xy = screen.root.relative(xy[0], xy[1])
        self.wh = screen.root.relative(wh[0], wh[1])
        self.color = color
        self.Alpha = opacity

        self.rect = pygame.Rect(self.xy, self.wh)

    def config(self, xy=None, wh=None, color=None, opacity=None):
        if color:
            self.color = color

        if opacity:
            self.Alpha = opacity
        if xy:
            self.xy = self.screen.root.relative(xy[0], xy[1])
            self.rect = pygame.Rect(self.xy, self.wh)
        if wh:
            self.wh = self.screen.root.relative(wh[0], wh[1])
            self.rect = pygame.Rect(self.xy, wh)

    def update(self):
        tmp = Surface((self.rect.w, self.rect.h))
        if self.Alpha:
            tmp.set_alpha(self.Alpha)
        pygame.draw.rect(tmp, self.color, pygame.Rect((0, 0), self.wh))
        self.screen.root.MainRoot.blit(tmp, self.xy)
