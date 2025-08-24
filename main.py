import arcade
from game import App
WIDTH = 1800
HEIGHT = 800
TITLE = "Angry Birds"

def main():
    try:
        window = arcade.Window(WIDTH, HEIGHT, TITLE)    
        game = App()
        window.show_view(game)
        arcade.run()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()