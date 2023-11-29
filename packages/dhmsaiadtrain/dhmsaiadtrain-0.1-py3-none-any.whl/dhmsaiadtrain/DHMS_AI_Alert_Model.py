# Model Training Script of DHMS AI Alert Service 
# Author: Daijie Bao 
# Date: 2023-06-09

# The model used for AI Alert Service is lstm-autoencoder model

# Import necessary packages
import os 
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from keras.layers import LSTM, RepeatVector, Dropout, TimeDistributed, Dense
from keras.models import Sequential, load_model
from keras.callbacks import EarlyStopping
from sklearn.decomposition import PCA
from read_util.read import read_local_file
import pickle

# Define the model training class
class DHMS_AI_Alert:
    """
    This is the model training class of DHMS AI Alert Service

    """
    def __init__(self, training_data_path: str, model_save_path: str, scaler_save_path: str, model_name: str, metric_list: list[str]):
        """
        This is the initialization function of the model training class

        :param training_data_path: the path of the training data
        :param model_save_path: the path to save the model
        :param scaler_save_path: the path to save the scaler
        :param model_name: the name of the model

        :return: None
        """
        self.training_data_path = training_data_path

        self.model_save_path = model_save_path

        self.scaler_save_path = scaler_save_path

        self.model_name = model_name

        self.metric_list = metric_list
    
    def convert_aiff_to_df_no_time_index(self, data_source: str):
        """
        Convert aiff vibration sensor data source to a pandas DataFrame without time index

        :param data_source: path to the aiff file on the local machine

        :return: a pandas DataFrame containing the converted data from the aiff file
        """
        src = read_local_file(data_source)

        data = src.data

        data_frame = pd.DataFrame(data, columns=['acceleration'])

        return data_frame
    
    # 降采样函数，将不同采样率的数据降采样为默认DHMS传感器数据采样点8192
    def down_sample_data_point(self, data: list, option: str):
        """
        Down sample the data point to default DHMS sensor data sample point which is 8192

        :param data: a list which contains the data to be down sampled
        :param option: the option to choose the down sample method

        :return: the down sampled data
        """
        assert len(data) % 8192 == 0, "Data length must be a multiple of 8192"

        # calculate the down sample factor
        factor = len(data) // 8192

        if option == "average":
            # 使用平均降采样法
            downsampled_data = [np.mean(data[i:i+factor]) for i in range(0, len(data), factor)]
        
        elif option == "extract":
            # 使用抽取法
            downsampled_data = data[::factor]
        
        elif option == "pca":
            # 重塑数据以适应PCA
            reshaped_data = np.array(data).reshape((-1, factor))
        
            # 使用PCA进行降采样
            pca = PCA(n_components=1)
            reduced_data = pca.fit_transform(reshaped_data)
        
            # 从PCA降采样结果中获取降采样数据
            downsampled_data = reduced_data.flatten().tolist()

        else:

            raise ValueError("Invalid option for down sample method.\n Invalid option. Choose from 'average', 'extract', or 'pca'.")
        
        return downsampled_data
    
    # Create a function to convert aiff to df by applying downsample data point.
    def convert_aiff_to_df_no_time_index_after_downsample(self, data_source: str, option: str):
        """
        Convert aiff vibration sensor data source to a pandas DataFrame without time index

        :param data_source: path to the aiff file on the local machine
        :param option: the option to choose the down sample method

        :return: a pandas DataFrame containing the converted data from the aiff file
        """
        src = read_local_file(data_source)

        data = src.data 

        # down sample the data
        downsampled_data = self.down_sample_data_point(data, option)

        # convert the down sampled data to a pandas DataFrame
        data_frame = pd.DataFrame(downsampled_data, columns=['acceleration'])

        return data_frame
    
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

        :return: a list of data length
        """
        device_length_list = []

        for folder in os.listdir(self.training_data_path):

            metric_length_list = []

            folder_path = os.path.join(self.training_data_path, folder)

            for filename in os.listdir(folder_path):

                file_path = os.path.join(folder_path, filename)

                length = self.get_data_length(file_path)

                metric_length_list.append(length)
            
            device_length_list.append(metric_length_list)

        return device_length_list
    
    def build_data_file_num_list(self):
        """
        Build a list of data file number

        :return: a list of data file number
        """
        device_data_file_num_list = []

        for folder in os.listdir(self.training_data_path):

            folder_path = os.path.join(self.training_data_path, folder)

            metric_file_num = len(os.listdir(folder_path))

            device_data_file_num_list.append([metric_file_num])

        return device_data_file_num_list

    def build_training_dataset_with_limit(self, limit: int, sr_info: dict):
        """
        Build the training dataset

        :return: a pandas DataFrame containing the training dataset
        """

        # Sort the sr_info based on actual folder location 
        sorted_sr_info = dict(sorted(sr_info.items(), key=lambda item: int(item[0].split('x.')[1])))

        dataset = []

        folder_list = os.listdir(self.training_data_path)

        folder_list.sort()

        for folder in folder_list:

            for metric, sr in sorted_sr_info.items():

                folder_path = os.path.join(self.training_data_path, folder)

                if sr == 8192: 

                    temp_data = []

                    file_list = os.listdir(folder_path)

                    file_list.sort()

                    for filename in file_list:

                        file_path = os.path.join(folder_path, filename)

                        data = self.convert_aiff_to_df_no_time_index(file_path)

                        temp_data.append(data)
                    
                    temp_data = pd.concat(temp_data, axis=0, ignore_index=True)

                    temp_data = temp_data.iloc[:limit]

                    dataset.append(temp_data)
                
                elif sr >= 8192 * 2 and sr % 8192 == 0:

                    temp_data = []

                    file_list = os.listdir(folder_path)

                    file_list.sort()

                    for filename in file_list:

                        file_path = os.path.join(folder_path, filename)

                        data = self.convert_aiff_to_df_no_time_index_after_downsample(file_path, 'pca')

                        temp_data.append(data)
                    
                    temp_data = pd.concat(temp_data, axis=0, ignore_index=True)

                    temp_data = temp_data.iloc[:limit]

                    dataset.append(temp_data)
        
        datasets = pd.concat(dataset, axis=1)

        datasets.columns = self.metric_list

        return datasets
    
    def build_training_dataset_without_limit(self, sr_info: dict):
        """
        Build the training dataset

        :return: a pandas DataFrame containing the training dataset
        """

        # Sort the sr_info based on actual folder location 
        sorted_sr_info = dict(sorted(sr_info.items(), key=lambda item: int(item[0].split('x.')[1])))

        dataset = []

        folder_list = os.listdir(self.training_data_path)

        folder_list.sort()

        for folder in folder_list:

            for metric, sr in sorted_sr_info.items():

                folder_path = os.path.join(self.training_data_path, folder)

                if sr == 8192: 

                    temp_data = []

                    file_list = os.listdir(folder_path)

                    file_list.sort()

                    for filename in file_list:

                        file_path = os.path.join(folder_path, filename)

                        data = self.convert_aiff_to_df_no_time_index(file_path)

                        temp_data.append(data)
                    
                    temp_data = pd.concat(temp_data, axis=0, ignore_index=True)

                    temp_data = temp_data.iloc

                    dataset.append(temp_data)
                
                elif sr >= 8192 * 2 and sr % 8192 == 0:

                    temp_data = []

                    file_list = os.listdir(folder_path)

                    file_list.sort()

                    for filename in file_list:

                        file_path = os.path.join(folder_path, filename)

                        data = self.convert_aiff_to_df_no_time_index_after_downsample(file_path, 'pca')

                        temp_data.append(data)
                    
                    temp_data = pd.concat(temp_data, axis=0, ignore_index=True)

                    temp_data = temp_data.iloc

                    dataset.append(temp_data)
        
        datasets = pd.concat(dataset, axis=1)

        datasets.columns = self.metric_list

        return datasets

    def preprocess_data(self, data: pd.DataFrame, sequence_length: int, metric_name=None):
        """
        Scale the dataset and reshape it to the format that can be input for deep learning alert model prediction.

        :param data: a pandas DataFrame which is the dataset for deep learning alert model prediction

        :return: the reshaped dataset
        """
        if metric_name is not None:
            
            scaler = MinMaxScaler()

            scaled_data = scaler.fit_transform(data)

            reshaped_data = scaled_data.reshape(int(scaled_data.shape[0]/sequence_length), sequence_length, scaled_data.shape[1])

            # Assuming you already have 'scaler' fitted on the training data
            scaler_filename = 'de_'+ self.model_name +'_'+ metric_name +'.pkl'

            with open(os.path.join(self.scaler_save_path, scaler_filename), 'wb') as f:
            
                pickle.dump(scaler, f)

            print("The scaler parameters are saved as" + scaler_filename + ".")
        
        else:

            scaler = MinMaxScaler()

            scaled_data = scaler.fit_transform(data)

            reshaped_data = scaled_data.reshape(int(scaled_data.shape[0]/sequence_length), sequence_length, scaled_data.shape[1])

            # Assuming you already have 'scaler' fitted on the training data
            scaler_filename = 'de_'+ self.model_name +'.pkl'

            with open(os.path.join(self.scaler_save_path, scaler_filename), 'wb') as f:
            
                pickle.dump(scaler, f)

            print("The scaler parameters are saved as" + scaler_filename + ".")

        return reshaped_data
    
    def build_two_layers_alert_model(self, training_data: pd.DataFrame, lstm_units: int, dropout_rate: float, optimizer: str, loss: str):
        """
        Build the lstm-autoencoder model

        :param training_data: the training dataset
        :param lstm_units: the number of lstm units
        :param dropout_rate: the dropout rate
        :param optimizer: the optimizer
        :param loss: the loss function

        :return: the lstm-autoencoder model
        """
        model = Sequential([

            LSTM(lstm_units, activation='relu', input_shape=(training_data.shape[1],training_data.shape[2])),

            Dropout(dropout_rate),

            RepeatVector(training_data.shape[1]),

            LSTM(lstm_units, activation='relu', return_sequences=True),

            Dropout(dropout_rate),

            TimeDistributed(Dense(training_data.shape[2]))])
        
        model.compile(optimizer=optimizer, loss=loss)

        model.summary()

        return model
    
    def build_four_layers_alert_model(self, training_data: pd.DataFrame, lstm_units: int, dropout_rate: float, optimizer: str, loss: str):
        """
        Build the lstm-autoencoder model

        :param training_data: the training dataset
        :param lstm_units: the number of lstm units
        :param dropout_rate: the dropout rate
        :param optimizer: the optimizer
        :param loss: the loss function

        :return: the lstm-autoencoder model
        """
        model = Sequential([

            LSTM(lstm_units, activation='relu', input_shape=(training_data.shape[1],training_data.shape[2]), return_sequences=True),

            LSTM(lstm_units, activation='relu', return_sequences = False),

            Dropout(dropout_rate),

            RepeatVector(training_data.shape[1]),

            LSTM(lstm_units, activation='relu', return_sequences=True),

            LSTM(lstm_units, activation='relu', return_sequences=True),

            Dropout(dropout_rate),

            TimeDistributed(Dense(training_data.shape[2]))])
        
        model.compile(optimizer=optimizer, loss=loss)

        model.summary()

        return model  

    def train_model(self, model, training_data, epochs, batch_size, validation_split):
        """
        Train the lstm-autoencoder model

        :param model: the lstm-autoencoder model
        :param training_data: the training dataset
        :param epochs: the number of epochs
        :param batch_size: the batch size
        :param validation_split: the validation split

        :return: the training history
        """
        history = model.fit(training_data, training_data, epochs=epochs, batch_size=batch_size, 
                            
                            validation_split=validation_split, callbacks=[EarlyStopping(monitor='val_loss', patience=5, mode='min')])

        return history
    
    def reconstruct_training_data(self, model_load_path: str, training_data: np.ndarray):
        """
        Reconstruct the training data using the trained lstm-autoencoder model

        :param model_load_path: the path to load the trained lstm-autoencoder model
        :param training_data: the training dataset

        :return: the reconstructed training data
        """
        # load the model from model load path
        model = load_model(model_load_path)

        # get the reconstructed training data
        train_predictions = model.predict(training_data)

        # Reshape both training data and reconstructed training data to 2D array
        training_data = training_data.reshape(int(training_data.shape[0]*training_data.shape[1]), training_data.shape[2])
        train_predictions = train_predictions.reshape(int(train_predictions.shape[0]*train_predictions.shape[1]), train_predictions.shape[2])

        return train_predictions, training_data

    # Create a function to get machine anomaly data indices for entire machine
    def calculate_anomaly_threshold(self, predict: np.ndarray, real_dataset: np.ndarray):
        """
        This function is used to get machine anomaly data indices for entire sensor
        :param predict: The predicted normal data which reconstructed from autoencoder
        :param real_dataset: The real normal data which used to train autoencoder
        :return: The machine anomaly data indices for entire sensor
        """
        mse_set, threshold_set = [], []

        for i in range(real_dataset.shape[1]):

            mse_set.append([])

            for j in range(real_dataset.shape[0]):

                mse = np.mean(np.square(predict[j, i] - real_dataset[j, i]))

                mse_set[i].append(mse)
            
            threshold = np.percentile(mse_set[i], 95)

            threshold_set.append(threshold)

        threshold_value = max(threshold_set)
    
        return threshold_value

    def plot_training_history(self, history):
        """
        Plot the training history

        :param history: the training history

        :return: None
        """
        plt.plot(history.history['loss'], label='Training loss')

        plt.plot(history.history['val_loss'], label='Validation loss')

        plt.legend(loc='upper right')

        plt.xlabel('Epochs')

        plt.ylabel('Loss [mse]')

        plt.show()

        return None
    
    def save_model(self, model):
        """
        Save the model

        :param model: the lstm-autoencoder model

        :return: the path to save the model
        """
        name = 'de_'+ self.model_name + '.h5'

        model_location_path = os.path.join(self.model_save_path, name)

        model.save(model_location_path)

        return model_location_path
