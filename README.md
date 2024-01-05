# Build / Install

```bash
mkdir build
meson setup --prefix=${HOME}/.local --buildtype=release ./build
cd build
ninja
ninja install
```
