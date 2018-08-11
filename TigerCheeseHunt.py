import arcade
import sys
import pygame

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
KEY_R = 114
KEYS_HELD = []

class MyGame(arcade.Window):
    tiger_posx = SCREEN_WIDTH / 2
    tiger_posy = SCREEN_HEIGHT / 2
    score = 0
    tiger = None
    cheeses = {}
    viewport_offset_x = 0
    viewport_offset_y = 0
    found_cheeses = []

    def __init__(self, width, height):
        super().__init__(width, height)
        pygame.mixer.init()
        pygame.mixer.music.load("C:\\Windows\\Media\\tada.wav")
        arcade.set_background_color(arcade.color.BLACK)
        self.reload()

    def reload(self):
        self.tiger_posx = SCREEN_WIDTH / 2
        self.tiger_posy = SCREEN_HEIGHT / 2
        self.score = 0
        self.found_cheeses = []

    def on_key_press(self, key, modifiers):
        if key == KEY_Q:
            sys.exit(0)
        if key == KEY_R and self.score:
            self.reload()
        else:
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
        if not 0 in self.found_cheeses:
            self.cheeses[0] = arcade.Sprite("cheese.png", SPRITE_SCALING_CHEESE)
            self.cheeses[0].set_position(150+self.viewport_offset_x, 150+self.viewport_offset_y)
            self.cheeses[0].draw()
        if not 1 in self.found_cheeses:
            self.cheeses[1] = arcade.Sprite("cheese.png", SPRITE_SCALING_CHEESE)
            self.cheeses[1].set_position((0-150)+self.viewport_offset_x, 150+self.viewport_offset_y)
            self.cheeses[1].draw()
        if not 2 in self.found_cheeses:
            self.cheeses[2] = arcade.Sprite("cheese.png", SPRITE_SCALING_CHEESE)
            self.cheeses[2].set_position((0-150)+self.viewport_offset_x, (0-150)+self.viewport_offset_y)
            self.cheeses[2].draw()
        SPRITE_SCALING_TIGER = 1.0
        self.tiger = arcade.Sprite("tiger.png", SPRITE_SCALING_TIGER)
        self.tiger.set_position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.tiger.draw()
        output = f"View: {self.viewport_offset_x}, {self.viewport_offset_y}"
        arcade.draw_text(output, 10, 40, arcade.color.WHITE, 14)
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 25, arcade.color.WHITE, 14)
        if self.score == 3:
            output = f"You win!  Press Q to exit or R to replay"
            arcade.draw_text(output, 10, 10, arcade.color.WHITE, 14)


    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        for key in KEYS_HELD:
            if key == KEY_W:
                #self.tiger_posy += 4
                self.viewport_offset_y -= 2
            if key == KEY_S:
                #self.tiger_posy -= 4
                self.viewport_offset_y += 2
            if key == KEY_A:
                #self.tiger_posx -= 4
                self.viewport_offset_x += 2
            if key == KEY_D:
                #self.tiger_posx += 4
                self.viewport_offset_x -= 2
        try:
            self.tiger.set_position(self.tiger_posx, self.tiger_posy)
            self.tiger.draw()
            i = 0
            while i < len(self.cheeses):
                if not i in self.found_cheeses:
                    colres = arcade.geometry.check_for_collision(self.tiger, self.cheeses[i])
                    if colres:
                        if not i in self.found_cheeses:
                            self.found_cheeses.append(i)
                        self.score += 1
                        if self.score == 3:
                            pygame.mixer.music.play()
                i += 1
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
