import pygame


class Window:

    def __init__(self, width = 640, height = 480):
        self.width = width
        self.height = height
        pygame.display.set_caption("Vegetable Samurai")
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        font_path = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_path, 48)
        self.background_image = pygame.image.load("background1.jpg").convert()

    def draw_background(self):
        pygame.display.flip()
        self.screen.blit(self.background_image, (0, 0))

    def resize(self, new_size):
        scale_factor = min(new_size[0] / self.width, new_size[1] / self.height)
        self.screen = pygame.display.set_mode((int(self.width * scale_factor), int(self.height * scale_factor)),
                                                pygame.RESIZABLE)
        self.background_image = pygame.transform.scale(self.background_image, (
        int(self.width * scale_factor), int(self.height * scale_factor)))
        self.draw_background()
        pygame.transform.smoothscale(self.background_image, self.screen.get_size())

