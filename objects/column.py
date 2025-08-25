from objects.passiveObject import PassiveObject
import math

class Column(PassiveObject):
    def __init__(self, x, y, space):
        #Inicializa la columna heredando de PassiveObject con la imagen especificada
        super().__init__("assets/img/column.png", x, y, space)
        #Rota el cuerpo 90 grados para que la columna sea vertical
        self.body.angle = math.pi / 2