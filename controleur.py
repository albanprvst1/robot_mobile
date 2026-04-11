import math

class ControleurIA:
    ROUTES = [
        [(-11, 0), (-2, 0), (-2, 5), (0, 7)], # Vers B
        [(2, 3), (4, 0), (9, 0), (10, -4)],    # Vers C
        [(4, 0), (0, -6), (-11, -6), (-11, -4)] # Retour A
    ]

    def __init__(self):
        self.route_idx, self.wp_idx, self.wait_timer = 0, 0, 0
        self.last_pos, self.stuck_time = None, 0

    def _vision_lidar(self, robot, env):
        meilleur_angle, max_dist = robot.orientation, -1.0
        for a in [robot.orientation + i for i in [-1.2, -0.6, 0, 0.6, 1.2]]:
            d = env.lancer_rayon(robot.x, robot.y, a, 4.0)
            if d > max_dist: max_dist, meilleur_angle = d, a
        return meilleur_angle

    def lire_commande(self, robot, env):
        if self.wait_timer > 0:
            self.wait_timer -= 1
            return {"v": 0.0, "omega": 0.0}

        route = self.ROUTES[self.route_idx]
        wx, wy = route[self.wp_idx]
        dist_wp = math.hypot(wx - robot.x, wy - robot.y)

        if dist_wp < 0.8:
            if self.wp_idx < len(route) - 1: self.wp_idx += 1
            else:
                target = ["B", "C", "A"][self.route_idx]
                if target not in robot.inventaire: robot.inventaire.append(target)
                self.route_idx = (self.route_idx + 1) % len(self.ROUTES)
                self.wp_idx, self.wait_timer = 0, 80
            return {"v": 0.0, "omega": 0.0}

        angle_cible = math.atan2(wy - robot.y, wx - robot.x)
        if env.lancer_rayon(robot.x, robot.y, angle_cible, 1.2) < 1.0:
            angle_final = self._vision_lidar(robot, env)
        else: angle_final = angle_cible

        diff = (angle_final - robot.orientation + math.pi) % (2 * math.pi) - math.pi
        v = (2.2 if env.alerte else 1.6) if abs(diff) < 0.5 else 0.4
        return {"v": v, "omega": 5.0 * diff}