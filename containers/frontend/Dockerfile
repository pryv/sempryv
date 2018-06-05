FROM node:latest as builder
COPY frontend /app
WORKDIR /app
RUN npm install && npm run build

FROM nginx:stable
COPY containers/frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html/

