import ctypes
import sys
import os

# GPU 사용 가능 여부 확인 tensorflow
def tf_gpu():
    import tensorflow as tf
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
      try:
        # GPU 사용 설정
        for gpu in gpus:

          print(gpu)
          tf.config.experimental.set_memory_growth(gpu, True)
        tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
      except RuntimeError as e:
        print(e)

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
