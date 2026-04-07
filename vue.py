import pygame
import math

class VuePygame:
    def __init__(self, scale=35):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.scale = scale
        self.font_big = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 28)

    def convertir_coordonnees(self, x, y):
        return int(400 + x * self.scale), int(300 - y * self.scale)

    def dessiner(self, env):
        fond = (25, 25, 45) if env.est_nuit else (235, 215, 180)
        self.screen.fill(fond)
        if env.zone_eau: env.zone_eau.dessiner(self)
        for obj in env.zones_vertes + env.zones_safes + env.murs + env.gardes:
            obj.dessiner(self)

        if env.robot:
            px, py = self.convertir_coordonnees(env.robot.x, env.robot.y)
            # Dessin Lidar
            for a in [env.robot.orientation + i for i in [-1.2, -0.6, -0.3, 0, 0.3, 0.6, 1.2]]:
                d = env.lancer_rayon(env.robot.x, env.robot.y, a, 3.0)
                p_fin = self.convertir_coordonnees(env.robot.x + d * math.cos(a), env.robot.y + d * math.sin(a))
                pygame.draw.line(self.screen, (0, 200, 0), (px, py), p_fin, 1)
            
            couleur = (220, 50, 50) if env.game_over else (50, 200, 50)
            pygame.draw.circle(self.screen, couleur, (px, py), int(0.3 * self.scale))
            pygame.draw.line(self.screen, (255,255,255), (px, py), 
                             (px + int(15*math.cos(env.robot.orientation)), py - int(15*math.sin(env.robot.orientation))), 2)

        if env.game_over: self._dessiner_game_over(env)
        pygame.display.flip()

    def _dessiner_game_over(self, env):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        t1 = self.font_big.render("GAME OVER", True, (220, 50, 50))
        t2 = self.font_small.render(env.game_over_raison, True, (255, 220, 100))
        self.screen.blit(t1, t1.get_rect(center=(400, 250)))
        self.screen.blit(t2, t2.get_rect(center=(400, 330)))