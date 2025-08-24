import arcade
import pymunk
from characters.bird import Bird

class YellowBird(Bird):
    def __init__(
        self,
        impulse_vector,
        x: float,
        y: float,
        space,
        mass: float = 5,
        radius: float = 12,
        max_impulse: float = 100,
        power_multiplier: float = 30,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
        static: bool = False,
    ):
        super().__init__(
            "assets/img/chuck.png",
            impulse_vector,
            x,
            y,
            space,
            mass,
            radius,
            max_impulse,
            power_multiplier,
            elasticity,
            friction,
            collision_layer,
            static,
        )

    def activate_special(self):
        if self.body.body_type == pymunk.Body.DYNAMIC:
            self.body.velocity = self.body.velocity * 8