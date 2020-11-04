import pygame

from numpy import array
from numpy import linalg
from numpy import cos, sin, arccos, arctan
from numpy import degrees
from numpy import dot
from numpy import deg2rad


class Ray:
    def __init__(self, x, y, radius):
        self.radius = radius
        self.ray_origin_position = [x, y]
        self.ray_direction = array([cos(deg2rad(radius)), sin(deg2rad(radius))])
        self.orientation = None
        self.incidence_angle = None

    def display(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.ray_origin_position,
                         self.ray_origin_position + self.ray_direction, 1)

    def cast(self, wall, is_not_sonar):
        # start point
        wall_x1 = wall.a[0]
        wall_y1 = wall.a[1]

        # end point
        wall_x2 = wall.b[0]
        wall_y2 = wall.b[1]

        # position of the ray
        ray_x1 = self.ray_origin_position[0]
        ray_y1 = self.ray_origin_position[1]
        ray_x2 = self.ray_origin_position[0] + self.ray_direction[0]
        ray_y2 = self.ray_origin_position[1] + self.ray_direction[1]

        # denominator
        den = (wall_x1 - wall_x2) * (ray_y1 - ray_y2) - (wall_y1 - wall_y2) * (ray_x1 - ray_x2)

        if den == 0:
            return None

        # numerator
        num = (wall_x1 - ray_x1) * (ray_y1 - ray_y2) - (wall_y1 - ray_y1) * (ray_x1 - ray_x2)

        # formula
        t = num / den
        u = -((wall_x1 - wall_x2) * (wall_y1 - ray_y1) - (wall_y1 - wall_y2) * (wall_x1 - ray_x1)) / den

        if 0 < t < 1 and u > 0:
            # Px, Py
            intersection_x = wall_x1 + t * (wall_x2 - wall_x1)
            intersection_y = wall_y1 + t * (wall_y2 - wall_y1)

            intersection_point = array([intersection_x, intersection_y])

            if is_not_sonar:
                # incidence angle
                a = array([wall_x2, wall_y2])
                b = intersection_point
                c = array([ray_x1, ray_y1])

                self.orientation = False  # Si es false es para la izquierda y true hacia la derecha

                # calcula los casos especiales de la orientacion
                tem_angle = get_norm_angle(self.radius)
                tem_wall_angle = degrees(arctan((wall_y2 - wall_y1) / (wall_x2 - wall_x1)))
                if c[0] < b[0] or (
                        wall_x1 < wall_x2 and get_quadrant(tem_angle) == 3 and 180 + tem_wall_angle < tem_angle
                ) or (
                        wall_x1 > wall_x2 and get_quadrant(tem_angle) == 2 and 180 - tem_wall_angle > tem_angle):
                    self.orientation = True

                ba = a - b
                bc = c - b
                cosine_angle = dot(ba, bc) / (linalg.norm(ba) * linalg.norm(bc))
                incidence_angle_rad = arccos(cosine_angle)

                self.incidence_angle = degrees(incidence_angle_rad)

            return intersection_point

    def get_incidence_angle(self):
        return self.incidence_angle

    def get_orientation(self):
        return self.orientation


def get_norm_angle(angle):
    if angle > 360 or angle < 0:
        while True:
            if angle > 360:
                angle -= 360
            if angle < 0:
                angle += 360
            if 0 <= angle <= 360:
                break
    return angle


def get_quadrant(angle):
    if 0 < angle < 90:
        return 1
    elif 90 < angle < 180:
        return 2
    elif 180 < angle < 270:
        return 3
    else:
        return 4
