#!/bin/bash
docker run -it \
           --name obj2rgbd \
           -v /home/oleg/GIT/obj2rgbd/:/app \
           --rm obj2rgbd:latest \
           /bin/bash
