from characters.pig import Pig
from objects.column import Column
from objects.passiveObject import PassiveObject
from objects.sling import Sling
from characters.redBird import RedBird

def get_objects(space):
    """Devuelve los sprites para el nivel 3 (pirámide)."""
    objects = [
        # Honda al extremo izquierdo
        Sling(space, x=50, y=138),
        # Pájaro inicial en la honda
        RedBird(impulse_vector=None, x=50, y=138, space=space, power_multiplier=0, static=True),
        # Pirámide
        Pig(x=860, y=190, space=space),  # Base izquierda
        Pig(x=940, y=190, space=space),  # Base derecha
        Column(x=860, y=190, space=space),  # Soporte base izquierda
        Column(x=940, y=190, space=space),  # Soporte base derecha
        PassiveObject(image_path="assets/img/beam.png", x=900, y=230, space=space),  # Bloque intermedio
        Pig(x=900, y=260, space=space),  # Cima
        Column(x=880, y=260, space=space),  # Soporte cima izquierda
        PassiveObject(image_path="assets/img/beam.png", x=920, y=260, space=space)  # Bloque cima derecha
    ]
    return objects