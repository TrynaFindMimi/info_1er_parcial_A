import arcade
from game_logic import Point2D

class Sling(arcade.Sprite):
    def __init__(self, space, x: float, y: float):
        """Inicializa la honda con un sprite estático en la posición (x, y)."""
        super().__init__("assets/img/sling-3.png", scale=1.0)
        self.center_x = x
        self.center_y = y
        self.space = space  # Guardar referencia al espacio físico (no usado actualmente)

    def draw(self):
        """Dibuja el sprite de la honda."""
        super().draw()

    def draw_elastic(self, start_point: Point2D, end_point: Point2D):
        """Dibuja las líneas elásticas de la honda desde start_point a end_point."""
        # Línea elástica frontal (desde start_point a end_point)
        arcade.draw_line(
            start_point.x, start_point.y,
            end_point.x, end_point.y,
            arcade.color.BROWN, 4
        )
        # Línea elástica trasera (simulada, ligeramente desplazada)
        offset_x, offset_y = 10, 0  # Desplazamiento para la segunda cuerda
        arcade.draw_line(
            start_point.x - offset_x, start_point.y - offset_y,
            end_point.x, end_point.y,
            arcade.color.BROWN, 4
        )