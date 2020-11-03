# subscribe to auctux
# https://www.youtube.com/channel/UCjPk9YDheKst1FlAf_KSpyA

from pygame.locals import *
from src.Limits import *
from src.particle import *
import random

WIDTH = 800  # ancho
HEIGHT = 800  # alto
SCREEN = (WIDTH, HEIGHT)


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN)

        # walls
        self.walls = []
        self.walls.append(Limits(146, 518, 455, 750))
        self.walls.append(Limits(336, 161, 56, 587))
        self.walls.append(Limits(49, 184, 541, 282))
        self.walls.append(Limits(162, 60, 389, 593))
        self.walls.append(Limits(45, 30, 112, 662))
        # ------------------- Aqui van las paredes que rodean la pantalla -----------------------------------
        # self.walls.append((Limits(0, 0, 800, 0)))
        # self.walls.append((Limits(0, 0, 0, 800)))
        # self.walls.append((Limits(800, 0, 800, 800)))
        # self.walls.append((Limits(0, 800, 800, 800)))

        self.particle = Particle()
        self.stop_game = False
        self.clock = pygame.time.Clock()
        self.pos = array([650, 250])

    def draw(self):
        for wall in self.walls:
            wall.display(self.screen)
        self.particle.display(self.screen, self.pos)

    def run(self):
        angle = 180
        numberOfRays = 10
        contador = 0
        posibleAngle = []
        while not self.stop_game:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_game = True
                    # mouse position
                if event.type == pygame.MOUSEMOTION:
                    tem_pos = event.pos
                    if len(
                            self.walls) == 5:  # Aqui se crean las paredes que iran dentro del sonar para detectar colision
                        self.walls.append(
                            Limits(tem_pos[0] - 7.5, tem_pos[1] - 7.5, tem_pos[0] - 7.5, tem_pos[1] + 7.5))  # frente
                        self.walls.append(
                            Limits(tem_pos[0] - 7.5, tem_pos[1] + 7.5, tem_pos[0] + 7.5, tem_pos[1] + 7.5))  # abajo
                        self.walls.append(
                            Limits(tem_pos[0] - 7.5, tem_pos[1] - 7.5, tem_pos[0] + 7.5, tem_pos[1] - 7.5))  # arriba
                        self.walls.append(
                            Limits(tem_pos[0] + 7.5, tem_pos[1] - 7.5, tem_pos[0] + 7.5, tem_pos[1] + 7.5))  # atras
                    elif len(self.walls) > 5:
                        self.walls[5] = Limits(tem_pos[0] - 7.5, tem_pos[1] - 7.5, tem_pos[0] - 7.5, tem_pos[1] + 7.5)
                        self.walls[6] = Limits(tem_pos[0] - 7.5, tem_pos[1] + 7.5, tem_pos[0] + 7.5, tem_pos[1] + 7.5)
                        self.walls[7] = Limits(tem_pos[0] - 7.5, tem_pos[1] - 7.5, tem_pos[0] + 7.5, tem_pos[1] - 7.5)
                        self.walls[8] = Limits(tem_pos[0] + 7.5, tem_pos[1] - 7.5, tem_pos[0] + 7.5, tem_pos[1] + 7.5)
                    self.pos = array([tem_pos[0], tem_pos[1]])

            #self.particle.look(self.screen, self.walls, 0, self.pos, self.pos, angle)

            # -------------------------------------Posible solucion 1 -----------------------------------------------
            # for i in range(numberOfRays):
            #     posibleAngle.append(random.randint(-20, 20))
            #
            # for i in range(numberOfRays):
            #     self.particle.look(self.screen, self.walls, 0, self.pos, self.pos, angle + posibleAngle[i])

            # -------------------------------------Posible solucion 2 -----------------------------------------------

            if contador <= numberOfRays:
                self.particle.look(self.screen, self.walls, 0, self.pos, self.pos, angle + random.randint(-20, 20))

            # Choose angle of sonar with key
            teclado = pygame.key.get_pressed()
            if teclado[K_RIGHT]:
                angle += 0.5
            if teclado[K_LEFT]:
                angle -= 0.5

            self.draw()
            self.clock.tick(10)
            pygame.display.update()


if __name__ == '__main__':
    D = Display()
    D.run()
