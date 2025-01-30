import argparse
import os
from termcolor import colored
import subprocess
from prereqs import main as prereqs_main
from template_create import main as template_create_main

VENV_PATH = "/usr/local/Cellar/oiv2cq/venv"

# Ensure the virtual environment is active before running any subcommands
def activate_virtualenv():
    if not os.path.exists(f"{VENV_PATH}/bin/activate"):
        print("Virtual environment not found. Please run 'oiv2cq setup' first.")
        exit(1)
    os.environ["VIRTUAL_ENV"] = VENV_PATH
    os.environ["PATH"] = f"{VENV_PATH}/bin:" + os.environ["PATH"]

# Wrapper to execute commands within the virtual environment
def run_command_with_venv(command):
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
        add_help=False,
    )
    parser.add_argument("command", help="Available commands: setup, template")
    parser.add_argument("--help", action="store_true", help="Show help message")

    args = parser.parse_args()

    if args.help:
        display_help()
    elif args.command == "setup":
        from prereqs import main as prereqs_main
        prereqs_main()
    elif args.command == "template":
        from template_create import main as template_create_main
        template_create_main()
    else:
        print(colored("Unknown command. Run 'oiv2cq --help' for available commands.", "red"))

if __name__ == "__main__":
    main()
