import arcade
import pymunk
from utils import create_circle_body_and_shape

class Pig(arcade.Sprite):
    def __init__(
        self,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.8,
        friction: float = 0.4,
        collision_layer: int = 0,
    ):
        #Inicializa el sprite con la imagen del cerdo y escala
        super().__init__("assets/img/pig_failed.png", 0.15)
        #Calcula el radio basado en el ancho del sprite
        radius = self.width / 2 - 3
        # Crea el cuerpo físico y la forma circular usando una función auxiliar
        self.body, self.shape = create_circle_body_and_shape(
            space, mass, radius, (x, y), elasticity, friction, collision_layer
        )

    def update(self, delta_time):
        #Actualiza la posición y rotación del sprite según el cuerpo físico
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle