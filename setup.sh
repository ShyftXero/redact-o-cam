#!/usr/bin/zsh

# svenv
sudo apt-get install v4l2loopback-dkms 
sudo modprobe v4l2loopback
sudo usermod -a -G video $USER
pip install -r requirements.txt
newgrp video # for this shell only. 