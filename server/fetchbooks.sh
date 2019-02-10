#!/bin/sh

cd /mnt/c/Users/akira/Programs/newmanga
. pyenv/bin/activate
cd server
. ./profile_local
flask fetchbooks
