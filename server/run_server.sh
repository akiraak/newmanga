#!/bin/sh

cd /mnt/c/Users/akira/Programs/newmanga
. pyenv/bin/activate
cd server
. ./profile_local
flask run --host=0.0.0.0 --port=5010
