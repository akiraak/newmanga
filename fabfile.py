from fabric import Connection, task
import subprocess

remote_dir = "~/projects/newmanga"

subprocess.call("rsync -av --delete --exclude-from=rsync-exclude.txt . tin:{}".format(remote_dir), shell=True)

curret_cmd = "cd {} && ".format(remote_dir)
c = Connection('akiraak@tin:22')
r = c.run(curret_cmd + '. pyenv/bin/activate && pip install -r requirements.txt')
