---
name: minimax-image-gen
description: 使用 MiniMax API 根据文本描述生成图像，并保存到本地。
---

# MiniMax 图像生成 (MiniMax Image Generation)

## 概述
调用 MiniMax 的 `image-01` 或 `image-01-live` 模型，将文本提示词转换为高质量图像，并自动下载到本地服务器。

## 使用条件
- 需要生成图片时。
- 需要将生成的图片作为文件发送给用户或存放在服务器上时。
- 环境中已配置 `MINIMAX_API_KEY`。

## 核心模式
运行 `minimax_gen.py` 脚本，并传入提示词。

### 调用示例
```bash
# 生成单张图片
python minimax_gen.py --prompt "一只正在喝咖啡的企鹅" --aspect_ratio "16:9"

# 同时生成多种比例的图片 (空格分隔)
python minimax_gen.py --prompt "赛博朋克城市" --aspect_ratio 4:3 3:4 16:9
```

### 预期输出
脚本会依次处理并输出所有生成的本地路径：
```text
RESULT_FILE_PATH: /path/to/outputs/gen_1.png
RESULT_FILE_PATH: /path/to/outputs/gen_2.png
```

## 输入参数
- `--prompt`: (必填) 图像描述文字。
- `--aspect_ratio`: (可选) 图像比例。支持传入多个比例（空格分隔），将为每个比例生成一张图片。可选值包括 `1:1`, `16:9`, `4:3`, `3:2`, `2:3`, `3:4`, `9:16`, `21:9`。
- `--model`: (可选) 模型选择，默认为 `image-01`。可选 `image-01` 或 `image-01-live`。
- `--output_dir`: (可选) 保存目录，默认为 `./outputs`。

## 常见问题
- **API Key 错误**: 检查 `.env` 文件或环境变量是否包含有效的 `MINIMAX_API_KEY`。
- **网络超时**: 生成图片通常需要 10-30 秒，如果服务器网络不稳定，请检查重试逻辑。
- **内容安全**: 如果提示词触发了 MiniMax 的合规性过滤，API 可能报错或不返回图片。
