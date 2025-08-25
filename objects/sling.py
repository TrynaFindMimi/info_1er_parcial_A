import arcade
from game_logic import Point2D

class Sling(arcade.Sprite):
    #Inicializa el sprite de la imagen de la honda y escala específica
    def __init__(self, space, x: float, y: float):
        super().__init__("assets/img/sling-3.png", scale=0.2)
    
        self.center_x = x
        self.center_y = y
        self.space = space

    def draw(self):
        super().draw()