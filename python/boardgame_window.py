import pygame, sys
from settings import *
from overworld import Overworld

class Game:
    def __init__(self):
        self.end_station = 5
        self.overworld = Overworld(0, self.end_station, screen)

    def run(self):
        self.overworld.run()

pygame.init()
pygame.display.set_caption("TOKAIDO")
pygame.display.set_icon(pygame.image.load("python/images/icon_game.png"))
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")
    game.run()

    pygame.display.update()
    clock.tick(60)