import pygame
from abc import ABC, abstractmethod

class Controleur(ABC):
    @abstractmethod
    def lire_commande(self):
        """Retourne un dictionnaire de commandes"""
        pass

class ControleurTerminal(Controleur):
    def lire_commande(self):
        try:
            print("\n--- Commande (v omega) ---")
            entree = input("> ").split()
            return {"v": float(entree[0]), "omega": float(entree[1])}
        except:
            return {"v": 0.0, "omega": 0.0}

class ControleurClavier(Controleur):
    def lire_commande(self):
        # On récupère l'état de toutes les touches
        keys = pygame.key.get_pressed()
        
        v = 0.0
        omega = 0.0
        
        # Flèches Haut/Bas pour la vitesse linéaire
        if keys[pygame.K_UP]:
            v = 2.0
        elif keys[pygame.K_DOWN]:
            v = -2.0
            
        # Flèches Gauche/Droite pour la rotation
        if keys[pygame.K_LEFT]:
            omega = 1.5
        elif keys[pygame.K_RIGHT]:
            omega = -1.5
            
        return {"v": v, "omega": omega}