# subscribe to auctux
# https://www.youtube.com/channel/UCjPk9YDheKst1FlAf_KSpyA

from pygame.locals import *
from src.Limits import *
from src.particle import *
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
        self.walls.append(Limits(146, 518, 455, 750))
        self.walls.append(Limits(336, 161, 56, 587))
        self.walls.append(Limits(49, 184, 541, 282))
        self.walls.append(Limits(162, 60, 389, 593))
        self.walls.append(Limits(45, 30, 112, 662))
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

    def draw(self):
        for wall in self.walls:
            wall.display(self.screen)
        # display(self.screen, self.pos)
        for wall in self.sonar_walls:
            wall.display(self.screen)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.pos[0], self.pos[1]), 12, 12)

    def run(self):
        angle = 180
        number_of_rays = 1
        number_second_rays = 1

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
            teclado = pygame.key.get_pressed()
            if teclado[K_RIGHT]:
                angle += 1.12
            if teclado[K_LEFT]:
                angle -= 1.12

            # self.particle.look(self.screen, self.walls, self.sonar_walls, 0, self.pos, self.pos, angle, 1000)
            for i in range(number_of_rays):
                tem_angle = angle + random.randint(-20, 20)
                self.particle.look(self.screen, self.walls, self.sonar_walls, 0, self.pos, self.pos,
                                   tem_angle, tem_angle, 255)
                for j in range(number_second_rays):
                    random_angle = random.randint(-10, 10)
                    tem_angle_2 = tem_angle + random_angle
                    self.particle.look(self.screen, self.walls, self.sonar_walls, 0, self.pos, self.pos,
                                       tem_angle_2, tem_angle_2, 255 - absolute(random_angle * 3))

            self.draw()
            self.clock.tick(10)
            pygame.display.update()


if __name__ == '__main__':
    D = Display()
    D.run()
