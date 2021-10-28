"""
Sprite Move With Walls

Simple program to show basic sprite usage.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_walls
"""

import arcade
import os
import pandas as pd
import constants
import arcade.gui

class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome to Slime Maze!", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-75,
                         arcade.color.DAVY_GREY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 + 200,
                         arcade.color.BLACK, font_size=60, anchor_x="center")
        arcade.draw_text("Reach the door to progress to the next level.", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 + 100,
                         arcade.color.DAVY_GREY, font_size=20, anchor_x="center")
        arcade.draw_text("Collect coins to earn points!", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 + 50,
                         arcade.color.DAVY_GREY, font_size=20, anchor_x="center")
        arcade.draw_text("Avoid enemy worms, the worms will eat you!", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2,
                         arcade.color.DAVY_GREY, font_size=20, anchor_x="center")
        arcade.draw_text("Press R to return to level select.", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 -50,
                         arcade.color.DAVY_GREY, font_size=20, anchor_x="center")
        arcade.draw_text("Use WASD or arrow keys to move.", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 -100,
                         arcade.color.DAVY_GREY, font_size=20, anchor_x="center")
        arcade.draw_text("Click to advance", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-200,
                         arcade.color.DAVY_GREY, font_size=15, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        levels_view = Levels()
        self.window.show_view(levels_view)

class Levels(arcade.View):
    def __init__(self):
        super().__init__()

        self.window.set_mouse_visible(True)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.ALMOND)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        one_start_button = arcade.gui.UIFlatButton(text="Level One", width=200)
        self.v_box.add(one_start_button.with_space_around(bottom=20))

        two_start_button = arcade.gui.UIFlatButton(text="Level Two", width=200)
        self.v_box.add(two_start_button.with_space_around(bottom=20))

        three_start_button = arcade.gui.UIFlatButton(text="Level Three", width=200)
        self.v_box.add(three_start_button.with_space_around(bottom=20))

        four_start_button = arcade.gui.UIFlatButton(text="Level Four", width=200)
        self.v_box.add(four_start_button)

        # --- Method 2 for handling click events,
        # assign self.on_click_start as callback
        # one_start_button.on_click = self.on_click_start

        @one_start_button.event("on_click")
        def one_start_button(event):
            game_view = GameView1()
            self.window.show_view(game_view)

        @two_start_button.event("on_click")
        def two_start_button(event):
            game_view2 = GameView2()
            self.window.show_view(game_view2)
        
        @three_start_button.event("on_click")
        def three_start_button(event):
            game_view3 = GameView3()
            self.window.show_view(game_view3)
        
        @four_start_button.event("on_click")
        def four_start_button(event):
            game_view4 = GameView4()
            self.window.show_view(game_view4)
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )


    def on_draw(self):
        arcade.start_render()
        self.manager.draw()

