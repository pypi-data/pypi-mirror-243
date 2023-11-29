# device info reader class for AI Alert Model 
# 设备id和metric对应关系读取类
# coded by Daijie Bao

# Import necessary packages for reading device info
import json

# Create a class for device info reader
class device_info_reader():
    """
    设备信息读取器

    """
    def __init__(self):
        """
        初始化设备信息读取器
        """
        pass

    def read_json_to_dict(self, input_path):
        """
        从指定路径读取 JSON 文件，并将其转换为 Python 字典。

        :param input_path: JSON 文件的输入路径。
        :return: 从 JSON 文件中读取的字典。
        """
        try:
            with open(input_path, 'r') as file:

                return json.load(file)
            
        except FileNotFoundError:
            print(f"文件未找到: {input_path}")

            return None
        
        except json.JSONDecodeError:
            print(f"解析 JSON 时出错: {input_path}")

            return None

    def save_dict_to_json(self, data, output_path):
        """
        将 Python 字典保存为 JSON 文件到指定路径。

        :param data: 要保存的 Python 字典。
        :param output_path: JSON 文件的输出路径。
        """
        try:
            with open(output_path, 'w') as file:

                json.dump(data, file, indent=4)

            print(f"数据已成功保存到 {output_path}")

        except Exception as e:
            print(f"保存文件时出错: {e}")
