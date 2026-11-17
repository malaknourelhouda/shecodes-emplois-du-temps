# SheCodes — Gestion des emplois du temps du département

Projet DevOps — Module DevOps, Thème 1.
Université de Béjaïa, Département d'Informatique.

## Équipe

| Membre | Rôle |
|---|---|
| Hammad Malak Nour El Houda | Socle applicatif, CI/CD, Docker, déploiement, observabilité |
| Roubache Alyssa | API référentiels + import CSV |
| Ziani Yasmine | Frontend + tests du module de conflits |
| Kerkadi Tiziri | Documentation, manuel utilisateur, jeu de données de démo |

## Sujet

Application web de gestion des emplois du temps d'un département universitaire.
Gestion des enseignants, modules, groupes, salles et créneaux, avec **détection
automatique des conflits** (enseignant / salle / groupe / capacité).

## Stack

- **Backend** : Python 3.12 + FastAPI + SQLAlchemy 2
- **Base** : PostgreSQL (prod/CI), SQLite (dev local)
- **Frontend** : HTML + JavaScript
- **CI/CD** : GitHub Actions
- **Conteneurisation** : Docker + Docker Compose

## Structure

\\\
app/
  main.py           point d'entrée FastAPI
  database.py       connexion SQLAlchemy
  models/           modèles ORM
  routers/          routes API
  services/         logique métier (conflits, imports)
tests/              tests pytest
.github/workflows/  pipeline CI/CD
docs/               documentation et manuel utilisateur
\\\

## Installation locale

\\\ash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
\\\

Swagger : http://localhost:8000/docs

## Répartition du travail

Voir les issues GitHub et l'historique des Pull Requests. Chaque membre a
livré sa fonctionnalité sur une branche dédiée, avec revue croisée avant fusion.
