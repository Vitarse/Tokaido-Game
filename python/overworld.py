import pygame
from game_data import stations

class Node(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((100,80))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)

class Overworld:
    def __init__(self, start_station, end_station, surface):

        #setup
        self.display_surface = surface
        self.end_station = end_station
        self.current_station = start_station

        #sprites
        self.setup_nodes()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(stations.values()):
            if index <= self.end_station:
                node_sprite = Node(node_data['node_pos'])
                self.nodes.add(node_sprite)

    def run(self):
        self.nodes.draw(self.display_surface)