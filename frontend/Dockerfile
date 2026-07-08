# ==========================================
# STAGE 1: Build the React Application
# ==========================================
# We use a Node image only to compile our code. 
# We use "as build" to name this stage so we can reference it later.
FROM node:20-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Build the app. For Vite, this outputs the compiled HTML/JS/CSS to a 'dist' folder
RUN npm run build

# ==========================================
# STAGE 2: Serve with Nginx
# ==========================================
# We start a fresh, tiny Nginx image. This image won't contain Node or our source code!
FROM nginx:alpine

# Copy our custom Nginx configuration to replace the default one
COPY nginx.conf /etc/nginx/conf.d/default.conf

# We copy ONLY the built artifacts ('dist' folder) from Stage 1 into this new Nginx stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
