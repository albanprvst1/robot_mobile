import math

class ControleurIA:
    def __init__(self):
        self.points = {'A': (-10, -4), 'B': (0, 8), 'C': (10, -4)}
        self.etapes = ['B', 'C', 'A']
        self.index_etape = 0
        self.wait_timer = 0
        self.last_pos = (0, 0)
        self.stuck_time = 0

    def lire_commande(self, robot, env):
        if self.wait_timer > 0:
            self.wait_timer -= 1
            return {"v": 0.0, "omega": 0.0}

        cible_nom = self.etapes[self.index_etape]
        cx, cy = self.points[cible_nom]
        
        # LOGIQUE DE DÉTOUR POUR B (Contourner le barrage)
        if cible_nom == 'B':
            if robot.y < 3:
                cx, cy = (-10, 1.5) if robot.x < 0 else (10, 1.5)
            elif 1.5 <= robot.y < 4:
                cx, cy = 0, 2

        # LOGIQUE RIVIÈRE C -> A (Utilisation de la nouvelle ouverture à gauche)
        if cible_nom == 'A' and robot.x > -8: 
            if robot.x > 9: # Phase 1 : Entrer dans l'eau à droite
                cx, cy = 11, -7.5
            elif robot.x > -10: # Phase 2 : Traverser toute la rivière vers la gauche
                cx, cy = -10.5, -7.5
            else: # Phase 3 : Remonter par l'ouverture
                cx, cy = -10.5, -4

        dx, dy = cx - robot.x, cy - robot.y
        dist = math.sqrt(dx**2 + dy**2)

        # Gestion Anti-Blocage
        if math.sqrt((robot.x-self.last_pos[0])**2 + (robot.y-self.last_pos[1])**2) < 0.01:
            self.stuck_time += 1
        else:
            self.stuck_time = 0
        self.last_pos = (robot.x, robot.y)
        
        if self.stuck_time > 20: # Si bloqué, petite marche arrière
            return {"v": -1.2, "omega": 2.0}

        # Sécurité Eau (Attendre la nuit)
        if cible_nom == 'A' and not env.est_nuit and robot.y < -6:
             return {"v": 0.0, "omega": 0.0}

        # Calcul de l'angle
        angle_cible = math.atan2(dy, dx)
        diff = (angle_cible - robot.orientation + math.pi) % (2*math.pi) - math.pi
        
        # Changement d'étape
        if dist < 0.8:
            if cible_nom == 'B' and robot.y < 7:
                pass 
            else:
                self.wait_timer = 80
                self.index_etape = (self.index_etape + 1) % len(self.etapes)
        
        return {"v": 1.6, "omega": 5.0 * diff}