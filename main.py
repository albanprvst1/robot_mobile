import pygame
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.environnement import Environnement, Garde, ZoneVerte, ZoneEau, ZoneSafe
from robot.controleur import ControleurIA
from robot.vue import VuePygame

env = Environnement()
# Zones Safes
coords = {'A': (-6, -4), 'B': (0, 5), 'C': (6, -4)}
for n, p in coords.items(): env.zones_safes.append(ZoneSafe(p[0], p[1], n))

# Gardes fluides
env.gardes = [Garde(-3, 2), Garde(3, 0), Garde(0, -2)]
env.zones_vertes.append(ZoneVerte(4, 0, 3, 2))
env.zone_eau = ZoneEau(0, -4, 10, 2)

robot = RobotMobile(x=-6, y=-4, moteur=MoteurDifferentiel())
env.ajouter_robot(robot)
vue, ia = VuePygame(), ControleurIA()

while True:
    if any(e.type == pygame.QUIT for e in pygame.event.get()): break
    robot.commander(**ia.lire_commande(robot, env))
    env.mettre_a_jour(0.016)
    vue.dessiner(env)
    vue.tick(60)
pygame.quit()