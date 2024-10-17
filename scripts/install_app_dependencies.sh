#!/bin/bash
sudo pip3 install virtualenv
cd /home/ubuntu/acmimanagement
virtualenv venv
source venv/bin/activate
sudo pip3 install -r requirements.txt
