import pygame
import math

class VuePygame:
    def __init__(self, largeur=800, hauteur=600, scale=50):
        pygame.init()
        self.screen = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Simulation Robot Mobile - MVC")
        self.largeur = largeur
        self.hauteur = hauteur
        self.scale = scale
        self.clock = pygame.time.Clock()

    def dessiner_robot(self, robot):
        self.screen.fill((255, 255, 255)) # Fond blanc
        
        # Conversion mètres -> pixels (0,0 au centre)
        px = int(self.largeur / 2 + robot.x * self.scale)
        py = int(self.hauteur / 2 - robot.y * self.scale)
        
        # Dessin du robot (Cercle bleu)
        rayon_pixel = 20
        pygame.draw.circle(self.screen, (0, 100, 255), (px, py), rayon_pixel)
        
        # Ligne de direction (Rouge)
        x_dir = px + int(30 * math.cos(robot.orientation))
        y_dir = py - int(30 * math.sin(robot.orientation))
        pygame.draw.line(self.screen, (255, 0, 0), (px, py), (x_dir, y_dir), 3)
        
        pygame.display.flip()

    def tick(self, fps=60):
        self.clock.tick(fps)