class GameView1(arcade.View):
    """ Main application class. """
    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.score = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/enemies/slimeBlock.png", 0.2)

        #Sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")

        maze = pd.read_csv("maze1.csv", skip_blank_lines = False)
        maze = maze.to_numpy()
        print(maze[0, 23])

        for y in range(0, 19):
            for x in range (0, 25):
                if maze[y,x] == "X" or maze[y,x] == "x":
                    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", constants.SPRITE_SCALING)
                    wall.center_x = x*constants.SCALE + 16
                    wall.center_y = y*constants.SCALE + 16
                    self.wall_list.append(wall)
                if maze[y,x] == "P" or maze[y,x] == "p":
                    self.player_sprite.center_x = x*constants.SCALE + 16
                    self.player_sprite.center_y = y*constants.SCALE + 16
                    self.player_list.append(self.player_sprite)
                if maze[y,x] == "D" or maze[y,x] == "d":
                    door = arcade.Sprite(":resources:images/tiles/doorClosed_mid.png", constants.SPRITE_SCALING)
                    door.center_x = x*constants.SCALE + 16
                    door.center_y = y*constants.SCALE + 16
                    self.door_list.append(door)
                if maze[y,x] == "C" or maze[y,x] == "c":
                    coin = arcade.Sprite(":resources:images/items/coinGold.png", constants.SPRITE_SCALING_COIN)
                    coin.center_x = x*constants.SCALE + 16
                    coin.center_y = y*constants.SCALE + 16
                    self.coin_list.append(coin)
                if maze[y,x] == "E" or maze[y,x] == "E":
                    enemy = arcade.Sprite(":resources:images/enemies/wormGreen.png", 0.2)
                    enemy.change_x = constants.MOVEMENT_SPEED * .4
                    enemy.center_x = x*constants.SCALE + 16
                    enemy.center_y = y*constants.SCALE + 16
                    self.enemy_list.append(enemy)
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(True)

    def on_draw(self):
        arcade.start_render()
        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.door_list.draw()
        self.enemy_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 16, 2, arcade.color.WHITE, 14)
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.W or key == arcade.key.UP:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED
        print(self.player_sprite.center_x, ", ", self.player_sprite.center_y)

        if key == arcade.key.R:
            levels_view = Levels()
            self.window.show_view(levels_view)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W or key == arcade.key.S or key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D or key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites
        self.physics_engine.update()

        self.enemy_list.update()
        # Check each enemy
        for enemy in self.enemy_list:
            # If the enemy hit a wall, reverse
            if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                enemy.change_x *= -1
                
        if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
            game_over_view = GameOverView()
            self.window.score = self.score
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.collect_coin_sound)
        
        # if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
        #     game_over_view = GameOverView()
        #     self.window.set_mouse_visible(True)
        #     self.window.show_view(game_over_view)
        
        if arcade.check_for_collision_with_list(self.player_sprite, self.door_list):
            win_view = YouWin()
            self.window.score = self.score + 25
            self.window.set_mouse_visible(True)
            self.window.show_view(win_view)

class GameView2(arcade.View):
    """ Main application class. """
    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.score = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/enemies/slimeBlock.png", 0.2)

        #Sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")

        maze = pd.read_csv("maze2.csv", skip_blank_lines = False)
        maze = maze.to_numpy()
        print(maze[0, 23])

        for y in range(0, 19):
            for x in range (0, 25):
                if maze[y,x] == "X" or maze[y,x] == "x":
                    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", constants.SPRITE_SCALING)
                    wall.center_x = x*constants.SCALE + 16
                    wall.center_y = y*constants.SCALE + 16
                    self.wall_list.append(wall)
                if maze[y,x] == "P" or maze[y,x] == "p":
                    self.player_sprite.center_x = x*constants.SCALE + 16
                    self.player_sprite.center_y = y*constants.SCALE + 16
                    self.player_list.append(self.player_sprite)
                if maze[y,x] == "D" or maze[y,x] == "d":
                    door = arcade.Sprite(":resources:images/tiles/doorClosed_mid.png", constants.SPRITE_SCALING)
                    door.center_x = x*constants.SCALE + 16
                    door.center_y = y*constants.SCALE + 16
                    self.door_list.append(door)
                if maze[y,x] == "C" or maze[y,x] == "c":
                    coin = arcade.Sprite(":resources:images/items/coinGold.png", constants.SPRITE_SCALING_COIN)
                    coin.center_x = x*constants.SCALE + 16
                    coin.center_y = y*constants.SCALE + 16
                    self.coin_list.append(coin)
                if maze[y,x] == "E" or maze[y,x] == "E":
                    enemy = arcade.Sprite(":resources:images/enemies/wormGreen.png", 0.2)
                    enemy.change_x = constants.MOVEMENT_SPEED * .4
                    enemy.center_x = x*constants.SCALE + 16
                    enemy.center_y = y*constants.SCALE + 16
                    self.enemy_list.append(enemy)
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(True)

    def on_draw(self):
        arcade.start_render()
        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.door_list.draw()
        self.enemy_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 16, 2, arcade.color.WHITE, 14)
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.W or key == arcade.key.UP:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED
        print(self.player_sprite.center_x, ", ", self.player_sprite.center_y)

        if key == arcade.key.R:
            levels_view = Levels()
            self.window.show_view(levels_view)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W or key == arcade.key.S or key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D or key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites
        self.physics_engine.update()

        self.enemy_list.update()
        # Check each enemy
        for enemy in self.enemy_list:
            # If the enemy hit a wall, reverse
            if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                enemy.change_x *= -1
                
        if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
            game_over_view = GameOverView()
            self.window.score = self.score
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.collect_coin_sound)
        
        # if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
        #     game_over_view = GameOverView()
        #     self.window.set_mouse_visible(True)
        #     self.window.show_view(game_over_view)
        
        if arcade.check_for_collision_with_list(self.player_sprite, self.door_list):
            win_view = YouWin()
            self.window.score = self.score + 25
            self.window.set_mouse_visible(True)
            self.window.show_view(win_view)

