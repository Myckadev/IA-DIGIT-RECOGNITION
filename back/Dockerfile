# Utilise une image Python officielle
FROM python:3.10

# Définition du répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements-linux.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code Django
COPY . .

# Exposer le port 8000 pour Django
EXPOSE 8000
