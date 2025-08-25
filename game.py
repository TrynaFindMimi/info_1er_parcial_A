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
from objects.passiveObject import PassiveObject
from objects.sling import Sling

from level.level1 import get_objects as get_level1_objects
from level.level2 import get_objects as get_level2_objects

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARNING)
logging.getLogger("pymunk").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)
logger = logging.getLogger("game")

WIDTH = 1800
HEIGHT = 800
GRAVITY = -900
FLOOR_Y = 120
FLOOR_HEIGHT = 300
FLOOR_COLOR = (60, 179, 113)

class App(arcade.View):
    def __init__(self):
        super().__init__()
        self.game_init()

    def game_init(self):
        self.background = arcade.load_texture("assets/img/background3.png")

        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)
        
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
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
        
        self.current_level = 1
        self.load_level(self.current_level)
        
        self.bird_queue = [YellowBird, RedBird, BlueBird]
        self.current_bird_index = 0
        
        self.fixed_start = Point2D(200, FLOOR_Y + 25)
        self.end_point = Point2D(200, 100)
        self.draw_line = False
        
        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler
        
        self.paused = False
        
        self.can_launch_bird = True
        self.is_bird_in_air = False
        self.no_more_birds = False
        self.enemies_alive = False

    def load_level(self, level_id):
        self.sprites.clear()
        self.birds.clear()
        self.world.clear()
        
        if level_id == 1:
            level_objects = get_level1_objects(self.space)
        elif level_id == 2:
            level_objects = get_level2_objects(self.space)
        else:
            raise FileNotFoundError(f"Level {level_id} not found.")

        for obj in level_objects:
            self.sprites.append(obj)
            if isinstance(obj, (Pig, Column, PassiveObject)):
                self.world.append(obj)
            elif isinstance(obj, (RedBird, BlueBird, YellowBird)):
                self.birds.append(obj)
        self.current_bird_index = 0
        self.no_more_birds = False
        self.can_launch_bird = True
        self.enemies_alive = any(isinstance(obj, Pig) for obj in self.world)

    def collision_handler(self, arbiter, space, data):
        impulse_norm = arbiter.total_impulse.length
        if impulse_norm < 100:
            return True
        print(f"Collision impulse: {impulse_norm}")
        if impulse_norm > 1200:
            for obj in self.world[:]:
                if obj.shape in arbiter.shapes:
                    if isinstance(obj, Pig):
                        obj.remove_from_sprite_lists()
                        self.space.remove(obj.shape, obj.body)
                    elif isinstance(obj, Column):
                        obj.remove_from_sprite_lists()
                        self.space.remove(obj.shape, obj.body)
        return True

    def check_for_pigs(self):
        return any(isinstance(obj, Pig) for obj in self.world)

    def on_update(self, delta_time: float):
        if not self.paused:
            self.space.step(1 / 60.0)
            self.sprites.update(delta_time)
            
            self.is_bird_in_air = any(bird.body.velocity.length > 50 for bird in self.birds)

            if not self.is_bird_in_air and not self.can_launch_bird and not self.no_more_birds:
                self.can_launch_bird = True
            
            if not self.is_bird_in_air and self.no_more_birds:
                if self.check_for_pigs():
                    self.enemies_alive = True
                    self.paused = True
                else:
                    self.next_level()
            
            for bird in self.birds[:]:
                if getattr(bird, 'should_remove', False) or bird.center_y < -100:
                    bird.remove_from_sprite_lists()
                    self.space.remove(bird.shape, bird.body)
            
            if not self.check_for_pigs() and not self.is_bird_in_air:
                self.next_level()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and not self.paused:
            if self.can_launch_bird and not self.no_more_birds:
                self.end_point = Point2D(x, y)
                self.draw_line = True
                logger.debug(f"Start Point: {self.fixed_start}")
            
            elif self.is_bird_in_air and self.birds:
                current_bird = self.birds[-1]
                
                # We've changed the logic here to always call the special ability.
                new_birds = current_bird.activate_special()
                
                # Now we only handle the new birds if the ability actually returns them.
                if new_birds:
                    current_bird.remove_from_sprite_lists()
                    self.space.remove(current_bird.shape, current_bird.body)
                    
                    for new_bird in new_birds:
                        self.sprites.append(new_bird)
                        self.birds.append(new_bird)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if buttons == arcade.MOUSE_BUTTON_LEFT and not self.paused:
            self.end_point = Point2D(x, y)
            logger.debug(f"Dragging to: {self.end_point}")

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if self.can_launch_bird and button == arcade.MOUSE_BUTTON_LEFT and not self.paused and not self.no_more_birds:
            logger.debug(f"Releasing from: {self.end_point}")
            self.draw_line = False
            
            bird_class = self.bird_queue[self.current_bird_index]
            impulse_vector = get_impulse_vector(self.fixed_start, self.end_point)
            bird = bird_class(impulse_vector, self.fixed_start.x, self.fixed_start.y, self.space, power_multiplier=60)
            self.sprites.append(bird)
            self.birds.append(bird)
            self.current_bird_index += 1
            self.can_launch_bird = False
            self.is_bird_in_air = True
            
            if self.current_bird_index >= len(self.bird_queue):
                self.no_more_birds = True
                self.can_launch_bird = False

            for sprite in self.birds[:]:
                if getattr(sprite, 'static', False):
                    sprite.remove_from_sprite_lists()
                    self.space.remove(sprite.shape, sprite.body)
                    break

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
        if self.draw_line and not self.no_more_birds:
            trajectory = self.calculate_trajectory(self.fixed_start, self.end_point, steps=50)
            if len(trajectory) > 1:
                for i in range(min(30, len(trajectory))):
                    point = trajectory[i]
                    alpha_value = int(255 * (1 - i / 30))
                    color = (128, 128, 128, alpha_value)
                    arcade.draw_circle_filled(point[0], point[1], 1.5, color)
        
        if self.paused:
            arcade.draw_text("PAUSED", WIDTH / 2, HEIGHT / 2, arcade.color.WHITE, 50, anchor_x="center")

        if self.enemies_alive and self.paused:
            arcade.draw_text("¡Nivel Fallido! Presiona 'R' para reiniciar",
                             WIDTH / 2, HEIGHT / 2 - 50,
                             arcade.color.RED, 30, anchor_x="center")

    def toggle_pause(self):
        self.paused = not self.paused

    def restart_level(self):
        self.game_init()

    def next_level(self):
        self.current_level += 1
        try:
            self.load_level(self.current_level)
        except FileNotFoundError:
            self.clear()
            arcade.draw_text("¡Juego completado!", WIDTH / 2, HEIGHT / 2, arcade.color.WHITE, 50, anchor_x="center")
            self.paused = True
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.R:
            if self.enemies_alive and self.paused:
                print("Reiniciando nivel por derrota...")
                self.restart_level()