class GameView3(arcade.View):
    """ Main application class. """
    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.score = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/enemies/slimeBlock.png", 0.2)

        #Sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")

        maze = pd.read_csv("maze3.csv", skip_blank_lines = False)
        maze = maze.to_numpy()
        print(maze[0, 23])

        for y in range(0, 19):
            for x in range (0, 25):
                if maze[y,x] == "X" or maze[y,x] == "x":
                    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", constants.SPRITE_SCALING)
                    wall.center_x = x*constants.SCALE + 16
                    wall.center_y = y*constants.SCALE + 16
                    self.wall_list.append(wall)
                if maze[y,x] == "P" or maze[y,x] == "p":
                    self.player_sprite.center_x = x*constants.SCALE + 16
                    self.player_sprite.center_y = y*constants.SCALE + 16
                    self.player_list.append(self.player_sprite)
                if maze[y,x] == "D" or maze[y,x] == "d":
                    door = arcade.Sprite(":resources:images/tiles/doorClosed_mid.png", constants.SPRITE_SCALING)
                    door.center_x = x*constants.SCALE + 16
                    door.center_y = y*constants.SCALE + 16
                    self.door_list.append(door)
                if maze[y,x] == "C" or maze[y,x] == "c":
                    coin = arcade.Sprite(":resources:images/items/coinGold.png", constants.SPRITE_SCALING_COIN)
                    coin.center_x = x*constants.SCALE + 16
                    coin.center_y = y*constants.SCALE + 16
                    self.coin_list.append(coin)
                if maze[y,x] == "E" or maze[y,x] == "E":
                    enemy = arcade.Sprite(":resources:images/enemies/wormGreen.png", 0.2)
                    enemy.change_x = constants.MOVEMENT_SPEED * .4
                    enemy.center_x = x*constants.SCALE + 16
                    enemy.center_y = y*constants.SCALE + 16
                    self.enemy_list.append(enemy)
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(True)

    def on_draw(self):
        arcade.start_render()
        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.door_list.draw()
        self.enemy_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 16, 2, arcade.color.WHITE, 14)
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.W or key == arcade.key.UP:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED
        print(self.player_sprite.center_x, ", ", self.player_sprite.center_y)

        if key == arcade.key.R:
            levels_view = Levels()
            self.window.show_view(levels_view)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W or key == arcade.key.S or key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D or key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites
        self.physics_engine.update()

        self.enemy_list.update()
        # Check each enemy
        for enemy in self.enemy_list:
            # If the enemy hit a wall, reverse
            if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                enemy.change_x *= -1
                
        if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
            game_over_view = GameOverView()
            self.window.score = self.score
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.collect_coin_sound)
        
        # if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
        #     game_over_view = GameOverView()
        #     self.window.set_mouse_visible(True)
        #     self.window.show_view(game_over_view)
        
        if arcade.check_for_collision_with_list(self.player_sprite, self.door_list):
            win_view = YouWin()
            self.window.score = self.score + 25
            self.window.set_mouse_visible(True)
            self.window.show_view(win_view)

