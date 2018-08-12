import arcade
import os
import pygame
import datetime
import sys

SPRITE_SCALING = 1.0

SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 768

MOVEMENT_SPEED = 5

KEYS_DOWN = []

CHEESE_BLOCK = "cheese.png"

MOVEMENT_KEYS = [
    arcade.key.UP,
    arcade.key.DOWN,
    arcade.key.LEFT,
    arcade.key.RIGHT
]

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        self.lpy = 0.0
        super().__init__(width, height, fullscreen=True)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.all_sprites_list = None
        self.coin_list = None
        self.score = 0
        self.player_sprite = None
        self.wall_list = None
        self.physics_engine = None
        self.mapdata = []
        self.vpx = 0
        self.vpy = 0
        self.cheese = None
        pygame.mixer.init()
        self.footsteps = pygame.mixer.Sound("walking.wav")
        self.ate_cheese = False
        self.dialogue = f""
        self.lst = datetime.datetime.now()
        self.immobile = False

    def common_reset(self):
        pygame.mixer.music.stop()
        self.ate_cheese = False
        self.lst = datetime.datetime.now()
        self.immobile = False

    def mapXX_ticks(self,map="01"):
        ##
        ## LEVEL SCRIPTING
        ##
        sst = (datetime.datetime.now()-self.lst).seconds
        if map == "01":
            self.immobile = (sst <= 9)
            if sst >= 1 and sst <= 4:
                self.dialogue = f"Holy hell!  What just happened?"
            elif sst >= 6 and sst <= 9:
                self.dialogue = f"I need to go find Christian and Regina!"
            elif sst >= 11 and sst <= 14:
                self.dialogue = f"GAMEPLAY TIP: Press the Q key if you need to quit playing"
            else:
                self.dialogue = f""

    def map01_setup(self):
        # Reset
        self.common_reset()
        # Music
        pygame.mixer.music.load("al_toe.ogg")
        pygame.mixer.music.play(loops=-1)
        # Textures
        self.blocks = {
            10: "NO_BLOCK.jpg",
            11: "brick.jpg",
            12: CHEESE_BLOCK,
            13: "rubble.jpg",
            14: "firepit.jpg",
            51: "carpet_b.jpg",
            52: "carpet.jpg",
            53: "carpet_s.jpg",
            54: "rubble_d.jpg"
        }
        # Default Position
        self.player_sprite.center_x = 1*32
        self.player_sprite.center_y = -(2*32)
        # Tiledata
        self.mapdata = [
            [99,99,99,11,11,11,99,99,99],
            [11,11,11,11,14,11,11,11,11],
            [11,54,13,13,10,53,51,52,12],
            [11,54,13,10,53,51,52,52,11],
            [11,10,10,53,51,52,52,52,11],
            [11,10,53,51,52,52,52,52,11],
            [11,53,51,52,52,52,52,52,11],
            [11,11,11,11,11,11,11,11,11]
        ]
        # Build the playfield
        y = 0
        while y < len(self.mapdata):
            x = 0
            while x < len(self.mapdata[y]):
                block_id = self.mapdata[y][x]
                # 99 is a no-op block (no sprite)
                if not block_id == 99:
                    block_name = self.blocks[block_id]
                    wall = arcade.Sprite(block_name, SPRITE_SCALING)
                    wall.center_x = x*32
                    wall.center_y = -(y*32)
                    self.all_sprites_list.append(wall)
                    # Cheese block, block 10 (blank floor) and blocks >= 50 (styled floor) are not walls
                    if not block_name == CHEESE_BLOCK and not block_id == 10 and not block_id >= 50:
                        # if it's not
                        self.wall_list.append(wall)
                    else:
                        # I like cheese
                        if block_name == CHEESE_BLOCK:
                            self.cheese = wall
                x += 1
            y += 1
        # bind the physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        # setup the background
        arcade.set_background_color(arcade.color.AMAZON)
        # the player needs to always be the top tile
        self.all_sprites_list.append(self.player_sprite)

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.cheese = None

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = arcade.Sprite("tiger.png",
                                           SPRITE_SCALING)

        # Viewport
        self.vpx = 0
        self.vpy = 0

        self.map01_setup()


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        self.vpx = self.player_sprite.get_position()[0]-(SCREEN_WIDTH/2)
        self.vpy = self.player_sprite.get_position()[1]-(SCREEN_HEIGHT/2)

        arcade.set_viewport(self.vpx, self.vpx+SCREEN_WIDTH, self.vpy, self.vpy+SCREEN_HEIGHT)

        # Draw all the sprites.
        self.all_sprites_list.draw()
        #self.player_sprite.draw()

        #output = f"Centre: {self.vpx}, {self.vpy}"
        arcade.draw_text(self.dialogue, self.vpx+10, self.vpy+10, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        if self.immobile:
            return

        """Called whenever a key is pressed. """

        #if key == arcade.key.UP:
        #    self.player_sprite.change_y = MOVEMENT_SPEED
        #elif key == arcade.key.DOWN:
        #    self.player_sprite.change_y = -MOVEMENT_SPEED
        #elif key == arcade.key.LEFT:
        #    self.player_sprite.change_x = -MOVEMENT_SPEED
        #elif key == arcade.key.RIGHT:
        #    self.player_sprite.change_x = MOVEMENT_SPEED

        start_footsteps = False
        if key in MOVEMENT_KEYS:
            start_footsteps = True
            for tkey in KEYS_DOWN:
                if tkey in MOVEMENT_KEYS:
                    start_footsteps = False
        if start_footsteps:
            self.footsteps.play(loops=-1)

        if not key in KEYS_DOWN:
            KEYS_DOWN.append(key)


    def on_key_release(self, key, modifiers):
        if key == arcade.key.Q:
            sys.exit(0)

        if self.immobile:
            return

        """Called when the user releases a key. """

        #if key == arcade.key.UP or key == arcade.key.DOWN:
        #    self.player_sprite.change_y = 0
        #elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
        #    self.player_sprite.change_x = 0

        if key in KEYS_DOWN:
            KEYS_DOWN.remove(key)

        stop_footsteps = True
        if key in MOVEMENT_KEYS:
            for tkey in KEYS_DOWN:
                if tkey in MOVEMENT_KEYS:
                    stop_footsteps = False
        if stop_footsteps:
            self.footsteps.stop()

    def update(self, delta_time):
        """ Movement and game logic """
        # Call update on all sprites (The sprites don't do much in this
        # example though.)

        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        if arcade.key.LEFT in KEYS_DOWN:
            if not arcade.key.RIGHT in KEYS_DOWN:
                self.player_sprite.change_x = -MOVEMENT_SPEED
        if arcade.key.RIGHT in KEYS_DOWN:
            if not arcade.key.LEFT in KEYS_DOWN:
                self.player_sprite.change_x = MOVEMENT_SPEED
        if arcade.key.LEFT in KEYS_DOWN and arcade.key.RIGHT in KEYS_DOWN:
            self.player_sprite.change_x = 0
        if arcade.key.UP in KEYS_DOWN:
            if not arcade.key.DOWN in KEYS_DOWN:
                self.player_sprite.change_y = MOVEMENT_SPEED
        if arcade.key.DOWN in KEYS_DOWN:
            if not arcade.key.UP in KEYS_DOWN:
                self.player_sprite.change_y = -MOVEMENT_SPEED
        if arcade.key.UP in KEYS_DOWN and arcade.key.DOWN in KEYS_DOWN:
            self.player_sprite.change_y = 0

        if not self.ate_cheese:
            colres = arcade.geometry.check_for_collision(self.player_sprite, self.cheese)
            if colres:
                self.ate_cheese = True
                self.cheese.kill()

        self.physics_engine.update()

        self.mapXX_ticks()

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
