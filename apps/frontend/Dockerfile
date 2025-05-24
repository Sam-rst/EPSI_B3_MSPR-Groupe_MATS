# Étape 1 : Builder les fichiers statiques avec Node
FROM node:18-alpine as builder

WORKDIR /app

# Copie les fichiers de l'app (ajuste si tu veux ignorer node_modules etc.)
COPY package.json package-lock.json ./
RUN npm install

COPY . .

# Génère les fichiers statiques web
RUN npx expo export:web

# Étape 2 : Servir avec NGINX
FROM nginx:alpine

# Copie les fichiers statiques dans NGINX
COPY --from=builder /app/web-build /usr/share/nginx/html

# Configuration NGINX personnalisée (optionnelle mais recommandée)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
