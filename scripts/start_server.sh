#!/bin/bash
cd /home/ubuntu/acmimanagement/
source venv/bin/activate
supervisord -c supervisord.conf
