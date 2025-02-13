# Projet IA de reconnaissance d'image

## Prérequis

- Python
- Redis
- Node 18+ && yarn
- MongoDB


## Installation du projet back & lancement

``python venv -m my_venv`` <br>
``pip install -r requirements-OS.txt``<br>
``python manage.py runserver`` <br>

## Pour lancer l'app en mode "prod"

``docker compose up --build -d``<br>

Le front sera disponible en localhost:3000.<br>
Avant d'utilisé l'app, si c'est la première fois que vous la lancez,

``docker logs -f celery`` afin de suivre l'état d'avancement du premier dump du model d'IA.<br>

et enjoy :D

## Pour lancer l'app en dev

## Installation du celery 

Celery permet la gestion de tâche de fond du modèle IA et permet donc son évolution permanente

``celery -A back worker --loglevel=info``<br>

## Installation du front 

``yarn install`` <br>
``yarn start`` <br>

Enjoy :D
