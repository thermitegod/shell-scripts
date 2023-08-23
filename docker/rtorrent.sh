#!/usr/bin/env bash

# docker pull ghcr.io/crazy-max/rtorrent-rutorrent:latest

docker run -d \
  --name rutorrent \
  --ulimit nproc=65535 \
  --ulimit nofile=32000:40000 \
  -p 6881:6881/udp \
  -p 8000:8000 \
  -p 8080:8080 \
  -p 9000:9000 \
  -p 50000:50000 \
  -v /mnt/cache/anime:/data \
  -v /mnt/anime/downloads:/downloads \
  ghcr.io/crazy-max/rtorrent-rutorrent
