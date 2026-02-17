from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel, MoteurOmnidirectionnel
import math

# Création des instances
diff = MoteurDifferentiel()
omni = MoteurOmnidirectionnel()

r1 = RobotMobile(moteur=diff)
r2 = RobotMobile(moteur=omni)

# Test Différentiel pour (3, 1)
r1.commander(v=3.0, omega=0.0)
r1.mettre_a_jour(1.0)
r1.commander(v=0.0, omega=math.pi/2)
r1.mettre_a_jour(1.0)
r1.commander(v=1.0, omega=0.0)
r1.mettre_a_jour(1.0)

# Test Omnidirectionnel pour (3, 1)
r2.commander(vx=3.0, vy=1.0, omega=0.0)
r2.mettre_a_jour(1.0)

print(f"Total Robots: {RobotMobile.nombre_robots()}")
print(f"R1 Final: {r1}")
print(f"R2 Final: {r2}")