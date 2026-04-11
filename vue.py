import pygame
import math

class VuePygame:
    def __init__(self, scale=32):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.scale = scale
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.fog_surface = pygame.Surface((800, 600), pygame.SRCALPHA)

    def convertir_coordonnees(self, x, y):
        return int(400 + x * self.scale), int(300 - y * self.scale)

    def dessiner(self, env):
        # 1. Dessin du monde (spectateur voit en sombre via le brouillard plus tard)
        fond = (25, 25, 45) if env.est_nuit else (230, 210, 180)
        self.screen.fill(fond)
        
        if env.zone_eau: env.zone_eau.dessiner(self)
        for obj in env.zones_vertes + env.zones_safes + env.murs:
            obj.dessiner(self)
        for g in env.gardes: g.dessiner(self)

        if env.robot:
            rx, ry = self.convertir_coordonnees(env.robot.x, env.robot.y)
            
            # 2. Brouillard de guerre (Fog of War)
            # 160 = opacité du brouillard pour le spectateur (0-255)
            self.fog_surface.fill((15, 15, 25, 160)) 
            points_vue = [(rx, ry)]
            nb_rayons = 40
            for i in range(nb_rayons + 1):
                angle = (i / nb_rayons) * 2 * math.pi
                d = env.lancer_rayon(env.robot.x, env.robot.y, angle, 7.0)
                p_fin = self.convertir_coordonnees(env.robot.x + d*math.cos(angle), 
                                                 env.robot.y + d*math.sin(angle))
                points_vue.append(p_fin)

            if len(points_vue) > 2:
                pygame.draw.polygon(self.fog_surface, (0, 0, 0, 0), points_vue)
            self.screen.blit(self.fog_surface, (0, 0))

            # 3. Lidar directionnel et Robot
            for i in range(-5, 6):
                a_lidar = env.robot.orientation + (i * 0.3)
                d_lidar = env.lancer_rayon(env.robot.x, env.robot.y, a_lidar, 3.0)
                p_lidar = self.convertir_coordonnees(env.robot.x + d_lidar*math.cos(a_lidar), 
                                                   env.robot.y + d_lidar*math.sin(a_lidar))
                pygame.draw.line(self.screen, (0, 255, 0, 150), (rx, ry), p_lidar, 1)

            pygame.draw.circle(self.screen, (50, 180, 50), (rx, ry), int(0.35 * self.scale))
            
            # Barre de batterie
            pygame.draw.rect(self.screen, (0,0,0), (rx-20, ry-25, 40, 5))
            pygame.draw.rect(self.screen, (0,255,0), (rx-20, ry-25, int(40 * env.robot.energie/100), 5))

        # Interface
        self.screen.blit(self.font.render(f"Objets: {len(env.robot.inventaire)}/3", True, (255,255,255)), (20, 20))
        self.screen.blit(self.font.render(f"Batterie: {int(env.robot.energie)}%", True, (255, 100, 100)), (20, 45))
        if env.alerte:
            self.screen.blit(self.font.render("!!! ALERTE !!!", True, (255, 0, 0)), (20, 70))
        
        if env.game_over:
            msg_font = pygame.font.SysFont("Arial", 50, True)
            msg = msg_font.render(env.game_over_raison, True, (255, 0, 0))
            self.screen.blit(msg, msg.get_rect(center=(400, 300)))
            
        pygame.display.flip()