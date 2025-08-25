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
        static: bool = False,
    ):
        #Inicializa el blue bird que hereda de Bird con valores específicos
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
            static,
        )

    def activate_special(self):
        print(f"Activando habilidad especial de BlueBird. Magnitud de velocidad actual: {self.body.velocity.length}")
        new_birds = []
        #Verifica si esta en vuelo el blue bird mediante la velocidad
        if self.body.velocity.length > 10:
            position = self.body.position
            velocity = self.body.velocity
            print(f"Creando 3 nuevos BlueBirds en posición {position} con velocidad base {velocity}")

            #Calcula el ángulo de la velocidad actual
            current_angle = math.atan2(velocity.y, velocity.x)
            print(f"Current angle: {math.degrees(current_angle)} degrees")

            #Define ángulos relativos para los nuevos pájaros (-30°, 0°, +30°)
            offsets = [-0.5236, 0, 0.5236]
            for i, offset in enumerate(offsets):
                new_angle = current_angle + offset
                # Desplaza la posición en y para evitar solapamiento
                offset_pos_y = position.y + (i - 1) * 5  # -5, 0, +5 pixels
                # Crea un nuevo pájaro azul en la posición ajustada
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
                #Aplica una nueva velocidad rotada con la misma magnitud
                magnitude = velocity.length
                new_velocity = pymunk.Vec2d(magnitude * math.cos(new_angle), magnitude * math.sin(new_angle))
                new_bird.body.velocity = new_velocity
                new_birds.append(new_bird)
                print(f"Nuevo pájaro {i+1} creado con velocidad {new_velocity} en posición ({position.x}, {offset_pos_y}), ángulo {math.degrees(new_angle)} grados")

            #Marca el pájaro original para eliminación
            self.should_remove = True
            print("BlueBird original marcado para eliminación")
        else:
            print("BlueBird no está en vuelo (velocidad demasiado baja), habilidad especial no activada")
        return new_birds