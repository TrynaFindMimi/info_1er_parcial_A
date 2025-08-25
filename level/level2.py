from characters.pig import Pig
from objects.column import Column
from objects.passiveObject import PassiveObject
from objects.sling import Sling


def get_objects(space):
    """Devuelve los sprites para el nivel 2 (torre alta)."""
    objects = [
        # Honda al extremo izquierdo
        Sling(space, x=200, y=138),
        
        # Base de la pirámide
        Column(x=800, y=190, space=space),
        PassiveObject(image_path="assets/img/beam.png", x=870, y=215, space=space, collision_layer=1),
        Column(x=940, y=190, space=space),

        # Primer nivel
        Pig(x=870, y=260, space=space),
        Column(x=870, y=290, space=space),
        
        # Cima de la pirámide
        Pig(x=870, y=320, space=space),


        Pig(x=740, y=190, space=space),
        Column(x=740, y=220, space=space),
        PassiveObject(image_path="assets/img/beam.png", x=740, y=250, space=space)
    ]
    return objects