# Sampling Preprocess manager of DHMS AI Alert Service
# Author: Daijie Bao
# Date: 2023-06-09

# Import necessary libraries
import os 
from read_util.read import read_local_file

class sampling_preprocess: 
    """
    Sampling Preprocess Class for AI Alert Service

    """
    def __init__(self, main_folder_path: str, device_id: str):
        """
        Initialize the sampling preprocess class

        :param main_folder_path: the path to the main folder
        :param device_id: the device id

        :return: None
        """
        self.main_folder_path = main_folder_path

        self.device_id = device_id

    def get_data_length(self, data_source: str):
        """
        Get the length of the data

        :param data_source: path to the aiff file on the local machine

        :return: the length of the data
        """
        src = read_local_file(data_source)

        length = src.length

        return length
    
    def build_length_list(self):
        """
        Build a list of data length

        :return: a list of data length and a dict with key as metric name and value as data length
        """
        device_length_list = []

        folder_list = os.listdir(self.main_folder_path)

        # Sort the folder order by default location in the system
        folder_list.sort()

        for folder in folder_list:

            if folder.startswith(self.device_id) and not folder.endswith('.txt'):

                metric_length_list = []

                folder_path = os.path.join(self.main_folder_path, folder)

                file_list = os.listdir(folder_path)

                # Sort the file order by default location in the system
                file_list.sort()

                for filename in file_list:

                    file_path = os.path.join(folder_path, filename)

                    length = self.get_data_length(file_path)

                    metric_length_list.append(length)
            
                device_length_list.append(metric_length_list)
            
            else: 

                continue

        return device_length_list
    
    def build_data_file_num_list(self):
        """
        Build a list of data file number

        :return: a list of data file number
        """
        device_data_file_num_list = []

        folder_list = os.listdir(self.main_folder_path)

        # Sort the folder order by default location in the system
        folder_list.sort()

        for folder in folder_list:

            if folder.startswith(self.device_id) and not folder.endswith('.txt'):

                folder_path = os.path.join(self.main_folder_path, folder)

                metric_file_num = len(os.listdir(folder_path))

                device_data_file_num_list.append([metric_file_num])
            
            else: 

                continue

        return device_data_file_num_list
    
    def sampling_rate_counter(self, sampling_rate_set: list, metric_list: list):
        """
        Count the number of unique sampling frequencies

        :param sampling_rate_set: a list of sampling frequencies

        :return: the number of unique sampling frequencies and a list of unique sampling frequencies
        """
        unique_sampling_rates = set()

        for sampling_rate in sampling_rate_set:

            unique_sampling_rates.update(sampling_rate)

        count = len(unique_sampling_rates)

        sampling_rate_list = list(unique_sampling_rates)

        sampling_info = {}

        for sampling_rate, metric in zip(sampling_rate_list, metric_list):

            metric = self.device_id + '_' + metric

            sampling_info[metric] = sampling_rate

        return count, sampling_info
    
    def group_sampling_rate(self, sampling_rate_info: dict):
        """
        Group the sampling rate by their common value

        :param sampling_rate_info: a dict with key as metric name and value as sampling rate

        :return: a list of sampling rate grouped by their common value
        """
        # Create an inverse dictionary where keys are original values and values are lists of original keys.
        inv_map = {}

        for key, value in sampling_rate_info.items():

            inv_map.setdefault(value, []).append(key)

        # Return lists of keys grouped by their common value.
        return [key_group for key_group in inv_map.values()]

    
    def file_num_counter(self, device_data_file_num_list: list):
        """
        Count the number of unique file numbers

        :param device_data_file_num_list: a list of file numbers

        :return: the number of unique file numbers and a list of unique file numbers
        """
        unique_file_num = set()

        for file_num in device_data_file_num_list:

            unique_file_num.update(file_num)
        
        count = len(unique_file_num)

        return count, list(unique_file_num)
        
        
