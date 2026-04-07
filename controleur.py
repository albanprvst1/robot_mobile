import math

class ControleurIA:
    ROUTES = [
        [(-11, 0), (-2, 0), (-2, 5), (0, 7)], # Vers B
        [(2, 3), (4, 0), (9, 0), (10, -4)],    # Vers C
        [(4, 0), (0, -6), (-11, -6), (-11, -4)] # Retour vers A (sécurisé)
    ]

    def __init__(self):
        self.route_idx, self.wp_idx, self.wait_timer = 0, 0, 0
        self.stuck_time, self.last_pos = 0, None

    def _vision_lidar(self, robot, env):
        meilleur_angle, max_dist = robot.orientation, -1.0
        # Scan plus précis pour trouver les trous dans les murs
        angles = [i * 0.3 for i in range(-5, 6)] 
        for a in [robot.orientation + i for i in angles]:
            d = env.lancer_rayon(robot.x, robot.y, a, distance_max=5.0)
            if d > max_dist:
                max_dist, meilleur_angle = d, a
        return meilleur_angle

    def lire_commande(self, robot, env):
        if self.wait_timer > 0:
            self.wait_timer -= 1
            return {"v": 0.0, "omega": 0.0}

        # Anti-blocage radical (si le robot ne bouge plus du tout)
        if self.last_pos and math.hypot(robot.x - self.last_pos[0], robot.y - self.last_pos[1]) < 0.01:
            self.stuck_time += 1
        else: self.stuck_time = 0
        self.last_pos = (robot.x, robot.y)

        if self.stuck_time > 40:
            self.stuck_time = 0
            return {"v": -1.0, "omega": 2.0} # Reculer et tourner

        # Navigation
        route = self.ROUTES[self.route_idx]
        wx, wy = route[self.wp_idx]
        dx, dy = wx - robot.x, wy - robot.y
        dist_wp = math.hypot(dx, dy)
        
        angle_cible = math.atan2(dy, dx)
        
        # Détection d'obstacle très proche (comme sur ton image)
        dist_devant = env.lancer_rayon(robot.x, robot.y, angle_cible, 1.2)
        if dist_devant < 1.0:
            angle_final = self._vision_lidar(robot, env)
        else:
            angle_final = angle_cible

        # Arrivée au point
        if dist_wp < 0.8:
            if self.wp_idx < len(route) - 1:
                self.wp_idx += 1
            else:
                if self.route_idx == 0: robot.inventaire.append("B")
                elif self.route_idx == 1: robot.inventaire.append("C")
                self.route_idx = (self.route_idx + 1) % len(self.ROUTES)
                self.wp_idx, self.wait_timer = 0, 100
            return {"v": 0.0, "omega": 0.0}

        diff = (angle_final - robot.orientation + math.pi) % (2 * math.pi) - math.pi
        # Vitesse adaptée : plus lent si l'angle est grand ou si mur proche
        v = (2.2 if env.alerte else 1.6) if abs(diff) < 0.4 else 0.5
        if dist_devant < 0.6: v = 0.3 # Prudence extrême
        
        return {"v": v, "omega": 5.5 * diff}