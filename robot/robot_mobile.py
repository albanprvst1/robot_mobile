import math

class RobotMobile:
    def __init__(self, x=0.0, y=0.0, orientation=0.0, moteur=None):
        # Attributs privés
        self.__x = x
        self.__y = y
        self.__orientation = orientation
        self.moteur = moteur  # Composition

    # --- Accesseurs (Encapsulation) ---
    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, value: float):
        self.__x = value

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, value: float):
        self.__y = value

    @property
    def orientation(self) -> float:
        return self.__orientation

    @orientation.setter
    def orientation(self, value: float):
        self.__orientation = value % (2 * math.pi)

    # --- Méthodes de délégation (Polymorphisme) ---
    def commander(self, **kwargs):
        if self.moteur is not None:
            self.moteur.commander(**kwargs)

    def mettre_a_jour(self, dt):
        if self.moteur is not None:
            self.moteur.mettre_a_jour(self, dt)

    def afficher(self):
        print(f"(x={self.x:.2f}, y={self.y:.2f}, orientation={self.orientation:.2f})")