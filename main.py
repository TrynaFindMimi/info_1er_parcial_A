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
FLOOR_Y = 120        # altura superior del piso (top surface)
FLOOR_HEIGHT = 300   # alto del rectángulo del piso
FLOOR_COLOR = (60, 179, 113)  # verde agradable


class App(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("assets/img/background3.png")
        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)

        # Piso como cuerpo estático tipo caja (impide atravesar)
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        # posicionar el centro de la caja para que su borde superior esté en FLOOR_Y
        floor_center_y = FLOOR_Y - FLOOR_HEIGHT / 2
        floor_body.position = (WIDTH / 2, floor_center_y)
        floor_shape = pymunk.Poly.create_box(floor_body, (WIDTH, FLOOR_HEIGHT))
        floor_shape.friction = 10.0
        floor_shape.elasticity = 0.0
        floor_shape.collision_type = 1
        self.space.add(floor_body, floor_shape)

        self.floor_body = floor_body
        self.floor_shape = floor_shape

        self.sprites = arcade.SpriteList()
        self.birds = arcade.SpriteList()
        self.world = arcade.SpriteList()
        self.add_columns()
        self.add_pigs()

        # inicio de la parábola ligeramente por encima de la superficie del piso
        self.fixed_start = Point2D(50, FLOOR_Y + 18)
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
            # colocar columnas sobre el piso
            column = Column(x, FLOOR_Y + 80, self.space)
            self.sprites.append(column)
            self.world.append(column)

    def add_pigs(self):
        # Estructura de cerdos en forma triangular
        # Cerdo base izquierdo
        pig1 = Pig(WIDTH / 2 - 30, FLOOR_Y + 70, self.space)
        # Cerdo base derecho
        pig2 = Pig(WIDTH / 2 + 30, FLOOR_Y + 70, self.space)
        # Cerdo superior
        pig3 = Pig(WIDTH / 2, FLOOR_Y + 120, self.space)
        
        for pig in [pig1, pig2, pig3]:
            self.sprites.append(pig)
            self.world.append(pig)

    def on_update(self, delta_time: float):
        self.space.step(1 / 60.0)
        self.update_collisions()
        self.sprites.update(delta_time)
        
        for bird in self.birds[:]:
            if getattr(bird, 'should_remove', False):
                bird.remove_from_sprite_lists()
                self.space.remove(bird.shape, bird.body)

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
            
            if y < FLOOR_Y:
                y = FLOOR_Y
                points.append((x, y))
                break
            points.append((x, y))
        return points

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))
        
        arcade.draw_lrbt_rectangle_filled(
            0,                         
            WIDTH,                     
            FLOOR_Y - FLOOR_HEIGHT,    
            FLOOR_Y,                   
            FLOOR_COLOR
        )
        self.sprites.draw()
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