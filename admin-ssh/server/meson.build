project('custom-sshd', 'c', 'cpp', default_options: ['c_std=c11', 'cpp_std=c++17'])
#libssh = dependency('libssh', version: '==0.8.3')
libssh = dependency('libssh')
executable('main', 'src/main.cpp', dependencies: libssh)
