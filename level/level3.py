from characters.pig import Pig
from objects.column import Column
from objects.passiveObject import PassiveObject
from objects.sling import Sling

def get_objects(space):
    objects = [
        Sling(space, x=200, y=138),

        Column(x=875, y=140, space=space),
        Column(x=925, y=140, space=space),
        Column(x=975, y=140, space=space),
        Column(x=1025, y=140, space=space),
        Column(x=1075, y=140, space=space),
        PassiveObject(image_path="assets/img/beam.png", x=880, y=190, space=space),
        PassiveObject(image_path="assets/img/beam.png", x=970, y=190, space=space),
        PassiveObject(image_path="assets/img/beam.png", x=1050, y=190, space=space),
        Column(x=945, y=250, space=space),
        Column(x=1005, y=250, space=space),
        PassiveObject(image_path="assets/img/beam.png", x=975, y=300, space=space),
        Column(x=975, y=360, space=space),
        PassiveObject(image_path="assets/img/beam.png", x=975, y=420, space=space),
        
        Pig(x=900, y=240, space=space),
        Pig(x=1050, y=240, space=space),
        Pig(x=975, y=440, space=space),

        
    
    
    ]
    return objects