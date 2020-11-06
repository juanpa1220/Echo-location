from src.ray import *
import random


def display(screen, pos):
    pygame.draw.circle(screen, (255, 255, 255), pos, 10, 10)  # sonar
    # for ray in self.rays:
    #     ray.display(screen)


class Particle:
    def __init__(self):
        self.rays = []

    def look(self, screen, walls, sonar_walls, iteration, sonar_position, origin_pos, incidence_angle,
             reflection_angle):
        self.rays = []
        is_not_sonar = True
        self.rays.append(Ray(sonar_position[0], sonar_position[1], reflection_angle))

        # if iteration == 0:
        #     self.rays.append(Ray(sonar_position[0], sonar_position[1], reflection_angle))
        # else:
        #     for i in range(10):
        #         self.rays.append(Ray(sonar_position[0], sonar_position[1], reflection_angle))
        #         self.rays.append(Ray(sonar_position[0], sonar_position[1], reflection_angle +
        #                              random.randint(-int(incidence_angle), int(reflection_angle + incidence_angle))))

        for ray in self.rays:

            closest = 10000000
            closest_point = None
            closest_wall = None

            for wall in walls:
                intersection_point = ray.cast(wall, True)
                if intersection_point is not None:
                    distance = linalg.norm(intersection_point - sonar_position)
                    if closest > distance > 4:
                        closest = distance
                        closest_point = intersection_point
                        closest_wall = wall

            for wall in sonar_walls:
                intersection_point = ray.cast(wall, False)
                if intersection_point is not None:
                    distance = linalg.norm(intersection_point - sonar_position)
                    if closest > distance > 15:
                        closest = distance
                        closest_point = intersection_point
                        closest_wall = wall
                        is_not_sonar = False

            if is_not_sonar and closest_wall is not None:
                ray.cast(closest_wall, True)
                incidence_angle = ray.get_incidence_angle()

                if ray.get_orientation():  # right
                    if ray.get_incidence_angle() > 90:
                        reflection_angle = reflection_angle + 2 * (180 - incidence_angle)
                    elif ray.get_incidence_angle() <= 90:
                        reflection_angle = reflection_angle - 2 * incidence_angle

                else:  # left
                    if ray.get_incidence_angle() > 90:
                        reflection_angle = reflection_angle - 2 * (180 - incidence_angle)

                    elif ray.get_incidence_angle() <= 90:
                        reflection_angle = reflection_angle + 2 * incidence_angle

            if closest_point is not None:
                if iteration == 0:
                    pygame.draw.line(screen, (255, 255, 255), sonar_position,
                                     (array(closest_point, int)[0], array(closest_point, int)[1]), 2)
                if iteration > 0:
                    pygame.draw.line(screen, (255, 255, 100), sonar_position,
                                     (array(closest_point, int)[0], array(closest_point, int)[1]), 2)

            if is_not_sonar and closest_point is not None and iteration < 2:
                self.look(screen, walls, sonar_walls, iteration + 1, array(closest_point, int), origin_pos,
                          incidence_angle, reflection_angle)
            if not is_not_sonar:
                pygame.draw.circle(screen, (255, 255, 255), origin_pos, 1, 1)
