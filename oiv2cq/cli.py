import argparse
import os
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

def main():
    activate_virtualenv()  # Activate the virtual environment before parsing arguments

    parser = argparse.ArgumentParser(description="oiv2cq CLI: Automate onboarding and plugin setup")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Prereqs command
    prereqs_parser = subparsers.add_parser("setup", help="Run prerequisite setup")
    prereqs_parser.set_defaults(func=prereqs_main)

    # Template command
    template_parser = subparsers.add_parser(
        "template",
        help="Clone the cloudquery-plugins repo and generate a local CloudQuery plugin template for development.",
    )
    template_parser.set_defaults(func=template_create_main)

    # Parse arguments
    args = parser.parse_args()

    # Execute subcommand or show help
    if args.command:
        args.func()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
