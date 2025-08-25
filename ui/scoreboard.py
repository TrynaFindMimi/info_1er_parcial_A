# ui/scoreboard.py
import arcade

class Scoreboard(arcade.Sprite):
    def __init__(self, score_image_path="assets/img/score.png", x=10, height=800, scale=1.0):
        try:
            super().__init__(score_image_path, scale)
        except FileNotFoundError:
            # Si la imagen no existe, usar un rectángulo temporal
            self.texture = arcade.create_rectangle_texture(100, 50, arcade.color.WHITE)
        self.center_x = x + self.width / 2
        self.center_y = height - 50 + self.height / 2
        self.score = 0
        self.level = 1  # Inicializar nivel, se actualizará desde game.py
        self.height = height  # Guardar height para usar en draw

    def draw(self):
        super().draw()
        # Dibujar el puntaje sobre la imagen
        arcade.draw_text(
            f"{self.score}",
            self.center_x + 50,
            self.center_y - 10,
            arcade.color.WHITE,
            24,
            anchor_x="left"
        )
        # Dibujar el nivel en el centro superior usando el ancho de la ventana
        arcade.draw_text(
            f"Level: {self.level}",
            arcade.get_window().width / 2,
            self.height - 30,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

    def add_points(self, points):
        self.score += points