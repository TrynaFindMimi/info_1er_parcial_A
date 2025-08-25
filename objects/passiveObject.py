import arcade
import pymunk
from utils import create_box_body_and_shape

class PassiveObject(arcade.Sprite):
    def __init__(
        self,
        image_path: str,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.2,
        friction: float = 8,
        collision_layer: int = 0,
    ):
        #Inicializa el sprite con la imagen especificada y escala predeterminada
        super().__init__("assets/img/beam.png", 1)
        #Crea un cuerpo físico y una forma rectangular usando una función auxiliar
        self.body, self.shape = create_box_body_and_shape(
            space, mass, (self.width, self.height), (x, y), elasticity, friction, collision_layer
        )

    def update(self, delta_time):
        #Actualiza la posición y rotación del sprite según el cuerpo físico
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle