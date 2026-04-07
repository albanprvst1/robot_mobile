import math

class ControleurIA:
    ROUTES = [
        [(-11, 0), (-2, 0), (-2, 5), (-1, 6.5), (0, 8)],
        [(0, 5), (2, 3), (4, 0), (9, 0), (10, -3), (10, -4)],
        [(11, -5), (11, -7.5), (-9, -7.5), (-11, -5), (-11, -2), (-10, -4)],
    ]
    _RIVER_WP_START = 1

    def __init__(self):
        self.route_idx, self.wp_idx = 0, 0
        self.wait_timer, self.stuck_time = 0, 0
        self.last_pos = None

    def _vision_lidar(self, robot, env):
        meilleur_angle, max_dist = robot.orientation, -1.0
        # Scan sur 180 degrés
        for a in [robot.orientation + i for i in [-1.2, -0.6, -0.3, 0, 0.3, 0.6, 1.2]]:
            d = env.lancer_rayon(robot.x, robot.y, a, distance_max=5.0)
            if d > max_dist: max_dist, meilleur_angle = d, a
        return meilleur_angle

    def lire_commande(self, robot, env):
        if self.wait_timer > 0:
            self.wait_timer -= 1
            return {"v": 0.0, "omega": 0.0}

        # Anti-blocage
        if self.last_pos and math.hypot(robot.x - self.last_pos[0], robot.y - self.last_pos[1]) < 0.02:
            self.stuck_time += 1
        else: self.stuck_time = 0
        self.last_pos = (robot.x, robot.y)
        if self.stuck_time > 30:
            self.stuck_time = 0
            return {"v": -1.2, "omega": 2.5}

        # Navigation cible
        route = self.ROUTES[self.route_idx]
        wx, wy = route[self.wp_idx]
        
        if self.route_idx == 2 and self.wp_idx >= self._RIVER_WP_START and not env.est_nuit:
            return {"v": 0.0, "omega": 0.0}

        dx, dy = wx - robot.x, wy - robot.y
        angle_cible = math.atan2(dy, dx)
        
        # Évitement Lidar
        if env.lancer_rayon(robot.x, robot.y, angle_cible, 1.5) < 1.5:
            angle_final = self._vision_lidar(robot, env)
        else:
            angle_final = angle_cible

        if math.hypot(dx, dy) < 0.7:
            if self.wp_idx < len(route) - 1: self.wp_idx += 1
            else:
                self.route_idx = (self.route_idx + 1) % len(self.ROUTES)
                self.wp_idx, self.wait_timer = 0, 80
            return {"v": 0.0, "omega": 0.0}

        diff = (angle_final - robot.orientation + math.pi) % (2 * math.pi) - math.pi
        v = 2.0 if abs(diff) < 0.5 else 0.8
        return {"v": v, "omega": 5.0 * diff}