# Build stage
FROM node:20-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
# Copy custom nginx config if we want to support React Router natively (optional, using default for MVP)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
