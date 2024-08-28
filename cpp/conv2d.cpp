#include <iostream>
#include <vector>
#include <fstream>
#define INPUT_HEIGHT 128
#define INPUT_WIDTH 64
#define KERNEL_HEIGHT 3
#define KERNEL_WIDTH 3

using namespace std;

void write_to_binary(const string &filename, const vector<int> &data)
{
    ofstream file(filename, ios::binary);
    file.write(reinterpret_cast<const char *>(data.data()), data.size() * sizeof(int));
    file.close();
}

int main()
{
    vector<vector<int>> input;
    vector<vector<int>> kernel;

    int temp = 0;
    for (int i = 0; i < INPUT_HEIGHT; i++)
    {
        vector<int> row;
        for (int j = 0; j < INPUT_WIDTH; j++)
        {
            row.push_back(temp);
            temp++;
        }
        input.push_back(row);
    }

    temp = 0;
    for (int i = 0; i < KERNEL_HEIGHT; i++)
    {
        vector<int> row;
        for (int j = 0; j < KERNEL_WIDTH; j++)
        {
            row.push_back(temp);
            temp++;
        }
        kernel.push_back(row);
    }

    int stride = 1;
    int padding = 0;

    int output_height = ((INPUT_HEIGHT - KERNEL_HEIGHT + (2 * padding)) / stride) + 1;
    int output_width = ((INPUT_WIDTH - KERNEL_WIDTH + (2 * padding)) / stride) + 1;

    cout << "Output Height: " << output_height << endl;
    cout << "Output Width: " << output_width << endl;

    vector<vector<int>> output(output_height, vector<int>(output_width, 0));

    for (int ih = 0; ih < output_height; ih++)
    {
        for (int iw = 0; iw < output_width; iw++)
        {
            int sum = 0;
            for (int kh = 0; kh < KERNEL_HEIGHT; kh++)
            {
                for (int kw = 0; kw < KERNEL_WIDTH; kw++)
                {
                    int ow = iw * stride + kw;
                    int oh = ih * stride + kh;
                    sum += input[oh][ow] * kernel[kh][kw];
                }
            }
            output[ih][iw] = sum;
        }
    }

    vector<int> output_1d;
    for (int i = 0; i < output_height; i++)
    {
        for (int j = 0; j < output_width; j++)
        {
            output_1d.push_back(output[i][j]);
        }
    }

    write_to_binary("cpp_conv2d_output.bin", output_1d);
    cout << "3D Convolution complete. Output written to 'cpp_conv2d_output.bin'." << endl;
    return 0;
}