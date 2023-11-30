# `coinespy` library

The `coinespy` library allows users to access Bosch Sensortec's MEMS sensors on the Application Board 2.0, Application Board 3.0 and Application Board 3.1 through a Python interface. It offers a flexible solution for developing a host independent wrapper interface for the sensors with robust error handling mechanism. The core functionalities remain the same as with usage of coinesAPI on C level.

This folder contains the Python wrapper on top of the COINES C library.

To build a new wheel, follow the steps as described in: https://packaging.python.org/tutorials/packaging-projects/

To install this package:

```bash
$ python setup.py install
```

dependencies libraries / software
- sudo apt-get install libdbus-1-dev
- sudo apt-get install libusb-1.0-0-dev
- sudo apt-get install libudev-dev
- sudo apt-get install gcc
- sudo apt-get install make
- sudo apt-get install dfu-util

to build library. Run command
    On Linux/Mac
    + lib Mac OS arm: make TARGET=PC ARCH=arm64 COINES_BACKEND=COINES_BRIDGE
    + lib 64bit: make TARGET=PC ARCH=x86_64 COINES_BACKEND=COINES_BRIDGE
    + lib 32bit should be build on system 32bit
    
    On Window
    + lib 32bit: mingw32-make TARGET=PC ARCH=x86 COINES_BACKEND=COINES_BRIDGE
    + lib 64bit: mingw32-make TARGET=PC ARCH=x86_64 COINES_BACKEND=COINES_BRIDGE