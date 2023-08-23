#!/usr/bin/env bash

# docker pull ghcr.io/flexget/flexget:latest

docker run -d \
  --name flexget \
  --restart unless-stopped \
  --user 1000:1000 \
  -p 5050:5050 \
  -v /home/brandon/.config/flexget:/config \
  -v /mnt/cache/anime/rtorrent/watch:/downloads \
  ghcr.io/flexget/flexget \
  daemon start --autoreload-config
