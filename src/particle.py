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
             reflection_angle, intensity, px, is_primary, x_multiplier, y_multiplier, traveled_distance, angle_energy):
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
            tem_angle_energy = 0

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
                        tem_angle_energy = 180 - incidence_angle

                    elif ray.get_incidence_angle() <= 90:
                        reflection_angle = reflection_angle - 2 * incidence_angle
                        tem_angle_energy = incidence_angle

                else:  # left
                    if ray.get_incidence_angle() > 90:
                        reflection_angle = reflection_angle - 2 * (180 - incidence_angle)
                        tem_angle_energy = 180 - incidence_angle

                    elif ray.get_incidence_angle() <= 90:
                        reflection_angle = reflection_angle + 2 * incidence_angle
                        tem_angle_energy = incidence_angle

            if closest_point is not None:
                if iteration == 0 and is_primary:
                    origin_pos = closest_point
                    x_multiplier, y_multiplier = ray.get_multipliers()
                    pygame.draw.line(screen, (255, 255, 255), sonar_position,
                                     (array(closest_point, int)[0], array(closest_point, int)[1]), 1)

                if iteration == 0 and not is_primary:
                    pygame.draw.line(screen, (255, 100, 255), sonar_position,
                                     (array(closest_point, int)[0], array(closest_point, int)[1]), 1)
                if iteration > 0:
                    pygame.draw.line(screen, (255, 255, 100), sonar_position,
                                     (array(closest_point, int)[0], array(closest_point, int)[1]), 1)

            if is_not_sonar and closest_point is not None and iteration <= 2:
                traveled_distance += closest
                intensity -= traveled_distance * 0.31875  # resta repecto a la distancia

                if iteration == 0 and is_primary:
                    angle_energy = tem_angle_energy
                    intensity -= (1 / angle_energy) * 500  # resta respecto al angulo de incidencia
                    tem_x = array(origin_pos, int)[0]
                    tem_y = array(origin_pos, int)[1]
                    if 0 < tem_x < 800 and 0 < tem_y < 800 and 0 <= intensity <= 255:
                        px[tem_x][tem_y] = [intensity, intensity, intensity]

                if (iteration < 2 and not is_primary and origin_pos is not None) or (is_primary and 0 < iteration <= 2):
                    angle_energy = absolute(angle_energy - tem_angle_energy)
                    intensity -= (1 / angle_energy) * 500 - 5.56  # resta respecto al angulo de incidencia
                    tem_distance = linalg.norm(origin_pos - closest_point)
                    tem_distance = int(tem_distance)
                    pixel_color = px[array(origin_pos, int)[0] - 10][array(origin_pos - 10, int)[1]]
                    if pixel_color[0] < intensity:
                        tem_x = array(origin_pos, int)[0] - tem_distance * x_multiplier
                        tem_y = array(origin_pos, int)[1] - tem_distance * y_multiplier
                        if 0 < tem_x < 800 and 0 < tem_y < 800 and 0 <= intensity <= 255:
                            px[tem_x][tem_y] = [intensity, intensity, intensity]

                if iteration < 2:
                    self.look(screen, walls, sonar_walls, iteration + 1, array(closest_point, int), origin_pos,
                              incidence_angle, reflection_angle, intensity, px, is_primary, x_multiplier, y_multiplier,
                              traveled_distance, angle_energy)

                    if iteration == 0 and is_primary:
                        return origin_pos, x_multiplier, y_multiplier

            return None, None, None
