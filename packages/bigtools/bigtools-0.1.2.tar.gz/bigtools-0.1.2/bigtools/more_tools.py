# -*- coding: UTF-8 -*-
# @Time : 2023/9/27 17:50 
# @Author : 刘洪波
import socket
import os
import time
from jsonschema import validate
from bigtools.yaml_tools import load_yaml


def extract_ip():
    """获取机器ip"""
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        ip = st.getsockname()[0]
    except Exception as e:
        print(e)
        ip = ''
    finally:
        st.close()
    return ip


def get_file_size(file_path):
    """
    获取文件大小
    :param:  file_path:文件路径（带文件名）
    :return: file_size：文件大小
    """
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    else:
        return 0


def equally_split_list_or_str(list_or_str: list or str, num: int):
    """
    将一个list 或 str 按长度num均分
    :param list_or_str:
    :param num:
    :return:
    """
    return [list_or_str[i*num:(i+1)*num] for i in range(int(len(list_or_str)/num) + 1) if list_or_str[i*num:(i+1)*num]]


def json_validate(schema, json_data):
    """
    验证json是否是模板规定的格式
    :param schema: 模板
    :param json_data:
    :return:
    """
    result = True
    error = None
    try:
        validate(instance=json_data, schema=schema)
    except Exception as e:
        error = e
        result = False
        print(e)
    return result, error


def load_config(config_dir: str):
    """
    获取配置
    PYTHON_CONFIG 默认值是 dev  其他值有 prod test
    :param config_dir: 配置文件存储的文件夹
    :return: dict
    """
    config_path = os.path.join(config_dir, os.getenv('PYTHON_CONFIG', 'dev') + '.yaml')
    if os.path.exists(config_path):
        return load_yaml(config_path)
    raise ValueError(f'Path not found: {config_path}')


def set_env(env_dict: dict):
    """设置环境变量"""
    for k, v in env_dict.items():
        os.environ[k] = v


def load_env(envs):
    """
    获取环境变量
    :param envs:  type 可以是 list 也可以是 dict, 也可是 [str, str, {k:v, k2:v2}]
    :return:
    """
    if isinstance(envs, list):
        env = {}
        for i in envs:
            if isinstance(i, str):
                env[i] = os.getenv(i)
            elif isinstance(i, dict):
                for k, v in i.items():
                    env[k] = os.getenv(k, v)
            else:
                raise ValueError(f'type is error: item is {i}, the type of item can only be str or dict')
        return env
    elif isinstance(envs, dict):
        return {k: os.getenv(k, v) for k, v in envs.items()}
    else:
        raise ValueError('type is error: the type of envs can only be list or dict')


def get_func_use_time(func):
    def inner(*arg, **kwarg):
        s_time = time.time()
        res = func(*arg, **kwarg)
        e_time = time.time()
        print(f'Time required: {e_time - s_time} seconds')
        return res

    return inner
