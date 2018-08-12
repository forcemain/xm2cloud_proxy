#! -*- utf-8 -*-


import os


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_proxy_dir():
    return os.path.dirname(get_base_dir())
