import pygame
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.environnement import Environnement, Garde, ZoneVerte, ZoneEau, ZoneSafe, Mur
from robot.controleur import ControleurIA
from robot.vue import VuePygame


def creer_env():
    env = Environnement(24, 18)
    L, H = 12, 9

    env.murs.extend([
        Mur(-L, -H, L, -H),
        Mur(-L, H, L, H),
        Mur(-L, -H, -L, H),
        Mur(L, -H, L, H)
    ])

    env.murs.append(Mur(-8, -6, 9, -6))
    env.zone_eau = ZoneEau(0, -7.5, 24, 3)
    env.murs.append(Mur(0, -6, 0, 4))
    env.murs.extend([
        Mur(-4, 1, -4, 9),
        Mur(4, 4, 4, 9),
        Mur(3, 4, 4, 4),
        Mur(4, 1, 12, 1),
        Mur(4, -3, 8, -3),
        Mur(8, -3, 8, -6)
    ])
    env.murs.extend([
        Mur(-10, -1, -5, -1),
        Mur(-5, -1, -5, -4),
        Mur(-8, -4, -8, -6)
    ])

    env.zones_safes.extend([
        ZoneSafe(-10, -4, "A"),
        ZoneSafe(0, 7, "B"),
        ZoneSafe(10, -4, "C")
    ])

    env.zones_vertes = [
        ZoneVerte(-10.5, 7.5, 3, 3),
        ZoneVerte(10.5, 7.5, 3, 3),
        ZoneVerte(-6, 2.5, 4, 1.5),
        ZoneVerte(6, 0, 4, 2),
        ZoneVerte(-1, -1, 2, 6)
    ]

    env.gardes = [
        Garde(-10, 2),
        Garde(10, 2),
        Garde(-2, 2),
        Garde(6, -4)
    ]

    return env


def creer_partie():
    env = creer_env()
    robot = RobotMobile(x=-10.0, y=-4.0, moteur=MoteurDifferentiel())
    env.ajouter_robot(robot)
    ia = ControleurIA()
    return env, robot, ia


pygame.init()
vue = VuePygame(32)
clock = pygame.time.Clock()

env, robot, ia = creer_partie()

restart_timer = 0
victory_freeze = False
game_over_count = 0   # compteur

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # victoire
    if len(robot.inventaire) >= 3 and not env.game_over:
        env.game_over = True
        env.game_over_raison = "WIN"
        victory_freeze = True

    # gestion game over
    if env.game_over:
        if env.game_over_raison != "WIN":
            if restart_timer == 0:
                game_over_count += 1   # incrément ici

            if restart_timer <= 0:
                restart_timer = 120

            restart_timer -= 1

            if restart_timer <= 0:
                env, robot, ia = creer_partie()
                restart_timer = 0
                victory_freeze = False
        else:
            victory_freeze = True

    if not env.game_over and not victory_freeze:
        robot.commander(**ia.lire_commande(robot, env))

    env.mettre_a_jour(0.016)

    # affichage compteur
    vue.dessiner(env)
    compteur_txt = vue.font.render(f"Game Over: {game_over_count}", True, (255, 255, 0))
    vue.screen.blit(compteur_txt, (20, 95))

    pygame.display.flip()
    clock.tick(60)