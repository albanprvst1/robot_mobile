import math
from abc import ABC, abstractmethod

class Obstacle(ABC):
    @abstractmethod
    def collision(self, x_robot, y_robot, rayon_robot) -> bool:
        """Retourne True s'il y a collision avec le robot."""
        pass

    @abstractmethod
    def dessiner(self, vue):
        """Méthode pour que la vue puisse dessiner l'obstacle."""
        pass

class ObstacleCirculaire(Obstacle):
    def __init__(self, x, y, rayon, couleur=(100, 100, 100)):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.couleur = couleur

    def collision(self, x_r, y_r, rayon_r) -> bool:
        # Distance entre les centres : d = sqrt((x2-x1)^2 + (y2-y1)^2)
        distance = math.sqrt((self.x - x_r)**2 + (self.y - y_r)**2)
        return distance <= (self.rayon + rayon_r)

    def dessiner(self, vue):
        # On délègue l'affichage à la vue pygame via une méthode utilitaire
        import pygame
        px, py = vue.convertir_coordonnees(self.x, self.y)
        pygame.draw.circle(vue.screen, self.couleur, (px, py), int(self.rayon * vue.scale))

class Environnement:
    def __init__(self, largeur=10.0, hauteur=10.0):
        self.largeur = largeur
        self.hauteur = hauteur
        self.robot = None
        self.obstacles = []

    def ajouter_robot(self, robot):
        self.robot = robot

    def ajouter_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def mettre_a_jour(self, dt):
        if self.robot is None: return

        # 1. Sauvegarde de l'état actuel (avant mouvement)
        old_x, old_y = self.robot.x, self.robot.y
        old_ori = self.robot.orientation

        # 2. On laisse le robot calculer son nouveau mouvement théorique
        self.robot.mettre_a_jour(dt)

        # 3. Vérification des collisions (obstacles et murs)
        collision = False
        rayon_robot = 0.4 # On définit un rayon fixe pour le robot
        
        # Test contre les obstacles
        for obs in self.obstacles:
            if obs.collision(self.robot.x, self.robot.y, rayon_robot):
                collision = True
                break
        
        # Test contre les limites du monde (murs)
        if abs(self.robot.x) > self.largeur/2 or abs(self.robot.y) > self.hauteur/2:
            collision = True

        # 4. Si collision, on annule (retour à l'ancienne position)
        if collision:
            self.robot.x, self.robot.y = old_x, old_y
            self.robot.orientation = old_ori