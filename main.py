import math
import logging
import arcade
import pymunk

from game_object import Bird, Column, Pig
from game_logic import get_impulse_vector, Point2D, get_distance

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARNING)
logging.getLogger("pymunk").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

logger = logging.getLogger("main")

WIDTH = 1800
HEIGHT = 800
TITLE = "Angry birds"
GRAVITY = -900


class App(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("assets/img/background3.png")
        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)

        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, [0, 15], [WIDTH, 15], 0.0)
        floor_shape.friction = 10
        self.space.add(floor_body, floor_shape)

        self.sprites = arcade.SpriteList()
        self.birds = arcade.SpriteList()
        self.world = arcade.SpriteList()
        self.add_columns()
        self.add_pigs()

        self.fixed_start = Point2D(50, 20)
        self.end_point = Point2D(200, 100)
        self.draw_line = False

        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler

    def collision_handler(self, arbiter, space, data):
        impulse_norm = arbiter.total_impulse.length
        if impulse_norm < 100:
            return True
        logger.debug(impulse_norm)
        if impulse_norm > 1200:
            for obj in self.world:
                if obj.shape in arbiter.shapes:
                    obj.remove_from_sprite_lists()
                    self.space.remove(obj.shape, obj.body)

        return True

    def add_columns(self):
        for x in range(WIDTH // 2, WIDTH, 400):
            column = Column(x, 50, self.space)
            self.sprites.append(column)
            self.world.append(column)

    def add_pigs(self):
        pig1 = Pig(WIDTH / 2, 100, self.space)
        self.sprites.append(pig1)
        self.world.append(pig1)

    def on_update(self, delta_time: float):
        self.space.step(1 / 60.0)
        self.update_collisions()
        self.sprites.update(delta_time)

    def update_collisions(self):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.end_point = Point2D(x, y)
            self.draw_line = True
            logger.debug(f"Start Point: {self.fixed_start}")

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if buttons == arcade.MOUSE_BUTTON_LEFT:
            self.end_point = Point2D(x, y)
            logger.debug(f"Dragging to: {self.end_point}")

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            logger.debug(f"Releasing from: {self.end_point}")
            self.draw_line = False
            impulse_vector = get_impulse_vector(self.fixed_start, self.end_point)
            bird = Bird("assets/img/red-bird3.png", impulse_vector, self.fixed_start.x, self.fixed_start.y, self.space, power_multiplier=60)  # power_multiplier aumentado
            self.sprites.append(bird)
            self.birds.append(bird)

    def calculate_trajectory(self, start_point, end_point, steps=50):
        from game_logic import get_impulse_vector
        impulse_vector = get_impulse_vector(start_point, end_point)
        g = -GRAVITY
        mass = 5
        power_multiplier = 60  
        max_impulse = 100
        impulse = min(max_impulse, impulse_vector.impulse) * power_multiplier
        angle = impulse_vector.angle
        v0 = impulse / mass
        vx = v0 * math.cos(angle)
        vy = v0 * math.sin(angle)
        points = []
        t_total = 2 * vy / g if g != 0 else 1
        t_total = max(t_total, 0.5)
        for i in range(steps):
            t = t_total * i / steps
            x = start_point.x + vx * t
            y = start_point.y + vy * t - 0.5 * g * t * t
            if y < 15:
                y = 15
                points.append((x, y))
                break
            points.append((x, y))
        return points

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))
        self.sprites.draw()
        arcade.draw_line(0, 15, WIDTH, 15, arcade.color.DARK_BROWN, 4)
        if self.draw_line:
            trajectory = self.calculate_trajectory(self.fixed_start, self.end_point, steps=50)
            if len(trajectory) > 1:
                for i in range(len(trajectory) - 1):
                    if i % 2 == 0:
                        arcade.draw_line(
                            trajectory[i][0], trajectory[i][1],
                            trajectory[i+1][0], trajectory[i+1][1],
                            arcade.color.GRAY, 2
                        )


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    game = App()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()