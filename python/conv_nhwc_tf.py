import tensorflow as tf
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
PADDING = 'VALID'  # Corresponds to no padding
HEIGHT = 128
WIDTH = 128

if __name__ == "__main__":

    conv = tf.keras.layers.Conv2D(
        filters=OUTPUT_CHANNELS,
        kernel_size=(KERNEL_SIZE, KERNEL_SIZE),
        strides=(STRIDE, STRIDE),
        padding=PADDING,
        data_format='channels_last',
        use_bias=True,
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

    input_tensor = tf.convert_to_tensor(input_matrix, dtype=tf.float32)
    input_tensor = tf.reshape(input_tensor, (1, HEIGHT, WIDTH, INPUT_CHANNELS))
    print("input shape ", input_tensor.shape)

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
    filters_tensor = tf.convert_to_tensor(filters_matrix, dtype=tf.float32)
    print("weights shape ", filters_tensor.shape)

    bias_tensor = tf.zeros(OUTPUT_CHANNELS, dtype=tf.float32)

    conv.build(input_tensor.shape)
    conv.set_weights([filters_tensor, bias_tensor])

    output = conv(input_tensor)
    print("output shape (NHWC) ", output.shape)

    output_np = output.numpy()
    output_1d = output_np.flatten()  # Flatten to 1D array

    # Write the 1D array to a binary file
    write_binary_file('py_nhwc_output.bin', output_1d)

    print("3D Convolution complete. Output written to 'py_nhwc_output.bin'.")
