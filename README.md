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

## Installation du celery 

Celery permet la gestion de tâche de fond du modèle IA et permet donc son évolution permanente

``celery -A back worker --loglevel=info``<br>

## Installation du front 

``yarn install`` <br>
``yarn start`` <br>

Enjoy :D