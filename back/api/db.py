import os
from mongoengine import connect

# Définition des paramètres MongoDB
DATABASE_NAME = os.getenv("DATABASE_NAME", "guess_number")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")  # Local par défaut
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 27017))

# Connexion à MongoDB
connect(DATABASE_NAME, host=DATABASE_HOST, port=DATABASE_PORT)
