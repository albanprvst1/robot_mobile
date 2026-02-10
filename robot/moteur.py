# robot/moteur.py
from abc import ABC, abstractmethod
from math import cos, sin

class Moteur(ABC):
    @abstractmethod
    def commander(self, *args):
        """Définit la consigne (vitesse, angle, etc.)"""
        pass

    @abstractmethod
    def mettre_a_jour(self, robot, dt):
        """Calcule le déplacement réel du robot pendant le temps dt"""
        pass