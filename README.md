# Convolution Implementation in C++ 
The repository contains convolution implementation in C++. The python script is used for validation

## Machine Requirements:
- Processor Architecture: x86_64
- RAM: Minimum 8GB
- OS: Ubuntu 20.04 
- Storage: Minimum 64GB

## Prequisites
* G++ (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0
* cmake version 3.29.3
* GNU Make 4.2.1
* Python 3.10.12 (create venv)

## Cloning the repo
Use the command below to clone the repo
```
    git clone https://github.com/Sanjay-JY/Convolution.git
    cd Convolution
```
## Activate python environment
```
source path_to_python_env/bin/activate
pip install -r requirements.txt
```

## How to Build and Run
To run conv2d
```
    sh run_conv2d.sh
```
To run conv3d
```
    sh run_conv3d.sh
```
To run conv3x3x64x128
```
    sh run_conv3x3x64x128.sh
```
To run conv in NHWC
```
    sh run_conv_nhwc.sh
```