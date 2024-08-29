#!/bin/bash

# Compile the C++ code
g++ ./cpp/conv_nhwc.cpp -o conv_nhwc

# Execute the compiled program
./conv_nhwc

# Run the Python script for convolution
python3 ./python/conv_nhwc.py

# Compare the output binary files
python3 ./python/compare_bin.py cpp_nhwc_output.bin py_nhwc_output.bin --dtype float32