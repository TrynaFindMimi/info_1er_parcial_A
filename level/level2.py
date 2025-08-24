from characters.pig import Pig
from objects.column import Column
from objects.passiveObject import PassiveObject
from objects.sling import Sling
from characters.redBird import RedBird

def get_objects(space):
    """Devuelve los sprites para el nivel 2 (torre alta)."""
    objects = [
        # Honda al extremo izquierdo
        Sling(space, x=200, y=138),
        # Pájaro inicial en la honda
        RedBird(impulse_vector=None, x=50, y=138, space=space, power_multiplier=0, static=True),
        # Torre alta
        Pig(x=850, y=190, space=space),  # Base
        Column(x=850, y=220, space=space),  # Soporte
        Pig(x=850, y=260, space=space),  # Segundo nivel
        PassiveObject(image_path="assets/img/beam.png", x=850, y=290, space=space),  # Bloque
        Pig(x=850, y=320, space=space),  # Cima
        Column(x=910, y=190, space=space),  # Soporte lateral
        PassiveObject(image_path="assets/img/beam.png", x=910, y=230, space=space)  # Bloque lateral
    ]
    return objects