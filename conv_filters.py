from torch import nn
import torch
import numpy as np

def write_binary_file(file_path, array):
    with open(file_path, 'wb') as f:
        array.tofile(f)

def write_npy_file(file_path, array):
    np.save(file_path, array)

INPUT_CHANNELS = 64
OUTPUT_CHANNELS = 128
KERNEL_SIZE = 3
STRIDE = 1
PADDING = 0
HEIGHT = 64
WIDTH = 64

if __name__ == "__main__":

    conv = nn.Conv2d(
        OUTPUT_CHANNELS,
        INPUT_CHANNELS,
        kernel_size=(KERNEL_SIZE, KERNEL_SIZE),
        stride=STRIDE,
        padding=PADDING,
    )

    temp = 0
    input_matrix = []
    for d in range(INPUT_CHANNELS):
        depth_slice = []
        temp=0
        for i in range(HEIGHT):
            row = []
            for j in range(WIDTH):
                row.append(temp)
                temp += 1
            depth_slice.append(row)
        input_matrix.append(depth_slice)
    input_tensor = torch.Tensor(input_matrix).reshape(1, INPUT_CHANNELS, HEIGHT, WIDTH)
    print("input shape ", input_tensor.shape)

    filters_matrix = []
    temp=0
    for k in range(OUTPUT_CHANNELS):
        kernel_matrix = []
        for d in range(INPUT_CHANNELS):
            depth_slice = []
            temp=0
            for i in range(KERNEL_SIZE):
                row = []
                for j in range(KERNEL_SIZE):
                    row.append(temp)
                    temp += 1
                depth_slice.append(row)
            kernel_matrix.append(depth_slice)
        filters_matrix.append(kernel_matrix)
    filters_tensor = torch.Tensor(filters_matrix).reshape(
        OUTPUT_CHANNELS, INPUT_CHANNELS, KERNEL_SIZE, KERNEL_SIZE
    )
    print("weights shape ", filters_tensor.shape)

    bias_matrix = [(0) for i in range(OUTPUT_CHANNELS)]
    bias_tensor = torch.Tensor(bias_matrix)

    conv.weight.data = filters_tensor
    conv.bias.data = bias_tensor

    output = conv(input_tensor)
    print("output shape ", output.shape)
    output_np = output.detach().numpy() 
    output_1d = output_np.flatten()    # Flatten to 1D array

    # Write the 1D array to a binary file
    write_binary_file('py_filter_output.bin', output_1d)

    print("3D Convolution complete. Output written to 'py_filter_output.bin'.")
