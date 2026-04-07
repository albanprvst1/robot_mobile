from abc import ABC, abstractmethod
from math import cos, sin

class Moteur(ABC):
    @abstractmethod
    def commander(self, *args): pass
    @abstractmethod
    def mettre_a_jour(self, robot, dt, friction): pass

class MoteurDifferentiel(Moteur):
    def __init__(self, v=0.0, omega=0.0):
        self.v, self.omega = v, omega
    def commander(self, v, omega):
        self.v, self.omega = v, omega
    def mettre_a_jour(self, robot, dt, friction=1.0):
        robot.orientation += self.omega * dt
        v_reelle = self.v * friction
        robot.x += v_reelle * cos(robot.orientation) * dt
        robot.y += v_reelle * sin(robot.orientation) * dt