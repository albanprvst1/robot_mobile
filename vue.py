import pygame
import math


class VuePygame:
    def __init__(self, scale=35):
        pygame.init()
        self.screen     = pygame.display.set_mode((800, 600))
        self.scale      = scale
        self.clock      = pygame.time.Clock()
        self.font_big   = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 28)

    def convertir_coordonnees(self, x, y):
        return int(400 + x * self.scale), int(300 - y * self.scale)

    def dessiner(self, env):
        fond = (25, 25, 45) if env.est_nuit else (235, 215, 180)
        self.screen.fill(fond)

        if env.zone_eau: env.zone_eau.dessiner(self)
        for zv in env.zones_vertes: zv.dessiner(self)
        for zs in env.zones_safes:  zs.dessiner(self)
        for m  in env.murs:         m.dessiner(self)
        for g  in env.gardes:       g.dessiner(self)

        if env.robot:
            px, py = self.convertir_coordonnees(env.robot.x, env.robot.y)
            couleur = (220, 50, 50) if env.game_over else (50, 200, 50)
            pygame.draw.circle(self.screen, couleur, (px, py), int(0.3 * self.scale))
            x_dir = px + int(15 * math.cos(env.robot.orientation))
            y_dir = py - int(15 * math.sin(env.robot.orientation))
            pygame.draw.line(self.screen, (255, 255, 255), (px, py), (x_dir, y_dir), 2)

        if env.game_over:
            self._dessiner_game_over(env)

        pygame.display.flip()

    def _dessiner_game_over(self, env):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        txt1 = self.font_big.render("GAME OVER", True, (220, 50, 50))
        txt2 = self.font_small.render(env.game_over_raison, True, (255, 220, 100))
        txt3 = self.font_small.render("Appuie sur R pour recommencer", True, (200, 200, 200))

        self.screen.blit(txt1, txt1.get_rect(center=(400, 230)))
        self.screen.blit(txt2, txt2.get_rect(center=(400, 320)))
        self.screen.blit(txt3, txt3.get_rect(center=(400, 380)))

    def tick(self, fps=60):
        self.clock.tick(fps)