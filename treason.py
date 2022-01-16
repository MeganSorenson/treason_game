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
        # player things
        self.player_dot = Dot(pygame.Color('red'), 10, [self.surface.get_width(
        ) // 2, self.surface.get_height() // 2], [0, 0], self.surface, 'player')

        self.player_bullets = []

        # enemy things
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

        self.enemy_bullets = []

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
            self.player_dot.set_velocity((0, -4))
        if event.key == pygame.K_DOWN:
            self.player_dot.set_velocity((0, 4))
        if event.key == pygame.K_LEFT:
            self.player_dot.set_velocity((-4, 0))
        if event.key == pygame.K_RIGHT:
            self.player_dot.set_velocity((4, 0))
        # key that shoots
        if event.key == pygame.K_SPACE:
            if velocity != [0, 0]:
                bullet = Dot(color, 5, center, velocity,
                             self.surface, 'player_bullet')
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

        # draw player things
        self.player_dot.draw()
        for bullet in self.player_bullets:
            bullet.draw()
            for enemy in self.enemy_dots:
                bullet.check_player_shot(enemy)

        # draw enemy things
        for enemy in self.enemy_dots:
            enemy.draw()
        for bullet in self.enemy_bullets:
            bullet.draw()
            bullet.check_player_shot(self.player_dot)

        # draw game text
        if self.continue_game == False:
            self.display_game_over()

        # reset self.player_bullets and self.enemy_bullets after so many bullets have been shot
        if len(self.player_bullets) > 150:
            for i in range(50):
                self.player_bullets.pop(0)
        if len(self.enemy_bullets) > 150:
            for i in range(50):
                self.enemy_bullets.pop(0)

        pygame.display.update()  # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        # update player things
        self.player_dot.move()
        self.player_dot.boundary_stop()
        for bullet in self.player_bullets:
            bullet.move()

        # update enemy things
        for enemy in self.enemy_dots:
            enemy.move()
            enemy.boundary_stop()
            # check if player dot in enemy range
            should_enemy_shoot = enemy.check_player_shot(self.player_dot)
            # if yes, shoot at player
            if should_enemy_shoot:
                color = enemy.get_color()
                center = enemy.get_center()
                velocity = enemy.get_velocity()
                bullet = Dot(color, 5, center, velocity,
                             self.surface, 'enemy_bullet')
                self.enemy_bullets.append(bullet)

        for bullet in self.enemy_bullets:
            bullet.move()

        self.frame_counter = self.frame_counter + 1

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        self.continue_game = False
        for enemy in self.enemy_dots:
            if not enemy.get_shot_status():
                self.continue_game = True

    def display_game_over(self):
        # displays game over message at end of game
        words1 = 'GAME OVER'
        words2 = 'successfully back-stabbed'
        # set font characteristics
        font_size1 = 70
        font_size2 = 40
        font1 = pygame.font.SysFont("", font_size1)
        font2 = pygame.font.SysFont("", font_size2)
        fg_color = pygame.Color("white")
        # create text box of string using font characteristics
        text_box1 = font1.render(words1, True, fg_color, self.bg_color)
        text_box2 = font2.render(words2, True, fg_color, self.bg_color)
        # location is middle of window
        location1 = ((self.surface.get_width() - text_box1.get_width()) // 2,
                     (self.surface.get_height() - text_box1.get_height()) // 2)
        location2 = ((self.surface.get_width() - text_box2.get_width()) // 2,
                     (self.surface.get_height() - text_box2.get_height()) // 2 + 50)
        # blit to game surface at location
        self.surface.blit(text_box1, location1)
        self.surface.blit(text_box2, location2)


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

    def get_shot_status(self):
        # gets the shot status of the dot
        return self.shot_yes

    def get_status(self):
        # gets the type of dot of self
        return self.status

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
                if self.status == 'player':  # if player, stop movement
                    self.velocity[i] = 0
                elif self.status == 'enemy':  # if enemy, bounce
                    self.velocity[i] = -self.velocity[i]

    def check_player_shot(self, other):
        # if self is a bullet --> checks if a bullet has hit an enemy
        #   changes self.shot accordingly
        # if self is an enemy -- > checks if another dot in extended surroundings (in direction of movement),
        #   returns if yes (bool)
        if self.status == 'player_bullet' or self.status == 'enemy_bullet':
            # check left side
            if other.get_center()[0] + other.get_radius() >= self.center[0] - self.radius:
                # check right side
                if other.get_center()[0] - other.get_radius() <= self.center[0] + self.radius:
                    # check top side
                    if other.get_center()[1] + other.get_radius() >= self.center[1] - self.radius:
                        # check bottom side
                        if other.get_center()[1] - other.get_radius() <= self.center[1] + self.radius:
                            if self.status == 'player_bullet':
                                if self.color == other.get_color() and not self.shot_yes:  # if hits opposite color, then other dot dies
                                    other.shot()
                                if not other.get_shot_status():
                                    self.shot()  # disapear bullet no matter what as long as other thing is not already shot
                            else:
                                if self.color != other.get_color() and not self.shot_yes:  # if hits opposite color, then other dot dies
                                    if other.get_status() != 'player':
                                        other.shot()
                                if not other.get_shot_status():
                                    self.shot()  # disapear bullet no matter what as long as other thing is not already shot

        if self.status == 'enemy' and not self.shot_yes:
            # this whole if statement also checks if enemy moving in the same direction as other dot is detected
            # check left side
            # check that dot is close to enemy
            if (self.center[0] - self.radius - 20) - (other.get_center()[0] + other.get_radius()) < 0:
                if self.velocity[0] < 0:  # check that enemy is moving towards dot
                    # check that dot hasn't gone past enemy
                    if self.center[0] + self.radius > other.get_center()[0] + other.get_radius():
                        # check that color and vertical coordinates line up
                        if other.get_color() != self.color and self.check_shoot_range(other, 'x'):
                            return True
            # check right side
            if (other.get_center()[0] - other.get_radius()) - (self.center[0] + self.radius + 20) < 0:
                if self.velocity[0] > 0:
                    if self.center[0] - self.radius < other.get_center()[0] - other.get_radius():
                        if other.get_color() != self.color and self.check_shoot_range(other, 'x'):
                            return True
            # check top side
            if (self.center[1] - self.radius - 20) - (other.get_center()[1] + other.get_radius()) < 0:
                if self.velocity[1] > 0:
                    if self.center[1] + self.radius < other.get_center()[1] + other.get_radius():
                        if other.get_color() != self.color and self.check_shoot_range(other, 'y'):
                            return True
            # check bottom side
            if (other.get_center()[1] - other.get_radius()) - (self.center[1] + self.radius + 20) < 0:
                if self.velocity[1] < 0:
                    if self.center[1] - self.radius > other.get_center()[1] - other.get_radius():
                        if other.get_color() != self.color and self.check_shoot_range(other, 'y'):
                            return True
            return False

    def check_shoot_range(self, other, side):
        # after enemy checks if player in surrounding, check if player in shootable range
        if side == 'x':  # check vertical coordinates
            # check top side
            if other.get_center()[1] + other.get_radius() >= self.center[1] - self.radius:
                # check bottom side
                if other.get_center()[1] - other.get_radius() <= self.center[1] + self.radius:
                    return True
        if side == 'y':  # check horizontal coordinates
            # check left side
            if other.get_center()[0] + other.get_radius() >= self.center[0] - self.radius:
                # check right side
                if other.get_center()[0] - other.get_radius() <= self.center[0] + self.radius:
                    return True
        return False


main()
