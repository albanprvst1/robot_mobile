import math
from robot.moteur import Moteur

class RobotMobile:
    _nb_robots = 0
    def __init__(self, x=0.0, y=0.0, orientation=0.0, moteur=None):
        self.__x = x
        self.__y = y
        self.__orientation = orientation
        self.moteur = moteur
        self.inventaire = []
        self.energie = 100.0
        RobotMobile._nb_robots += 1

    @property
    def x(self): return self.__x
    @x.setter
    def x(self, v): self.__x = v
    @property
    def y(self): return self.__y
    @y.setter
    def y(self, v): self.__y = v
    @property
    def orientation(self): return self.__orientation
    @orientation.setter
    def orientation(self, v): self.__orientation = v % (2*math.pi)

    def commander(self, **kwargs):
        if self.moteur: self.moteur.commander(**kwargs)

    def mettre_a_jour(self, dt, env):
        if self.energie <= 0: return
        
        friction = 0.6 if env.robot_cache() else 1.0
        friction *= (1.0 - (len(self.inventaire) * 0.15))
        
        # Consommation batterie
        if self.moteur:
            conso = (abs(self.moteur.v) * 0.4 + abs(self.moteur.omega) * 0.2 + len(self.inventaire)) * dt
            self.energie = max(0, self.energie - conso)
            self.moteur.mettre_a_jour(self, dt, friction)