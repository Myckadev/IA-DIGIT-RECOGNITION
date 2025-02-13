# Utilise une image Node pour le build
FROM node:18 as build

# Définition du répertoire de travail
WORKDIR /app

# Copier les fichiers et installer les dépendances
COPY package.json yarn.lock ./
RUN yarn install

# Copier le reste du code et builder l'application
COPY . .
RUN yarn run build

# Serveur Nginx pour servir le frontend
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose le port 80 pour Nginx
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
