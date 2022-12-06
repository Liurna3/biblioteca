import pygame, sys, time
from bibloteca.settings import *

from bibloteca.Control import Control
from bibloteca.Player import Player
from bibloteca.FoodFactory import FoodFactory
from bibloteca.BitmapText import BitmapText

class Game:
    TICK = pygame.USEREVENT + 1
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.time.set_timer(TICK, 500)
   
    
    def __init__(self, window_width, window_height, framerate):
        # setup
        self.players = []
        self.barColor = (0, 0, 0)
        self.window_width = window_width
        self.window_height = window_height
        self.framerate = framerate
        self.display_surface = pygame.display.set_mode((window_width, window_height))
        self.food = FoodFactory(self.window_width, self.window_height)
        self.last_time = time.time()
        self.score = 0
        self.max_vidas = 25
        self.delay_tick = 10
        self.lock = True
        self.gameOverMessage = "GAME OVER"
        self.gameOverMessageColor = (255,0,0)
        self.initMessage = "INICIANDO"
        self.initMessageColor = (0,0,255)
        self.scoreMessage = "Puntaje: "
        self.scoreMessageColor = (255,255,255)
        self.gameOver = False

    def players_update(self):
        for player in self.players:
            player.update()
    
    def players_draw(self):
        for player in self.players:
            player.draw(self.display_surface)

    def addPlayer(self, player):
        self.players.append(player)
    
    def set_max_vidas(self, max_vidas):
        self.max_vidas = max_vidas

    def setBackground(self, image_path):
        Game.background_image = pygame.image.load(image_path)
    
    def setEatSound(self, sound_path):
        Game.eat_soud = pygame.mixer.Sound(sound_path)

    def setNameApp(self, name):
        pygame.display.set_caption(name)

    def setFoodImage(self, image_path):
        self.food.setImage(image_path)
    
    def setBarColor(self, color):
        self.barColor = color
    
    def setGameOverMessage(self, message, color):
        self.gameOverMessage = message
        self.gameOverMessageColor = color
    
    def setInitMessage(self, message, color):
        self.initMessage = message
        self.initMessageColor = color
    
    def setScoreMessage(self, message, color):
        self.scoreMessage = message
        self.scoreMessageColor = color
    
    def setMaxVidas(self, max_vidas):
        self.max_vidas = max_vidas

    def setGameOver(self):
        self.gameOver = True
    
    def setFontTitle(self, font_path, size):
        BitmapText.setFontTitle(font_path, size)
    
    def setFontDisplay(self, font_path, size):
        BitmapText.setFontDisplay(font_path, size)

    def isGameOver(self):
        return self.gameOver

    def getScore(self):
        return self.score

    def loop(self):
        self.display_surface.blit(Game.background_image, (0, 0))

        # event loop
        for event in pygame.event.get():
            if event.type == Game.TICK and self.food.activeFood() < self.max_vidas:
                if self.delay_tick > 0:
                    self.delay_tick -= 1
                else:
                    self.food.create()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # game logic

        self.food.update()

        if self.delay_tick <= 0 and  self.food.activeFood() < self.max_vidas:
            self.players_update()

        self.food.draw(self.display_surface)
        self.players_draw()

        if (self.collide_food(self.players)):
            self.score += 1
            Game.eat_soud.play(0)

        self.draw_ui()

        pygame.display.update()
        
    def reset(self):
        self.score = 0
        self.gameOver = False
        i = 0
        for player in self.players:
            player.setPosition(self.window_height/len(self.players) + i*200, self.window_height/2)
            i += 1
        self.food.reset()
        self.delay_tick = 10
        
    
    def collide_food(self, players):
        for player in players:
            if pygame.sprite.spritecollide(player, self.food.group, True):
                return True
    
    def draw_ui(self):
        nfood = self.food.activeFood()


        if (nfood >= self.max_vidas):
            BitmapText.title(
                self.display_surface,
                self.gameOverMessage,
                color=self.gameOverMessageColor,
                cap=True
            )
            self.setGameOver()

        if self.delay_tick > 0:
            BitmapText.title(
                self.display_surface,
                self.initMessage,
                color=self.initMessageColor,
                alpha=255/10*self.delay_tick,
                y=0
            )

        
        BitmapText.display(
            self.display_surface,
            self.scoreMessage + str(self.score),
            20,
            20,
            color=self.scoreMessageColor)

        height_100 = self.window_height - 40
        delta = (height_100 / self.max_vidas) * nfood

        height = height_100 - delta
        top = 20 + delta

        pygame.draw.rect(
            surface=self.display_surface,
            border_radius=10,
            color=self.barColor,
            rect=pygame.Rect(self.window_width - 80, top, 60, height),
            width=0
        )


    def run(self):
        # delta time    
        self.loop()
        pygame.time.Clock().tick(self.framerate)
