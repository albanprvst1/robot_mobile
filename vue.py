import pygame
import math

class VuePygame:
    def __init__(self, scale=35):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.scale, self.font_big, self.font_small = scale, pygame.font.SysFont("Arial", 60, True), pygame.font.SysFont("Arial", 24)

    def convertir_coordonnees(self, x, y): return int(400 + x * self.scale), int(300 - y * self.scale)

    def dessiner(self, env):
        self.screen.fill((25, 25, 45) if env.est_nuit else (230, 210, 180))
        if env.zone_eau: env.zone_eau.dessiner(self)
        for obj in env.zones_vertes + env.zones_safes + env.murs + env.gardes: obj.dessiner(self)
        if env.robot:
            px, py = self.convertir_coordonnees(env.robot.x, env.robot.y)
            c_lidar = (255, 50, 50) if env.alerte else (0, 200, 0)
            for a in [env.robot.orientation + i for i in [-1.2, -0.6, 0, 0.6, 1.2]]:
                d = env.lancer_rayon(env.robot.x, env.robot.y, a, 2.5)
                p2 = self.convertir_coordonnees(env.robot.x + d*math.cos(a), env.robot.y + d*math.sin(a))
                pygame.draw.line(self.screen, c_lidar, (px, py), p2, 1)
            pygame.draw.circle(self.screen, (50, 180, 50), (px, py), int((0.3 + len(env.robot.inventaire)*0.1)*self.scale))
        
        self.screen.blit(self.font_small.render(f"Inventaire: {', '.join(env.robot.inventaire)}", True, (255,255,255)), (20,20))
        if env.alerte: self.screen.blit(self.font_small.render("ALERTE : GARDES AGRESSIFS", True, (255,50,50)), (20,50))
        if env.game_over:
            t = self.font_big.render("GAME OVER", True, (255,50,50))
            self.screen.blit(t, t.get_rect(center=(400,300)))
        pygame.display.flip()