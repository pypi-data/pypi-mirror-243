import pygame.draw

from .. import itemBase, Screen


class Line(itemBase):
    def __init__(self, screen: Screen, a=(0, 0), b=(10, 10), width=1, color="white"):
        super().__init__("Line")
        self.rect = pygame.Rect((0, 0), (0, 0))
        self.screen = screen
        screen.Items.append(self)
        self.a = screen.root.relative(a[0], a[1])
        self.b = screen.root.relative(b[0], b[1])
        self.width = width
        self.color = color

    def config(self, a=(0, 0), b=(10, 10), width=1, color="white"):
        self.a = self.screen.root.relative(a[0], a[1])
        self.b = self.screen.root.relative(b[0], b[1])
        self.width = width
        self.color = color
        
    def update(self):
        self.rect = pygame.draw.line(self.screen.root.MainRoot, self.color, self.a, self.b, self.width)
