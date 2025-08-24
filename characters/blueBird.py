import pymunk
import math
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
        print(f"Activating BlueBird special. Current velocity length: {self.body.velocity.length}")
        new_birds = []  # Lista para retornar
        if self.body.velocity.length > 10:  # Umbral para asegurar vuelo
            position = self.body.position
            velocity = self.body.velocity
            print(f"Creating 3 new BlueBirds at position {position} with base velocity {velocity}")

            # Calcular la dirección actual (en radianes)
            current_angle = math.atan2(velocity.y, velocity.x)
            print(f"Current angle: {math.degrees(current_angle)} degrees")

            # Definir offsets relativos a la dirección actual (-30°, 0°, +30°)
            offsets = [-0.5236, 0, 0.5236]  # -30°, 0°, +30° en radianes
            for i, offset in enumerate(offsets):
                new_angle = current_angle + offset
                # Offset en posición para evitar overlap (5 pixels en y por offset)
                offset_pos_y = position.y + (i - 1) * 5  # -5, 0, +5 pixels
                new_bird = BlueBird(
                    impulse_vector=None,
                    x=position.x,
                    y=offset_pos_y,
                    space=self.shape.space,
                    mass=self.body.mass,
                    radius=self.shape.radius,
                    elasticity=self.shape.elasticity,
                    friction=self.shape.friction,
                    collision_layer=self.shape.collision_type
                )
                # Calcular nueva velocity rotada según el nuevo ángulo, manteniendo magnitud
                magnitude = velocity.length
                new_velocity = pymunk.Vec2d(magnitude * math.cos(new_angle), magnitude * math.sin(new_angle))
                new_bird.body.velocity = new_velocity
                new_birds.append(new_bird)
                print(f"New bird {i+1} created with velocity {new_velocity} at position ({position.x}, {offset_pos_y}), angle {math.degrees(new_angle)} degrees")

            # Remover el pájaro original
            self.should_remove = True
            print("Original BlueBird marked for removal")
        else:
            print("BlueBird not in flight (velocity too low), special not activated")
        return new_birds  # Retorna la lista (vacía si no en vuelo)