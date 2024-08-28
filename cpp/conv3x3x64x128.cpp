#include <iostream>
#include <vector>
#include <fstream>

#define INPUT_HEIGHT 64
#define INPUT_WIDTH 64
#define INPUT_CHANNEL 64
#define KERNEL_HEIGHT 3
#define KERNEL_WIDTH 3
#define KERNEL_CHANNEL 64
#define OUTPUT_CHANNEL 128

using namespace std;

void write_to_binary(const string &filename, const vector<float> &data)
{
    ofstream file(filename, ios::binary);
    file.write(reinterpret_cast<const char *>(data.data()), data.size() * sizeof(float));
    file.close();
}

int main()
{
    vector<vector<vector<vector<float>>>> input;
    vector<vector<vector<vector<float>>>> kernel;

    int temp = 0;

    vector<vector<vector<float>>> channel;
    for (int i = 0; i < INPUT_CHANNEL; i++)
    {
        temp = 0;
        vector<vector<float>> col;
        for (int j = 0; j < INPUT_HEIGHT; j++)
        {
            vector<float> row;
            for (int k = 0; k < INPUT_WIDTH; k++)
            {
                row.push_back(temp);
                temp++;
            }
            col.push_back(row);
        }
        channel.push_back(col);
    }
    input.push_back(channel);

    int N = input.size();
    int C = input[0].size();
    int H = input[0][0].size();
    int W = input[0][0][0].size();
    cout << "Input: \n";
    cout << "N:" << N << " C:" << C << " H:" << H << " W:" << W << "\n";

    temp = 0;

    for (int c = 0; c < OUTPUT_CHANNEL; c++)
    {
        vector<vector<vector<float>>> channel;
        for (int i = 0; i < KERNEL_CHANNEL; i++)
        {
            temp = 0;
            vector<vector<float>> col;
            for (int j = 0; j < KERNEL_HEIGHT; j++)
            {
                vector<float> row;
                for (int k = 0; k < KERNEL_WIDTH; k++)
                {
                    row.push_back(temp);
                    temp++;
                }
                col.push_back(row);
            }
            channel.push_back(col);
        }
        kernel.push_back(channel);
    }

    N = kernel.size();
    C = kernel[0].size();
    H = kernel[0][0].size();
    W = kernel[0][0][0].size();
    cout << "Kernel: \n";
    cout << "N:" << N << " C:" << C << " H:" << H << " W:" << W << "\n";

    int stride = 1;
    int padding = 0;

    int output_height = ((INPUT_HEIGHT - KERNEL_HEIGHT + (2 * padding)) / stride) + 1;
    int output_width = ((INPUT_WIDTH - KERNEL_WIDTH + (2 * padding)) / stride) + 1;

    cout << "Output Height: " << output_height << endl;
    cout << "Output Width: " << output_width << endl;

    vector<vector<vector<vector<float>>>> output(1, vector<vector<vector<float>>>(OUTPUT_CHANNEL, vector<vector<float>>(output_height, vector<float>(output_width, 0))));

    for (int outc = 0; outc < OUTPUT_CHANNEL; outc++)
    {
        for (int ih = 0; ih < output_height; ih++)
        {
            for (int iw = 0; iw < output_width; iw++)
            {
                float sum = 0;
                for (int kc = 0; kc < KERNEL_CHANNEL; kc++)
                {
                    for (int kh = 0; kh < KERNEL_HEIGHT; kh++)
                    {
                        for (int kw = 0; kw < KERNEL_WIDTH; kw++)
                        {
                            int oh = ih * stride + kh;
                            int ow = iw * stride + kw;
                            sum += input[0][kc][oh][ow] * kernel[outc][kc][kh][kw];
                        }
                    }
                }
                output[0][outc][ih][iw] = sum;
            }
        }
    }

    vector<float> output_1d;
    for (int i = 0; i < OUTPUT_CHANNEL; i++)
    {
        for (int j = 0; j < output_height; j++)
        {
            for (int k = 0; k < output_width; k++)
            {
                output_1d.push_back(output[0][i][j][k]);
            }
        }
    }

    write_to_binary("cpp_filter_output.bin", output_1d);

    cout << "3D Convolution complete. Output written to 'cpp_filter_output.bin'." << endl;

    return 0;
}
