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
HEIGHT = 128
WIDTH = 128

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
    for d in range(HEIGHT):
        depth_slice = []
        for i in range(WIDTH):
            row = []
            temp = 0
            for j in range(INPUT_CHANNELS):
                row.append(temp)
                temp += 1
            depth_slice.append(row)
        input_matrix.append(depth_slice)
    
    # Reshape to NHWC format
    input_tensor = torch.Tensor(input_matrix).reshape(1, HEIGHT, WIDTH, INPUT_CHANNELS)
    print("Input shape (NHWC):", input_tensor.shape)
    
    # Permute to NCHW format
    input_tensor = input_tensor.permute(0, 3, 1, 2)
    print("Permuted input shape (NCHW):", input_tensor.shape)

    filters_matrix = []
    temp = 0
    for k in range(KERNEL_SIZE):
        kernel_matrix = []
        for d in range(KERNEL_SIZE):
            depth_slice = []
            for i in range(INPUT_CHANNELS):
                row = []
                temp = 0
                for j in range(OUTPUT_CHANNELS):
                    row.append(temp)
                    temp += 1
                depth_slice.append(row)
            kernel_matrix.append(depth_slice)
        filters_matrix.append(kernel_matrix)

    # Reshape to KKIO format
    filters_tensor = torch.Tensor(filters_matrix).reshape(
        KERNEL_SIZE, KERNEL_SIZE, INPUT_CHANNELS, OUTPUT_CHANNELS
    )
    print("Weights shape (KKIO):", filters_tensor.shape)
    
    # Permute to OIKK format
    filters_tensor = filters_tensor.permute(3, 2, 0, 1)
    print("Permuted weights shape (OIKK):", filters_tensor.shape)

    # Export input and kernel tensors to numpy files
    write_npy_file('input_py.npy', input_tensor.numpy())
    write_npy_file('kernel_py.npy', filters_tensor.numpy())

    # Re-assign the permuted tensors to the convolution layer
    conv.weight.data = filters_tensor
    conv.bias.data = torch.zeros(OUTPUT_CHANNELS)

    # Perform convolution
    output = conv(input_tensor)
    print("Output shape:", output.shape)

    # Permute output from NCHW to NHWC
    output = output.permute(0, 2, 3, 1)
    print("Permuted output shape (NHWC):", output.shape)

    # Export the output
    output_np = output.detach().numpy()
    write_npy_file('output_py.npy', output_np)
    output_1d = output_np.flatten()    # Flatten to 1D array for binary file
    write_binary_file('py_nhwc_output.bin', output_1d)

    print("3D Convolution complete. Output written to 'py_nhwc_output.bin'.")
