FROM node:18
WORKDIR /app
COPY apps/frontend/package*.json ./
RUN npm install -g pnpm && pnpm install
COPY apps/frontend .
CMD ["pnpm", "dev"]
