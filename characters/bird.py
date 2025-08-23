import arcade
import pymunk
from game_logic import ImpulseVector
from utils import create_circle_body_and_shape

class Bird(arcade.Sprite):
    def __init__(
        self,
        image_path: str,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 5,
        radius: float = 12,
        max_impulse: float = 100,
        power_multiplier: float = 30,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)
        self.body, self.shape = create_circle_body_and_shape(
            space, mass, radius, (x, y), elasticity, friction, collision_layer
        )
        impulse = min(max_impulse, impulse_vector.impulse) * power_multiplier
        impulse_pymunk = impulse * pymunk.Vec2d(1, 0)
        self.body.apply_impulse_at_local_point(impulse_pymunk.rotated(impulse_vector.angle))
        self.time_low_energy = 0
        self.should_remove = False

    def update(self, delta_time):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle
        velocity = self.body.velocity.length
        if velocity < 20:
            self.time_low_energy += delta_time
            if self.time_low_energy >= 3.0:
                self.should_remove = True
        else:
            self.time_low_energy = 0

    def activate_special(self):
        """Método para efectos especiales, implementado por subclases."""
        pass