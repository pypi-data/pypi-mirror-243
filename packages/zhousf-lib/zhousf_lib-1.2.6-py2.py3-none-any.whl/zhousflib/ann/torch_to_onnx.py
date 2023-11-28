# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/11/27 
# @Function:
# 注意onnxruntime与opset版本的对应关系
# pip install torch -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# pip install transformers -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# pip install onnxruntime==1.14.1 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# pip install onnxruntime-gpu -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
import shutil
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
    ort_session, _, _ = load_onnx(model_dir=Path(r"F:\torch\onnx"))
    ort_input = ort_session.get_inputs()
    args = example_inputs_demo()
    ort_inputs = {ort_input[0].name: to_numpy(args[0]),
                  ort_input[1].name: to_numpy(args[1]),
                  ort_input[2].name: to_numpy(args[2])}
    ort_outs = ort_session.run(None, ort_inputs)
    print(ort_outs)
    """
    onnx_file = None
    bin_file = None
    tokenizer = None
    state_dict = None
    for file in model_dir.glob("*.onnx"):
        onnx_file = file
        break
    if device_id == -1:
        session = onnxruntime.InferenceSession(str(onnx_file))
    else:
        session = onnxruntime.InferenceSession(str(onnx_file), providers=['CUDAExecutionProvider'], provider_options=[{'device_id': device_id}])
    for file in model_dir.glob("*.bin"):
        bin_file = file
    if bin_file:
        # 加载模型权重
        if device_id == -1:
            map_location = "cpu"
        else:
            map_location = "cuda:{0}".format(device_id)
        state_dict = torch.load(bin_file, map_location=map_location)
    try:
        # 加载tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
    except Exception as e:
        pass
    return session, tokenizer, state_dict


def convert_onnx(model_dir: Path, export_dir: Path, example_inputs=None, module: torch.nn.Module = None, **kwargs):
    """
    导出onnx
    :param model_dir: 模型目录
    :param export_dir: 导出目录
    :param example_inputs: 输入示例
    :param module: 神经网络
    :param kwargs: 自定义参数
    :return:
    """
    if not export_dir.exists():
        export_dir.mkdir(parents=True)
    if module is None:
        config = AutoConfig.from_pretrained(pretrained_model_name_or_path=model_dir)
        model = AutoModel.from_pretrained(model_dir, config=config)
    else:
        model = module
    torch.onnx.export(model, example_inputs, export_dir.joinpath("model.onnx"), **kwargs)
    # 权重文件，这个是给预测的后处理模块初始化权重文件做准备
    for bin_file in model_dir.glob("*.bin"):
        shutil.copy(bin_file, export_dir)
    # tokenizer文件，这个是给预测的input data做准备
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        tokenizer.save_pretrained(export_dir)
    except Exception as e:
        pass
    print("done.")


def example_inputs_demo(device="cpu", input_size=10, batch_size=128):
    """
    输入样例
    :return:
    """
    ids = torch.LongTensor(input_size, batch_size).zero_()
    seq_len = torch.LongTensor(input_size, batch_size).zero_()
    mask = torch.LongTensor(input_size, batch_size).zero_()
    if device == "cpu":
        return [ids, seq_len, mask]
    else:
        return [ids.cuda(), seq_len.cuda(), mask.cuda()]


def convert_bert_demo():
    """
    转换示例：以bert转onnx为例
    :return:
    """
    convert_onnx(model_dir=Path(r"F:\torch\train_model"),
                 export_dir=Path(r"F:\torch\onnx"),
                 example_inputs=(example_inputs_demo(device="cpu"), ),
                 verbose=True,
                 export_params=True,
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
    convert_bert_demo()
    # ort_session, _, _ = load_onnx(model_dir=Path(r"F:\torch\onnx"))
    # ort_input = ort_session.get_inputs()
    # args = example_inputs_demo()
    # ort_inputs = {ort_input[0].name: to_numpy(args[0]),
    #               ort_input[1].name: to_numpy(args[1]),
    #               ort_input[2].name: to_numpy(args[2])}
    # options = onnxruntime.RunOptions()
    # ort_outs = ort_session.run(None, ort_inputs, run_options=options)
    # print(ort_outs)

