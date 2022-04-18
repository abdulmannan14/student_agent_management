#!/bin/bash
cd /home/ubuntu/limoucloud_backend/
source venv/bin/activate
supervisord -c supervisord.conf
