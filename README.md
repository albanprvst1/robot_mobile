# 🤖 Simulation de Robot Mobile - Architecture MVC

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Architecture](https://img.shields.io/badge/Architecture-MVC-green.svg)
![Pygame](https://img.shields.io/badge/Library-Pygame-orange.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

------------------------------------------------------------------------

## 📚 Contexte académique

Ce projet a été réalisé dans le cadre du module de **Programmation
Orientée Objet (POO) pour la Robotique**\
**Année universitaire : 2025--2026**\
**IMT Nord Europe**

------------------------------------------------------------------------

## 👥 Membres du groupe

-   **Alban Pruvost**
-   **Jules Clerc**

------------------------------------------------------------------------

## 🎯 Objectif du projet

L'objectif de ce TP est de concevoir un **simulateur de robot mobile en
2D** en appliquant :

-   Les principes fondamentaux de la **Programmation Orientée Objet**
-   Le patron de conception **Modèle -- Vue -- Contrôleur (MVC)**
-   Les notions d'**abstraction, encapsulation, héritage et
    polymorphisme**

Le simulateur permet de :

-   Piloter un robot différentiel ou omnidirectionnel
-   Évoluer dans un environnement 2D
-   Gérer des obstacles circulaires
-   Simuler des collisions avec gestion physique simple

------------------------------------------------------------------------

# 🏗️ Architecture MVC

## 🔹 Modèle (Model)

Contient toute la logique métier.

-   `RobotMobile`
    -   Gestion de l'état interne du robot\
    -   Position $(x, y)$\
    -   Orientation $\theta$
-   `Moteur`
    -   Abstraction des lois cinématiques\
    -   Implémentation via héritage et polymorphisme
-   `Environnement`
    -   Gestion de l'espace 2D\
    -   Gestion des obstacles\
    -   Détection et gestion des collisions

------------------------------------------------------------------------

## 🔹 Vue (View)

Responsable de l'affichage.

-   `VuePygame`
    -   Rendu graphique en temps réel\
    -   Gestion d'échelle\
    -   Rafraîchissement dynamique
-   `VueTerminal`
    -   Affichage textuel\
    -   Utile pour le débogage

------------------------------------------------------------------------

## 🔹 Contrôleur (Controller)

Gère les interactions utilisateur.

-   `ControleurClavier`
    -   Pilotage via les touches du clavier
-   `ControleurTerminal`
    -   Commandes via la console

------------------------------------------------------------------------

# 🚀 Installation & Exécution

## 1️⃣ Prérequis

-   Python **3.10 ou supérieur**
-   pip

Vérification :

``` bash
python --version
```

------------------------------------------------------------------------

## 2️⃣ Installation des dépendances

Le projet utilise **Pygame** :

``` bash
pip install pygame
```

------------------------------------------------------------------------

## 3️⃣ Lancer la simulation

``` bash
python main.py
```

------------------------------------------------------------------------

# 🎮 Contrôles Clavier

  Touche            Action
  ----------------- ----------------------------------------------
  ⬆ Flèche HAUT     Avancer (vitesse linéaire positive)
  ⬇ Flèche BAS      Reculer (vitesse linéaire négative)
  ⬅ Flèche GAUCHE   Rotation gauche (vitesse angulaire positive)
  ➡ Flèche DROITE   Rotation droite (vitesse angulaire négative)
  Échap             Quitter la simulation

------------------------------------------------------------------------

# 📂 Organisation du projet

``` plaintext
robot-mobile/
├── robot/
│   ├── __init__.py
│   ├── robot_mobile.py   # Modèle principal
│   ├── moteur.py         # Abstraction cinématique
│   ├── environnement.py  # Gestion environnement & collisions
│   ├── vue.py            # Vues (Pygame / Terminal)
│   └── controleur.py     # Contrôleurs
├── main.py               # Point d’entrée (orchestration MVC)
└── README.md             # Documentation
```

------------------------------------------------------------------------

# 🧠 Concepts POO Illustrés

-   Encapsulation
-   Responsabilité unique
-   Séparation des préoccupations (MVC)
-   Héritage
-   Polymorphisme
-   Modularité

------------------------------------------------------------------------

# 📈 Améliorations possibles

-   Ajout de capteurs simulés (LIDAR, ultrasons)
-   Ajout d'algorithmes d'évitement d'obstacles
-   Ajout d'un mode autonome
-   Sauvegarde / chargement d'environnements
-   Interface graphique enrichie

------------------------------------------------------------------------

# 📄 Licence

Projet académique -- Usage pédagogique uniquement.
