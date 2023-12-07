#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py) that deletes
out-of-date archives
"""

from fabric.api import env, run, local
from datetime import datetime

env.hosts = ['100.26.230.60', '52.91.183.162']
env.user = 'ubuntu'
env.key_filename = '/root/alx-system_engineering-devops/ssh-key'


def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = int(number)
    if number < 0:
        return
    try:
        local(
            "ls -1t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}"
            .format(number + 1)
        )
        run(
            "ls -1t /data/web_static/releases | tail -n +{} | "
            "xargs -I {{}} rm -rf /data/web_static/releases/{{}}"
            .format(number + 1)
            )
    except Exception as e:
        pass


if __name__ == "__main__":
    current_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    do_clean(current_time)
