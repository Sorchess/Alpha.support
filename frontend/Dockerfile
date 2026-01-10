FROM node:20-alpine as build

WORKDIR /app

# Копируем файлы зависимостей отдельно для кэширования
COPY package.json package-lock.json* ./
RUN npm ci --silent

# Копируем остальной код
COPY . .
RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD [ "nginx", "-g", "daemon off;" ]