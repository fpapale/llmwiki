import os
import paramiko
import sys

host = "192.168.0.68"
user = "fpapale"
password = "ViaGoceano2021"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(host, username=user, password=password)
    
    # Executing sync
    cmd = "cd ~/docker/llmwiki && git checkout -- install.sh && git fetch --all && git checkout origin/main -- sync_wiki.sh && bash sync_wiki.sh"
    print(f"\nExecuting: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    for line in stdout:
        sys.stdout.buffer.write(line.encode('utf-8', 'replace'))
        sys.stdout.flush()
    for line in stderr:
        sys.stderr.buffer.write(line.encode('utf-8', 'replace'))
        sys.stderr.flush()
        
    exit_status = stdout.channel.recv_exit_status()
    print(f"\nExit status: {exit_status}")

except Exception as e:
    print(f"Errore: {e}")
finally:
    ssh.close()
