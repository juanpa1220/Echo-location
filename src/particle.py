from src.ray import *


class Particle:
    def __init__(self):
        self.rays = []

    def display(self, screen, pos):
        pygame.draw.circle(screen, (255, 255, 255), pos, 5, 5)  # sonar
        # for ray in self.rays:
        #     ray.display(screen)

    def look(self, screen, walls, iteration, sonar_position, origin_pos, incidence_angle):
        # for i in range(incidence_angle - 10, incidence_angle + 10, 1):
        #     self.rays.append(Ray(pos[0], pos[1], deg2rad(1)))

        self.rays = []
        self.rays.append(Ray(sonar_position[0], sonar_position[1], incidence_angle))

        for ray in self.rays:

            closest = 10000000
            closest_point = None
            closest_wall = None

            for wall in walls[:5]:

                intersection_point = ray.cast(wall)

                if intersection_point is not None:
                    distance = linalg.norm(intersection_point - sonar_position)

                    if closest > distance > 5:
                        closest = distance
                        closest_point = intersection_point
                        closest_wall = wall

            if closest_wall is not None and ray.get_incidence_angle() is not None:
                ray.cast(closest_wall)
                if ray.get_orientation():  # derecha
                    if ray.get_incidence_angle() > 90:
                        incidence_angle += 2 * (180 - ray.get_incidence_angle())

                    elif ray.get_incidence_angle() <= 90:
                        incidence_angle -= 2 * (ray.get_incidence_angle())

                else:  # izquierda
                    if ray.get_incidence_angle() > 90:
                        incidence_angle -= 2 * (180 - ray.get_incidence_angle())

                    elif ray.get_incidence_angle() <= 90:
                        incidence_angle += 2 * ray.get_incidence_angle()

            if closest_point is not None:
                if iteration == 0:
                    pygame.draw.line(screen, (255, 255, 255), sonar_position,
                                     (array(closest_point, int)[0], array(closest_point, int)[1]), 2)
                if iteration == 1:
                    pygame.draw.line(screen, (255, 255, 100), sonar_position,
                                     (array(closest_point, int)[0], array(closest_point, int)[1]), 2)
                if iteration == 2:
                    pygame.draw.line(screen, (255, 255, 100), sonar_position,
                                     (array(closest_point, int)[0], array(closest_point, int)[1]), 2)

            if closest_point is not None and iteration < 2:
                self.look(screen, walls, iteration + 1, array(closest_point, int), origin_pos, incidence_angle)
