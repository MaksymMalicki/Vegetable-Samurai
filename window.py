"""
Window module is responsible for creating a window with given width, height,
font and background image.
"""

import pygame


class Window:
    """
    Class Window:
    attributes:
        width: window width
        height: window height
        screen: pygame object
        font: pygame font used for counters
        background_image: pygame image displayed in the background
    methods:
        contructor: assigns the provided values to the class attributes
        draw_background:
        resize: responsible for resizing with correct scale
    """

    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        pygame.display.set_caption("Vegetable Samurai")
        self.screen = pygame.display.set_mode((width, height))
        font_path = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_path, 48)
        self.background_image = pygame.image.load("images/background2.jpg").convert()

    def draw_background(self):
        """
        draw_background() is responsible for displaying the image in the back of the window
        :param
        :return: none
        """
        pygame.display.flip()
        self.screen.blit(self.background_image, (0, 0))

    def resize(self, new_size):
        """
        resize() method is responsible for resizing the window correctly, maintaining the scale
        :param
            new_size: the size of the new window
        :return: none
        """
        scale_factor = min(new_size[0] / self.width, new_size[1] / self.height)
        self.screen = pygame.display.set_mode((int(self.width * scale_factor), int(self.height * scale_factor)))
        self.background_image = pygame.transform.scale(self.background_image, (
            int(self.width * scale_factor), int(self.height * scale_factor)))
        self.draw_background()
        pygame.transform.smoothscale(self.background_image, self.screen.get_size())
