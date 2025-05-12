# TP Neo4j avec Flask

TP académique démontrant l'utilisation de Neo4j avec Flask pour implémenter une API simple de réseau social.

## À propos de ce TP

Ce projet est un travail pratique étudiant réalisé dans le cadre d'un cours sur les bases de données NoSQL. L'objectif est de mettre en pratique les concepts de bases de données orientées graphe avec Neo4j.

## Fonctionnalités

- API RESTful pour gérer des utilisateurs, publications et commentaires
- Utilisation de Neo4j comme base de données graphe
- Démonstration des relations entre entités dans un contexte de réseau social

## Technologies utilisées

- Flask (framework web Python)
- Neo4j (base de données graphe)
- Docker (pour faciliter le déploiement)

## Installation et démarrage rapide

1. Cloner le dépôt
2. Installer les dépendances: `pip install -r requirements.txt`
3. Créer un fichier `.env` avec les variables Neo4j et Flask
4. Lancer l'application: `python app.py`

## Structure du projet

```
Neo4j/
├── app.py                  # Point d'entrée de l'application
├── config.py               # Configuration de l'application
├── docker-compose.yml      # Configuration Docker
├── requirements.txt        # Dépendances Python
├── models/                 # Modèles de données
├── routes/                 # Contrôleurs API
└── services/               # Services
```

## API Endpoints principaux

- `/users` - Gestion des utilisateurs
- `/posts` - Gestion des publications
- `/comments` - Gestion des commentaires

## Utilisation avec Docker

```bash
docker-compose up -d
```

---

Travail réalisé par schwarzT404 | https://github.com/schwarzT404/Neo4j 