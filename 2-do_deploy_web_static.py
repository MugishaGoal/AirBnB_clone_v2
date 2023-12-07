#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['100.26.230.60', '52.91.183.162']


def do_deploy(archive_path):
    """Distribute an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_split = archive_path.split("/")[-1]
        pa_extract = file_split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, pa_extract))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_split, path, pa_extract))
        run('rm /tmp/{}'.format(file_split))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, pa_extract))
        run('rm -rf {}{}/web_static'.format(path, pa_extract))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, pa_extract))
        return True
    except Exception as e:
        print("Error during deployment: {}".format(e))
        return False
