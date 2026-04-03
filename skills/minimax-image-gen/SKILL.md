---
name: minimax-image-gen
description: 使用 MiniMax API 根据文本描述生成单张或多张图像，支持风格、比例、种子及自定义分辨率。
---

# MiniMax 图像生成 (MiniMax Image Generation)

## 概述
调用 MiniMax 的 `image-01` 或 `image-01-live` 模型，进行多功能生图。

## 各场景调用示例

### 1. 基础快速生成
```bash
python3 skills/minimax-image-gen/minimax_gen.py --prompt "一只正在喝咖啡的企鹅"
```

### 2. 多比例同步生成 (多张图)
```bash
python3 skills/minimax-image-gen/minimax_gen.py --prompt "赛博朋克风格上海" --aspect_ratio 4:3 3:4 16:9
```

### 3. 进阶功能调用
```bash
python3 skills/minimax-image-gen/minimax_gen.py --prompt "雨夜中的老街" --model image-01-live --style "漫画" --n 2
```

## 安装与配置
1. **安装依赖**：
   ```bash
   pip install -r skills/minimax-image-gen/requirements.txt
   ```
2. **配置秘钥**：
   确保 `skills/minimax-image-gen/.env` 文件中包含：
   ```text
   MINIMAX_API_KEY=你的_API_KEY
   ```

## 输入参数说明
| 参数 | 说明 | 默认值 | 备注 |
| :--- | :--- | :--- | :--- |
| `--prompt` | **(必填)** 图像内容描述 | 无 | 支持中英文 |
| `--aspect_ratio` | 图像比例列表 | `4:3` | 支持多值。 |
| `--model` | 使用模型 | `image-01` | `image-01` / `image-01-live` |
| `--n` | 生成数量 | `1` | 1-9 |
| `--style` | 画风设定 | 无 | 仅限 Live 模型：`漫画`, `元气`, `中世纪`, `水彩` |
| `--style_weight` | 风格权重 | `0.8` | (0, 1] |
| `--output_dir` | 保存目录 | 项目根目录/outputs | 脚本会自动处理 |

## 输出处理
脚本会在控制台打印所有生成结果的本地绝对路径：
```text
RESULT_FILE_PATH: /path/to/outputs/gen_1.png
```
OpenClaw 应当解析并获取所有 `RESULT_FILE_PATH` 开头的路径。
