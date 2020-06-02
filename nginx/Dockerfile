# Use the Nginx image
FROM nginx


RUN apt-get update && apt-get install -y nginx-extras


# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log


# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own nginx.conf
COPY nginx.conf /etc/nginx


