#!/bin/bash

# Compile the C++ code
g++ ./cpp/conv3x3x64x128.cpp -o conv_filter

# Execute the compiled program
./conv_filter

# Run the Python script for convolution
python3 ./python/conv_filters.py

# Compare the output binary files
python3 ./python/compare_bin.py cpp_filter_output.bin py_filter_output.bin --dtype float32
