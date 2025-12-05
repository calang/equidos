# Equids

Visual identification of equids (horses, donkeys, mules) pre-registered individuals.

## Project Description

See [Project_Description](Project_Description.md) for details.

## Requirements

Linux or MacOS system with:

- `mamba` or `miniconda` or `conda` for managing the virtual environment.
- Python 3.11 (included in the `mamba` environment description: `env.yml`)

## Installation

### 1. `.env` file setting

```bash
cp .env_template .env
```

Then, edit `.env` as needed.

### 2. Create or update the virtual environment

This will create or update a `mamba` (`conda`-like) virtual environment with all necessary packages.

```bash
make update-env
```

## Files

- agent_prompts/ - prompts used with AI agents
- data/ - datasets, preprocessed data, and results
- docs/ - documentation files
- src/ - source code
- tests/ - unit tests
- .bashrc - bash configuration file to set environment variables
- .env_template - template for environment variables .env file
- Makefile - makefile with commands for common tasks
- env.yml - `mamba` environment description file
<!-- notebooks/ - Jupyter notebooks for exploration and prototyping -->
