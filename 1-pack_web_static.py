#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo
"""
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
    """Creates the 'versions' directory if it doesn't exist"""
    local("mkdir -p versions")

    """Creates the archive filename with the current timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)

    """Creates the archive"""
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    """Checks if the archive was created successfully"""
    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None

if __name__ == "__main__":
    do_pack()
