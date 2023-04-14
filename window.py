import pygame

class Window:

    def __init__(self):
        pygame.display.set_caption("Vegetable Samurai")
        self.screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
        font_path = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_path, 48)
        
    def draw(self):
        pygame.display.update()
        background_image1 = pygame.image.load("background1.jpg") 
        self.screen.blit(background_image1,(0, 0))

        
        
        
    
