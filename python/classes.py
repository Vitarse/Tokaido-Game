import pygame


class Player:
    def __init__(self, pseudo, couleur, station, argent, personnage, genre):
        self.pseudo = pseudo
        self.color = couleur
        self.locate = station
        self.x = 0
        self.y = 0
        self.purse = argent
        self.perso = personnage
        if self.perso == None:
            self.perso = None
        self.gender = genre
        self.pts = 0
        self.amen = 0
        self.riz = 0
        self.mont = 0
        self.mer = 0
        self.meetdeck = []
        self.souvdeck = []
        self.mealdeck = []

    def afficher(self):
        print(f"{self.pseudo}, {self.color}, station {self.locate}, {self.purse} pieces, {self.pts} points, {self.perso}, {self.gender}")

class Case:
    def __init__(self, pos, number):
        self.nom = str(number)
        self.position = pos
        self.surface = pygame.Surface((65,65),pygame.SRCALPHA)
        self.surface.fill((29,35,189,0))
        self.rect = self.surface.get_rect(topleft= self.position)

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Repas:
    def __init__(self, picture_path, position):
        self.pos = position
        self.dim = (120,200)
        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image, self.dim)
        self.surface = pygame.Surface(self.dim, pygame.SRCALPHA)
        self.surface.fill((29,35,189,0))
        self.rect = self.surface.get_rect(topleft=self.pos)

class Amen:
    def __init__(self, picture_path, position):
        self.pos = position
        self.image = pygame.image.load(picture_path)
        self.surface = pygame.Surface((150,150), pygame.SRCALPHA)
        self.surface.fill((29,35,189,0))
        self.rect = self.surface.get_rect(topleft=self.pos)

class Character_select:
    def __init__(self,name,position):
        self.position = position
        self.image = pygame.image.load("python/images/tuiles/"+name+".png")
        self.image = pygame.transform.scale(self.image,(400,400))
        self.rect = self.image.get_rect(topleft=self.position)