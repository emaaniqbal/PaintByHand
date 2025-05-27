import pygame


class UIshape:
    """
    Shape class to simplfy adding UI elements into pygame interface
    """

    def __init__(self, clr, x, y, sizex=40, sizey=40, des=""):
        self.clr = clr
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, sizex, sizey)
        self.des = des
