#!/bin/bash

# Compile the C++ code
g++ ./cpp/conv3d.cpp -o conv3d

# Execute the compiled program
./conv3d

# Run the Python script for convolution
python3 ./python/conv3d.py

# Compare the output binary files
python3 ./python/compare_bin.py cpp_conv3d_output.bin py_conv3d_output.bin --dtype int32
