import arcade
from game_logic import Point2D

class Sling(arcade.Sprite):
    def __init__(self, space, x: float, y: float):
        super().__init__("assets/img/sling-3.png", scale=0.2)
    
        self.center_x = x
        self.center_y = y
        self.space = space

    def draw(self):
        super().draw()

    def draw_elastic(self, start_point: Point2D, end_point: Point2D):
        arcade.draw_line(
            start_point.x, start_point.y,
            end_point.x, end_point.y,
            arcade.color.RED, 4
        )

        offset_x, offset_y = (end_point.x - start_point.x) * 0.1, (end_point.y - start_point.y) * 0.1
        arcade.draw_line(
            start_point.x + offset_x, start_point.y + offset_y,
            end_point.x, end_point.y,
            arcade.color.RED, 4
        )