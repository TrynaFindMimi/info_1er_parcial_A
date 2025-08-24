import pymunk
from characters.bird import Bird

class BlueBird(Bird):
    def __init__(
        self,
        impulse_vector,
        x: float,
        y: float,
        space,
        mass: float = 3,  # Más ligero
        radius: float = 10,  # Más pequeño
        max_impulse: float = 100,
        power_multiplier: float = 30,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
        static: bool = False,  # Agrega el parámetro static
    ):
        super().__init__(
            "assets/img/blue.png",
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
            static,  # Pasa static al padre
        )

    def activate_special(self):
        """Divide el pájaro en 3 con trayectorias divergentes al hacer clic izquierdo mientras está en vuelo."""
        if self.body.velocity.length > 0:  # Verifica si el pájaro está en vuelo
            angle = self.body.angle
            position = self.body.position
            velocity = self.body.velocity
            # Crear tres pájaros con 30 grados de separación
            for offset in [-0.5236, 0, 0.5236]:  # -30, 0, +30 grados en radianes
                new_bird = BlueBird(
                    impulse_vector=None,
                    x=position.x,
                    y=position.y,
                    space=self.shape.space,
                    mass=self.body.mass,
                    radius=self.shape.radius
                )
                new_velocity = velocity.rotated(offset)
                new_bird.body.velocity = new_velocity
                self.shape.space.add(new_bird.body, new_bird.shape)
            # Remover el pájaro original
            self.should_remove = True