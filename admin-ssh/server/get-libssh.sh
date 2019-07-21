#!/usr/bin/env bash
set -xeuo pipefail

wget -N 'https://www.libssh.org/files/0.8/libssh-0.8.3.tar.xz'
tar -xf 'libssh-0.8.3.tar.xz'
cd 'libssh-0.8.3'
mkdir 'build'
cd 'build'
cmake .. -G Ninja -DCMAKE_INSTALL_PREFIX=/usr
ninja
ninja install
