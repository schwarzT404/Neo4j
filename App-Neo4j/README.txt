# Projet API Neo4j avec Flask

Application RESTful développée avec le framework Flask et la base de données orientée graphe Neo4j, démontrant l'implémentation d'un réseau social avec gestion des utilisateurs, publications et commentaires.

[![GitHub](https://img.shields.io/badge/GitHub-schwarzT404-blue?style=flat&logo=github)](https://github.com/schwarzT404/Neo4j)

## Table des matières

- [Introduction](#introduction)
- [Objectifs du projet](#objectifs-du-projet)
- [Fondements théoriques](#fondements-théoriques)
- [Technologies utilisées](#technologies-utilisées)
- [Architecture du système](#architecture-du-système)
- [Installation](#installation)
- [Configuration](#configuration)
- [Structure du projet](#structure-du-projet)
- [API Endpoints](#api-endpoints)
- [Déploiement avec Docker](#déploiement-avec-docker)
- [Tests](#tests)
- [Limitations connues](#limitations-connues)
- [Travaux futurs](#travaux-futurs)
- [Contribuer](#contribuer)
- [Licence](#licence)
- [Références](#références)

## Introduction

Ce projet implémente une API RESTful basée sur Flask et Neo4j pour gérer un réseau social simple avec des relations entre utilisateurs, publications et commentaires. L'application illustre l'utilisation pratique d'une base de données orientée graphe pour modéliser et interroger des données hautement connectées, démontrant ainsi les avantages de Neo4j pour ce type d'applications.

## Objectifs du projet

1. Démontrer l'utilisation de Neo4j comme base de données pour une application web
2. Implémenter une API RESTful complète avec Flask
3. Modéliser des relations complexes entre entités (utilisateurs, publications, commentaires)
4. Fournir un exemple fonctionnel d'architecture pour les applications basées sur des données connectées
5. Illustrer les bonnes pratiques de développement (structure modulaire, configuration par variables d'environnement, etc.)

## Fondements théoriques

### Bases de données orientées graphe

Les bases de données orientées graphe comme Neo4j sont particulièrement adaptées aux données hautement connectées. Contrairement aux bases de données relationnelles qui utilisent des jointures pour établir des relations, Neo4j stocke directement les relations entre les entités sous forme de graphe, ce qui permet:

- Des requêtes plus performantes sur les données connectées
- Une modélisation plus intuitive des relations complexes
- Une meilleure flexibilité pour l'évolution du schéma de données

Dans ce projet, nous utilisons trois principaux types de nœuds (User, Post, Comment) et définissons des relations entre eux telles que `CREATED`, `LIKES`, `COMMENTED_ON`, etc.

## Technologies utilisées

- **Flask**: Framework web Python léger et flexible
- **Neo4j**: Base de données orientée graphe NoSQL
- **py2neo**: Bibliothèque Python pour interagir avec Neo4j
- **Docker**: Pour la conteneurisation et le déploiement simplifié
- **Python-dotenv**: Pour la gestion sécurisée de la configuration

## Architecture du système

L'application suit une architecture en couches:

1. **Couche API** (routes): Gère les requêtes HTTP et les réponses
2. **Couche Service**: Implémente la logique métier
3. **Couche Modèle**: Définit les entités et leurs relations
4. **Couche Accès aux données**: Gère les interactions avec la base de données Neo4j

## Installation

1. Cloner le dépôt:
```bash
git clone https://github.com/schwarzT404/Neo4j.git
cd Neo4j
```

2. Créer un environnement virtuel et l'activer:
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances:
```bash
pip install -r requirements.txt
```

## Configuration

1. Créer un fichier `.env` à la racine du projet avec les variables suivantes:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
DEBUG=True
SECRET_KEY=votre_clé_secrète
```

2. Personnaliser les paramètres selon votre environnement de déploiement

## Structure du projet

```
Neo4j/
├── app.py                  # Point d'entrée de l'application
├── config.py               # Configuration de l'application
├── docker-compose.yml      # Configuration Docker
├── requirements.txt        # Dépendances Python
├── models/                 # Modèles de données et schéma du graphe
├── routes/                 # Contrôleurs API
│   ├── user_routes.py      # Routes pour la gestion des utilisateurs
│   ├── post_routes.py      # Routes pour la gestion des publications
│   └── comment_routes.py   # Routes pour la gestion des commentaires
└── services/               # Services pour la logique métier
    └── db_service.py       # Service de connexion et d'accès à la BD
```

## API Endpoints

### Utilisateurs
- `GET /users` - Récupérer tous les utilisateurs
- `GET /users/<id>` - Récupérer un utilisateur par ID
- `POST /users` - Créer un nouvel utilisateur
- `PUT /users/<id>` - Mettre à jour un utilisateur
- `DELETE /users/<id>` - Supprimer un utilisateur

### Publications
- `GET /posts` - Récupérer toutes les publications
- `GET /posts/<id>` - Récupérer une publication par ID
- `POST /posts` - Créer une nouvelle publication
- `PUT /posts/<id>` - Mettre à jour une publication
- `DELETE /posts/<id>` - Supprimer une publication

### Commentaires
- `GET /comments` - Récupérer tous les commentaires
- `GET /comments/<id>` - Récupérer un commentaire par ID
- `POST /comments` - Créer un nouveau commentaire
- `PUT /comments/<id>` - Mettre à jour un commentaire
- `DELETE /comments/<id>` - Supprimer un commentaire

## Déploiement avec Docker

1. Démarrer les services avec Docker Compose:
```bash
docker-compose up -d
```

2. Accéder à l'interface Neo4j:
   - Neo4j Browser: http://localhost:7474
   - Identifiants par défaut: neo4j/password

3. L'API sera disponible à l'adresse: http://localhost:5000

## Tests

Pour exécuter les tests unitaires:
```bash
pytest
```

Les tests couvrent:
- Création, lecture, mise à jour et suppression des utilisateurs
- Création, lecture, mise à jour et suppression des publications
- Création, lecture, mise à jour et suppression des commentaires
- Relations entre les différentes entités

## Limitations connues

- Pas de mécanisme d'authentification implémenté
- Pas de pagination pour les requêtes retournant de nombreux résultats
- Tests de performances non inclus
- Interface utilisateur non implémentée (API uniquement)

## Travaux futurs

- Implémentation de l'authentification avec JWT
- Ajout de la pagination pour les listes d'objets
- Développement d'une interface utilisateur en React
- Support de requêtes plus complexes (recherche de contenu, filtrage)
- Optimisation des performances pour les grandes quantités de données

## Contribuer

Les contributions sont les bienvenues. Pour contribuer:

1. Forker le dépôt
2. Créer une branche pour votre fonctionnalité
3. Ajouter vos modifications avec des tests
4. Soumettre une pull request

## Licence

Ce projet est sous licence MIT.

## Références

- [Documentation officielle Neo4j](https://neo4j.com/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Py2neo Documentation](https://py2neo.org/v4/)
- [RESTful API Design Best Practices](https://restfulapi.net/)

---

Développé par [schwarzT404](https://github.com/schwarzT404) 