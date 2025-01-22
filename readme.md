# README for OIV2CQ CLI

## Overview
The OIV2CQ CLI tool streamlines the onboarding and development process for Twilio's internal CloudQuery plugin projects. This package bundles two key functionalities:

1. **Prerequisites Setup** (`oiv2cq setup`):
   - Installs and configures dependencies such as Python, GitHub CLI, and CloudQuery CLI.
   - Sets up SSH keys for GitHub access and ensures all required tools are available.

2. **Template Creation** (`oiv2cq template`):
   - Clones the CloudQuery plugins repository.
   - Automates the creation of a plugin template using a sparse-checkout of the cookiecutter repository.
   - Prompts the user for required parameters and generates a fully customized plugin folder.

## Installation
### Using Homebrew
1. Install the OIV2CQ CLI:
   ```bash
   brew tap markgraziano-twlo/oiv2cq && brew install oiv2cq
   ```

2. Verify installation:
   ```bash
   oiv2cq --help
   ```

## Usage
### 1. Prerequisites Setup
To set up the required tools and dependencies:
```bash
oiv2cq setup
```
This command will:
- Install or upgrade Python, GitHub CLI, and CloudQuery CLI.
- Authenticate your GitHub CLI session.
- Configure SSH keys for GitHub access.

### 2. Template Creation
To create a new plugin template:
```bash
oiv2cq template
```
This command will:
- Clone the CloudQuery plugins repository into your specified directory.
- Create a new branch for your plugin.
- Prompt you for plugin-specific details (e.g., plugin name, API base URL).
- Generate a plugin folder using the cookiecutter template.

## Requirements
- Python 3.9+
- Homebrew (for dependency installation)
- GitHub CLI (installed during `setup` if missing)


