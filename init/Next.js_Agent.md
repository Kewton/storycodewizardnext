## ./Dockerfile
### ./Dockerfile
```txt
FROM node:23.11.0-alpine

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

CMD ["npm", "start"]
```