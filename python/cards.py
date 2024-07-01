# classe des différentes cartes
class SouvenirCard:
    def __init__(self, nom, famille, prix):
        self.name = nom
        self.category = famille
        self.price = prix
    
class PanoramaCard:
    def __init__(self, nom, paysage, nombre):
        self.name = nom
        self.land = paysage
        self.nbr = nombre

class SourceChaudeCard:
    def __init__(self, points):
        self.pts = points

class RencontreCard:
    def __init__(self, nom, effet):
        self.name = nom
        self.effect = effet

class RepasCard:
    def __init__(self, nom, points, prix):
        self.name = nom
        self.pts = points
        self.price = prix

class AccomplissementCard:
    def __init__(self, nom):
        self.name = nom
        self.pts = 3

class PersonnageCard:
    def __init__(self, nom, argent, skill):
        self.name = nom
        self.purse = argent
        self.skill = skill
