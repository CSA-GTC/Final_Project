'''

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Gregory Clarke
Advanced Computer Programing
5/28/2019

Version 1.0

'''

import pygame, sys, random, math
import pygame as pg
from pygame.locals import *

backgroundc = (0, 0, 0)
entity_color = (255, 255, 255)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
RED = (255, 0, 0)
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)


class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Paddle(Entity):
    """
    Player controlled or AI controlled, main interaction with
    the gamen
    """

    def __init__(self, x, y, width, height):
        super(Paddle, self).__init__(x, y, width, height)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(entity_color)

class Line(Paddle):
    """
    AI controlled paddle, simply moves towards the ball
    and nothing else.
    """

    def __init__(self, x, y, width, height):
        super(Line, self).__init__(x, y, width, height)

        self.x_change = 5

    def update(self):
        """
        Moves the Paddle while ensuring it stays in bounds
        """
        # Moves the Paddle up if the ball is above,
        # and down if below.
        self.rect.move_ip(self.x_change, 0)

        # The paddle can never go above the window since it follows
        # the ball, but this keeps it from going under.
        if self.rect.x + self.width > window_width:
            self.x_change *= -1

        if self.rect.x + self.width < 0 + self.width:
            self.x_change *= -1

class Square(Paddle):
    """
    AI controlled paddle, simply moves towards the ball
    and nothing else.
    """

    def __init__(self, x, y, width, height):
        super(Square, self).__init__(x, y, width, height)
        self.image.fill(GRAY)



class Ball(Entity):

    """
    The ball!  Moves around the screen.
    """

    def __init__(self, x, y, width, height):
        super(Ball, self).__init__(x, y, width, height)

        self.image = pygame.image.load("green_dot.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.x_direction = random.randint(1, 2)
        if self.x_direction == 1:
            self.x_direction = 1

        if self.x_direction == 2:
            self.x_direction = -1

        self.y_direction = random.randint(1, 2)
        if self.y_direction == 0:
            self.y_direction = 1

        if self.y_direction == 2:
            self.y_direction = -1

        # Current speed.
        self.speed = 6

    def update(self):
        if self.speed > 25:
            self.speed = 25
        # Move the ball!
        self.rect.move_ip(self.speed * self.x_direction,
                          self.speed * self.y_direction)

        # Keep the ball in bounds, and make it bounce off the sides.
        if self.rect.y < 0:
            self.y_direction *= -1
            self.image = pygame.image.load("blue_dot.png").convert_alpha()
            self.speed += .5

        elif self.rect.y > window_height - 50:
            self.y_direction *= -1
            self.image = pygame.image.load("green_dot.png").convert_alpha()
            self.speed += .5

        if self.rect.x < 0:
            self.x_direction *= -1
            self.image = pygame.image.load("blue_dot.png").convert_alpha()
            self.speed += .5

        elif self.rect.x > window_width - 50:
            self.x_direction *= -1
            self.image = pygame.image.load("green_dot.png").convert_alpha()
            self.speed += .5

        if self.rect.colliderect(line.rect):
            self.image = pygame.image.load("green_dot.png").convert_alpha()
            self.speed += .5
            self.y_direction *= -1

        if self.rect.colliderect(square.rect):
            self.image = pygame.image.load("blue_dot.png").convert_alpha()
            self.speed += .5
            if self.y_direction == 1:
                self.y_direction = -1

            if self.x_direction == 1:
                self.x_direction = -1



pygame.init()

window_width = 640
window_height = 480
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Final Program - Gregory Clarke")
clock = pygame.time.Clock()
screen_rect = screen.get_rect()

line = Line(window_width/2, 50, 200, 4)
ball = Ball(window_width/2, window_height/2, 50, 50)
square = Square(540, 380, 100, 100)

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(line)
all_sprites_list.add(ball)
all_sprites_list.add(square)

font = pygame.font.SysFont('arial', 32)  # fonts

textSurfaceObj = font.render("PRESS SPACE TO START", True, WHITE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (window_width/2, window_height/2)

textSurfaceObj2 = font.render("CHANGE", True, WHITE)
textRectObj2 = textSurfaceObj2.get_rect()
textRectObj2.center = (570, 25)

COLOR = BLUE

GAME = True

START = True
RUNNING = False


while GAME:

    if START == True:
        screen.fill(BLACK)
        screen.blit(textSurfaceObj, textRectObj)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    START = False
                    RUNNING = True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if mouse[0] > 280 and mouse[0] < 360 and mouse[1] > 200 and mouse[1] < 280:
                    START = False
                    RUNNING = True

            pygame.display.update()

   
    if RUNNING == True:

        # Event processing here
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if mouse[0] > 500 and mouse[1] < 40:

                    new = random.randint(1, 3)
                    if new == 1:
                        if COLOR != BLUE:
                            COLOR = BLUE

                    if new == 2:
                        if COLOR != BLACK:
                            COLOR = BLACK

                    if new == 3:
                        if COLOR != RED:
                            COLOR = RED

        screen.fill(COLOR)
        all_sprites_list.update()
        all_sprites_list.draw(screen)
        screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
    