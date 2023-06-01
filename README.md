# Pythonic control functions
Limited to the **Unitree A1 _and_ SDK version 3.2.**

**HIGHLEVEL functions** only!

This is a reference library which uses the [unitree_legged_sdk v3.2](https://github.com/unitreerobotics/unitree_legged_sdk).

Python functionality is added through [pybind11](https://github.com/pybind/pybind11) and built with CMake.

## Dependencies
- [Boost](https://www.boost.org/) (version 1.5.4 or higher)
- [CMake](https://cmake.org/) (version 2.8.3 or higher)
- [LCM](https://github.com/lcm-proj/lcm/releases) (version 1.4.0)
- [g++](https://gcc.gnu.org/) (version 8.3.0 or higher)
- [pybind11](https://github.com/pybind/pybind11) (version 2.10.4 or higher)
- [Python](https://www.python.org/) (version 3.6)

Install Boost, CMake, the latest 8.x version of g++ and the latest version of Python 3.6 with the following command:
```
sudo apt-get update
sudo apt-get install libboost-all-dev make cmake g++-8 gcc-8 python3.6
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

Make sure the path to the pybind11 files will be `/quadruped_py_control/python_wrapper/third-party/pybind11/`. Copy all files from the download to the pybind11-folder in this repository!

If you cannot find `msgpack.hpp` while compiling, run:

`sudo apt get libmsgpack*`

In `python_interface.cpp` all C-Style arrays have been commented out. Pybind11 does not support the direct conversion of C-Arrays to Python lists. A workaround may be found [here](https://github.com/pybind/pybind11/issues/2149).

In both `CMakeLists.txt` the compiler standard has been set to **14** due to compatibility reasons with pybind11.

In both `CMakeLists.txt` make sure that the correct architecture type is selected! `amd` for RaspberryPi and VirtualMachine and `arm` when working with the NVIDIA NX!

`libunitree_legged_sdk_amd64.so` or `libunitree_legged_sdk_arm64.so`

## Building
Download the quadruped_py_control library (and unzip) to `/home/[username]` and build with
```
cd quadruped_py_control
mkdir build
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
sudo python3 py_test.py
```
in the respective folder.

## Important
When working with an IDE (preferably Visual Studio Code) make sure to set the C++ compiler and the Python interpreter to the respective version!
