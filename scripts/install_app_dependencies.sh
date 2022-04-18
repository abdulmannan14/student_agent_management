#!/bin/bash
sudo pip3 install virtualenv
cd /home/ubuntu/limoucloud_backend
virtualenv venv
source venv/bin/activate
sudo pip3 install -r requirements.txt
