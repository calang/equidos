# Equids

Visual identification of equids (horses, donkeys, mules) pre-registered individuals.

<!-- TOC -->
* [Equids](#equids)
  * [Project Description](#project-description)
  * [Requirements](#requirements)
  * [Installation](#installation)
    * [1. `.env` file setting](#1-env-file-setting)
    * [2. Create or update the virtual environment](#2-create-or-update-the-virtual-environment)
  * [Files](#files)
<!-- TOC -->

## Project Description

See [Project_Description](Project_Description.md) for details.

## Requirements

Linux, MacOS or WSL system with:

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

## Use of AI Coding Agents
This project uses AI coding agents to assist in code generation, debugging, and documentation.

### Files
- `agents.ms`: base instructions for all AI coding agents, directing to all other relevant files.
- `agent_prompts/`: This directory contains the prompts used with AI coding agents. Each prompt is documented with its purpose and context.
- `agent_references/`: references and resources used to generate code, data files or documentation.
- `coding-standads/`: coding standards and best practices followed in this project.
