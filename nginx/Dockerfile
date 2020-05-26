# Use the Nginx image
FROM nginx


RUN apt-get update && apt-get install -y nginx-extras


# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own nginx.conf
COPY nginx.conf /etc/nginx


