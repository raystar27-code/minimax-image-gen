---
name: minimax-image-gen
description: 使用 MiniMax API 根据文本描述生成单张或多张图像，支持风格、比例、种子及自定义分辨率。
---

# MiniMax 图像生成 (MiniMax Image Generation)

## 概述
调用 MiniMax 的 `image-01` 或 `image-01-live` 模型，支持多比例、批量化及风格化图像生成。

## 各场景调用示例

### 1. 基础快速生成
```bash
python minimax_gen.py --prompt "一只正在喝咖啡的企鹅" --aspect_ratio 16:9
```

### 2. 多比例同步生成 (多张图)
```bash
python minimax_gen.py --prompt "赛博朋克风格上海" --aspect_ratio 4:3 3:4 16:9
```

### 3. 风格化批量生成 (限 Live 模型)
使用“漫画”风格生成 2 张图片：
```bash
python minimax_gen.py --prompt "雨夜中的老街" --model image-01-live --style "漫画" --n 2
```

### 4. 精确控制 (固定种子与关闭优化)
```bash
python minimax_gen.py --prompt "..." --seed 12345 --no_optimizer
```

## 输入参数说明

| 参数 | 说明 | 默认值 | 备注 |
| :--- | :--- | :--- | :--- |
| `--prompt` | **(必填)** 图像内容描述 | 无 | 支持中英文 |
| `--aspect_ratio` | 图像比例列表 | `1:1` | 支持多值。如果选了比例，宽高设置失效。 |
| `--model` | 使用模型 | `image-01` | `image-01` (高质), `image-01-live` (极速) |
| `--n` | 单次请求生成的数量 | `1` | 范围 1-9。 |
| `--style` | 画风设定 | 无 | **仅限 `image-01-live`**。可选：`漫画`, `元气`, `中世纪`, `水彩` |
| `--style_weight` | 风格权重 | `0.8` | 范围 (0, 1]。 |
| `--seed` | 随机种子 | 无 | 用于复现结果 |
| `--width` / `--height` | 自定义分辨率 | 无 | **仅限 `image-01`**。需 512-2048 且为 8 倍数。 |
| `--no_optimizer` | 关闭提示词自动优化 | 默认开启 | 开启后 API 会自动润色你的提示词 |
| `--output_dir` | 保存目录 | `./outputs` | 默认为脚本所在目录的 outputs 文件夹 |

## 输出处理
脚本会在控制台打印所有生成结果的本地绝对路径：
```text
RESULT_FILE_PATH: /path/to/outputs/gen_1.png
RESULT_FILE_PATH: /path/to/outputs/gen_2.png
```
OpenClaw 应当识别并解析所有以 `RESULT_FILE_PATH:` 开头的行。
