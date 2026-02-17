import pygame
import sys
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.controleur import ControleurClavier
from robot.vue import VuePygame

# 1. Initialisation du MODÈLE
robot = RobotMobile(moteur=MoteurDifferentiel())

# 2. Initialisation de la VUE
vue = VuePygame()

# 3. Initialisation du CONTRÔLEUR
controleur = ControleurClavier()

dt = 0.016  # Environ 60 FPS (1/60s)
running = True

print("Simulation lancée. Utilisez les flèches du clavier !")

while running:
    # Gérer la fermeture de la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # A. Le CONTRÔLEUR lit les touches
    commande = controleur.lire_commande()
    
    # B. Le MODÈLE se met à jour
    robot.commander(**commande)
    robot.mettre_a_jour(dt)
    
    # C. La VUE dessine
    vue.dessiner_robot(robot)
    
    # Limiter à 60 FPS
    vue.tick(60)

pygame.quit()
sys.exit()