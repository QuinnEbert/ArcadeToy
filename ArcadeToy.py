import arcade
import sys

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 384

def draw_pine_tree(x, y):
    """ This function draws a pine tree at the specified location. """

    # Draw the triangle on top of the trunk.
    # We need three x, y points for the triangle.
    arcade.draw_triangle_filled(x + 40, y,       # Point 1
                                x, y - 100,      # Point 2
                                x + 80, y - 100, # Point 3
                                arcade.color.DARK_GREEN)

    # Draw the trunk
    arcade.draw_lrtb_rectangle_filled(x + 30, x + 50, y - 100, y - 140,
                                      arcade.color.DARK_BROWN)

KEY_Q = 113
KEY_W = 119
KEY_S = 115
KEY_A = 97
KEY_D = 100
KEYS_HELD = []

class MyGame(arcade.Window):
    tiger_posx = 64
    tiger_posy = 64
    tiger = None
    cheese = None

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)

    def on_key_press(self, key, modifiers):
        if key == KEY_Q:
            sys.exit(0)
        if not key in KEYS_HELD:
            KEYS_HELD.append(key)
    def on_key_release(self, key, modifiers):
        if key in KEYS_HELD:
            KEYS_HELD.remove(key)

    def setup(self):
        # Set up your game here
        pass

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        SPRITE_SCALING_CHEESE = 0.3
        self.cheese = arcade.Sprite("cheese.png", SPRITE_SCALING_CHEESE)
        self.cheese.set_position(300, 300)
        self.cheese.draw()
        SPRITE_SCALING_TIGER = 1.0
        self.tiger = arcade.Sprite("tiger.png", SPRITE_SCALING_TIGER)
        self.tiger.set_position(self.tiger_posx, self.tiger_posy)
        self.tiger.draw()


    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        for key in KEYS_HELD:
            if key == KEY_W:
                self.tiger_posy += 4
            if key == KEY_S:
                self.tiger_posy -= 4
            if key == KEY_A:
                self.tiger_posx -= 4
            if key == KEY_D:
                self.tiger_posx += 4
        try:
            self.tiger.set_position(self.tiger_posx, self.tiger_posy)
            self.tiger.draw()
            colres = arcade.geometry.check_for_collision(self.tiger, self.cheese)
            if colres:
                print("You win!")
                sys.exit(0)
        except AttributeError:
            # This is a cheap hack for a failure that only happens on the first
            # frame...
            pass


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
