# 🤖 Simulation de Robot Mobile d'Infiltration - Architecture MVC

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Architecture](https://img.shields.io/badge/Architecture-MVC-green.svg)
![Pygame](https://img.shields.io/badge/Library-Pygame-orange.svg)
![AI](https://img.shields.io/badge/AI-Autonomous-red.svg)

---

## 📚 Contexte académique

Ce projet a été réalisé dans le cadre du module de **Programmation Orientée Objet (POO) pour la Robotique**  
**Année universitaire : 2025--2026**  
**EDN LILLE**

---

## 👥 Membres du groupe

- **Alban Pruvost**
- **Jules Clerc**

---

## 🎯 Objectif du projet

L'objectif de ce projet est de concevoir un **simulateur de robot autonome d'infiltration** en 2D.  
Le robot doit naviguer de manière intelligente pour collecter des objets dans des zones spécifiques (A, B, C) tout en évitant des gardes et en gérant ses ressources.

Le simulateur met en œuvre :

- **Navigation Autonome** : Suivi de waypoints et évitement d'obstacles en temps réel.
- **Système de Stealth** : Gestion de la visibilité (cône de vision des gardes, herbes hautes).
- **Cycle Jour/Nuit** : Influence dynamique de l'environnement sur la simulation.
- **Gestion Énergétique** : Consommation de batterie basée sur l'effort moteur et la charge transportée.

---

## 🏗️ Architecture MVC

### 🔹 Modèle (Model)

Contient la logique métier et les règles de la simulation physique.

- **`RobotMobile`** : Gère l'état interne (énergie, inventaire, position) et l'encapsulation des données.
- **`MoteurDifferentiel`** : Implémente les lois cinématiques pour transformer les commandes en mouvement.
- **`Environnement`** : Gère la carte, les collisions (murs, eau), les gardes et les cycles temporels.
- **`Obstacle` (ABC)** : Classe abstraite définissant le comportement des éléments du décor (Mur, Zone).

---

### 🔹 Vue (View)

Responsable du rendu graphique et de l'interface utilisateur.

- **`VuePygame`** :
  - Rendu du **brouillard de guerre** dynamique.
  - Visualisation des rayons **LIDAR** du robot.
  - Affichage du HUD (barre d'énergie, inventaire).
  - Gestion de l'ambiance lumineuse (Jour/Nuit).

---

### 🔹 Contrôleur (Controller)

Gère l'intelligence et le pilotage.

- **`ControleurIA`** :
  - Algorithme de **raycasting** pour l'évitement d'obstacles.
  - Machine à états pour le suivi des routes (waypoints).
  - Système de déblocage automatique (`stuck_frames`).

---

## 🚀 Installation & Exécution

### 1️⃣ Prérequis

- Python **3.10 ou supérieur**
- La bibliothèque `pygame`

### 2️⃣ Installation

```bash
pip install pygame
````

### 3️⃣ Lancer la simulation

```bash
python main.py
```

---

## 🧠 Concepts POO Illustrés

* **Encapsulation** : Utilisation de membres privés et de décorateurs `@property` dans `RobotMobile`.
* **Abstraction** : Classes de base `Obstacle` et `Moteur` pour définir des interfaces communes.
* **Héritage** : Spécialisation des obstacles (`Mur`, `ZoneEau`) et des zones de jeu.
* **Polymorphisme** : Gestion générique des collisions et des mises à jour d'objets variés.
* **Séparation des préoccupations** : Découplage total entre l'IA (cerveau) et la physique (corps).

---

## 📂 Organisation du projet

```plaintext
robot-mobile/
├── robot/
│   ├── robot_mobile.py   # Modèle de données et état du robot
│   ├── moteur.py         # Logique cinématique (Héritage)
│   ├── environnement.py  # Gestion du monde, des gardes et de la physique
│   ├── vue.py            # Rendu graphique Pygame et HUD
│   └── controleur.py     # IA autonome et évitement par rayons
├── main.py               # Orchestration du système MVC et boucle de jeu
└── README.md             # Documentation
```

---

## 📈 Améliorations possibles

* [ ] Implémentation d'un algorithme de pathfinding global (type A*).
* [ ] Ajout de capteurs ultrasons pour une détection à 360°.
* [ ] Système de recharge solaire lié au cycle jour/nuit.
* [ ] Éditeur de niveaux pour créer des environnements personnalisés.

---

## 📄 Licence

Projet académique — Usage pédagogique uniquement.
