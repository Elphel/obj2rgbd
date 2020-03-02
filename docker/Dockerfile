FROM python:3.7

RUN apt-get update && \
    apt-get install -y \
    curl \
    bzip2 \
    libfreetype6 \
    libgl1-mesa-dev \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    xvfb && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pip --upgrade
RUN pip install --no-cache-dir numpy \
                               scipy \
                               pandas \
                               matplotlib \
                               pillow \
                               OpenEXR

ENV BLENDER_URL https://download.blender.org/release/Blender2.80/blender-2.80-linux-glibc217-x86_64.tar.bz2

RUN mkdir /usr/local/blender && \
    curl -SL $BLENDER_URL -o blender.tar.bz2 && \
    tar -jxvf blender.tar.bz2 -C /usr/local/blender --strip-components=1 && \
    rm blender.tar.bz2 && \
    ln -sf /usr/local/blender/blender /usr/local/bin

RUN mkdir git && cd git && \
    git clone https://git.elphel.com/Elphel/obj2rgbd.git

ENV DISPLAY 1:

#COPY init_fake_display.sh /usr/local/bin/init_fake_display.sh

#CMD ['/bin/bash', '/usr/local/bin/init_fake_display.sh']

ENTRYPOINT bash -c "Xvfb :1 -screen 0 1920x1080x24+32 -fbdir /var/tmp &" && bash


#time blender -b -noaudio -P blender_generate_image_and_depth.py -- input/1527256815_550165_v01/1527256815_550165.obj
#CMD Xvfb :1 -screen 0 1920x1080x24+32 -fbdir /var/tmp
#ENTRYPOINT export DISPLAY="TEST"