class GameView4(arcade.View):
    """ Main application class. """
    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.score = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/enemies/slimeBlock.png", 0.2)

        #Sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")

        maze = pd.read_csv("maze4.csv", skip_blank_lines = False)
        maze = maze.to_numpy()
        print(maze[0, 23])

        for y in range(0, 19):
            for x in range (0, 25):
                if maze[y,x] == "X" or maze[y,x] == "x":
                    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", constants.SPRITE_SCALING)
                    wall.center_x = x*constants.SCALE + 16
                    wall.center_y = y*constants.SCALE + 16
                    self.wall_list.append(wall)
                if maze[y,x] == "P" or maze[y,x] == "p":
                    self.player_sprite.center_x = x*constants.SCALE + 16
                    self.player_sprite.center_y = y*constants.SCALE + 16
                    self.player_list.append(self.player_sprite)
                if maze[y,x] == "D" or maze[y,x] == "d":
                    door = arcade.Sprite(":resources:images/tiles/doorClosed_mid.png", constants.SPRITE_SCALING)
                    door.center_x = x*constants.SCALE + 16
                    door.center_y = y*constants.SCALE + 16
                    self.door_list.append(door)
                if maze[y,x] == "C" or maze[y,x] == "c":
                    coin = arcade.Sprite(":resources:images/items/coinGold.png", constants.SPRITE_SCALING_COIN)
                    coin.center_x = x*constants.SCALE + 16
                    coin.center_y = y*constants.SCALE + 16
                    self.coin_list.append(coin)
                if maze[y,x] == "E" or maze[y,x] == "E":
                    enemy = arcade.Sprite(":resources:images/enemies/wormGreen.png", 0.2)
                    enemy.change_x = constants.MOVEMENT_SPEED * .4
                    enemy.center_x = x*constants.SCALE + 16
                    enemy.center_y = y*constants.SCALE + 16
                    self.enemy_list.append(enemy)
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(True)

    def on_draw(self):
        arcade.start_render()
        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.door_list.draw()
        self.enemy_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 16, 2, arcade.color.WHITE, 14)
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.W or key == arcade.key.UP:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED
        print(self.player_sprite.center_x, ", ", self.player_sprite.center_y)

        if key == arcade.key.R:
            levels_view = Levels()
            self.window.show_view(levels_view)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W or key == arcade.key.S or key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D or key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites
        self.physics_engine.update()

        self.enemy_list.update()
        # Check each enemy
        for enemy in self.enemy_list:
            # If the enemy hit a wall, reverse
            if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                enemy.change_x *= -1
                
        if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
            game_over_view = GameOverView()
            self.window.score = self.score
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.collect_coin_sound)
        
        # if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
        #     game_over_view = GameOverView()
        #     self.window.set_mouse_visible(True)
        #     self.window.show_view(game_over_view)
        
        if arcade.check_for_collision_with_list(self.player_sprite, self.door_list):
            win_view = YouWin()
            self.window.score = self.score + 25
            self.window.set_mouse_visible(True)
            self.window.show_view(win_view)

class YouWin(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        self.background = arcade.load_texture("win.PNG")

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("Click to return to level selector.", 310, 300, arcade.color.WHITE, 24)

        output_total = f"Total Score: {self.window.score}"
        arcade.draw_text(output_total, 320, 250, arcade.color.WHITE, 16)
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        levels_view = Levels()
        self.window.show_view(levels_view)

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        output_total = f"Total Score: {self.window.score}"
        arcade.draw_text(output_total, 320, 250, arcade.color.WHITE, 16)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        levels_view = Levels()
        self.window.show_view(levels_view)


def main():
    """ Main function """
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, "Maze Game")
    window.score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()