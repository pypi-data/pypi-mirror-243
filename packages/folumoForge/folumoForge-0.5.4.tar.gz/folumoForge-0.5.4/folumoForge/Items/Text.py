import pygame

from .. import itemBase, Screen


class Text(itemBase):
    def __init__(self, screen: Screen, font="Arial", text="Sample Text.", color="white", bg=None, size=12, xy=(0, 0)):
        super().__init__("Text")
        self.screen = screen
        screen.Items.append(self)

        self.xy = screen.root.relative(xy[0], xy[1])
        self.font = font
        self.text = text
        self.color = color
        self.bg = bg
        self.size = size

        self.RenderedText = self._text()
        self.rect = self.RenderedText.get_rect()
        self.rect.x = self.xy[0]
        self.rect.y = self.xy[1]

    def _text(self):
        try:
            if self.bg:
                return pygame.font.Font(self.font, self.size).render(self.text, False, self.color, self.bg)
            else:
                return pygame.font.Font(self.font, self.size).render(self.text, False, self.color)
        except FileNotFoundError:
            try:
                if self.bg:
                    return pygame.font.SysFont(self.font, self.size, True).render(self.text, False, self.color, self.bg)
                else:
                    return pygame.font.SysFont(self.font, self.size, True).render(self.text, False, self.color)
            except ValueError:
                if self.bg:
                    return pygame.font.SysFont("Ariel", 12, True).render("Sample Text", False, self.color, self.bg)
                else:
                    return pygame.font.SysFont("Ariel", 12, True).render("Sample Text", False, self.color)

    def config(self, font=None, text=None, color=None, bg=None, size=None, xy=None):
        if xy:
            self.xy = self.screen.root.relative(xy[0], xy[1])
        if font:
            self.font = font
        if text:
            self.text = text

        if color:
            self.color = color
        if bg:
            self.bg = bg

        if size:
            self.size = size

        self.RenderedText = self._text()

    def update(self):
        self.rect = self.screen.root.MainRoot.blit(self.RenderedText, self.xy)
