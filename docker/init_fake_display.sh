#!/bin/bash
touch /testfile.txt
Xvfb :1 -screen 0 1920x1080x24+32 -fbdir /var/tmp &
