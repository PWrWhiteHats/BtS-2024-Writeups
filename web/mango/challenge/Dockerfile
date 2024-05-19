# api
FROM node:18 AS api

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# db
FROM mongo:latest

# Install Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# data directory for MongoDB
RUN mkdir -p /data/db

COPY --from=api /app /app

WORKDIR /app

EXPOSE 3000

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
