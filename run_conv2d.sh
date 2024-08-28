#!/bin/bash

# Compile the C++ code
g++ ./cpp/conv2d.cpp -o conv2d

# Execute the compiled program
./conv2d

# Run the Python script for convolution
python3 ./python/conv2d.py

# Compare the output binary files
python3 ./python/compare_bin.py cpp_conv2d_output.bin py_conv2d_output.bin --dtype int32
