import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from termcolor import colored

# Function to run shell commands
def run_command(command, capture_output=False):
    result = subprocess.run(command, shell=True, text=True, capture_output=capture_output)
    if result.returncode != 0:
        print(colored(f"Error executing command: {command}\n{result.stderr}", "red"))
        sys.exit(1)
    return result.stdout.strip() if capture_output else None

# Function to prompt for a valid directory
def prompt_for_directory(prompt_message):
    while True:
        directory = input(colored(prompt_message, "yellow")).strip()
        directory = os.path.abspath(os.path.expanduser(directory))
        if Path(directory).is_dir():
            return directory
        print(colored(f"Invalid directory: {directory}. Please ensure the path exists.", "red"))

def main():
    # Step 1: Prompt for project folder
    print(colored("Please navigate to your preferred projects folder.", "yellow"))
    print(colored("Note: The folder must already exist.", "red"))
    project_folder = prompt_for_directory("Enter the full path to your projects folder: ")
    project_folder = Path(project_folder)

    # Step 2: Clone the repository
    repo_url = "git@github.com:twilio-internal/cloudquery-plugins.git"
    print(colored(f"Cloning repository: {repo_url}", "cyan"))
    run_command(f"git clone {repo_url} {project_folder / 'cloudquery-plugins'}")

    # Step 2.1: Create a feature branch
    repo_path = project_folder / "cloudquery-plugins"
    os.chdir(repo_path)
    print(colored(f"Changed directory to: {repo_path}", "green"))
    plugin_name = input(colored("Enter the snake_case identifier for your plugin (e.g., proofpoint_psat): ", "yellow")).strip()
    if not plugin_name:
        print(colored("Plugin name is required.", "red"))
        sys.exit(1)
    branch_name = f"feature/{plugin_name}-init"
    print(colored(f"Creating feature branch: {branch_name}", "cyan"))
    run_command(f"git checkout -b {branch_name}")
    print(colored(f"Created and switched to branch: {branch_name}", "green"))

    # Step 3: Verify and navigate into the plugins folder
    plugins_dir = repo_path / "plugins"
    if not plugins_dir.is_dir():
        print(colored(f"The expected plugins directory '{plugins_dir}' does not exist. Please check the repository structure.", "red"))
        sys.exit(1)

    # Step 4: Sparse checkout cookiecutter template
    cookiecutter_repo_url = "https://github.com/markgraziano-twlo/cloudquery-cookiecutter.git"
    temp_repo_dir = project_folder / "temp_cookiecutter_repo"
    cookiecutter_folder = "{{cookiecutter.plugin_name}}"

    print(colored(f"Fetching {cookiecutter_folder} from {cookiecutter_repo_url}...", "cyan"))

    # Clone the repo sparsely with only the required folder
    run_command(f"git clone --depth 1 --filter=blob:none --sparse {cookiecutter_repo_url} {temp_repo_dir}")
    os.chdir(temp_repo_dir)
    run_command(f"git sparse-checkout set {cookiecutter_folder}")

    # Copy the cookiecutter template folder to the plugins directory
    shutil.copytree(
        temp_repo_dir / cookiecutter_folder,
        plugins_dir / cookiecutter_folder  # Keep the placeholder format
    )
    print(colored(f"Copied {cookiecutter_folder} to {plugins_dir / cookiecutter_folder}", "green"))

    # Cleanup the temporary repository directory
    shutil.rmtree(temp_repo_dir)
    print(colored("Temporary cookiecutter repository cleaned up.", "green"))

    # Step 5: Prompt for cookiecutter variables
    plugin_path = plugins_dir / cookiecutter_folder
    print(colored(f"Changed directory to template: {plugin_path}", "green"))

    plugin_camel_case = input(colored("Enter the CamelCase identifier for your plugin (e.g., ProofpointPsat): ", "yellow")).strip()
    record_type = input(colored("Enter the snake_case name for the record type (e.g., events, user_ids): ", "yellow")).strip()
    api_base_url = input(colored("Enter the base URL for the API: ", "yellow")).strip()
    team_name_email = input(colored("Enter your Full Name, Team Name: ", "yellow")).strip()

    record_type_class = ''.join(word.capitalize() for word in record_type.split('_'))

    cookiecutter_json = {
        "plugin_name": plugin_name,
        "PluginName": plugin_camel_case,
        "record_type": record_type,
        "RecordTypeClass": record_type_class,
        "APIBaseURL": api_base_url,
        "TeamNameTeamEmail": team_name_email
    }

    # Save cookiecutter.json in the plugins directory
    with open(plugins_dir / "cookiecutter.json", "w") as f:
        json.dump(cookiecutter_json, f, indent=4)
    print(colored(f"Generated cookiecutter.json at {plugins_dir}", "green"))

    # Step 6: Run cookiecutter refactoring
    try:
        print(colored("Running cookiecutter refactoring...", "cyan"))
        os.chdir(plugins_dir)  # Ensure the working directory is correct
        run_command(f"pipx run cookiecutter {plugins_dir} --no-input")
        print(colored("Performed cookiecutter refactoring.", "green"))

        plugin_path = plugins_dir / plugin_name
        if not plugin_path.is_dir():
            print(colored(f"Error: Plugin directory '{plugin_path}' not found after refactoring.", "red"))
            sys.exit(1)
        print(colored(f"Plugin directory after refactoring: {plugin_path}", "green"))

        # Delete cookiecutter.json after successful refactoring
        os.remove(plugins_dir / "cookiecutter.json")
        print(colored("Deleted cookiecutter.json after refactoring.", "green"))

    except Exception as e:
        print(colored(f"Error during cookiecutter refactoring: {e}", "red"))
        sys.exit(1)

    # Step 7: OpenAPI cleanup
    openapi_support = input(colored("Does the source support OpenAPI (y/n)? ", "yellow")).strip().lower()
    if openapi_support == 'n':
        for root, dirs, files in os.walk(plugin_path, topdown=False):
            for name in files:
                if "oapi" in name:
                    os.remove(Path(root) / name)
            for name in dirs:
                if "oapi" in name:
                    shutil.rmtree(Path(root) / name)
        print(colored("Deleted OpenAPI-related files and folders.", "green"))

    # Step 8: Completion message
    print(colored("\u2714 All steps completed successfully! Your environment is ready for use. You can now continue working in this terminal.", "green"))

if __name__ == "__main__":
    main()
