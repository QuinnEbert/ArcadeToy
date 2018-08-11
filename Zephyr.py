import arcade
import sys
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

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
    viewport_offset_x = 0
    viewport_offset_y = 0
    walls = []
    walls_pe = SpriteList()
    w = []

    def __init__(self, width, height):
        super().__init__(width, height)

        # Build the walls
        self.w = [
            [1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        x = 0
        while x < len(self.w):
            y = 0
            self.walls.append([])
            while y < len(self.w[x]):
                if self.w[x][y]:
                    new_wall = arcade.Sprite("brick.jpg", 1.0)
                    self.walls[x].append(new_wall)
                    walls_pe.append(new_wall)
                else:
                    self.walls[x].append(None)
                y += 1
            x += 1

        pygame.mixer.init()
        pygame.mixer.music.load("C:\\Windows\\Media\\tada.wav")
        arcade.set_background_color(arcade.color.BLACK)
        self.reload()

    def reload(self):
        self.tiger_posx = SCREEN_WIDTH / 2
        self.tiger_posy = SCREEN_HEIGHT / 2
        self.score = 0

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
        SPRITE_SCALING_TIGER = 0.5
        self.tiger = arcade.Sprite("tiger.png", SPRITE_SCALING_TIGER)
        self.tiger.set_position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.tiger.draw()
        x = 0
        while x < len(self.walls):
            y = 0
            while y < len(self.walls[x]):
                try:
                    self.walls[x][y].set_position(((y)*32+self.viewport_offset_x), ((-x)*32+self.viewport_offset_y))
                    self.walls[x][y].draw()
                except AttributeError:
                    pass
                y += 1
            x += 1
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
            x = 0
            while x < len(self.walls):
                y = 0
                while y < len(self.walls[x]):
                    try:
                        colres = arcade.geometry.check_for_collision(self.tiger, self.walls[x][y])
                        # Rudimentary backoff
                        if colres:
                            print("BUMP")
                            for key in KEYS_HELD:
                                if key == KEY_W:
                                    #self.tiger_posy += 4
                                    self.viewport_offset_y += 3
                                if key == KEY_S:
                                    #self.tiger_posy -= 4
                                    self.viewport_offset_y -= 3
                                if key == KEY_A:
                                    #self.tiger_posx -= 4
                                    self.viewport_offset_x -= 3
                                if key == KEY_D:
                                    #self.tiger_posx += 4
                                    self.viewport_offset_x += 3
                    except TypeError:
                        pass
                    y += 1
                x += 1
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
