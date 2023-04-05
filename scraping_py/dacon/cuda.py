import ctypes
import sys
import os

def test_cuda_and_cudnn():
    # Check for GPU
    try:
        import torch
        assert torch.cuda.is_available(), "No GPU detected"
        print(f"GPU Detected: {torch.cuda.get_device_name(0)}")
    except (ImportError, AssertionError) as e:
        print(e)
        sys.exit(1)

    # Check for CUDA
    try:
        libnames = ('libcuda.so', 'libcuda.dylib', 'nvcuda.dll')
        for libname in libnames:
            try:
                cuda = ctypes.CDLL(libname)
                print("CUDA detected")
                break
            except OSError:
                pass
        else:
            raise OSError("No CUDA library found")
    except OSError as e:
        print(e)
        sys.exit(1)

    # Check for cuDNN
    try:
        libnames = ('libcudnn.so', 'libcudnn.dylib', 'cudnn64_7.dll')
        for libname in libnames:
            try:
                cudnn = ctypes.CDLL(libname)
                print("cuDNN detected")
                break
            except OSError:
                pass
        else:
            raise OSError("No cuDNN library found")
    except OSError as e:
        print(e)
        sys.exit(1)

test_cuda_and_cudnn()