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
        static: bool = False,
    ):
        
        super().__init__(image_path, 0.1) 
    
        
        body_type = pymunk.Body.STATIC if static else pymunk.Body.DYNAMIC
        moment = pymunk.moment_for_circle(mass, 0, radius) if not static else float('inf')
        body = pymunk.Body(mass, moment, body_type=body_type)
        body.position = (x, y)
        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

        if not static:
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
        
        pass