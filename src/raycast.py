# subscribe to auctux
# https://www.youtube.com/channel/UCjPk9YDheKst1FlAf_KSpyA

from pygame.locals import *
from src.Limits import *
from src.particle import *
from PIL import Image
import numpy as np
from numpy import absolute
import random

WIDTH = 800  # ancho
HEIGHT = 800  # alto
SCREEN = (WIDTH, HEIGHT)


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN)
        init_sonar_x = 650
        init_sonar_y = 250

        # walls
        self.walls = []
        self.sonar_walls = []

        # self.walls.append(Limits(146, 518, 455, 750))
        # self.walls.append(Limits(336, 161, 56, 587))
        # self.walls.append(Limits(49, 184, 541, 282))
        # self.walls.append(Limits(162, 60, 389, 593))
        # self.walls.append(Limits(45, 30, 112, 662))

        # esquinas
        self.walls.append(Limits(110, 0, 0, 100))
        self.walls.append(Limits(0, 700, 100, 810))
        self.walls.append(Limits(800, 700, 690, 800))
        self.walls.append(Limits(690, 0, 800, 100))

        self.walls.append(Limits(120, 80, 180, 200))
        self.walls.append(Limits(180, 200, 300, 320))
        self.walls.append(Limits(300, 320, 200, 400))

        self.walls.append(Limits(100, 200, 0, 500))

        # equis
        self.walls.append(Limits(80, 500, 300, 700))
        self.walls.append(Limits(300, 500, 80, 700))

        # rombo de arriba
        self.walls.append(Limits(355, 50, 300, 100))
        self.walls.append(Limits(355, 50, 400, 100))
        self.walls.append(Limits(300, 100, 345, 150))
        self.walls.append(Limits(400, 100, 345, 150))

        # rombo de abajo
        self.walls.append(Limits(455, 400, 400, 450))
        self.walls.append(Limits(455, 400, 500, 450))
        self.walls.append(Limits(400, 450, 445, 500))
        self.walls.append(Limits(500, 450, 445, 500))

        self.walls.append(Limits(640, 780, 350, 790))

        self.sonar_walls.append(
            Limits(init_sonar_x - 10, init_sonar_y - 10, init_sonar_x - 10, init_sonar_y + 10))  # frente
        self.sonar_walls.append(
            Limits(init_sonar_x - 10, init_sonar_y + 10, init_sonar_x + 10, init_sonar_y + 10))  # abajo
        self.sonar_walls.append(
            Limits(init_sonar_x - 10, init_sonar_y - 10, init_sonar_x + 10, init_sonar_y - 10))  # arriba
        self.sonar_walls.append(
            Limits(init_sonar_x + 10, init_sonar_y - 10, init_sonar_x + 10, init_sonar_y + 10))  # atras

        self.particle = Particle()
        self.stop_game = False
        self.clock = pygame.time.Clock()
        self.pos = array([init_sonar_x, init_sonar_y])

        self.i = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        self.px = np.array(self.i)

    def draw(self):
        # for wall in self.walls:
        #     wall.display(self.screen)
        # for wall in self.sonar_walls:
        #     wall.display(self.screen)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.pos[0], self.pos[1]), 12, 12)

    def run(self):
        angle = 170
        number_of_rays = 20
        number_second_rays = 2

        while not self.stop_game:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_game = True

                # mouse position
                if event.type == pygame.MOUSEMOTION:
                    tem_pos = event.pos
                    self.pos = array([tem_pos[0], tem_pos[1]])

                    self.sonar_walls[0] = Limits(tem_pos[0] - 10, tem_pos[1] - 10, tem_pos[0] - 10, tem_pos[1] + 10)
                    self.sonar_walls[1] = Limits(tem_pos[0] - 10, tem_pos[1] + 10, tem_pos[0] + 10, tem_pos[1] + 10)
                    self.sonar_walls[2] = Limits(tem_pos[0] - 10, tem_pos[1] - 10, tem_pos[0] + 10, tem_pos[1] - 10)
                    self.sonar_walls[3] = Limits(tem_pos[0] + 10, tem_pos[1] - 10, tem_pos[0] + 10, tem_pos[1] + 10)

            # Choose angle of sonar with key
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_RIGHT]:
                angle += 1.12
            if key_pressed[K_LEFT]:
                angle -= 1.12

            # Get a numpy array to display from the simulation
            pixels = np.roll(self.px, (1, 2), (0, 1))
            np_image = pixels

            # Convert to a surface and splat onto screen offset by border width and height
            surface = pygame.surfarray.make_surface(np_image)
            self.screen.blit(surface, (0, 0))

            # self.particle.look(self.screen, self.walls, self.sonar_walls, 0, self.pos, self.pos, angle, angle,
            #                    255, self.px, True, 1, 1, 0, 0)
            for i in range(number_of_rays):
                tem_angle = angle + random.uniform(-10, 10)
                origin_pos, x_multiplier, y_multiplier = self.particle.look(self.screen, self.walls, self.sonar_walls,
                                                                            0, self.pos, self.pos, tem_angle, tem_angle,
                                                                            255, self.px, True, 0, 0, 0, 0)
                for j in range(number_second_rays):
                    random_angle = random.uniform(-5, 5)
                    tem_angle_2 = tem_angle + random_angle
                    self.particle.look(self.screen, self.walls, self.sonar_walls, 0, self.pos, origin_pos,
                                       tem_angle_2, tem_angle_2, 255 - absolute(random_angle * 3), self.px, False,
                                       x_multiplier, y_multiplier, 0, 0)

            self.draw()
            self.clock.tick(10)
            pygame.display.update()


if __name__ == '__main__':
    D = Display()
    D.run()
