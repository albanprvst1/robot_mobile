import math

class RobotMobile:
    def __init__(self, x, y, orientation):
        # On initialise les attributs PRIVÉS
        self.__x = x
        self.__y = y
        self.__orientation = orientation

    # --- Accesseurs pour X (Alignés sur le def __init__) ---
    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, value: float):
        self.__x = value

    # --- Accesseurs pour Y ---
    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, value: float):
        self.__y = value

    # --- Accesseurs pour Orientation ---
    @property
    def orientation(self) -> float:
        return self.__orientation

    @orientation.setter
    def orientation(self, value: float):
        self.__orientation = value 

    # --- Méthodes ---
    def avancer(self, distance):
        # Ici on utilise self.x (la property) qui tape dans self.__x
        self.x = self.x + distance * math.cos(self.orientation)
        self.y = self.y + distance * math.sin(self.orientation)

    def afficher(self):
        print(f"(x={self.x:.2f}, y={self.y:.2f}, orientation={self.orientation:.2f})")

    def tourner(self, angle):
        self.orientation = (self.orientation + angle) % (2 * math.pi)