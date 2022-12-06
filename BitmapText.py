import pygame

pygame.font.init()

class BitmapText:
    """"""

    # estilos del texto
    DEFAULT = pygame.font.SysFont('Consolas', 30)
    TITLE = pygame.font.SysFont('Consolas', 100)
    NORMAL = pygame.font.SysFont('Consolas', 30)

    def __init__(self):
        pass

    def setFontTitle(font_path, size):
        BitmapText.TITLE = pygame.font.SysFont(font_path, size)
    
    def setFontDisplay(font_path, size):
        BitmapText.NORMAL = pygame.font.SysFont(font_path, size)

    @classmethod
    def display(cls, surface, text, x, y, color=(255,255,255), font=DEFAULT):
        text_surface = font.render(text, False, color)
        surface.blit(text_surface, (x, y))

    @classmethod
    def title(cls, surface,text, x=0, y=0, color=(255,255,255), alpha=255, font=TITLE, cap=False):
        text = font.render(text, False, color)
        text.set_alpha(alpha)
        text_rect = text.get_rect()
        text_rect.centerx = surface.get_rect().centerx + x
        text_rect.centery = surface.get_rect().centery + y

        if cap:
            pygame.draw.rect(surface, (0,0,0), text_rect)
        surface.blit(text, text_rect)

