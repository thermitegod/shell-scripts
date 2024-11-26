#!/usr/bin/env bash

# docker logs -f flexget
# docker exec -it flexget flexget -c /config/config.yml check

###############

# docker stop flexget
# docker rm flexget
# docker pull ghcr.io/flexget/flexget:latest

docker run -d \
  --name flexget \
  --restart unless-stopped \
  --user 1000:1000 \
  -e TZ=$TZ \
  -v /home/brandon/.config/flexget:/config \
  -v /mnt/cache/anime/rtorrent/watch:/downloads \
  ghcr.io/flexget/flexget \
  daemon start --autoreload-config

# docker image ls
# docker image rm OLD-HASH

