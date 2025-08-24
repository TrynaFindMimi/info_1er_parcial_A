from objects.passiveObject import PassiveObject
import math

class Column(PassiveObject):
    def __init__(self, x, y, space):
        super().__init__("assets/img/column.png", x, y, space)
        # Set the body's angle to make it vertical
        self.body.angle = math.pi / 2