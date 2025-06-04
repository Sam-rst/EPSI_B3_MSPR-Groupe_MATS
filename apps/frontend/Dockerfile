# Stage de build
FROM node:20-alpine AS builder

WORKDIR /app

# Copie des fichiers de dépendances
COPY package*.json ./

# Installation des dépendances
RUN npm install

# Copie du reste des fichiers
COPY . .

# Build de l'application en ignorant les erreurs ESLint
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build -- --no-lint

# Stage de production
FROM node:20-alpine AS runner

WORKDIR /app

# Copie des fichiers nécessaires depuis le stage de build
COPY --from=builder /app/next.config.mjs ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Exposition du port
EXPOSE 3030

# Variables d'environnement
ENV NODE_ENV=production
ENV PORT=3030

# Commande de démarrage
CMD ["node", "server.js"]
