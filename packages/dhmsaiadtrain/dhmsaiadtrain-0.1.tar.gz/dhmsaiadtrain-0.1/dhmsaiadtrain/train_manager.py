# 德姆斯AI告警主训练程序
# coded by Daijie Bao 

# Import necessary packages for training
import os
import tensorflow as tf
from GPU_manager import GPU_manager
from device_info_reader import device_info_reader
from sampling_preprocess import sampling_preprocess
from DHMS_AI_Alert_Model import DHMS_AI_Alert

# 创建训练主程序
def main(path_to_data: str, path_to_info: str, path_to_model: str, path_to_scaler: str, path_to_anomaly_threshold: str):
    """
    主程序

    :param path_to_data: 本地训练数据输入文件夹路径
    :param path_to_info: metric和device id对应关系json文件输入路径
    :param path_to_model: 模型输出文件夹路径
    :param path_to_scaler: scaler输出文件夹路径
    :param path_to_anomaly_threshold: anomaly threshold的json文件输出文件夹路径

    :return: None
    """
    # Set the random seed for reproducibility
    seed_value = 42
    tf.random.set_seed(seed_value)

    # Check if a GPU is available and move the model training to GPU if available
    gpu_manager = GPU_manager()
    gpu_manager.enable_GPU_memory_growth() # Enable GPU memory growth for all GPUs

    # Read the device info from json file
    DeviceInfoReader = device_info_reader()

    # Read the device info from json file
    device_info_dict = DeviceInfoReader.read_json_to_dict(path_to_info)

    # Create a empty python dictionary to store the anomaly threshold for each device 
    anomaly_threshold_dict = {}

    for device_id, metric_list in device_info_dict.items():

        # define the path to the device folder
        device_folder_name = "download_" + device_id
        path_to_device_folder = os.path.join(path_to_data, device_folder_name)

        # Sort the metric list for building training dataset 
        sorted_metric_list= sorted(metric_list, key=lambda metric: int(metric.split("x.")[1]))

        # Create a sampling preprocess class
        sampling_manager = sampling_preprocess(path_to_device_folder, device_id)

        # Set the limit of training dataset 
        file_num_list = sampling_manager.build_data_file_num_list()
        # Count the file num
        fn_counter, fn_list = sampling_manager.file_num_counter(file_num_list)
        limit = min(fn_list)/12
        print("The limit of training dataset for device"+ device_id + " is: ", limit)

        # check the sampling rate for each metric
        length_list = sampling_manager.build_length_list()
        # Count the sampling rate
        sr_counter, sr_info = sampling_manager.sampling_rate_counter(length_list, sorted_metric_list)

        # Initialize the model creator class
        model_creator = DHMS_AI_Alert(path_to_device_folder, path_to_model, path_to_scaler, device_id, sorted_metric_list)

        # Building training dataset 
        train_dataset = model_creator.build_training_dataset_with_limit(limit, sr_info)
        print("Here is the training dataset overview for this device ", train_dataset.head())
        print("The shape of the training dataset: ", train_dataset.shape)

        # Preprocess the data
        reshape_train_data= model_creator.preprocess_data(train_dataset, 1)
        print('The shape of the reshaped training dataset for this device: ', reshape_train_data.shape)
        print('The type of the reshaped training dataset for this device: ', type(reshape_train_data))

        # Build the model
        model = model_creator.build_two_layers_alert_model(reshape_train_data, 64, 0.2,'adagrad', 'mse')

        # Train the model
        history = model_creator.train_model(model, reshape_train_data, 50, 16384, 0.05)

        # Plot the training history
        model_creator.plot_training_history(history)

        # Save the model
        model_location_path = model_creator.save_model(model)

        # Reconstruct the training data 
        train_prediction, train_data = model_creator.reconstruct_training_data(model_location_path, reshape_train_data)
        print('Training data shape: ', train_data.shape)
        print('Training prediction shape: ', train_prediction.shape)
        print('The type of train_data: ', type(train_data))
        print('The type of train_prediction: ', type(train_prediction))

        # calculate the anomaly threshold for the device 
        threshold = model_creator.calculate_anomaly_threshold(train_prediction, train_data)
        print('Anomaly threshold for this device: ', threshold)  

        # Save the anomaly threshold for this device to the dictionary
        anomaly_threshold_dict[device_id] = threshold

    # Save the anomaly threshold dictionary to json file
    DeviceInfoReader.save_dict_to_json(anomaly_threshold_dict, path_to_anomaly_threshold)

    print("Training is done.")

    return None 

# 创建调用主程序的函数接口
def train(path_to_data: str, path_to_info: str, path_to_model: str, path_to_scaler: str, path_to_anomaly_threshold: str):
    """
    调用主程序的函数接口

    :param path_to_data: 本地训练数据输入文件夹路径
    :param path_to_info: metric和device id对应关系json文件输入路径
    :param path_to_model: 模型输出文件夹路径
    :param path_to_scaler: scaler输出文件夹路径
    :param path_to_anomaly_threshold: anomaly threshold的json文件输出文件夹路径

    :return: None
    """
    
    # Call the main function
    main(path_to_data, path_to_info, path_to_model, path_to_scaler, path_to_anomaly_threshold)

    return None



