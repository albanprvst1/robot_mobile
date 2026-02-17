from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel, MoteurOmnidirectionnel
import math

print("--- TEST MOTEUR DIFFÉRENTIEL ---")
moteur_diff = MoteurDifferentiel()
robot1 = RobotMobile(moteur=moteur_diff)

# 1. Avancer de 3m (v=3, dt=1)
robot1.commander(v=3.0, omega=0.0)
robot1.mettre_a_jour(1.0)
# 2. Tourner de 90° vers le haut
robot1.commander(v=0.0, omega=math.pi/2)
robot1.mettre_a_jour(1.0)
# 3. Avancer de 1m sur Y
robot1.commander(v=1.0, omega=0.0)
robot1.mettre_a_jour(1.0)
robot1.afficher()

print("\n--- TEST MOTEUR OMNIDIRECTIONNEL ---")
moteur_omni = MoteurOmnidirectionnel()
robot2 = RobotMobile(moteur=moteur_omni)

# Aller directement en (3, 1) en 1 seconde
robot2.commander(vx=3.0, vy=1.0, omega=0.0)
robot2.mettre_a_jour(1.0)
robot2.afficher()