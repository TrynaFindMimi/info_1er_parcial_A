from characters.pig import Pig
from objects.column import Column
from objects.passiveObject import PassiveObject
from objects.sling import Sling

def get_objects(space):
    """Devuelve los sprites para el nivel 1 (estructura triangular)."""
    objects = [
        Sling(space, x=200, y=138),
        Column(x=927, y=190, space=space), 
        Pig(x=997, y=200, space=space),
        Column(x=1015, y=190, space=space),
        Column(x=1035, y=190, space=space), 
        Pig(x=1047, y=200, space=space),
        Column(x=1105, y=190, space=space), 
        PassiveObject("assets/img/beam.png", x=975, y=250, space=space, collision_layer=1),
        PassiveObject("assets/img/beam.png", x=1075, y=250, space=space, collision_layer=1),
        Column(x=995, y=310, space=space),
        Pig(x=1037, y=350, space=space),
        Column(x=1065, y=310, space=space),
        PassiveObject("assets/img/beam.png", x=1035, y=400, space=space, collision_layer=1),
    ]

    return objects
