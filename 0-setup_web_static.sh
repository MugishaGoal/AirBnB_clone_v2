#!/usr/bin/env bash
# A Bash script that sets up the web servers for the deployment of web_static

# Installs Nginx if not installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get -y install nginx
fi

# Creates necessary directories
mkdir -p /data/web_static/releases/test /data/web_static/shared

# Creates a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Creates or recreate symbolic link
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test /data/web_static/current

# Gives ownership to ubuntu user and group
chown -hR ubuntu:ubuntu /data/

# Updates Nginx configuration
config="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n"
sed -i "/server_name _;/a $config" /etc/nginx/sites-available/default

# Restarts Nginx
service nginx restart

exit 0
