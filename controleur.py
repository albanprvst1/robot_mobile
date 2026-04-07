import math


class ControleurIA:
    ROUTES = [
        [(-11, 0), (-2, 0), (-2, 5), (-1, 6.5), (0, 8)],
        [(0, 5), (2, 3), (4, 0), (9, 0), (10, -3), (10, -4)],
        [(11, -5), (11, -7.5), (-9, -7.5), (-11, -5), (-11, -2), (-10, -4)],
    ]
    _RIVER_WP_START = 1

    def __init__(self):
        self.route_idx  = 0
        self.wp_idx     = 0
        self.wait_timer = 0
        self.last_pos   = None
        self.stuck_time = 0

    # ------------------------------------------------------------------
    def _mur_devant(self, robot, env, angle, distance=0.5):
        """
        Retourne True uniquement si un mur est DIRECTEMENT
        dans la direction angle, à moins de `distance`.
        Sonde fine : 3 points proches (centre, légère gauche, légère droite).
        """
        for decal in [0, 0.15, -0.15]:
            a  = angle + decal
            sx = robot.x + distance * math.cos(a)
            sy = robot.y + distance * math.sin(a)
            if any(m.collision(sx, sy, 0.28) for m in env.murs):
                return True
            if abs(sx) > env.largeur / 2 - 0.3 or abs(sy) > env.hauteur / 2 - 0.3:
                return True
        return False

    def _direction_libre(self, robot, env, angle_souhaite):
        """
        Si l'angle souhaité est libre → on le retourne directement (pas de déviation).
        Sinon on cherche le plus petit écart gauche/droite qui évite le mur.
        """
        if not self._mur_devant(robot, env, angle_souhaite):
            return angle_souhaite, False   # (angle, recule)

        for i in range(1, 20):
            for signe in [1, -1]:
                a = angle_souhaite + signe * i * (math.pi / 18)  # pas de 10°
                if not self._mur_devant(robot, env, a):
                    return a, False

        # Vraiment coincé → reculer
        return angle_souhaite + math.pi, True

    # ------------------------------------------------------------------
    def _vecteur_fuite(self, robot, gardes, rayon):
        fx, fy, min_dist = 0.0, 0.0, 999.0
        for g in gardes:
            d = math.hypot(robot.x - g.x, robot.y - g.y)
            min_dist = min(min_dist, d)
            if 0 < d < rayon:
                force = (rayon / d) ** 2
                fx += force * (robot.x - g.x) / d
                fy += force * (robot.y - g.y) / d
        return fx, fy, min_dist

    def _zone_verte_la_plus_proche(self, robot, zones_vertes):
        best, best_d = None, 999
        for zv in zones_vertes:
            d = math.hypot(robot.x - zv.x, robot.y - zv.y)
            if d < best_d:
                best_d, best = d, (zv.x, zv.y)
        return best, best_d

    def _normaliser(self, x, y):
        n = math.hypot(x, y)
        return (x / n, y / n) if n > 0.001 else (0.0, 0.0)

    def _commande(self, robot, env, angle_cible, v_max):
        angle_libre, recule = self._direction_libre(robot, env, angle_cible)
        if recule:
            return {"v": -1.2, "omega": 2.5}
        diff = (angle_libre - robot.orientation + math.pi) % (2 * math.pi) - math.pi
        # Ralentit seulement si déviation > 40° (pas à chaque petit ajustement)
        v = v_max if abs(diff) < 0.7 else 0.5
        return {"v": v, "omega": 5.0 * diff}

    # ------------------------------------------------------------------
    def lire_commande(self, robot, env) -> dict:

        if self.wait_timer > 0:
            self.wait_timer -= 1
            return {"v": 0.0, "omega": 0.0}

        rayon_danger = 1.25 if env.est_nuit else 2.0
        rayon_alerte = rayon_danger * 1.5

        fx, fy, min_dist = self._vecteur_fuite(robot, env.gardes, rayon_alerte)
        en_danger = min_dist < rayon_danger
        en_alerte = min_dist < rayon_alerte

        # ── CAS 1 : caché → immobile ───────────────────────────────────
        if env.robot_cache() and en_danger:
            return {"v": 0.0, "omega": 0.0}

        # ── CAS 2 : DANGER → fuite ─────────────────────────────────────
        if en_danger:
            if self.last_pos is not None:
                if math.hypot(robot.x - self.last_pos[0],
                              robot.y - self.last_pos[1]) < 0.02:
                    self.stuck_time += 1
                else:
                    self.stuck_time = 0
            self.last_pos = (robot.x, robot.y)
            if self.stuck_time > 15:
                self.stuck_time = 0
                return {"v": -1.5, "omega": 3.0}
            gx, gy = self._normaliser(fx, fy)
            return self._commande(robot, env, math.atan2(gy, gx), 3.0)

        # ── CAS 3 : ALERTE → vers cache ────────────────────────────────
        if en_alerte:
            cache, dist_cache = self._zone_verte_la_plus_proche(robot, env.zones_vertes)
            if cache and dist_cache > 0.5:
                cx, cy = cache
                ax, ay = self._normaliser(cx - robot.x, cy - robot.y)
                gx, gy = self._normaliser(fx, fy)
                angle_cache = math.atan2(0.7*ay + 0.3*gy, 0.7*ax + 0.3*gx)
                return self._commande(robot, env, angle_cache,
                                      2.3 if not env.est_nuit else 1.9)

        # ── CAS 4 : navigation normale ─────────────────────────────────
        route  = self.ROUTES[self.route_idx]
        wx, wy = route[self.wp_idx]

        if (self.route_idx == 2
                and self.wp_idx >= self._RIVER_WP_START
                and not env.est_nuit):
            return {"v": 0.0, "omega": 0.0}

        if self.last_pos is not None:
            if math.hypot(robot.x - self.last_pos[0],
                          robot.y - self.last_pos[1]) < 0.02:
                self.stuck_time += 1
            else:
                self.stuck_time = 0
        self.last_pos = (robot.x, robot.y)

        if self.stuck_time > 30:
            self.stuck_time = 0
            return {"v": -1.2, "omega": 2.5}

        dx, dy = wx - robot.x, wy - robot.y
        dist   = math.hypot(dx, dy)

        if dist < 0.7:
            if self.wp_idx < len(route) - 1:
                self.wp_idx += 1
            else:
                self.route_idx = (self.route_idx + 1) % len(self.ROUTES)
                self.wp_idx    = 0
                self.wait_timer = 80
            return {"v": 0.0, "omega": 0.0}

        v_max = 2 if not env.est_nuit else 2.3
        return self._commande(robot, env, math.atan2(dy, dx), v_max)