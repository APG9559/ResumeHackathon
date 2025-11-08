# Use a lightweight Node.js base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy dependency files first for better build caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the app’s port (change if your app uses a different one)
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
