# Design Decision: Using Ubuntu 22.04 as the base image as specifically required by the assignment.
FROM ubuntu:22.04

# Assumption: The container will be used in a controlled environment where a self-signed certificate is acceptable[cite: 43].
# Trade-off: Installing openssl increases the image size slightly, but it's necessary for generating the certificate during build[cite: 42, 45, 47].
RUN apt-get update && \
    apt-get install -y nginx openssl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Generate a self-signed certificate for HTTPS support 
RUN mkdir -p /etc/nginx/ssl && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt \
    -subj "/C=IL/ST=Center/L=City/O=DevOps/CN=localhost"

# Copy configuration and custom HTML [cite: 11, 15]
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html

# Remove default configuration to avoid port conflicts
RUN rm /etc/nginx/sites-enabled/default

# Expose ports for HTTP, Error responses, and HTTPS [cite: 13, 47]
EXPOSE 8080 8081 443

CMD ["nginx", "-g", "daemon off;"]