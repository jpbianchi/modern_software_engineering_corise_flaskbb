To be able to run CI workflow in codespaces, I used the act tool.
Setup:
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

Install docker:
sudo apt-get update
sudo apt-get install docker.io

Run docker:

sudo systemctl start docker
sudo systemctl enable docker

# if you get this error: ""systemd" is not running in this container due to its overhead.
# Use the "service" command to start services instead", use these commands
sudo service docker start
sudo service docker enable

# then check
sudo service docker status

# then run

sudo ./bin/act  > act.log
# then open act.log and watch the workflow in real time


# https://github.com/nektos/act#example-commands
# Command structure:
act [<event>] [options]
If no event name passed, will default to "on: push"
If actions handles only one event it will be used as default instead of "on: push"

# List all actions for all events:
act -l

# List the actions for a specific event:
act workflow_dispatch -l

# List the actions for a specific job:
act -j test -l

# Run the default (`push`) event:
act

# Run a specific event:
act pull_request

# Run a specific job:
act -j test

# Collect artifacts to the /tmp/artifacts folder:
act --artifact-server-path /tmp/artifacts

# Run a job in a specific workflow (useful if you have duplicate job names)
act -j lint -W .github/workflows/checks.yml

# Run in dry-run mode:
act -n

# Enable verbose-logging (can be used with any of the above commands)
act -v

