"""A Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""
from fabric.api import put, run, env
from os.path import exists

env.hosts = ['142.44.167.228', '144.217.246.195']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        bool: True if successful, False otherwise.
    """
    """Check if the archive exists"""
    if not exists(archive_path):
        return False

    try:
        """Extract necessary information from the archive_path"""
        file_name = archive_path.split("/")[-1]
        base_name = file_name.split(".")[0]
        release_path = "/data/web_static/releases/"

        """Upload the archive to /tmp/"""
        put(archive_path, '/tmp/')

        """Create necessary directories and extract archive"""
        run('mkdir -p {}{}/'.format(release_path, base_name))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, release_path, base_name))

        """Remove the temporary archive"""
        run('rm /tmp/{}'.format(file_name))

        """Move contents and create symbolic link"""
        run('mv {0}{1}/web_static/* {0}{1}/'.format(release_path, base_name))
        run('rm -rf {}{}/web_static'.format(release_path, base_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(release_path, base_name))

        """Print a success message"""
        print("New version deployed!")

        return True

    except Exception as e:
        """Print an error message and return False"""
        print("Error during deployment: {}".format(e))
        return False
