# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/11/27 
# @Function:
# 注意：导出和加载时torch版本要一致，不然会报错：file not found: traced_model_cpu/version
import shutil
from pathlib import Path

import torch
from transformers import AutoModel, AutoConfig, AutoTokenizer


def load_script_model(model_dir: Path, map_location="cpu"):
    """
    加载模型
    :param model_dir: 模型目录
    :param map_location: 绑定硬件
    :return:
    """
    pt_file = None
    bin_file = None
    model = None
    tokenizer = None
    state_dict = None
    for file in model_dir.glob("*.pt"):
        pt_file = file
        break
    for file in model_dir.glob("*.bin"):
        bin_file = file
    if pt_file:
        # 加载模型
        model = torch.jit.load(pt_file, map_location=map_location)
    if bin_file:
        # 加载模型权重
        state_dict = torch.load(bin_file, map_location=map_location)
    try:
        # 加载tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
    except Exception as e:
        pass
    model.eval()
    return model, tokenizer, state_dict


def convert_script_model(model_dir: Path, export_dir: Path, device="cpu", example_inputs=None, **kwargs):
    """
    转torchScript
    :param model_dir: 训练模型目录，包含bin文件、config.json
    :param export_dir: 导出模型目录
    :param device: 绑定硬件, cpu|cuda:0|cuda:1
    :param example_inputs: 输入样例
    :param kwargs: 网络自定义参数
    :return:
    model, tokenizer, state_dict = load_script_model(Path(r"F:\torch\script"))
    fc = nn.Linear(768, 1, bias=True)
    fc.weight.data = torch_to_script.get_state_dict_v(state_dict, "fc.weight")
    """
    if not export_dir.exists():
        export_dir.mkdir(parents=True)
    config = AutoConfig.from_pretrained(pretrained_model_name_or_path=model_dir, **kwargs)
    model = AutoModel.from_pretrained(model_dir, config=config)
    is_use_gpu = False if device == "cpu" else True
    if is_use_gpu:
        model = model.to(device)
    traced_model = torch.jit.trace(model, example_inputs=example_inputs, strict=False)
    if is_use_gpu:
        torch.jit.save(traced_model, export_dir.joinpath("traced_model_gpu.pt"))
    else:
        torch.jit.save(traced_model, export_dir.joinpath("traced_model_cpu.pt"))
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


def convert_bert_demo():
    """
    转换示例：以bert转torchScript为例
    :return:
    """

    def example_inputs(device="cpu"):
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

    """
    以bert为例：
    example_inputs       输入样例
    output_hidden_states 输出隐藏层
    output_attentions    输出意力层
    """
    convert_script_model(model_dir=Path(r"F:\torch\train_model"),
                         export_dir=Path(r"F:\torch\script"),
                         device="cpu", example_inputs=example_inputs(),
                         torchscript=True, use_cache=False, output_hidden_states=True, output_attentions=True)


def get_state_dict_v(state_dict: dict, state_name: str):
    """
    根据名称获取权重值
    :param state_dict: 权重字典
    :param state_name: 名称
    :return:
    """
    for name in state_dict:
        if name == state_name:
            return state_dict.get(name)
    return None


if __name__ == "__main__":
    convert_bert_demo()
    # model, tokenizer, state_dict = load_script_model(Path(r"F:\torch\script"))
    # fc_weight = get_state_dict_v(state_dict, "fc.weight")
    # print(fc_weight)
