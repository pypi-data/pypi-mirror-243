# --encoding:utf-8--

import os
import configparser

current_env = os.getenv("ENV")
config = configparser.ConfigParser()
parentDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file_name = "/config.ini"
if current_env == "PRO":
    config_file_name = "/config-pro.ini"
elif current_env == "TENCENT":
    config_file_name = "/config-tencent.ini"
with open(parentDirPath + config_file_name, "r") as config_file:
    config.readfp(config_file)


class ConfigReader:
    def __init__(self):
        return

    @staticmethod
    def get_value(schema, key):
        return config.get(schema, key)

    @staticmethod
    def get_value(schema, key):
        return config.get(schema, key)

    @staticmethod
    def get_global_value(self, key):
        return config.get('global', key)