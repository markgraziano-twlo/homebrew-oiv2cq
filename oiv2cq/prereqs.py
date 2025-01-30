import os
import subprocess
from termcolor import colored

# Wrapper to run shell commands within the virtual environment
def run_command(command, description):
    print(colored(f"Starting: {description}", "yellow"))
    try:
        subprocess.run(command, shell=True, check=True)
        print(colored(f"✔ {description} completed successfully.\n", "green"))
    except subprocess.CalledProcessError as e:
        print(colored(f"✘ {description} failed: {e}", "red"))
        exit(1)

# Install or upgrade critical tools
def install_prerequisites():
    run_command("brew install python || brew upgrade python", "Installing or upgrading Python")
    run_command("brew install gh || brew upgrade gh", "Installing or upgrading GitHub CLI")
    run_command("brew install cloudquery/tap/cloudquery || brew upgrade cloudquery", "Installing or upgrading CloudQuery CLI")
    run_command("pip install --upgrade cloudquery-plugin-sdk", "Installing or upgrading CloudQuery Python SDK")

# SSH Key setup remains unchanged
def setup_ssh_key():
    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, exist_ok=True)
    key_name = "id_rsa_twilio_internal"
    key_path = os.path.join(ssh_dir, key_name)
    if os.path.exists(key_path):
        print(colored(f"✔ SSH key already exists at {key_path}. Skipping key generation.", "green"))
    else:
        run_command(f"ssh-keygen -t rsa -b 4096 -f {key_path} -N ''", "Generating SSH key")
    run_command(f"eval \"$(ssh-agent -s)\" && ssh-add {key_path}", "Adding SSH key to SSH agent")
    run_command(f"gh ssh-key add {key_path}.pub --title \"Work Laptop - Twilio Internal\"", "Adding SSH key to GitHub")

# Docker check remains unchanged
def check_docker():
    try:
        subprocess.run("docker --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(colored("✔ Docker is already installed.\n", "green"))
    except subprocess.CalledProcessError:
        print(colored("Docker is not installed. Please install Docker Desktop manually.", "red"))

# Main function
def main():
    print(colored("Starting developer onboarding process...", "yellow"))
    install_prerequisites()
    check_docker()
    setup_ssh_key()
    print(colored("\u2714 All steps completed successfully! Your environment is ready for use.", "green"))

if __name__ == "__main__":
    main()
