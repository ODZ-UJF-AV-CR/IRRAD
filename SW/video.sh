#!/bin/bash
vlc v4l2:// :v4l2-dev=/dev/video0 :v4l2-width=640 :v4l2-height=480 --sout="#transcode{vcodec=MJPG,vb=800,scale=1,acodec=none}:http{mux=mpjpeg,dst=147.231.24.61:8080/}" -I dummy
