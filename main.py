import arcade
from game import App
WIDTH = 1800
HEIGHT = 800
TITLE = "Angry Birds"
def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)    
    game = App()
    window.show_view(game)
    arcade.run()
if __name__ == "__main__":
    main()