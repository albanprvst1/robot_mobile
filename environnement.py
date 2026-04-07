import math
import random
import pygame
from abc import ABC, abstractmethod

class Obstacle(ABC):
    @abstractmethod
    def collision(self, xr, yr, rr) -> bool: pass

class Mur(Obstacle):
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def collision(self, xr, yr, rr):
        dx, dy = self.x2 - self.x1, self.y2 - self.y1
        if dx == 0 and dy == 0: return False
        t = max(0, min(1, ((xr - self.x1)*dx + (yr - self.y1)*dy) / (dx**2 + dy**2)))
        px, py = self.x1 + t*dx, self.y1 + t*dy
        return math.sqrt((xr-px)**2 + (yr-py)**2) <= rr

    def dessiner(self, vue):
        p1 = vue.convertir_coordonnees(self.x1, self.y1)
        p2 = vue.convertir_coordonnees(self.x2, self.y2)
        pygame.draw.line(vue.screen, (50, 30, 10), p1, p2, 6)

class ZoneEau(Obstacle):
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def collision(self, xr, yr, rr):
        return (self.x - self.w/2 <= xr <= self.x + self.w/2 and
                self.y - self.h/2 <= yr <= self.y + self.h/2)

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x - self.w/2, self.y + self.h/2)
        pygame.draw.rect(vue.screen, (0, 100, 200),
                         (px, py, int(self.w * vue.scale), int(self.h * vue.scale)))

class ZoneSafe:
    def __init__(self, x, y, nom):
        self.x, self.y, self.nom = x, y, nom

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x, self.y)
        s = int(0.8 * vue.scale)
        pygame.draw.rect(vue.screen, (200, 180, 150), (px - s//2, py - s//2, s, s))
        pygame.draw.polygon(vue.screen, (150, 0, 0),
                            [(px-s//2-4, py-s//2), (px+s//2+4, py-s//2), (px, py-s)])

class ZoneVerte:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def contient(self, x, y):
        return (self.x - self.w/2 <= x <= self.x + self.w/2 and
                self.y - self.h/2 <= y <= self.y + self.h/2)

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x - self.w/2, self.y + self.h/2)
        s = pygame.Surface((int(self.w * vue.scale), int(self.h * vue.scale)), pygame.SRCALPHA)
        s.fill((34, 139, 34, 180))
        vue.screen.blit(s, (px, py))

class Garde:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx, self.vy = random.choice([-1, 1]), random.choice([-1, 1])

    def mettre_a_jour(self, dt, env):
        nx, ny = self.x + self.vx * dt, self.y + self.vy * dt
        if abs(nx) > env.largeur/2 or any(m.collision(nx, ny, 0.4) for m in env.murs):
            self.vx *= -1
        if abs(ny) > env.hauteur/2 or any(m.collision(nx, ny, 0.4) for m in env.murs):
            self.vy *= -1
        self.x += self.vx * dt
        self.y += self.vy * dt

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x, self.y)
        pygame.draw.circle(vue.screen, (255, 0, 0), (px, py), int(0.4 * vue.scale))

class Environnement:
    def __init__(self, largeur, hauteur):
        self.largeur, self.hauteur, self.heure = largeur, hauteur, 12.0
        self.murs, self.zones_vertes, self.zones_safes, self.gardes = [], [], [], []
        self.zone_eau, self.robot = None, None
        self.game_over        = False
        self.game_over_raison = ""

    def ajouter_robot(self, robot):
        self.robot = robot

    @property
    def est_nuit(self):
        return self.heure < 6 or self.heure > 20

    def robot_cache(self):
        if not self.robot: return False
        return any(zv.contient(self.robot.x, self.robot.y) for zv in self.zones_vertes)

    def lancer_rayon(self, x_dep, y_dep, angle, distance_max=6.0):
        """Simule un capteur Lidar."""
        pas, dist = 0.2, 0.0
        while dist < distance_max:
            dist += pas
            rx, ry = x_dep + dist * math.cos(angle), y_dep + dist * math.sin(angle)
            if any(m.collision(rx, ry, 0.1) for m in self.murs) or \
               abs(rx) > self.largeur/2 or abs(ry) > self.hauteur/2:
                return dist
        return distance_max

    def mettre_a_jour(self, dt):
        if self.game_over: return
        self.heure = (self.heure + dt * 0.5) % 24
        for g in self.gardes: g.mettre_a_jour(dt, self)
        if not self.robot: return
        old_x, old_y = self.robot.x, self.robot.y
        self.robot.mettre_a_jour(dt)
        if any(m.collision(self.robot.x, self.robot.y, 0.3) for m in self.murs) or \
           (self.zone_eau and self.zone_eau.collision(self.robot.x, self.robot.y, 0.3) and not self.est_nuit):
            self.robot.x, self.robot.y = old_x, old_y
        
        # Détection
        dist_detec = 1.0 if self.est_nuit else 1.75
        for g in self.gardes:
            d = math.hypot(self.robot.x - g.x, self.robot.y - g.y)
            if (not self.robot_cache() and d < dist_detec) or (self.robot_cache() and d < 0.3):
                self.game_over, self.game_over_raison = True, "Repéré !"
                return