FROM node:18-alpine

WORKDIR /app

COPY . /app

RUN npm ci --legacy-peer-deps

RUN npm run build


EXPOSE 80

CMD ["npm", "run", "dev"]