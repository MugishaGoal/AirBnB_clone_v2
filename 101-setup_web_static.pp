# A Puppet script that sets up the web servers for the deployment of web_static

# Nginx configuration content
$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://linktr.ee/firdaus_h_salim/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

# Ensure Nginx is installed
package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
}

# Create necessary directories for web server setup
file { '/data':
  ensure  => 'directory'
}

file { '/data/web_static':
  ensure => 'directory'
}

file { '/data/web_static/releases':
  ensure => 'directory'
}

file { '/data/web_static/releases/test':
  ensure => 'directory'
}

file { '/data/web_static/shared':
  ensure => 'directory'
}

# Create a sample HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "this webpage is found in data/web_static/releases/test/index.htm\n"
}

# Create or update the symbolic link to the current release
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
}

# Ensure correct ownership of the /data/ directory
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

# Create directories for Nginx web server
file { '/var/www':
  ensure => 'directory'
}

file { '/var/www/html':
  ensure => 'directory'
}

# Create sample HTML files for Nginx web server
file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "This is my first upload in /var/www/index.html***\n"
}

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page - Error page\n"
}

# Update Nginx configuration file
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => $nginx_conf,
  notify  => Exec['nginx_restart'],
}

# Restart Nginx when the configuration is updated
exec { 'nginx_restart':
  command => '/etc/init.d/nginx restart',
  refreshonly => true,
}
