import pygame
import math

class VuePygame:
    def __init__(self, largeur=800, hauteur=600, scale=50):
        pygame.init()
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.scale = scale
        self.clock = pygame.time.Clock()

    def dessiner_robot(self, robot):
        self.screen.fill((255, 255, 255)) # Fond blanc
        
        # Conversion mètres -> pixels (Centre de l'écran)
        px = int(400 + robot.x * self.scale)
        py = int(300 - robot.y * self.scale)
        
        # Dessin du corps (Cercle bleu)
        pygame.draw.circle(self.screen, (0, 0, 255), (px, py), 20)
        
        # Dessin de l'orientation (Ligne rouge)
        x_dir = px + int(25 * math.cos(robot.orientation))
        y_dir = py - int(25 * math.sin(robot.orientation))
        pygame.draw.line(self.screen, (255, 0, 0), (px, py), (x_dir, y_dir), 3)
        
        pygame.display.flip()

    def tick(self):
        self.clock.tick(60) # 60 FPS