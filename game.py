import pygame
import time
from window import Window

class Game():

    def __init__(self):
        pygame.init()
        self.window = Window()
        self.clock = pygame.time.Clock()

    def start(self):
        while not self.event_handler(): 
            self.clock.tick(60) 
            self.window.draw()
            

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.VIDEORESIZE:
                #chosen_background = pygame.image.load("background1.jpg")
                #background = pygame.transform.smoothscale(chosen_background, self.window.window.get_size())
                print(self.window.screen.get_size())
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                pygame.draw.rect(self.window.screen, (0, 255, 0), (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], 10, 10))
                
