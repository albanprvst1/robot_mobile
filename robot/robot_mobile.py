import math
from robot.moteur import Moteur

class RobotMobile:
    # Attribut statique
    _nb_robots = 0

    def __init__(self, x=0.0, y=0.0, orientation=0.0, moteur=None):
        self.__x = x
        self.__y = y
        self.__orientation = orientation
        
        # Validation du moteur via méthode statique
        if self.moteur_valide(moteur):
            self.moteur = moteur
        else:
            self.moteur = None
            
        RobotMobile._nb_robots += 1

    # --- Accesseurs ---
    @property
    def x(self) -> float: return self.__x
    @x.setter
    def x(self, value: float): self.__x = value

    @property
    def y(self) -> float: return self.__y
    @y.setter
    def y(self, value: float): self.__y = value

    @property
    def orientation(self) -> float: return self.__orientation
    @orientation.setter
    def orientation(self, value: float): self.__orientation = value % (2 * math.pi)

    # --- Statique & Classe ---
    @classmethod
    def nombre_robots(cls) -> int:
        return cls._nb_robots

    @staticmethod
    def moteur_valide(moteur):
        return isinstance(moteur, Moteur)

    # --- Méthodes ---
    def commander(self, **kwargs):
        if self.moteur:
            self.moteur.commander(**kwargs)

    def mettre_a_jour(self, dt):
        if self.moteur:
            self.moteur.mettre_a_jour(self, dt)

    def __str__(self):
        m_name = type(self.moteur).__name__ if self.moteur else "Invalide"
        return f"Robot(x={self.x:.2f}, y={self.y:.2f}, θ={self.orientation:.2f}, Moteur={m_name})"

    def afficher(self):
        print(self)