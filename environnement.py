import math
import random
import pygame
from abc import ABC, abstractmethod


class Obstacle(ABC):
    @abstractmethod
    def collision(self, xr, yr, rr) -> bool:
        pass


class Mur(Obstacle):
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def collision(self, xr, yr, rr):
        dx, dy = self.x2 - self.x1, self.y2 - self.y1
        if dx == 0 and dy == 0:
            return False
        t = max(0, min(1, ((xr - self.x1) * dx + (yr - self.y1) * dy) / (dx**2 + dy**2)))
        px, py = self.x1 + t * dx, self.y1 + t * dy
        return math.hypot(xr - px, yr - py) <= rr

    def dessiner(self, vue):
        p1 = vue.convertir_coordonnees(self.x1, self.y1)
        p2 = vue.convertir_coordonnees(self.x2, self.y2)
        pygame.draw.line(vue.screen, (50, 30, 10), p1, p2, 6)

    def coupe_segment(self, ax, ay, bx, by):
        def orientation(px, py, qx, qy, rx, ry):
            val = (qy - py) * (rx - qx) - (qx - px) * (ry - qy)
            if abs(val) < 1e-9:
                return 0
            return 1 if val > 0 else 2

        def on_segment(px, py, qx, qy, rx, ry):
            return (
                min(px, rx) - 1e-9 <= qx <= max(px, rx) + 1e-9
                and min(py, ry) - 1e-9 <= qy <= max(py, ry) + 1e-9
            )

        p1x, p1y = ax, ay
        q1x, q1y = bx, by
        p2x, p2y = self.x1, self.y1
        q2x, q2y = self.x2, self.y2

        o1 = orientation(p1x, p1y, q1x, q1y, p2x, p2y)
        o2 = orientation(p1x, p1y, q1x, q1y, q2x, q2y)
        o3 = orientation(p2x, p2y, q2x, q2y, p1x, p1y)
        o4 = orientation(p2x, p2y, q2x, q2y, q1x, q1y)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and on_segment(p1x, p1y, p2x, p2y, q1x, q1y):
            return True
        if o2 == 0 and on_segment(p1x, p1y, q2x, q2y, q1x, q1y):
            return True
        if o3 == 0 and on_segment(p2x, p2y, p1x, p1y, q2x, q2y):
            return True
        if o4 == 0 and on_segment(p2x, p2y, q1x, q1y, q2x, q2y):
            return True

        return False


class ZoneEau(Obstacle):
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def collision(self, xr, yr, rr):
        return (
            self.x - self.w / 2 <= xr <= self.x + self.w / 2
            and self.y - self.h / 2 <= yr <= self.y + self.h / 2
        )

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x - self.w / 2, self.y + self.h / 2)
        pygame.draw.rect(vue.screen, (0, 100, 200), (px, py, int(self.w * vue.scale), int(self.h * vue.scale)))


