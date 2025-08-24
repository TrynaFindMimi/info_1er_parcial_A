from characters.pig import Pig
from objects.column import Column
from objects.passiveObject import PassiveObject
from objects.sling import Sling
from characters.redBird import RedBird

def get_objects(space):
    """Devuelve los sprites para el nivel 1 (estructura triangular)."""
    objects = [
        # Honda al extremo izquierdo
        Sling(space, x=50, y=138),
        # Pájaro inicial en la honda
        RedBird(impulse_vector=None, x=50, y=138, space=space, power_multiplier=0, static=True),
        # Estructura triangular
        Pig(x=870, y=190, space=space),  # Base izquierda
        Pig(x=930, y=190, space=space),  # Base derecha
        Pig(x=900, y=240, space=space),  # Cima
        Column(x=870, y=190, space=space),  # Soporte izquierda
        Column(x=930, y=190, space=space),  # Soporte derecha
        PassiveObject(image_path="assets/img/beam.png", x=900, y=215, space=space)  # Bloque central
    ]
    return objects