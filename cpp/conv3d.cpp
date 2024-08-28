#include <iostream>
#include <vector>
#include <fstream>
#define INPUT_HEIGHT 128
#define INPUT_WIDTH 64
#define KERNEL_HEIGHT 3
#define KERNEL_WIDTH 3
#define CHANNEL 3

using namespace std;

void write_to_binary(const string &filename, const vector<int> &data)
{
    ofstream file(filename, ios::binary);
    file.write(reinterpret_cast<const char *>(data.data()), data.size() * sizeof(int));
    file.close();
}

int main()
{
    vector<vector<vector<int>>> input;
    vector<vector<vector<int>>> kernel;

    int temp = 0;
    for (int k = 0; k < CHANNEL; k++)
    {
        vector<vector<int>> col;
        for (int i = 0; i < INPUT_HEIGHT; i++)
        {
            vector<int> row;
            for (int j = 0; j < INPUT_WIDTH; j++)
            {
                row.push_back(temp);
                temp++;
            }
            col.push_back(row);
        }
        input.push_back(col);
    }

    temp = 0;
    for (int k = 0; k < CHANNEL; k++)
    {
        vector<vector<int>> col;
        for (int i = 0; i < KERNEL_HEIGHT; i++)
        {
            vector<int> row;
            for (int j = 0; j < KERNEL_WIDTH; j++)
            {
                row.push_back(temp);
                temp++;
            }
            col.push_back(row);
        }
        kernel.push_back(col);
    }

    int stride = 1;
    int padding = 0;

    int output_height = ((INPUT_HEIGHT - KERNEL_HEIGHT + (2 * padding)) / stride) + 1;
    int output_width = ((INPUT_WIDTH - KERNEL_WIDTH + (2 * padding)) / stride) + 1;

    cout << "Output Height: " << output_height << endl;
    cout << "Output Width: " << output_width << endl;

    vector<vector<vector<int>>> output(1, vector<vector<int>>(output_height, vector<int>(output_width, 0)));

    for (int ih = 0; ih < output_height; ih++)
    {
        for (int iw = 0; iw < output_width; iw++)
        {
            int sum = 0;
            for (int kc = 0; kc < CHANNEL; kc++)
            {
                for (int kh = 0; kh < KERNEL_HEIGHT; kh++)
                {
                    for (int kw = 0; kw < KERNEL_WIDTH; kw++)
                    {
                        int ow = iw * stride + kw;
                        int oh = ih * stride + kh;
                        sum += input[kc][oh][ow] * kernel[kc][kh][kw];
                    }
                }
            }
            output[0][ih][iw] = sum;
        }
    }

    vector<int> output_1d;
    for (int j = 0; j < output_height; j++)
    {
        for (int k = 0; k < output_width; k++)
        {
            output_1d.push_back(output[0][j][k]);
        }
    }

    write_to_binary("cpp_conv3d_output.bin", output_1d);

    cout << "3D Convolution complete. Output written to 'cpp_conv3d_output.bin'." << endl;

    return 0;
}
