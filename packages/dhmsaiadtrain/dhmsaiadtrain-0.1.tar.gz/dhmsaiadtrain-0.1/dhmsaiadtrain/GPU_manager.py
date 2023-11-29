# AI Alert Model Training GPU Manager
# GPU 管理器 
# Used for TensorFlow 2.0 or higher version
# Coded by: Daijie Bao

# Import necessary packages for training GPU Manager
import tensorflow as tf 

# Create a class for GPU Manager
class GPU_manager():
    """
    GPU管理器

    """
    def __init__(self):
        """
        初始化AI模型训练的GPU管理器及检查GPU可用性

        """

        self.gpus = tf.config.experimental.list_physical_devices('GPU')

        self.gpu_available = len(self.gpus) > 0 # Check if a GPU is available

        if not self.gpu_available:

            print("No GPUs available. Please check if you system has GPU available or Please install GPU version of TensorFlow")
        
        return None

    def check_gpu_availability(self):
        """
        检查可用GPU以及详细GPU信息
        """
        # Check if a GPU is available
        if self.gpu_available:

            print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))

            # Get the number of available GPUs
            print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
        
        else: 
            print("GPUs not available.")

        return None
    
    def enable_GPU_memory_growth(self, all_gpus=True):
        """
        启用GPU内存增长, 默认启用所有GPU内存增长

        """
        if self.gpu_available:
            try:
                if all_gpus:
                    for gpu in self.gpus:
                        tf.config.experimental.set_memory_growth(gpu, True)
                else:
                    tf.config.experimental.set_memory_growth(self.gpus[0], True)
                
                print("GPU memory growth enabled.")
            
            except RuntimeError as e:
                print(f"GPU memory growth cannot be set: {e}")

        else: 
            print("Memory growth cannot be set. GPUs not available.")
        
        return None 
    
    def set_gpu(self, gpu_id=0):
        """
        设置使用的GPU, 默认使用第一个GPU

        """
        if self.gpu_available and gpu_id < len(self.gpus):
            try:
                tf.config.experimental.set_visible_devices(self.gpus[gpu_id], 'GPU')
                print(f"Set GPU {gpu_id} for AI Model Training.")
            
            except RuntimeError as e:
                print(f"GPU {gpu_id} cannot be set for AI Model Training: {e}")
        
        else:
            print("Invalid GPU index or GPUs not available.")

    

    