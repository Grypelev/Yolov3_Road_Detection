#!/bin/bash

echo Type Image Path?
read image

echo Do you want to increase contrast? \(y,n\)
read opinion
export opinion

yes = "y"
if ["$opinion" == "$y"]; then python3 /home/lefteris/darknet/contrast.py fi