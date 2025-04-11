# import os
# import tensorflow as tf


print("TF version:", tf.__version__)
print("GPU Available:", tf.config.list_physical_devices('GPU'))
print("GPU Device:", tf.test.gpu_device_name())

# print(tf.__version__)

# print('1: ', tf.config.list_physical_devices('GPU'))
# print('2: ', tf.test.is_built_with_cuda)
# print('3: ', tf.test.gpu_device_name())
# print('4: ', tf.config.get_visible_devices())

# cuda_path = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin"

# files_to_check = ["cudart64_110.dll", "cudnn64_8.dll"]

# for f in files_to_check:
#     full_path = os.path.join(cuda_path, f)
#     print(f"{f}: {'✅ Found' if os.path.exists(full_path) else '❌ Not Found'}")

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))