import pygame
import sys
from Point import *

segments = [
    ([Point(180, 135), Point(215, 135)]),
    ([Point(285, 135), Point(320, 135)]),
    ([Point(320, 135), Point(320, 280)]),
    ([Point(320, 320), Point(320, 355)]),
    ([Point(320, 355), Point(215, 355)]),
    ([Point(180, 390), Point(180, 286)]),
    ([Point(180, 286), Point(140, 286)]),
    ([Point(320, 320), Point(360, 320)]),
    ([Point(180, 250), Point(180, 135)]),
]

# pygame stuff
pygame.init()
size = width, height = 550, 550
speed = [2, 2]
purple = 105, 75, 255
white = 255, 255, 255
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Clear screen to white before drawing
    screen.fill(white)

    # Draw line segments to have reference
    for segment in segments:
        pygame.draw.line(screen, purple, (segment[0].x, segment[0].y), (segment[1].x, segment[1].y))


    # screen.blit(ball, ball_rect)

    pygame.display.flip()
    clock.tick(60)
