import os
import paramiko
import sys

host = "192.168.0.68"
user = "fpapale"
password = "ViaGoceano2021"

local_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
remote_root = "docker/llmwiki"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to {user}@{host}...")
    ssh.connect(host, username=user, password=password)
    print("Connected via SSH.")

    # Prepare deployment directory in user's home
    commands = [
        f"mkdir -p ~/{remote_root}",
        f"cd ~/{remote_root} && if [ -d '.git' ]; then git pull; else git clone https://github.com/fpapale/llmwiki.git .; fi",
        f"mkdir -p ~/{remote_root}/runtime/config"
    ]

    for cmd in commands:
        print(f"\nExecuting: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status() # Wait for completion

    print("\nTransferring local files via SFTP...")
    sftp = ssh.open_sftp()
    
    files_to_transfer = [
        ("runtime/config/config.docker.yml", f"{remote_root}/runtime/config/config.docker.yml"),
        ("runtime/config/secrets.env", f"{remote_root}/runtime/config/secrets.env"),
        ("install.sh", f"{remote_root}/install.sh")
    ]
    
    for local_rel, remote_rel in files_to_transfer:
        local_path = os.path.join(local_root, local_rel)
        if os.path.exists(local_path):
            print(f"Uploading {local_path} to ~/{remote_rel}...")
            sftp.put(local_path, remote_rel)
        else:
            print(f"Warning: Local file {local_path} not found, skipping.")

    sftp.close()

    print("\nExecuting install.sh on remote server...")
    install_commands = [
        f"chmod +x ~/{remote_root}/install.sh",
        f"cd ~/{remote_root} && ./install.sh"
    ]
    
    for cmd in install_commands:
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        for line in stdout:
            sys.stdout.buffer.write(line.encode('utf-8', 'replace'))
            sys.stdout.flush()
        for line in stderr:
            sys.stderr.buffer.write(line.encode('utf-8', 'replace'))
            sys.stderr.flush()
            
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            print(f"Command failed with exit status {exit_status}")
            sys.exit(exit_status)

    print("\nDeploy completato con successo!")

except Exception as e:
    print(f"Errore durante il deploy: {e}")
finally:
    ssh.close()
    print("Connection closed.")
