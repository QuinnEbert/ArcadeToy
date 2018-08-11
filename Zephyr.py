import arcade
import os

SPRITE_SCALING = 1.0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 3

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.all_sprites_list = None
        self.coin_list = None

        self.score = 0
        self.player_sprite = None
        self.wall_list = None
        self.physics_engine = None

    def setup(self):
        print("SETUP")
        self.all_sprites_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.score = 0
        self.player_sprite = arcade.Sprite("tiger.png",
                                           SPRITE_SCALING/2)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 64
        self.all_sprites_list.append(self.player_sprite)

        # -- Set up the walls
        # Create a row of boxes
        for x in range(128, 256+32, 32):
            wall = arcade.Sprite("brick.jpg", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 256
            self.all_sprites_list.append(wall)
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(128, 256, 32):
            wall = arcade.Sprite("brick.jpg", SPRITE_SCALING)
            wall.center_x = 256
            wall.center_y = y
            self.all_sprites_list.append(wall)
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        print("DRAW")
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_sprite.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            print("UP")
            i = 0
            while i < len(self.wall_list):
                i += 1
            #self.player_sprite.change_y = MOVEMENT_SPEED
        if key == arcade.key.DOWN:
            print("DOWN")
            i = 0
            while i < len(self.wall_list):
                self.wall_list[i].change_y = -MOVEMENT_SPEED
                i += 1
            #self.player_sprite.change_y = -MOVEMENT_SPEED
        if key == arcade.key.LEFT:
            print("LEFT")
            i = 0
            while i < len(self.wall_list):
                self.wall_list[i].change_x = -MOVEMENT_SPEED
                i += 1
            #self.player_sprite.change_x = -MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            print("RIGHT")
            i = 0
            while i < len(self.wall_list):
                self.wall_list[i].change_x = MOVEMENT_SPEED
                i += 1
            #self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            #self.player_sprite.change_y = 0
            print("UP OR DOWN")
            i = 0
            while i < len(self.wall_list):
                self.wall_list[i].change_y = 0
                i += 1
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            #self.player_sprite.change_x = 0
            print("LEFT OR RIGHT")
            i = 0
            while i < len(self.wall_list):
                self.wall_list[i].change_x = 0
                i += 1

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
