import os
import subprocess
from termcolor import colored

# Virtual environment path
VENV_PATH = os.path.expanduser("~/.oiv2cq/venv")


def activate_virtualenv():
    """Activates the virtual environment by setting environment variables."""
    os.environ["VIRTUAL_ENV"] = VENV_PATH
    os.environ["PATH"] = f"{VENV_PATH}/bin:" + os.environ["PATH"]


# Wrapper to run shell commands within the virtual environment
def run_command(command, description):
    print(colored(f"Starting: {description}", "yellow"))
    try:
        subprocess.run(command, shell=True, check=True)
        print(colored(f"✔ {description} completed successfully.\n", "green"))
    except subprocess.CalledProcessError as e:
        print(colored(f"✘ {description} failed: {e}", "red"))
        exit(1)


def install_prerequisites():
    """Installs or upgrades critical dependencies."""
    run_command("brew install python || brew upgrade python", "Installing or upgrading Python")
    run_command("brew install gh || brew upgrade gh", "Installing or upgrading GitHub CLI")
    run_command("brew install cloudquery/tap/cloudquery || brew upgrade cloudquery",
                "Installing or upgrading CloudQuery CLI")
    run_command("pip install --upgrade cloudquery-plugin-sdk", "Installing or upgrading CloudQuery Python SDK")


def authenticate_github():
    """Authenticates with GitHub using the GitHub CLI."""
    print(colored("Authenticating with GitHub using the GitHub CLI...", "yellow"))
    run_command("gh auth login --scopes 'admin:public_key'", "Authenticating with GitHub")


def setup_ssh_key():
    """Sets up an SSH key and adds it to the user's GitHub account."""
    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, exist_ok=True)
    key_name = "id_rsa_twilio_internal"
    key_path = os.path.join(ssh_dir, key_name)

    if os.path.exists(key_path):
        print(colored(f"✔ SSH key already exists at {key_path}. Skipping key generation.", "green"))
    else:
        run_command(f"ssh-keygen -t rsa -b 4096 -f {key_path} -N ''", "Generating SSH key")

    run_command(f"eval \"$(ssh-agent -s)\" && ssh-add {key_path}", "Adding SSH key to SSH agent")

    # Adding the key to GitHub
    print(colored("Adding the SSH key to GitHub...", "yellow"))
    add_key_result = subprocess.run(
        ["gh", "ssh-key", "add", f"{key_path}.pub", "--title", "Work Laptop - Twilio Internal"],
        capture_output=True,
        text=True,
    )

    if add_key_result.returncode == 0:
        print(colored("✔ SSH key successfully added to GitHub.", "green"))
    elif "already exists" in add_key_result.stderr:
        print(colored("✔ SSH key already exists in GitHub. Skipping addition.", "yellow"))
    else:
        print(colored(f"✘ Failed to add SSH key to GitHub: {add_key_result.stderr.strip()}", "red"))
        exit(1)


def check_docker():
    """Checks if Docker is installed and prompts for installation if missing."""
    try:
        subprocess.run("docker --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(colored("✔ Docker is already installed.\n", "green"))
    except subprocess.CalledProcessError:
        print(colored("Docker is not installed. Please install Docker Desktop manually.", "red"))


def main():
    """Main entry point for setting up prerequisites."""
    print(colored("Starting developer onboarding process...", "yellow"))

    # Activate the virtual environment
    activate_virtualenv()

    # Install prerequisites
    install_prerequisites()

    # Authenticate with GitHub
    authenticate_github()

    # Check for Docker installation
    check_docker()

    # Setup SSH key
    setup_ssh_key()

    print(colored("\u2714 All steps completed successfully! Your environment is ready for use.", "green"))


if __name__ == "__main__":
    main()
