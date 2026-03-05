import pygame
import math
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.environnement import Environnement, Garde, ZoneVerte, ZoneEau, ZoneSafe, Mur
from robot.controleur import ControleurIA
from robot.vue import VuePygame

# --- INITIALISATION ---
env = Environnement(largeur=24, hauteur=18)

# --- LIMITES EXTÉRIEURES ---
L, H = 12, 9
env.murs.extend([Mur(-L, -H, L, -H), Mur(-L, H, L, H), Mur(-L, -H, -L, H), Mur(L, -H, L, H)])

# --- STRUCTURES PRINCIPALES ---
env.murs.append(Mur(-8, -6, 9, -6))     # Mur Rivière
env.zone_eau = ZoneEau(0, -7.5, 24, 3)  # Rivière
env.murs.append(Mur(0, -6, 0, 4))       # Barrage Central

# --- RÉSEAU VERS B & C ---
env.murs.extend([
    Mur(-4, 1, -4, 9), Mur(4, 4, 4, 9), Mur(3, 4, 4, 4), # Secteur B
    Mur(4, 1, 12, 1), Mur(4, -3, 8, -3), Mur(8, -3, 8, -6) # Secteur C
])

# --- QUARTIER A ---
env.murs.extend([Mur(-10, -1, -5, -1), Mur(-5, -1, -5, -4), Mur(-8, -4, -8, -6)])

# --- ZONES SAFES ---
env.zones_safes.extend([ZoneSafe(-10, -4, "A"), ZoneSafe(0, 7, "B"), ZoneSafe(10, -4, "C")])

# --- VERDURE INTÉGRÉE (PLACEMENT ARCHITECTURAL) ---
env.zones_vertes = [
    # 1. Habillage des coins morts (Stabilité visuelle)
    ZoneVerte(-10.5, 7.5, 3, 3),   # Remplit l'angle mort en haut à gauche
    ZoneVerte(10.5, 7.5, 3, 3),    # Remplit l'angle mort en haut à droite
    
    # 2. Bordures de couloir (Guide visuel pour le robot)
    ZoneVerte(-6, 2.5, 4, 1.5),    # Souligne le mur horizontal de A
    ZoneVerte(6, 0, 4, 2),       # Accompagne la chicane vers C
    
    # 3. Intégration au Barrage (Le "poumon" central)
    # On place l'herbe le long de la ligne verticale pour simuler une haie
    ZoneVerte(-1, -1, 2, 6),       
    
]

# --- GARDES & INSTANCIATION ---
env.gardes = [Garde(-9, 1), Garde(9, 1), Garde(0, 2), Garde(-2, 6), Garde(2, 6), Garde(10, -5)]
robot = RobotMobile(x=-10, y=-4, moteur=MoteurDifferentiel())
env.ajouter_robot(robot)
vue, ia = VuePygame(scale=32), ControleurIA()

# --- BOUCLE ---
clock = pygame.time.Clock()
while True:
    if any(e.type == pygame.QUIT for e in pygame.event.get()): break
    robot.commander(**ia.lire_commande(robot, env))
    env.mettre_a_jour(0.016)
    vue.dessiner(env)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()