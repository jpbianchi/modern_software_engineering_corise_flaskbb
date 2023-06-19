#!/usr/bin/env bash
source /home/vscode/venv/bin/activate

# for act
export PATH="./bin:$PATH" 

# for tests
pip install playwright --upgrade
playwright install

# act uses docker, so let's spin it
# sudo apt install docker.io
sudo service docker start
sudo service docker enable

# run this script with . venv.sh
