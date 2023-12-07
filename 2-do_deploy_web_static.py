#!/usr/bin/python3
"""A Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""
from fabric.api import put, run, env
from os.path import exists

env.hosts = ['100.26.230.60', '52.91.183.162']
env.user = 'ubuntu'
env.key_filename = '/root/alx-system_engineering-devops/ssh-key'


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        bool: True if successful, False otherwise.
    """
    """Check if the archive exists"""
    if exists(archive_path) is False:
        return False
    try:
        file_s = archive_path.split("/")[-1]
        pa_ext = file_s.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, pa_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_s, path, pa_ext))
        run('rm /tmp/{}'.format(file_s))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, pa_ext))
        run('rm -rf {}{}/web_static'.format(path, pa_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, pa_ext))
        return True

    except Exception as e:
        """Print an error message and return False"""
        print("Error during deployment: {}".format(e))
        return False
