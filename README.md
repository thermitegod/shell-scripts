# Build / Install

Build

```bash
meson setup --prefix=${HOME}/.local --buildtype=release ./build
ninja -C build
```

Install

```bash
ninja -C build install

./tools_bin_setup.py # install symlinks to python scripts
./tools_symlink_chrome.py # install symlinks for chrome profiles
```
