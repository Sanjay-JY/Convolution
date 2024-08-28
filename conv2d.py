import torch
import torch.nn.functional as F
import numpy as np

# Function to write NumPy array to binary file
def write_binary_file(file_path, array):
    with open(file_path, 'wb') as f:
        array.tofile(f)

INPUT_HEIGHT = 128
INPUT_WIDTH = 64
KERNEL_HEIGHT = 3
KERNEL_WIDTH = 3

# Initialize input matrix
temp = 0
input_matrix = []
for i in range(INPUT_HEIGHT):
    row = []
    for j in range(INPUT_WIDTH):
        row.append(temp)
        temp += 1
    input_matrix.append(row)

# Initialize kernel matrix
temp = 0
kernel_matrix = []
for i in range(KERNEL_HEIGHT):
    row = []
    for j in range(KERNEL_WIDTH):
        row.append(temp)
        temp += 1
    kernel_matrix.append(row)

# Convert lists to numpy arrays and then to PyTorch tensors
input_tensor = torch.tensor(input_matrix, dtype=torch.int).unsqueeze(0).unsqueeze(0)  # Shape: [1, 1, INPUT_HEIGHT, INPUT_WIDTH]
kernel_tensor = torch.tensor(kernel_matrix, dtype=torch.int).unsqueeze(0).unsqueeze(0)  # Shape: [1, 1, KERNEL_HEIGHT, KERNEL_WIDTH]

# Perform 2D convolution using PyTorch
output_tensor = F.conv2d(input_tensor, kernel_tensor, stride=1, padding=0)

# Convert output tensor to 1D array
output_np = output_tensor.numpy()  # Convert to NumPy array
output_1d = output_np.flatten()         # Flatten to 1D array

print("Input: ",input_tensor.shape)
print("Kernel: ",kernel_tensor.shape)
print("Output: ",output_tensor.shape)
# Write the 1D array to a binary file
write_binary_file('py_conv2d_output.bin', output_1d)

print("Convolution complete. Output written to 'py_output.bin'.")
