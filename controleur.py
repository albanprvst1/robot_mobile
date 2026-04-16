import math


class ControleurIA:
    ROUTE_AB = [
        (-11.0, -4.0),
        (-11.0, 0.0),
        (-6.0, 0.0),
        (-2.0, 0.0),
        (-2.0, 5.0),
        (0.0, 7.0),
    ]

    ROUTE_BC = [
        (0.5, 6.2),
        (1.8, 5.4),
        (2.4, 3.2),
        (4.0, 0.0),
        (8.0, 0.0),
        (10.0, -4.0),
    ]

    def __init__(self):
        self.phase = 0   # 0->B, 1->C, 2->A
        self.wp_idx = 0
        self.wait_timer = 0

        self.last_pos = None
        self.stuck_frames = 0
        self.recover_timer = 0
        self.recover_turn = 1.0

        self.avoid_angle = None
        self.avoid_timer = 0

    def _angle_diff(self, a, b):
        return (a - b + math.pi) % (2 * math.pi) - math.pi

    def _distance(self, x1, y1, x2, y2):
        return math.hypot(x2 - x1, y2 - y1)

    def _current_route(self):
        if self.phase == 0:
            return self.ROUTE_AB
        if self.phase == 1:
            return self.ROUTE_BC
        return list(reversed(self.ROUTE_BC)) + list(reversed(self.ROUTE_AB)) + [(-10.0, -4.0)]

    def _update_stuck(self, robot):
        pos = (robot.x, robot.y)

        if self.last_pos is None:
            self.last_pos = pos
            return

        moved = self._distance(pos[0], pos[1], self.last_pos[0], self.last_pos[1])

        if moved < 0.015:
            self.stuck_frames += 1
        else:
            self.stuck_frames = 0

        self.last_pos = pos

    def _garde_plus_proche(self, robot, env):
        plus_proche = None
        meilleure_distance = 999.0
        for g in env.gardes:
            d = self._distance(robot.x, robot.y, g.x, g.y)
            if d < meilleure_distance:
                meilleure_distance = d
                plus_proche = g
        return plus_proche, meilleure_distance

    def _best_clear_angle(self, robot, env, base_angle):
        meilleur_angle = base_angle
        meilleur_score = -1e9

        for delta in [-1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2, 1.6]:
            a = base_angle + delta
            clearance = env.lancer_rayon(robot.x, robot.y, a, 4.6)
            align = math.cos(self._angle_diff(a, base_angle))
            score = 1.9 * clearance + 0.75 * align - 0.12 * abs(delta)
            if score > meilleur_score:
                meilleur_score = score
                meilleur_angle = a

        return meilleur_angle

    def _angle_evitement_garde(self, robot, env, garde, wx, wy):
        angle_fuite = math.atan2(robot.y - garde.y, robot.x - garde.x)
        angle_wp = math.atan2(wy - robot.y, wx - robot.x)

        meilleur_angle = angle_fuite
        meilleur_score = -1e9

        for delta in [-1.4, -1.0, -0.6, -0.3, 0.0, 0.3, 0.6, 1.0, 1.4]:
            a = angle_fuite + delta
            clearance = env.lancer_rayon(robot.x, robot.y, a, 3.8)
            align_wp = math.cos(self._angle_diff(a, angle_wp))
            score = 1.5 * clearance + 0.8 * align_wp - 0.08 * abs(delta)
            if score > meilleur_score:
                meilleur_score = score
                meilleur_angle = a

        return meilleur_angle

    def _commande_angle(self, robot, angle_final, v_nominale=1.75, gain=4.3):
        diff = self._angle_diff(angle_final, robot.orientation)

        if abs(diff) > 1.0:
            v = 0.18
        elif abs(diff) > 0.55:
            v = min(v_nominale, 0.82)
        else:
            v = v_nominale

        return {"v": v, "omega": gain * diff}

    def _advance_phase_if_needed(self, robot):
        route = self._current_route()
        wx, wy = route[self.wp_idx]
        if self._distance(robot.x, robot.y, wx, wy) >= 0.7:
            return

        if self.wp_idx < len(route) - 1:
            self.wp_idx += 1
            return

        if self.phase == 0:
            if "B" not in robot.inventaire:
                robot.inventaire.append("B")
            self.phase = 1
            self.wp_idx = 0
            self.wait_timer = 8
            return

        if self.phase == 1:
            if "C" not in robot.inventaire:
                robot.inventaire.append("C")
            self.phase = 2
            self.wp_idx = 0
            self.wait_timer = 8
            return

        if "A" not in robot.inventaire:
            robot.inventaire.append("A")
        self.wait_timer = 999999

    def lire_commande(self, robot, env):
        self._update_stuck(robot)

        if self.avoid_timer > 0:
            self.avoid_timer -= 1
        else:
            self.avoid_angle = None

        if self.recover_timer > 0:
            self.recover_timer -= 1
            return {"v": -0.45, "omega": 2.2 * self.recover_turn}

        if self.stuck_frames > 18:
            self.stuck_frames = 0
            self.recover_timer = 12
            self.recover_turn *= -1.0
            self.avoid_angle = None
            self.avoid_timer = 0
            return {"v": -0.45, "omega": 2.2 * self.recover_turn}

        if self.wait_timer > 0:
            self.wait_timer -= 1
            return {"v": 0.0, "omega": 0.0}

        self._advance_phase_if_needed(robot)

        route = self._current_route()
        wx, wy = route[self.wp_idx]

        garde, d_garde = self._garde_plus_proche(robot, env)

        # marge de sécurité garde
        if garde is not None and d_garde < env.distance_securite_garde + 0.45:
            if self.avoid_angle is None:
                self.avoid_angle = self._angle_evitement_garde(robot, env, garde, wx, wy)
                self.avoid_timer = 12
            return self._commande_angle(robot, self.avoid_angle, v_nominale=1.05, gain=4.0)

        angle_cible = math.atan2(wy - robot.y, wx - robot.x)

        # vrai évitement mur, pas juste spawn
        clearance_ahead = env.lancer_rayon(robot.x, robot.y, angle_cible, 1.25)
        if clearance_ahead < 0.95:
            angle_final = self._best_clear_angle(robot, env, angle_cible)
        else:
            angle_final = angle_cible

        # garde une trajectoire stable près des gardes
        if garde is not None and d_garde < env.distance_securite_garde + 1.0:
            angle_secure = self._angle_evitement_garde(robot, env, garde, wx, wy)

            tx = robot.x + math.cos(angle_final)
            ty = robot.y + math.sin(angle_final)
            sx = robot.x + math.cos(angle_secure)
            sy = robot.y + math.sin(angle_secure)

            dist_target = self._distance(tx, ty, garde.x, garde.y)
            dist_secure = self._distance(sx, sy, garde.x, garde.y)

            if dist_secure > dist_target + 0.10:
                angle_final = angle_secure

        cmd = self._commande_angle(robot, angle_final, v_nominale=1.95, gain=4.3)

        if env.robot_dans_haute_herbe():
            cmd["v"] = max(cmd["v"], 1.75)

        if env.alerte:
            cmd["v"] = min(cmd["v"], 1.20)

        return cmd