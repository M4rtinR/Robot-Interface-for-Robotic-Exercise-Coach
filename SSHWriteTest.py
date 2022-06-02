import os
import paramiko

ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect("192.168.43.57", username="nao", password="nao")
sftp = ssh.open_sftp()
sftp.put("/home/martin/Test.txt", ".local/share/PackageManager/apps/boot-config/html/Test.txt")
sftp.close()
ssh.close()
