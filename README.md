# Pythonic control functions

This is a reference library which uses the [unitree_legged_sdk v3.2](https://github.com/unitreerobotics/unitree_legged_sdk).

Python functionality is added through [pybind11](https://github.com/pybind/pybind11) and built with CMake.

This repository was created while working for the [KISS Project](https://projekt-kiss.net/) at the Hochschule Furtwangen University.

This repository is optimized for the NX-System, that comes with the Robot.

## Quick Installation Guide

Download the repository:

```
git clone --recursive https://github.com/Maddy1206/quadruped_py_control.git
```

Python scripts can be started already because the pre-compiled libraries are downloaded with this repository.

If you want to run the robot with C++ programs you need to build them first.
Head over to [Building](#building).

## Dependencies

- [Boost](https://www.boost.org/) (version 1.5.4 or higher)
- [CMake](https://cmake.org/) (version 2.8.3 or higher)
- [LCM](https://github.com/lcm-proj/lcm/releases) (version 1.4.0)
- [g++](https://gcc.gnu.org/) (version 7.5.0 or higher)
- [pybind11](https://github.com/pybind/pybind11) (version 2.10.4 or higher)
- [Python](https://www.python.org/) (version 3.6)

Install Boost, CMake, the latest 8.x version of g++ and the latest version of Python 3.6 with the following command:

```
sudo apt-get update
sudo apt-get install libboost-all-dev make cmake g++-7 gcc-7 python3.6
```

Download LCM and unzip to `/home/[username]` and build the software:

```
cd lcm-1.4.0
mkdir build
cmake ..
make
sudo make install
```

## Libraries

You must download the pybind11 library seperately and put it in the specific folder.

Make sure the path to the pybind11 files will be `/quadruped_py_control/python_wrapper/third-party/pybind11/`. Copy all files from the download to the pybind11-folder in this repository or use `git`:

```
cd ~/quadruped_py_control/python_wrapper/third-party
git clone https://github.com/pybind/pybind11.git
```

The source code of the [pyrealsense2 library](https://github.com/IntelRealSense/librealsense/releases/tag/v2.53.1) has not been added to this repo because the compiling process takes longer than 30 minutes. Instead, the pre-compiled libraries have been added to `/lib/python/`.

If you cannot find `git`, run:

`sudo apt-get install git`

If you cannot find `msgpack.hpp` while compiling, run:

`sudo apt-get install libmsgpack*`

In `python_interface.cpp` the exposure of C++ classes and types is declared with the help of [pybind11](https://github.com/pybind/pybind11).

In both `CMakeLists.txt` the compiler standard has been set to **14** due to compatibility reasons with pybind11.

In both `CMakeLists.txt` make sure that the correct architecture type is selected! `amd` for RaspberryPi and VirtualMachine and `arm` when working with the NVIDIA NX!

`libunitree_legged_sdk_amd64.so` or `libunitree_legged_sdk_arm64.so`

## Building

Download the quadruped_py_control library (and unzip) to `/home/[username]` and build with

```
cd quadruped_py_control
mkdir build
cd build
cmake ..
make
```

The C++ files should be written to the build-folder and the CPython library to the `../lib/python` folder.

Run the C++ commands with

```
sudo ./example_walk
```

and the Python commands with

```
sudo python3 example_walk.py
```

in the respective folder.

## Important

When working with an IDE (preferably Visual Studio Code) make sure to set the C++ compiler and the Python interpreter to the respective version!
