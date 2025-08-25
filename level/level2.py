from characters.pig import Pig
from objects.column import Column
from objects.passiveObject import PassiveObject
from objects.sling import Sling

def get_objects(space):
    objects = [
            Sling(space, x=200, y=138),
            Column(x=970, y=190, space=space),
            Column(x=1070, y=190, space=space),
            PassiveObject("assets/img/beam.png", x=1020, y=250, space=space, collision_layer=1),

            Column(x=995, y=310, space=space),
            Column(x=1045, y=310, space=space),
            PassiveObject("assets/img/beam.png", x=1020, y=370, space=space, collision_layer=1),
            Pig(x=1020, y=410, space=space),
        ]

    return objects