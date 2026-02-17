import pygame
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.environnement import Environnement, ObstacleCirculaire
from robot.controleur import ControleurClavier
from robot.vue import VuePygame

# 1. Le Modèle (Robot + Environnement)
robot = RobotMobile(moteur=MoteurDifferentiel())
env = Environnement(largeur=14, hauteur=10)
env.ajouter_robot(robot)

# Ajout de quelques obstacles
env.ajouter_obstacle(ObstacleCirculaire(x=3, y=2, rayon=1.0))
env.ajouter_obstacle(ObstacleCirculaire(x=-2, y=-1, rayon=0.8, couleur=(200, 50, 50)))

# 2. La Vue
vue = VuePygame(scale=40)

# 3. Le Contrôleur
controleur = ControleurClavier()

running = True
dt = 0.016

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # Logique MVC
    commande = controleur.lire_commande()
    robot.commander(**commande)
    
    # C'est l'environnement qui gère la mise à jour (et les collisions)
    env.mettre_a_jour(dt)
    
    # On dessine tout l'environnement
    vue.dessiner(env)
    vue.tick(60)

pygame.quit()