import time
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.controleur import ControleurTerminal
from robot.vue import VueTerminal

# 1. Création du MODÈLE
robot = RobotMobile(moteur=MoteurDifferentiel())

# 2. Création du CONTRÔLEUR
controleur = ControleurTerminal()

# 3. Création de la VUE
vue = VueTerminal()

dt = 0.1  # Pas de temps
running = True

while running:
    # A. La VUE affiche l'état actuel
    vue.dessiner_robot(robot)
    
    # B. Le CONTRÔLEUR récupère l'ordre
    commande = controleur.lire_commande()
    
    # C. On applique au MODÈLE
    robot.commander(**commande)
    robot.mettre_a_jour(dt)