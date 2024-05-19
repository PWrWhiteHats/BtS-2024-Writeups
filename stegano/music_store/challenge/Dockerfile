# Use the official Apache HTTP Server image from Docker Hub
FROM httpd:2.4

# Label the image
LABEL maintainer="admin@localhost"

# Copy website files to the appropriate directory in the container
# Assuming your website files are in a directory named 'website'
COPY ./html/ /usr/local/apache2/htdocs/

# Expose port 80
EXPOSE 80
