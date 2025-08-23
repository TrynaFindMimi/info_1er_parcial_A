from objects.passiveObject import PassiveObject

class Column(PassiveObject):
    def __init__(self, x, y, space):
        super().__init__("assets/img/column.png", x, y, space)