# subscribe to auctux
# https://www.youtube.com/channel/UCjPk9YDheKst1FlAf_KSpyA

from pygame.locals import *
from src.Limits import *
from src.particle import *

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
                        self.walls.append(Limits(tem_pos[0], tem_pos[1], tem_pos[0], tem_pos[1] + 15))  # frente
                        self.walls.append(
                            Limits(tem_pos[0], tem_pos[1] + 15, tem_pos[0] + 15, tem_pos[1] + 15))  # abajo
                        self.walls.append(Limits(tem_pos[0], tem_pos[1], tem_pos[0] + 15, tem_pos[1]))  # arriba
                        self.walls.append(
                            Limits(tem_pos[0] + 15, tem_pos[1], tem_pos[0] + 15, tem_pos[1] + 15))  # atras
                    elif len(self.walls) > 5:
                        self.walls[5] = Limits(tem_pos[0], tem_pos[1], tem_pos[0], tem_pos[1] + 15)
                        self.walls[6] = Limits(tem_pos[0], tem_pos[1] + 15, tem_pos[0] + 15, tem_pos[1] + 15)
                        self.walls[7] = Limits(tem_pos[0], tem_pos[1], tem_pos[0] + 15, tem_pos[1])
                        self.walls[8] = Limits(tem_pos[0] + 15, tem_pos[1], tem_pos[0] + 15, tem_pos[1] + 15)
                    self.pos = array([tem_pos[0], tem_pos[1]])

            self.particle.look(self.screen, self.walls, 0, self.pos, self.pos, angle)
            # Choose angle of sonar with key

            teclado = pygame.key.get_pressed()
            if teclado[K_RIGHT]:
                angle += 0.5
            if teclado[K_LEFT]:
                angle -= 0.5

            self.draw()
            self.clock.tick(100)
            pygame.display.update()


if __name__ == '__main__':
    D = Display()
    D.run()
