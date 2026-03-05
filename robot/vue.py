import pygame
import math

class VuePygame:
    def __init__(self, scale=35):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.scale, self.clock = scale, pygame.time.Clock()

    def convertir_coordonnees(self, x, y):
        return int(400 + x*self.scale), int(300 - y*self.scale)

    def dessiner(self, env):
        fond = (25, 25, 45) if env.est_nuit else (235, 215, 180)
        self.screen.fill(fond)
        
        # Ordre de rendu : Eau -> Vert -> Safe -> Murs -> Gardes -> Robot
        if env.zone_eau: env.zone_eau.dessiner(self)
        for zv in env.zones_vertes: zv.dessiner(self)
        for zs in env.zones_safes: zs.dessiner(self)
        for m in env.murs: m.dessiner(self)
        for g in env.gardes: g.dessiner(self)
        
        if env.robot:
            px, py = self.convertir_coordonnees(env.robot.x, env.robot.y)
            pygame.draw.circle(self.screen, (50, 200, 50), (px, py), int(0.3 * self.scale))
            x_dir = px + int(15 * math.cos(env.robot.orientation))
            y_dir = py - int(15 * math.sin(env.robot.orientation))
            pygame.draw.line(self.screen, (255, 255, 255), (px, py), (x_dir, y_dir), 2)
            
        pygame.display.flip()

    def tick(self, fps=60): self.clock.tick(fps)