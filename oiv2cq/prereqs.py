import os
import subprocess
from termcolor import colored

def run_command(command, description):
    """Runs a shell command and waits for it to complete."""
    print(colored(f"Starting: {description}", "yellow"))
    try:
        subprocess.run(command, shell=True, check=True)
        print(colored(f"\u2714 {description} completed successfully.\n", "green"))
    except subprocess.CalledProcessError as e:
        print(colored(f"\u2718 {description} failed: {e}", "red"))
        exit(1)  # Exit if a critical step fails

def install_homebrew():
    """Installs Homebrew if not already installed."""
    print(colored("Checking for Homebrew installation...", "yellow"))
    try:
        subprocess.run("brew --version", shell=True, check=True)
        print(colored("\u2714 Homebrew is already installed.\n", "green"))
    except subprocess.CalledProcessError:
        print(colored("Homebrew is not installed. Installing now...", "yellow"))
        run_command(
            '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
            "Installing Homebrew"
        )

def setup_ssh_key():
    """Sets up an SSH key for GitHub and handles user authorization."""
    print(colored("Setting up an SSH key for GitHub access...", "yellow"))

    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, exist_ok=True)  # Ensure the .ssh directory exists
    key_name = "id_rsa_twilio_internal"
    key_path = os.path.join(ssh_dir, key_name)

    if os.path.exists(key_path):
        print(colored(f"\u2714 SSH key already exists at {key_path}. Skipping key generation.", "green"))
    else:
        print(colored("Generating a new SSH key...", "yellow"))
        run_command(f"ssh-keygen -t rsa -b 4096 -f {key_path} -N ''", "Generating SSH key")

    print(colored("Adding the SSH key to the SSH agent...", "yellow"))
    run_command("eval \"$(ssh-agent -s)\" && ssh-add " + key_path, "Adding SSH key to SSH agent")

    public_key_path = f"{key_path}.pub"
    print(colored("Adding the SSH key to GitHub...", "yellow"))
    add_key_result = subprocess.run(
        ["gh", "ssh-key", "add", public_key_path, "--title", "Work Laptop - Twilio Internal"],
        capture_output=True,
        text=True,
    )
    if add_key_result.returncode == 0:
        print(colored("\u2714 SSH key successfully added to GitHub.", "green"))
    elif "already exists" in add_key_result.stderr:
        print(colored("\u2714 SSH key already exists in GitHub. Skipping addition.", "yellow"))
    else:
        print(colored(f"\u2718 Failed to add SSH key to GitHub: {add_key_result.stderr.strip()}", "red"))

    print(colored("Opening GitHub SSH keys settings page...", "yellow"))
    run_command("open https://github.com/settings/keys", "Opening GitHub SSH settings page")

    print(colored("\u26A0 IMPORTANT: Manually configure the SSH key for SAML SSO authorization.", "yellow"))
    print(colored("1. Locate the newly added SSH key titled 'Work Laptop - Twilio Internal'.", "yellow"))
    print(colored("2. Click the 'Configure SSO' button next to the key.", "yellow"))
    print(colored("3. Follow the prompts to authorize the key for your organization.", "yellow"))
    print(colored("Testing the SSH connection to GitHub...", "yellow"))
    result = subprocess.run("ssh -T git@github.com", shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        print(colored("\u2714 SSH connection to GitHub successful!", "green"))
    else:
        print(colored(f"\u2718 SSH connection failed: {result.stderr.strip()}", "red"))

def check_docker():
    """Checks if Docker is installed, or prompts the user to install Docker Desktop."""
    print(colored("Checking for Docker installation...", "yellow"))
    try:
        subprocess.run("docker --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(colored("\u2714 Docker is already installed.\n", "green"))
    except subprocess.CalledProcessError:
        print(colored("Docker is not installed. Opening Docker Desktop download page...", "yellow"))
        run_command("open https://www.docker.com/products/docker-desktop/", "Opening Docker Desktop download page")
        print(colored("\u26A0 Please download and install Docker Desktop. Once installed, press Enter to continue.", "yellow"))
        input("Press Enter once Docker Desktop is installed...")
        try:
            subprocess.run("docker --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(colored("\u2714 Docker installation confirmed.\n", "green"))
        except subprocess.CalledProcessError:
            print(colored("\u2718 Docker installation could not be confirmed. Please ensure Docker Desktop is installed and running.", "red"))
            exit(1)

def main():
    print(colored("Starting developer onboarding process...", "yellow"))

    # Install Homebrew
    install_homebrew()

    # Install or Upgrade Python
    run_command("brew install python || brew upgrade python", "Installing or upgrading Python")

    # Install or Upgrade GitHub CLI
    run_command("brew install gh || brew upgrade gh", "Installing or upgrading GitHub CLI")

    # GitHub Authentication with admin:public_key scope
    print(colored("Next step: Authenticate with GitHub CLI (with admin:public_key scope).", "yellow"))
    run_command("gh auth login --scopes 'admin:public_key'", "GitHub authentication")
    print(colored("\u2714 GitHub authentication completed. Moving to the next step.", "green"))

    # Install CloudQuery CLI
    run_command("brew install cloudquery/tap/cloudquery || brew upgrade cloudquery", "Installing or upgrading CloudQuery CLI")

    # Install Python SDK
    run_command("pip install --upgrade cloudquery-plugin-sdk", "Installing or upgrading CloudQuery Python SDK")

    # Check Docker Installation
    check_docker()

    # SSH Key Setup
    setup_ssh_key()

    print(colored("\u2714 All steps completed successfully! Your environment is ready for use. You can now continue working in this terminal.", "green"))

if __name__ == "__main__":
    main()
