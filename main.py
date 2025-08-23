import math
import logging
import arcade
import pymunk
from game_logic import get_impulse_vector, Point2D
from characters.redBird import RedBird
from characters.blueBird import BlueBird
from characters.yellowBird import YellowBird
from characters.pig import Pig
from objects.column import Column
from objects.sling import Sling
from levels import load_level
from ui.buttons import PauseButton, RestartButton, NextButton
from ui.scoreboard import Scoreboard
from assets.sounds import SoundManager

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARNING)
logging.getLogger("pymunk").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)
logger = logging.getLogger("main")

# Constantes
WIDTH = 1800
HEIGHT = 800
TITLE = "Angry Birds"
GRAVITY = -900
FLOOR_Y = 120        # altura superior del piso (top surface)
FLOOR_HEIGHT = 300   # alto del rectángulo del piso
FLOOR_COLOR = (60, 179, 113)  # verde agradable

class App(arcade.View):
    def __init__(self):
        super().__init__()
        # Fondo
        self.background = arcade.load_texture("assets/img/background3.png")
        
        # Física
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
        
        # Sprites
        self.sprites = arcade.SpriteList()
        self.birds = arcade.SpriteList()
        self.world = arcade.SpriteList()
        
        # Niveles
        self.current_level = 1
        self.load_level(self.current_level)
        
        # Cola de pájaros
        self.bird_queue = [RedBird, BlueBird, YellowBird]
        self.current_bird_index = 0
        
        # Resorte/Honda
        self.sling = Sling(self.space, 50, FLOOR_Y + 18)
        
        # Sistema de puntaje
        self.scoreboard = Scoreboard()
        
        # Interfaz de usuario
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        self.pause_button = PauseButton(50, HEIGHT - 50, self)
        self.restart_button = RestartButton(150, HEIGHT - 50, self)
        self.next_button = NextButton(250, HEIGHT - 50, self)
        self.ui_manager.add(self.pause_button)
        self.ui_manager.add(self.restart_button)
        self.ui_manager.add(self.next_button)
        
        # Sonidos
        self.sound_manager = SoundManager()
        
        # inicio de la parábola ligeramente por encima de la superficie del piso
        self.fixed_start = Point2D(50, FLOOR_Y + 18)
        self.end_point = Point2D(200, 100)
        self.draw_line = False
        
        # Manejador de colisiones
        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler
        
        # Estado de pausa
        self.paused = False

    def load_level(self, level_id):
        """Carga un nivel desde levels/level_{level_id}.json"""
        self.sprites.clear()
        self.birds.clear()
        self.world.clear()
        level_objects = load_level(level_id)
        for obj in level_objects:
            self.sprites.append(obj)
            if not isinstance(obj, arcade.Sprite):  # Evitar agregar StaticObject sin cuerpo
                self.world.append(obj)
        self.current_bird_index = 0
        self.scoreboard.reset()

    def collision_handler(self, arbiter, space, data):
        impulse_norm = arbiter.total_impulse.length
        if impulse_norm < 100:
            return True
        logger.debug(f"Collision impulse: {impulse_norm}")
        if impulse_norm > 1200:
            for obj in self.world[:]:
                if obj.shape in arbiter.shapes:
                    points = 100 if isinstance(obj, Pig) else 50
                    self.scoreboard.add_points(points)
                    obj.remove_from_sprite_lists()
                    self.space.remove(obj.shape, obj.body)
                    self.sound_manager.play_destroy()
        return True

    def on_update(self, delta_time: float):
        if not self.paused:
            self.space.step(1 / 60.0)
            self.sprites.update(delta_time)
            for bird in self.birds[:]:
                if getattr(bird, 'should_remove', False):
                    bird.remove_from_sprite_lists()
                    self.space.remove(bird.shape, bird.body)
            if not self.world and self.birds:  # Nivel completado
                self.next_level()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and not self.paused:
            self.end_point = Point2D(x, y)
            self.draw_line = True
            logger.debug(f"Start Point: {self.fixed_start}")

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if buttons == arcade.MOUSE_BUTTON_LEFT and not self.paused:
            self.end_point = Point2D(x, y)
            logger.debug(f"Dragging to: {self.end_point}")

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT and not self.paused:
            logger.debug(f"Releasing from: {self.end_point}")
            self.draw_line = False
            if self.current_bird_index < len(self.bird_queue):
                impulse_vector = get_impulse_vector(self.fixed_start, self.end_point)
                bird_class = self.bird_queue[self.current_bird_index]
                bird = bird_class(impulse_vector, self.fixed_start.x, self.fixed_start.y, self.space, power_multiplier=60)
                self.sprites.append(bird)
                self.birds.append(bird)
                self.current_bird_index += 1
                self.sound_manager.play_launch()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.birds and not self.paused:
            self.birds[-1].activate_special()
            self.sound_manager.play_special()

    def calculate_trajectory(self, start_point, end_point, steps=50):
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
            0, WIDTH, FLOOR_Y - FLOOR_HEIGHT, FLOOR_Y, FLOOR_COLOR
        )
        self.sprites.draw()
        self.sling.draw()
        if self.draw_line:
            trajectory = self.calculate_trajectory(self.fixed_start, self.end_point, steps=50)
            if len(trajectory) > 1:
                for i in range(len(trajectory) - 1):
                    if i % 2 == 0:
                        arcade.draw_line(
                            trajectory[i][0], trajectory[i][1],
                            trajectory[i + 1][0], trajectory[i + 1][1],
                            arcade.color.GRAY, 2
                        )
            self.sling.draw_elastic(self.fixed_start, self.end_point)
        self.scoreboard.draw()
        self.ui_manager.draw()
        if self.paused:
            arcade.draw_text("PAUSED", WIDTH / 2, HEIGHT / 2, arcade.color.WHITE, 50, anchor_x="center")

    def toggle_pause(self):
        self.paused = not self.paused

    def restart_level(self):
        self.load_level(self.current_level)

    def next_level(self):
        self.current_level += 1
        try:
            self.load_level(self.current_level)
        except FileNotFoundError:
            # Último nivel completado
            arcade.draw_text("GAME COMPLETED!", WIDTH / 2, HEIGHT / 2, arcade.color.WHITE, 50, anchor_x="center")
            self.paused = True

def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    game = App()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()