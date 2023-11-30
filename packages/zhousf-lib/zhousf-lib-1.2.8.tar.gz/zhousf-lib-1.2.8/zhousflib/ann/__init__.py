# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/11/27 
# @Function: 人工神经网络
import torch


def check_cuda():
    assert torch.cuda.is_available(), 'torch.cuda is not available, please check device_id.'


def check_device_id(device_id: int = -1):
    """
    :param device_id: cpu上运行：-1 | gpu上运行：0 or 1 or 2...
    :return:
    """
    assert device_id >= -1, 'Expected device_id >= 1, but device_id={0}.'.format(device_id)


def get_device(device_id: int = -1):
    """
    :param device_id: cpu上运行：-1 | gpu上运行：0 or 1 or 2...
    :return:
    """
    check_device_id(device_id)
    if device_id == -1:
        map_location = torch.device('cpu')
    else:
        check_cuda()
        map_location = torch.device("cuda:{0}".format(device_id))
    """
    Map tensors from GPU 1 to GPU 0
    map_location={'cuda:1': 'cuda:0'}
    https://pytorch.org/docs/stable/generated/torch.load.html
    """
    return map_location