class ZoneSafe:
    def __init__(self, x, y, nom):
        self.x, self.y, self.nom = x, y, nom

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x, self.y)
        s = int(0.8 * vue.scale)
        pygame.draw.rect(vue.screen, (200, 180, 150), (px - s // 2, py - s // 2, s, s))
        pygame.draw.polygon(vue.screen, (150, 0, 0), [(px - s // 2, py - s // 2), (px + s // 2, py - s // 2), (px, py - s)])


class ZoneVerte:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def contient(self, x, y):
        return (
            self.x - self.w / 2 <= x <= self.x + self.w / 2
            and self.y - self.h / 2 <= y <= self.y + self.h / 2
        )

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x - self.w / 2, self.y + self.h / 2)
        s = pygame.Surface((int(self.w * vue.scale), int(self.h * vue.scale)), pygame.SRCALPHA)
        s.fill((34, 139, 34, 180))
        vue.screen.blit(s, (px, py))


class Garde:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.orientation = random.uniform(0, 2 * math.pi)
        self.v = 1.2

    def mettre_a_jour(self, dt, env):
        vit = self.v * (1.8 if env.alerte else 1.0)
        nx = self.x + math.cos(self.orientation) * vit * dt
        ny = self.y + math.sin(self.orientation) * vit * dt

        if abs(nx) > env.largeur / 2 or abs(ny) > env.hauteur / 2 or any(m.collision(nx, ny, 0.5) for m in env.murs):
            self.orientation += math.pi / 2 + random.uniform(-0.5, 0.5)
        else:
            self.x, self.y = nx, ny

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x, self.y)
        pygame.draw.circle(vue.screen, (220, 20, 20), (px, py), int(0.4 * vue.scale))
        p2 = vue.convertir_coordonnees(
            self.x + 1.2 * math.cos(self.orientation),
            self.y + 1.2 * math.sin(self.orientation)
        )
        pygame.draw.line(vue.screen, (255, 0, 0), (px, py), p2, 2)


class Environnement:
    def __init__(self, largeur, hauteur):
        self.largeur, self.hauteur, self.heure = largeur, hauteur, 12.0
        self.murs, self.zones_vertes, self.zones_safes, self.gardes = [], [], [], []
        self.zone_eau, self.robot = None, None
        self.game_over = False
        self.game_over_raison = ""
        self.alerte = False

        self.distance_securite_garde = 1.25

    def ajouter_robot(self, robot):
        self.robot = robot

    @property
    def est_nuit(self):
        return self.heure < 6 or self.heure > 20

    def robot_dans_haute_herbe(self):
        if not self.robot:
            return False
        return any(zv.contient(self.robot.x, self.robot.y) for zv in self.zones_vertes)

    def robot_cache(self):
        return self.robot_dans_haute_herbe()

    def vue_directe_libre(self, x1, y1, x2, y2):
        for mur in self.murs:
            if mur.coupe_segment(x1, y1, x2, y2):
                return False
        return True

    def lancer_rayon(self, x_dep, y_dep, angle, distance_max=8.0):
        pas, dist = 0.12, 0.0
        while dist < distance_max:
            dist += pas
            rx = x_dep + dist * math.cos(angle)
            ry = y_dep + dist * math.sin(angle)
            if any(m.collision(rx, ry, 0.1) for m in self.murs) or abs(rx) > self.largeur / 2 or abs(ry) > self.hauteur / 2:
                return dist
        return distance_max

    def mettre_a_jour(self, dt):
        if self.game_over:
            return

        self.heure = (self.heure + dt * 0.4) % 24

        for g in self.gardes:
            g.mettre_a_jour(dt, self)

        if not self.robot:
            return

        old_x, old_y = self.robot.x, self.robot.y
        self.robot.mettre_a_jour(dt, self)

        if any(m.collision(self.robot.x, self.robot.y, 0.3) for m in self.murs) or \
           (self.zone_eau and self.zone_eau.collision(self.robot.x, self.robot.y, 0.3) and not self.est_nuit):
            self.robot.x, self.robot.y = old_x, old_y

        if self.robot.energie <= 0:
            self.game_over = True
            self.game_over_raison = "BATTERIE VIDE"
            return

        # Contact direct garde / robot
        for g in self.gardes:
            if math.hypot(self.robot.x - g.x, self.robot.y - g.y) < 0.72:
                self.game_over = True
                self.game_over_raison = "CAPTURE !"
                return

        self.alerte = False

        for g in self.gardes:
            d = math.hypot(self.robot.x - g.x, self.robot.y - g.y)
            angle_vers_robot = math.atan2(self.robot.y - g.y, self.robot.x - g.x)
            diff_angle = abs((angle_vers_robot - g.orientation + math.pi) % (2 * math.pi) - math.pi)

            if not self.vue_directe_libre(g.x, g.y, self.robot.x, self.robot.y):
                continue

            if self.robot_dans_haute_herbe():
                seuil_distance = 2.3
                seuil_angle = 0.55
                seuil_capture = 1.0
            else:
                seuil_distance = 4.0
                seuil_angle = 0.8
                seuil_capture = 1.5

            if d < seuil_distance and diff_angle < seuil_angle:
                if d < seuil_capture:
                    self.game_over = True
                    self.game_over_raison = "REPERE !"
                    return
                self.alerte = True