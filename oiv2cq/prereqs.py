import os
import subprocess
import sys
from termcolor import colored


# Wrapper to run shell commands within the virtual environment
def run_command(command, description):
    print(colored(f"Starting: {description}", "yellow"))
    try:
        subprocess.run(command, shell=True, check=True)
        print(colored(f"✔ {description} completed successfully.\n", "green"))
    except subprocess.CalledProcessError as e:
        print(colored(f"✘ {description} failed: {e}", "red"))
        sys.exit(1)


# Create virtual environment
VENV_PATH = os.path.expanduser("~/.oiv2cq_venv")


def create_virtualenv():
    if not os.path.exists(VENV_PATH):
        print(colored("Virtual environment not found. Creating it now...", "yellow"))
        run_command(f"python3 -m venv {VENV_PATH}", "Creating virtual environment")
    print(colored("Activating virtual environment...", "green"))
    activate_virtualenv()


def activate_virtualenv():
    activate_script = os.path.join(VENV_PATH, "bin", "activate")
    if not os.path.exists(activate_script):
        print(colored("Activation script not found. Please run 'oiv2cq setup' first.", "red"))
        sys.exit(1)
    os.environ["VIRTUAL_ENV"] = VENV_PATH
    os.environ["PATH"] = f"{VENV_PATH}/bin:" + os.environ["PATH"]


def install_prerequisites():
    run_command("brew install python || brew upgrade python", "Installing or upgrading Python")
    run_command("brew install gh || brew upgrade gh", "Installing or upgrading GitHub CLI")
    run_command("brew install cloudquery/tap/cloudquery || brew upgrade cloudquery",
                "Installing or upgrading CloudQuery CLI")
    run_command("pip install --upgrade cloudquery-plugin-sdk", "Installing or upgrading CloudQuery Python SDK")


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

    # Open GitHub settings for manual SAML SSO configuration
    print(colored("Opening GitHub SSH keys settings page...", "yellow"))
    run_command("open https://github.com/settings/keys", "Opening GitHub SSH settings page")

    print(colored("\U0001F6A8 IMPORTANT: Manually configure the SSH key for SAML SSO authorization.", "yellow"))
    print(colored("1. Locate the newly added SSH key titled 'Work Laptop - Twilio Internal'.", "yellow"))
    print(colored("2. Click the 'Configure SSO' button next to the key.", "yellow"))
    print(colored("3. Follow the prompts to authorize the key for your organization.", "yellow"))
    input(colored("Press Enter after you have completed the SAML SSO configuration to continue...", "yellow"))

    print(colored("Testing the SSH connection to GitHub...", "yellow"))
    result = subprocess.run("ssh -T git@github.com", shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        print(colored("\u2714 SSH connection to GitHub successful!", "green"))
    else:
        print(colored(f"\u2718 SSH connection failed: {result.stderr.strip()}", "red"))


def check_docker():
    print(colored("Checking for Docker installation...", "yellow"))
    try:
        result = subprocess.run("docker --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(colored(f"\u2714 Docker is installed: {result.stdout.strip()}", "green"))
    except subprocess.CalledProcessError:
        print(colored("✘ Docker is not installed or not running. Please install Docker Desktop manually.", "red"))
        print(colored("Opening Docker Desktop download page...", "yellow"))
        run_command("open https://www.docker.com/products/docker-desktop/", "Opening Docker Desktop download page")
        print(colored("\u26A0 After installing Docker Desktop, you can verify it using:", "yellow"))
        print(colored("    docker --version", "cyan"))
        print(colored("Then re-run 'oiv2cq setup' if needed.", "yellow"))
        sys.exit(1)




def main():
    print(colored("Starting developer onboarding process...", "yellow"))

    # Create and activate the virtual environment
    create_virtualenv()
    activate_virtualenv()

    # Install prerequisites
    install_prerequisites()

    # Check Docker installation and service status
    check_docker()

    # SSH Key setup with SAML SSO authorization
    setup_ssh_key()

    print(colored("\u2714 All steps completed successfully! Your environment is ready for use.", "green"))


if __name__ == "__main__":
    main()
