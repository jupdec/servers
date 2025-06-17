FROM node:22.12-alpine AS builder

WORKDIR /build

# Copy package files first for better caching
COPY servers/servers/src/cluster-http/package*.json ./
COPY servers/servers/tsconfig.json ./tsconfig.json

# Install dependencies
RUN npm install

# Copy source files
COPY servers/servers/src/cluster-http/ ./

# Build the application
RUN npm run build

FROM node:22-alpine AS release

WORKDIR /app

# Copy built files and package files
COPY --from=builder /build/dist /app/dist
COPY --from=builder /build/package*.json /app/

# Install production dependencies only
ENV NODE_ENV=production
RUN npm ci --ignore-scripts --omit=dev

# Expose port for HTTP server
EXPOSE 3000

# Command to run the application
CMD ["node", "dist/index.js"]