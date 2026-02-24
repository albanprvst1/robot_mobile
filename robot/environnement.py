import math
import random
import pygame
from abc import ABC, abstractmethod

class EntiteEnvironnement(ABC):
    @abstractmethod
    def dessiner(self, vue):
        pass

class Obstacle(EntiteEnvironnement):
    @abstractmethod
    def collision(self, x_robot, y_robot, rayon_robot) -> bool:
        pass

class ZoneSafe(EntiteEnvironnement):
    def __init__(self, x, y, nom, rayon=0.6):
        self.x, self.y, self.nom, self.rayon = x, y, nom, rayon

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x, self.y)
        pygame.draw.circle(vue.screen, (255, 215, 0), (px, py), int(self.rayon * vue.scale), 2)
        font = pygame.font.SysFont("Arial", 18, bold=True)
        texte = font.render(self.nom, True, (200, 150, 0))
        vue.screen.blit(texte, (px - 8, py - 25))

class Garde(Obstacle):
    def __init__(self, x, y, rayon=0.4):
        self.x, self.y, self.rayon = x, y, rayon
        self.couleur = (255, 50, 50)
        angle = random.uniform(0, 2 * math.pi)
        vitesse = 1.5
        self.vx = math.cos(angle) * vitesse
        self.vy = math.sin(angle) * vitesse

    def se_deplacer(self, dt, limite_x, limite_y):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if abs(self.x) > limite_x/2: self.vx *= -1
        if abs(self.y) > limite_y/2: self.vy *= -1

    def collision(self, xr, yr, rr):
        return math.sqrt((self.x - xr)**2 + (self.y - yr)**2) <= (self.rayon + rr)

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x, self.y)
        pygame.draw.circle(vue.screen, self.couleur, (px, py), int(self.rayon * vue.scale))

class ZoneVerte(EntiteEnvironnement):
    def __init__(self, x, y, largeur, hauteur):
        self.x, self.y, self.w, self.h = x, y, largeur, hauteur

    def est_interieur(self, xr, yr):
        return (self.x - self.w/2 <= xr <= self.x + self.w/2 and
                self.y - self.h/2 <= yr <= self.y + self.h/2)

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x - self.w/2, self.y + self.h/2)
        rect = pygame.Rect(px, py, int(self.w * vue.scale), int(self.h * vue.scale))
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        surface.fill((34, 139, 34, 150)) 
        vue.screen.blit(surface, (px, py))

class ZoneEau(Obstacle):
    def __init__(self, x, y, largeur, hauteur):
        self.x, self.y, self.w, self.h = x, y, largeur, hauteur

    def collision(self, xr, yr, rr):
        return (self.x - self.w/2 <= xr <= self.x + self.w/2 and
                self.y - self.h/2 <= yr <= self.y + self.h/2)

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self.x - self.w/2, self.y + self.h/2)
        rect = pygame.Rect(px, py, int(self.w * vue.scale), int(self.h * vue.scale))
        pygame.draw.rect(vue.screen, (0, 100, 255), rect)

class Environnement:
    def __init__(self, largeur=16.0, hauteur=12.0):
        self.largeur, self.hauteur = largeur, hauteur
        self.robot = None
        self.gardes, self.zones_vertes, self.zones_safes = [], [], []
        self.zone_eau = None
        self.heure = 12.0 

    def ajouter_robot(self, robot): self.robot = robot

    @property
    def est_nuit(self): return self.heure < 6.0 or self.heure > 20.0

    def mettre_a_jour(self, dt):
        self.heure = (self.heure + dt * 0.3) % 24.0
        for g in self.gardes: g.se_deplacer(dt, self.largeur, self.hauteur)
        if not self.robot: return
        old_pos = (self.robot.x, self.robot.y)
        self.robot.mettre_a_jour(dt)
        coll = any(g.collision(self.robot.x, self.robot.y, 0.3) for g in self.gardes)
        if self.zone_eau and not self.est_nuit:
            if self.zone_eau.collision(self.robot.x, self.robot.y, 0.3): coll = True
        if abs(self.robot.x) > self.largeur/2 or abs(self.robot.y) > self.hauteur/2: coll = True
        if coll: self.robot.x, self.robot.y = old_pos