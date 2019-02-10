#!/bin/sh

cd /home/akiraak/projects/newmanga
. pyenv/bin/activate
cd server
. ./profile_pro
flask run --host=0.0.0.0 --port=5010
