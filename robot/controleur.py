from abc import ABC, abstractmethod

class Controleur(ABC):
    @abstractmethod
    def lire_commande(self):
        pass

class ControleurTerminal(Controleur):
    def lire_commande(self):
        try:
            print("\nCommande (v omega) :")
            entree = input("> ").split()
            v = float(entree[0])
            omega = float(entree[1])
            return {"v": v, "omega": omega}
        except (ValueError, IndexError):
            print("Format invalide ! Utilisez : 1.0 0.5")
            return {"v": 0.0, "omega": 0.0}