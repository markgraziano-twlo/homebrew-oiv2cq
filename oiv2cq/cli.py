import argparse
import os
from termcolor import colored
import subprocess

# Move VENV_PATH to a user-writable directory
VENV_PATH = os.path.expanduser("~/.oiv2cq/venv")

def create_virtualenv_if_missing():
    """Creates the virtual environment if it doesn't already exist."""
    if not os.path.exists(VENV_PATH):
        print(colored("Virtual environment not found. Creating it now...", "yellow"))
        subprocess.run(f"python3 -m venv {VENV_PATH}", shell=True, check=True)
        print(colored(f"✔ Virtual environment created at {VENV_PATH}\n", "green"))

def activate_virtualenv():
    """Activates the virtual environment by setting environment variables."""
    os.environ["VIRTUAL_ENV"] = VENV_PATH
    os.environ["PATH"] = f"{VENV_PATH}/bin:" + os.environ["PATH"]

def run_command_with_venv(command):
    """Runs a command within the virtual environment."""
    full_command = f"source {VENV_PATH}/bin/activate && {command}"
    subprocess.run(full_command, shell=True, check=True)

def display_help():
    help_text = f"""
{colored('OIV2CQ CLI', 'cyan', attrs=['bold'])}
{colored('Usage:', 'yellow', attrs=['bold'])}
  {colored('oiv2cq setup', 'green')}       - Run the prerequisite setup
  {colored('oiv2cq template', 'green')}    - Generate a local CloudQuery plugin template
  {colored('oiv2cq --help', 'green')}      - Show this help message

{colored('Available Commands:', 'yellow', attrs=['bold'])}
  {colored('setup', 'green')}       Set up development dependencies
  {colored('template', 'green')}    Clone and generate a CloudQuery plugin template
"""
    print(help_text)

def main():
    parser = argparse.ArgumentParser(
        description="oiv2cq CLI: Automate onboarding and plugin setup",
        add_help=False,  # Custom help instead of default argparse behavior
    )
    parser.add_argument("command", nargs="?", help="Available commands: setup, template")
    parser.add_argument("--help", action="store_true", help="Show help message")

    args = parser.parse_args()

    # Handle help or display it by default if no command is given
    if not args.command or args.help:
        display_help()
        return

    # Only check or create the virtual environment for commands other than setup
    if args.command != "setup":
        create_virtualenv_if_missing()
        activate_virtualenv()

    # Handle commands
    if args.command == "setup":
        # Create the virtual environment as part of setup
        create_virtualenv_if_missing()
        activate_virtualenv()

        from prereqs import main as prereqs_main
        prereqs_main()

    elif args.command == "template":
        from template_create import main as template_create_main
        template_create_main()

    else:
        print(colored(f"Unknown command: {args.command}. Run 'oiv2cq --help' for available commands.", "red"))

if __name__ == "__main__":
    main()
