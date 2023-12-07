#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates and
distributes an archive to your web servers
"""

from fabric.api import env, local, run
from datetime import datetime
from os.path import exists

env.hosts = ['100.26.230.60', '52.91.183.162']
env.user = 'ubuntu'
env.key_filename = '/root/alx-system_engineering-devops/ssh-key/ssh-key'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        time_format = "%Y%m%d%H%M%S"
        date = datetime.utcnow().strftime(time_format)
        local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -czvf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Deploys the archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception as e:
        return False


def deploy():
    """Deploys the web static content to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
