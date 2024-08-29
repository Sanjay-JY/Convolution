import numpy as np
import argparse

def read_binary_file(file_path, dtype=np.int32):
    with open(file_path, 'rb') as f:
        data = np.fromfile(f, dtype=dtype)
    return data

def compute_difference(file1, file2, dtype):
    data1 = read_binary_file(file1, dtype)
    data2 = read_binary_file(file2, dtype)

    if data1.shape != data2.shape:
        raise ValueError(f"Files have different shapes: {data1.shape} vs {data2.shape}")

    difference = np.abs(data1 - data2)
    return difference

def main():
    parser = argparse.ArgumentParser(description="Compare two binary files and find differences.")
    parser.add_argument("file1", help="Path to the first binary file")
    parser.add_argument("file2", help="Path to the second binary file")
    parser.add_argument("--dtype", default="int32", help="Data type of the binary files (default: int32)")

    args = parser.parse_args()

    file1 = args.file1
    file2 = args.file2
    dtype = getattr(np, args.dtype)

    try:
        diff = compute_difference(file1, file2, dtype)
        min = np.min(diff)
        max = np.max(diff)
        non_zero_indices = np.nonzero(diff)[0]

        if non_zero_indices.size == 0 or max<0.0001:
            print("The binary files are identical upto 4 decimal places.")
        else:
            print(f"Differences found at {len(non_zero_indices)} positions:")
            for index in non_zero_indices:
                print(f"Position {index}: File1 = {read_binary_file(file1, dtype)[index]}, File2 = {read_binary_file(file2, dtype)[index]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
