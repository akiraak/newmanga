#!/bin/sh

cd /home/akiraak/projects/newmanga
. pyenv/bin/activate
cd server
. ./profile_pro
flask fetchbooks