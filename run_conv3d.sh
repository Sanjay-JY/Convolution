#!/bin/bash

# Compile the C++ code
g++ conv3d.cpp -o conv3d

# Execute the compiled program
./conv3d

# Run the Python script for convolution
python3 conv3d.py

# Compare the output binary files
python3 compare_bin.py cpp_conv3d_output.bin py_conv3d_output.bin --dtype int32
