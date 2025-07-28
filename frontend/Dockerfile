FROM node:20-alpine
WORKDIR /app
COPY frontend-react/package*.json ./
RUN npm install
COPY frontend-react/ ./
RUN npm run build
EXPOSE 8501
CMD ["npx", "vite", "preview", "--port", "8501", "--host"]
