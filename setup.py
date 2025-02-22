from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy, os, sys

import os
import sys

if sys.platform == 'darwin':
    os.environ['CFLAGS']   = '-DGGML_USE_ACCELERATE -O3 -std=gnu11 -I/opt/homebrew/Cellar/sdl2/2.28.3/include/SDL2'
    os.environ['CXXFLAGS'] = '-DGGML_USE_ACCELERATE -O3 -std=c++11 -I/opt/homebrew/Cellar/sdl2/2.28.3/include/SDL2'
    os.environ['LDFLAGS']  = '-framework Accelerate -L/opt/homebrew/Cellar/sdl2/2.28.3/lib'
else:
    os.environ['CFLAGS']   = '-mavx -mavx2 -mfma -mf16c -O3 -std=gnu11 -I/opt/homebrew/Cellar/sdl2/2.28.3/include/SDL2'
    os.environ['CXXFLAGS'] = '-mavx -mavx2 -mfma -mf16c -O3 -std=c++11 -I/opt/homebrew/Cellar/sdl2/2.28.3/include/SDL2'
    os.environ['LDFLAGS']  = '-L/opt/homebrew/Cellar/sdl2/2.28.3/lib -lSDL2'

ext_modules = [
    Extension(
        name="whispercpp",
        sources=["whispercpp.pyx", "whisper.cpp/whisper.cpp", "stream.cpp"],
        language="c++",
        extra_compile_args=["-std=c++11"],
        include_dirs=['/opt/homebrew/Cellar/sdl2/2.28.3/include/SDL2/']        
   )
]
ext_modules = cythonize(ext_modules)

whisper_clib = ('whisper_clib', {'sources': ['whisper.cpp/ggml.c']})

setup(
    name='whispercpp',
    version='1.0',
    description='Python bindings for whisper.cpp',
    author='Luke Southam',
    author_email='luke@devthe.com',
    libraries=[whisper_clib],
    ext_modules = cythonize("whispercpp.pyx"),
    include_dirs = ['./whisper.cpp/', '/opt/homebrew/Cellar/sdl2/2.28.3/include/SDL2/', numpy.get_include()],
    install_requires=[
      'numpy',
      'ffmpeg-python',
      'requests'
    ],
)
