# 101-setup_web_static.pp

# Install Nginx package
package { 'nginx':
  ensure => 'installed',
}

# Create necessary directories
file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create or recreate the symbolic link
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => "server {\n\tlisten 80 default_server;\n\tserver_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n\n\tlocation / {\n\t\t# your other configurations...\n\t}\n}\n",
  notify  => Exec['nginx_restart'],
}

# Restart Nginx when the configuration is updated
exec { 'nginx_restart':
  command     => 'service nginx restart',
  refreshonly => true,
}
