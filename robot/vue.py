import pygame
import math

class VuePygame:
    def __init__(self, largeur=800, hauteur=600, scale=50):
        pygame.init()
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.scale = scale
        self.clock = pygame.time.Clock()

    def convertir_coordonnees(self, x, y):
        px = int(self.screen.get_width() / 2 + (x * self.scale))
        py = int(self.screen.get_height() / 2 - (y * self.scale))
        return px, py

    def dessiner(self, environnement):
        self.screen.fill((255, 255, 255)) # Fond blanc
        
        # 1. Dessiner les obstacles
        for obs in environnement.obstacles:
            obs.dessiner(self)
            
        # 2. Dessiner le robot
        if environnement.robot:
            r = environnement.robot
            px, py = self.convertir_coordonnees(r.x, r.y)
            rayon_px = int(0.4 * self.scale)
            
            # Corps
            pygame.draw.circle(self.screen, (0, 100, 255), (px, py), rayon_px)
            # Direction
            x_dir = px + int(rayon_px * math.cos(r.orientation))
            y_dir = py - int(rayon_px * math.sin(r.orientation))
            pygame.draw.line(self.screen, (255, 0, 0), (px, py), (x_dir, y_dir), 3)
            
        pygame.display.flip()

    def tick(self, fps=60):
        self.clock.tick(fps)