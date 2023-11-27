# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/11/27 
# @Function:  
# 注意onnxruntime与opset版本的对应关系
# pip install torch -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# pip install transformers -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# pip install onnxruntime==1.14.1 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# pip install onnxruntime-gpu -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
from pathlib import Path

import torch
import onnxruntime
from transformers import AutoModel, AutoConfig, AutoTokenizer


def load_onnx(model_dir: Path, device_id: int = -1):
    """
    加载onnx模型
    :param model_dir: 模型目录
    :param device_id: 绑定硬件
    :return:
    ort_session = load_onnx(model_dir=Path(r"F:\torch\onnx"))
    ort_input = ort_session.get_inputs()
    args = example_inputs_demo()
    ort_inputs = {ort_input[0].name: to_numpy(args[0]),
                  ort_input[1].name: to_numpy(args[1]),
                  ort_input[2].name: to_numpy(args[2])}
    ort_outs = ort_session.run(None, ort_inputs)
    print(ort_outs)
    """
    onnx_file = None
    for file in model_dir.glob("*.onnx"):
        onnx_file = file
        break
    if device_id == -1:
        session = onnxruntime.InferenceSession(str(onnx_file))
    else:
        session = onnxruntime.InferenceSession(str(onnx_file), providers=['CUDAExecutionProvider'], provider_options=[{'device_id': device_id}])
    return session


def convert_onnx(model_dir: Path, export_dir: Path, example_inputs=None, **kwargs):
    """
    导出onnx
    :param model_dir: 模型目录
    :param export_dir: 导出目录
    :param example_inputs: 输入示例
    :param kwargs: 自定义参数
    :return:
    """
    if not export_dir.exists():
        export_dir.mkdir(parents=True)
    config = AutoConfig.from_pretrained(pretrained_model_name_or_path=model_dir)
    model = AutoModel.from_pretrained(model_dir, config=config)
    torch.onnx.export(model, example_inputs, export_dir.joinpath("model.onnx"), **kwargs)
    print("done.")


def example_inputs_demo(device="cpu"):
    """
    输入样例
    :return:
    """
    input_size = 10
    batch_size = 128
    ids = torch.LongTensor(input_size, batch_size).zero_()
    seq_len = torch.LongTensor(input_size, batch_size).zero_()
    mask = torch.LongTensor(input_size, batch_size).zero_()
    if device == "cpu":
        return ids, seq_len, mask,
    else:
        return ids.cuda(), seq_len.cuda(), mask.cuda(),


def convert_bert_demo():
    """
    转换示例：以bert转onnx为例
    :return:
    """
    convert_onnx(model_dir=Path(r"F:\torch\train_model"),
                 export_dir=Path(r"F:\torch\onnx"),
                 example_inputs=example_inputs_demo(device="cpu"),
                 verbose=True,
                 opset_version=11,
                 input_names=['input_ids', 'token_type_ids', 'attention_mask'],
                 output_names=['output'],
                 dynamic_axes={'input_ids': {0: 'batch_size'},
                               'token_type_ids': {0: 'batch_size'},
                               'attention_mask': {0: 'batch_size'},
                               'output': {0: 'batch_size'}}
                 )


def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


if __name__ == "__main__":
    # convert_bert_demo()
    ort_session = load_onnx(model_dir=Path(r"F:\torch\onnx"))
    ort_input = ort_session.get_inputs()
    args = example_inputs_demo()
    ort_inputs = {ort_input[0].name: to_numpy(args[0]),
                  ort_input[1].name: to_numpy(args[1]),
                  ort_input[2].name: to_numpy(args[2])}
    ort_outs = ort_session.run(None, ort_inputs)
    print(ort_outs)

