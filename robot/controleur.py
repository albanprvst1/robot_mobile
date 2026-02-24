import math
from abc import ABC, abstractmethod

class Controleur(ABC):
    @abstractmethod
    def lire_commande(self, robot, env): pass

class ControleurIA(Controleur):
    def __init__(self):
        self.points = {'A': (-6, -4), 'B': (0, 5), 'C': (6, -4)}
        self.etapes = ['B', 'C', 'A']
        self.index_etape = 0

    def lire_commande(self, robot, env):
        cible_nom = self.etapes[self.index_etape]
        cx, cy = self.points[cible_nom]
        dx, dy = cx - robot.x, cy - robot.y
        dist = math.sqrt(dx**2 + dy**2)

        # Attente Eau (C vers A)
        if cible_nom == 'A' and not env.est_nuit and 2.0 < dist < 5.0:
            return {"v": 0.0, "omega": 0.0}

        # Evitement Gardes
        for g in env.gardes:
            if math.sqrt((g.x-robot.x)**2 + (g.y-robot.y)**2) < 2.0:
                return {"v": -1.0, "omega": 2.0}

        # Navigation
        angle_cible = math.atan2(dy, dx)
        diff = (angle_cible - robot.orientation + math.pi) % (2*math.pi) - math.pi
        
        if dist < 0.5:
            self.index_etape = (self.index_etape + 1) % len(self.etapes)
        
        return {"v": 1.2, "omega": 3.0 * diff}