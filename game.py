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
from level.levels import load_level
from ui.scoreboard import Scoreboard
from ui.buttons import PauseButton, PlayButton, RestartButton, NextLevelButton

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARNING)
logging.getLogger("pymunk").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)
logger = logging.getLogger("game")

# Constantes del juego
WIDTH = 1800
HEIGHT = 800
GRAVITY = -900
FLOOR_Y = 120
FLOOR_HEIGHT = 300
FLOOR_COLOR = (60, 179, 113)

class App(arcade.View):
    """
    Clase principal del juego Angry Birds, que maneja toda la lógica,
    física y rendering.
    """
    def __init__(self):
        super().__init__()
        print("Initializing App")
        self.game_init()

    def game_init(self):
        """
        Configura todas las variables y objetos del juego.
        Esta función se llama al inicio y cada vez que se reinicia un nivel.
        """
        print("Starting game_init")
        self.background = arcade.load_texture("assets/img/background3.png")
        print("Background loaded")

        # Inicializa el espacio de PyMunk para la física
        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)
        print("Physics space initialized")
        
        # Configura el suelo estático
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
        print("Floor configured")
        
        self.sprites = arcade.SpriteList()
        self.birds = arcade.SpriteList()
        self.world = arcade.SpriteList()
        print("Sprite lists initialized")
        
        self.current_level = 3
        try:
            print(f"Attempting to load level {self.current_level}")
            self.load_level(self.current_level)
            print(f"Level {self.current_level} loaded successfully")
        except Exception as e:
            print(f"Error loading level {self.current_level}: {e}")
        
        self.bird_queue = [YellowBird, RedBird, BlueBird]
        self.current_bird_index = 0
        self.fixed_start = Point2D(200, FLOOR_Y + 25)
        self.end_point = Point2D(200, 100)
        self.draw_line = False
        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler
        self.paused = False
        self.scoreboard = Scoreboard(height=HEIGHT)  # Inicialización explícita después de load_level
        print("Scoreboard initialized")
        self.sprites.append(self.scoreboard)
        
        # Botones
        self.pause_button = PauseButton(self.toggle_pause, width=WIDTH, height=HEIGHT)
        self.restart_button = RestartButton(self.restart_level, width=WIDTH, height=HEIGHT)
        self.play_button = PlayButton(self.toggle_pause, width=WIDTH, height=HEIGHT)
        self.next_level_button = NextLevelButton(self.next_level, width=WIDTH, height=HEIGHT)
        self.sprites.append(self.pause_button)
        self.sprites.append(self.restart_button)
        print("Buttons initialized")
        
        self.can_launch_bird = True
        self.is_bird_in_air = False
        self.level_won = False
        print("Game initialization completed")

    def load_level(self, level_id):
        print(f"Loading level {level_id}")
        self.sprites.clear()
        self.birds.clear()
        self.world.clear()
        level_objects = load_level(level_id, self.space)
        for obj in level_objects:
            self.sprites.append(obj)
            if isinstance(obj, (Pig, Column, PassiveObject)):
                self.world.append(obj)
            elif isinstance(obj, (RedBird, BlueBird, YellowBird)):
                self.birds.append(obj)
        self.current_bird_index = 0
        self.scoreboard.level = self.current_level
        print(f"Level {level_id} objects loaded")

    def collision_handler(self, arbiter, space, data):
        print("Collision detected")
        impulse_norm = arbiter.total_impulse.length
        if impulse_norm < 100:
            return True
        print(f"Collision impulse: {impulse_norm}")
        if impulse_norm > 1200:
            for obj in self.world[:]:
                if obj.shape in arbiter.shapes:
                    obj.remove_from_sprite_lists()
                    self.space.remove(obj.shape, obj.body)
                    if hasattr(self, 'scoreboard'):
                        print("Adding points to scoreboard")
                        self.scoreboard.add_points(100)
                    else:
                        print("Scoreboard not available")
        return True

    def on_update(self, delta_time: float):
        """Actualiza la posición de los sprites y la física."""
        print("Updating game state")
        if not self.paused:
            self.space.step(1 / 60.0)
            self.sprites.update(delta_time)
            
            # Revisa si hay pájaros en vuelo para mantener is_bird_in_air
            self.is_bird_in_air = any(bird.body.velocity.length > 50 for bird in self.birds)
            if not self.birds or all(bird.body.velocity.length < 50 or bird.center_y < -100 for bird in self.birds):
                self.can_launch_bird = True
                if not self.is_bird_in_air:
                    self.is_bird_in_air = False
            
            for bird in self.birds[:]:
                if getattr(bird, 'should_remove', False):
                    bird.remove_from_sprite_lists()
                    self.space.remove(bird.shape, bird.body)
                    print(f"Removed bird: {type(bird).__name__}")
            
            # Verificar victoria o derrota
            if not self.world:
                self.level_won = True
                self.paused = True
                print("Level won")
            elif not self.birds and self.world:
                self.restart_level()
                print("Level restarted due to loss")

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Maneja el clic del ratón: inicia el lanzamiento, activa habilidades o botones.
        """
        print(f"Mouse pressed at ({x}, {y})")
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.paused and not self.level_won:
                if self.play_button.collides_with_point((x, y)):
                    self.play_button.on_click()
                    print("Play button clicked")
            if self.level_won:
                if self.next_level_button.collides_with_point((x, y)):
                    self.next_level_button.on_click()
                    self.level_won = False
                    self.paused = False
                    print("Next level button clicked")
            if self.pause_button.collides_with_point((x, y)):
                self.pause_button.on_click()
                print("Pause button clicked")
            if self.restart_button.collides_with_point((x, y)):
                self.restart_button.on_click()
                print("Restart button clicked")
            
            if not self.paused and not self.level_won:
                if self.can_launch_bird:
                    self.end_point = Point2D(x, y)
                    self.draw_line = True
                    logger.debug(f"Start Point: {self.fixed_start}")
                    print("Bird launch started")
                elif self.is_bird_in_air and self.birds:
                    current_bird = self.birds[-1]
                    print(f"Attempting special for {type(current_bird).__name__} at position {current_bird.center_x}, {current_bird.center_y}")
                    new_birds = current_bird.activate_special()
                    if new_birds:
                        print(f"Adding {len(new_birds)} new birds to sprites and birds")
                        for new_bird in new_birds:
                            self.sprites.append(new_bird)
                            self.birds.append(new_bird)
                    else:
                        print("No new birds created")

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        """Maneja el arrastre del ratón para apuntar."""
        print(f"Mouse dragged to ({x}, {y})")
        if self.can_launch_bird and buttons == arcade.MOUSE_BUTTON_LEFT and not self.paused:
            self.end_point = Point2D(x, y)
            logger.debug(f"Dragging to: {self.end_point}")

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        """Maneja la liberación del ratón para lanzar el pájaro."""
        print(f"Mouse released at ({x}, {y})")
        if self.can_launch_bird and button == arcade.MOUSE_BUTTON_LEFT and not self.paused:
            logger.debug(f"Releasing from: {self.end_point}")
            self.draw_line = False
            if self.current_bird_index < len(self.bird_queue):
                impulse_vector = get_impulse_vector(self.fixed_start, self.end_point)
                bird_class = self.bird_queue[self.current_bird_index]
                bird = bird_class(impulse_vector, self.fixed_start.x, self.fixed_start.y, self.space, power_multiplier=60)
                self.sprites.append(bird)
                self.birds.append(bird)
                self.current_bird_index += 1
                self.can_launch_bird = False
                self.is_bird_in_air = True
                print(f"Launched {bird_class.__name__}")
                for sprite in self.birds[:]:
                    if getattr(sprite, 'static', False):
                        sprite.remove_from_sprite_lists()
                        self.space.remove(sprite.shape, sprite.body)
                        break

    def calculate_trajectory(self, start_point, end_point, steps=50):
        """Calcula la trayectoria del pájaro para dibujar la línea de puntos."""
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
        """Dibuja todos los elementos en la pantalla."""
        print("Drawing frame")
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))
        arcade.draw_lrbt_rectangle_filled(
            0, WIDTH, FLOOR_Y - FLOOR_HEIGHT, FLOOR_Y, FLOOR_COLOR
        )
        self.sprites.draw()
        if self.draw_line:
            trajectory = self.calculate_trajectory(self.fixed_start, self.end_point, steps=50)
            if len(trajectory) > 1:
                for i in range(min(30, len(trajectory))):
                    point = trajectory[i]
                    alpha_value = int(255 * (1 - i / 30))
                    color = (128, 128, 128, alpha_value)
                    arcade.draw_circle_filled(point[0], point[1], 1.5, color)
        
        if self.paused:
            arcade.draw_rectangle_filled(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT, (0, 0, 0, 128))
            arcade.draw_text("PAUSED", WIDTH / 2, HEIGHT / 2 + 50, arcade.color.WHITE, 50, anchor_x="center")
            self.play_button.draw()
        
        if self.level_won:
            arcade.draw_rectangle_filled(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT, (0, 0, 0, 128))
            arcade.draw_text("GANASTE", WIDTH / 2, HEIGHT / 2 + 50, arcade.color.WHITE, 50, anchor_x="center")
            self.next_level_button.draw()

    def toggle_pause(self):
        """Pausa o despausa el juego."""
        print("Toggling pause")
        if not self.level_won:
            self.paused = not self.paused

    def restart_level(self):
        """Reinicia el nivel actual."""
        print("Restarting level")
        self.game_init()

    def next_level(self):
        """Avanza al siguiente nivel."""
        print(f"Advancing to level {self.current_level + 1}")
        self.current_level += 1
        if self.current_level > 3:
            self.current_level = 1
        self.load_level(self.current_level)
        self.level_won = False
        self.paused = False