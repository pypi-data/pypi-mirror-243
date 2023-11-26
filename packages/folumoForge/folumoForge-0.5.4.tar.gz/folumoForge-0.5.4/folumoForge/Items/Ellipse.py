import pygame

from .. import itemBase, Screen


class Ellipse(itemBase):
    def __init__(self, screen: Screen, xy=(0, 0), wh=(50, 50), color="white", width=0):
        super().__init__("Ellipse")
        self.rect = pygame.Rect((0, 0), (0, 0))

        self.screen = screen
        screen.Items.append(self)

        self.xy = screen.root.relative(xy[0], xy[1])
        self.wh = screen.root.relative(wh[0], wh[1])
        self.color = color
        self.width = width
        self.rectE = pygame.Rect(self.xy, self.wh)

    def config(self, xy, wh, color, width):
        self.xy = self.screen.root.relative(xy[0], xy[1])
        self.wh = self.screen.root.relative(wh[0], wh[1])
        self.color = color
        self.width = width
        self.rectE = pygame.Rect(self.xy, self.wh)

    def update(self):
        self.rect = pygame.draw.ellipse(self.screen.root.MainRoot, self.color, self.rectE, self.width)
