# ui/buttons.py
import arcade

class Button(arcade.Sprite):
    def __init__(self, image_path, x, y, scale=0.5, action=None, width=None, height=None):
        super().__init__(image_path, scale)
        self.center_x = x
        self.center_y = y
        self.action = action  # Función a llamar al click
        self.width = width
        self.height = height

    def on_click(self):
        if self.action:
            self.action()

# Botones específicos
class PauseButton(Button):
    def __init__(self, action, width=1800, height=800, x=None, y=None):
        if x is None:
            x = width - 100
        if y is None:
            y = height - 50
        super().__init__("assets/img/boton_pausa.png", x, y, action=action, width=width, height=height)

class PlayButton(Button):
    def __init__(self, action, width=1800, height=800, x=None, y=None):
        if x is None:
            x = width / 2
        if y is None:
            y = height / 2 - 50
        super().__init__("assets/img/boton_play.png", x, y, action=action, width=width, height=height)

class RestartButton(Button):
    def __init__(self, action, width=1800, height=800, x=None, y=None):
        if x is None:
            x = width - 200
        if y is None:
            y = height - 50
        super().__init__("assets/img/boton_reiniciar.png", x, y, action=action, width=width, height=height)

class NextLevelButton(Button):
    def __init__(self, action, width=1800, height=800, x=None, y=None):
        if x is None:
            x = width / 2
        if y is None:
            y = height / 2 - 50
        super().__init__("assets/img/boton_siguiente.png", x, y, action=action, width=width, height=height)