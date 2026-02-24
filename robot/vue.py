import pygame
import math

class VuePygame:
    def __init__(self, scale=40):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.scale, self.clock = scale, pygame.time.Clock()

    def convertir_coordonnees(self, x, y):
        return int(400 + x*self.scale), int(300 - y*self.scale)

    def dessiner(self, env):
        fond = (30, 30, 50) if env.est_nuit else (200, 230, 255)
        self.screen.fill(fond)
        for zs in env.zones_safes: zs.dessiner(self)
        if env.zone_eau: env.zone_eau.dessiner(self)
        for zv in env.zones_vertes: zv.dessiner(self)
        for g in env.gardes: g.dessiner(self)
        if env.robot:
            px, py = self.convertir_coordonnees(env.robot.x, env.robot.y)
            pygame.draw.circle(self.screen, (50, 255, 50), (px, py), int(0.3 * self.scale))
        pygame.display.flip()

    def tick(self, fps=60): self.clock.tick(fps)