import pygame
import random


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((1000, 800))
    # set the title of the display window
    pygame.display.set_caption(
        'treason')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        self.player_dot = Dot(pygame.Color('red'), 10, [self.surface.get_width(
        ) // 2, self.surface.get_height() // 2], [0, 0], self.surface, 'player')

        self.player_bullets = []

        self.number_enemies = 10
        enemy_colors = ['red', 'green', 'orange']
        self.enemy_dots = []
        for i in range(self.number_enemies + 1):
            color = random.choice(enemy_colors)
            radius = 15
            x = random.randint(radius, self.surface.get_width() - radius)
            y = random.randint(radius, self.surface.get_height() - radius)
            velocity_choices = [[0, 3], [0, -3], [3, 0], [-3, 0]]
            enemy = Dot(pygame.Color(color), radius, [
                        x, y], random.choice(velocity_choices), self.surface, 'enemy')
            self.enemy_dots.append(enemy)

        self.max_frames = 150
        self.frame_counter = 0

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            # run at most with FPS Frames Per Second
            self.game_Clock.tick(self.FPS)

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

    def handle_keydown(self, event):
        # handles a user event of pressing a key down
        # event is the event list
        # different arrow keys will eventually move the player ball differently
        color = self.player_dot.get_color()
        center = self.player_dot.get_center()
        velocity = self.player_dot.get_velocity()
        # keys that move player ball
        if event.key == pygame.K_UP:
            self.player_dot.set_velocity((0, -3))
        if event.key == pygame.K_DOWN:
            self.player_dot.set_velocity((0, 3))
        if event.key == pygame.K_LEFT:
            self.player_dot.set_velocity((-3, 0))
        if event.key == pygame.K_RIGHT:
            self.player_dot.set_velocity((3, 0))
        # key that shoots
        if event.key == pygame.K_SPACE:
            if velocity != [0, 0]:
                bullet = Dot(color, 5, center, velocity,
                             self.surface, 'bullet')
                self.player_bullets.append(bullet)
        # keys that change player ball color
        if event.key == pygame.K_x:
            self.player_dot.set_color(pygame.Color('red'))
        if event.key == pygame.K_c:
            self.player_dot.set_color(pygame.Color('orange'))
        if event.key == pygame.K_v:
            self.player_dot.set_color(pygame.Color('green'))

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color)  # clear the display surface first

        self.player_dot.draw()
        for bullet in self.player_bullets:
            bullet.draw()
            for enemy in self.enemy_dots:
                bullet.check_shot(enemy)

        for enemy in self.enemy_dots:
            enemy.draw()

        # reset self.player_bullets after so many bullets have been shot
        if len(self.player_bullets) > 150:
            self.player_bullets = []

        pygame.display.update()  # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        self.player_dot.move()
        self.player_dot.boundary_stop()
        for bullet in self.player_bullets:
            bullet.move()
        self.frame_counter = self.frame_counter + 1

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        pass


class Dot:
    # An object in this class represents a Dot that moves

    def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface, status):
        # Initialize a Dot.
        # - self is the Dot to initialize
        # - color is the pygame.Color of the dot
        # - center is a list containing the x and y int
        #   coords of the center of the dot
        # - radius is the int pixel radius of the dot
        # - velocity is a list containing the x and y components
        # - surface is the window's pygame.Surface object
        #   status is what type of dot it is

        self.color = dot_color
        self.radius = dot_radius
        self.center = dot_center
        self.velocity = dot_velocity
        self.surface = surface
        self.status = status
        self.shot_yes = False

    def move(self):
        # Change the location of the Dot by adding the corresponding
        # speed values to the x and y coordinate of its center
        # - self is the Dot

        for i in range(0, 2):
            self.center[i] = (self.center[i] + self.velocity[i])

    def draw(self):
        # Draw the dot on the surface
        # - self is the Dot
        if self.shot_yes:
            if self.status == 'enemy' or self.status == 'bullet':
                pass
        else:
            pygame.draw.circle(self.surface, self.color,
                               self.center, self.radius)

    def set_velocity(self, formula):
        # sets the velocity of the dot
        # formula is a tuple with the (x,y) changes to the dots current velocity
        # self is the dot
        for i in range(0, 2):
            self.velocity[i] = formula[i]

    def get_velocity(self):
        # gets the velocity of the dot
        velocity = [3, 3]
        for i in range(0, 2):
            velocity[i] *= self.velocity[i]
        return velocity

    def get_color(self):
        # gets the color of the dot
        return self.color

    def get_center(self):
        # gets the center coordinates of the dot
        x = self.center[0]
        y = self.center[1]
        return [x, y]

    def get_radius(self):
        # gets the radius of the dot
        return self.radius

    def set_color(self, color):
        # sets the color of the dot
        # color is a pygame color
        self.color = color

    def shot(self):
        # makes the dot be shot
        self.shot_yes = True

    def boundary_stop(self):
        # checks if dot has hit boundary, and stops velocity if it has
        surface_width_height = (self.surface.get_width(),
                                self.surface.get_height())
        for i in range(0, 2):
            if self.center[i] <= self.radius or self.center[i] + self.radius >= surface_width_height[i]:
                self.velocity[i] = 0

    def check_shot(self, other):
        # checks if another dot has hit you
        # changes self.shot accordingly
        # check left side
        if other.get_center()[0] + other.get_radius() >= self.center[0] - self.radius:
            # check right side
            if other.get_center()[0] - other.get_radius() <= self.center[0] + self.radius:
                # check top side
                if other.get_center()[1] + other.get_radius() >= self.center[1] - self.radius:
                    # check bottom side
                    if other.get_center()[1] - other.get_radius() <= self.center[1] + self.radius:
                        self.shot()
                        other.shot()


main()
