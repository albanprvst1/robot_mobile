import pygame
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.environnement import Environnement, Garde, ZoneVerte, ZoneEau, ZoneSafe, Mur
from robot.controleur import ControleurIA
from robot.vue import VuePygame

def creer_env():
    env = Environnement(24, 18)
    L, H = 12, 9
    # Murs extérieurs
    env.murs.extend([Mur(-L, -H, L, -H), Mur(-L, H, L, H), Mur(-L, -H, -L, H), Mur(L, -H, L, H)])
    env.murs.append(Mur(-8, -6, 9, -6))
    env.zone_eau = ZoneEau(0, -7.5, 24, 3)
    env.murs.append(Mur(0, -6, 0, 4))
    env.murs.extend([Mur(-4, 1, -4, 9), Mur(4, 4, 4, 9), Mur(3, 4, 4, 4), Mur(4, 1, 12, 1), Mur(4, -3, 8, -3), Mur(8, -3, 8, -6)])
    env.murs.extend([Mur(-10, -1, -5, -1), Mur(-5, -1, -5, -4), Mur(-8, -4, -8, -6)])
    
    env.zones_safes.extend([ZoneSafe(-10, -4, "A"), ZoneSafe(0, 7, "B"), ZoneSafe(10, -4, "C")])
    env.zones_vertes = [ZoneVerte(-10.5, 7.5, 3, 3), ZoneVerte(10.5, 7.5, 3, 3), ZoneVerte(-6, 2.5, 4, 1.5), ZoneVerte(6, 0, 4, 2), ZoneVerte(-1, -1, 2, 6)]
    
    # GARDES REPOSITIONNÉS (loin des murs)
    env.gardes = [
        Garde(-10, 2), Garde(10, 2),  # Haut gauche et droite
        Garde(-2, 2),  Garde(2, 6),   # Centre
        Garde(-6, -4), Garde(6, -4)   # Près de la rivière
    ]
    return env

env = creer_env()
robot = RobotMobile(x=-10, y=-4, moteur=MoteurDifferentiel())
env.ajouter_robot(robot)
vue, ia, clock = VuePygame(32), ControleurIA(), pygame.time.Clock()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); exit()
    if not env.game_over: robot.commander(**ia.lire_commande(robot, env))
    env.mettre_a_jour(0.016)
    vue.dessiner(env)
    clock.tick(60)