import math
from robot.moteur import Moteur

class RobotMobile:
    _nb_robots = 0
    def __init__(self, x=0.0, y=0.0, orientation=0.0, moteur=None):
        self.x, self.y, self.orientation = x, y, orientation
        self.moteur = moteur
        self.inventaire = [] # Pour stocker "A", "B", "C"
        RobotMobile._nb_robots += 1

    def commander(self, **kwargs):
        if self.moteur: self.moteur.commander(**kwargs)

    def mettre_a_jour(self, dt, env):
        # Fatigue et Terrain
        friction = 0.6 if env.robot_cache() else 1.0
        friction *= (1.0 - (len(self.inventaire) * 0.15)) # -15% par objet
        if self.moteur:
            self.moteur.mettre_a_jour(self, dt, friction)