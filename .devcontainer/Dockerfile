# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.233.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.10"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Define the path to the virtualenv to work with
ARG VENV_PATH="/home/vscode/venv"

# Setup a virtual environment, install the necessary modules, delete tmp files
RUN su vscode -c "python -m venv /home/vscode/venv" 

# Setup docker
RUN curl -s https://get.docker.com/ | sudo bash
RUN sudo usermod -aG docker vscode

# Setup act
RUN curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Setup aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && sudo ./aws/install

# Setup terraform
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends rcm \
    && curl https://apt.releases.hashicorp.com/gpg | gpg --dearmor > /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" > /etc/apt/sources.list.d/hashicorp.list \
    && apt update \
    && apt -y install --no-install-recommends terraform
