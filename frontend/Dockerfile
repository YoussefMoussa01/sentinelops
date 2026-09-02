FROM node:20-alpine AS build

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY src ./src
COPY index.html .
COPY vite.config.ts .
COPY tsconfig.json .
COPY tsconfig.node.json .
COPY tailwind.config.js .
COPY postcss.config.js .

# Build
RUN npm run build

# Production image
FROM nginx:alpine

# Copy build output
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
RUN echo 'server { listen 80; server_name _; location / { root /usr/share/nginx/html; try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]