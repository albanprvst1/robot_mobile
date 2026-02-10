import math
from robot.robot_mobile import RobotMobile

# Initialisation à (0,0,0)
robot = RobotMobile(0, 0, 0)

# 1. Avancer de 1 mètre
robot.avancer(1.0)

# 2. Tourner de 45 degrés (conversion en radians nécessaire : deg * pi / 180)
angle_rad = 45 * math.pi / 180
robot.tourner(angle_rad)

# 3. Avancer de 3 mètres
robot.avancer(3.0)

# Affichage du résultat final
robot.afficher()