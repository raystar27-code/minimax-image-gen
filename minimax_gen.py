import os
import requests
import json
import argparse
import time
from datetime import datetime
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
API_URL = "https://api.minimaxi.com/v1/image_generation"

def generate_image(prompt, aspect_ratio="1:1", model="image-01", output_dir="./outputs"):
    """
    调用 MiniMax API 生成图片并进行下载和保存。
    """
    if not MINIMAX_API_KEY:
        error_msg = "未找到 MINIMAX_API_KEY，请检查环境变量或 .env 文件。"
        print(f"错误: {error_msg}")
        return None

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": "url",
        "n": 1,
        "prompt_optimizer": True  # 默认开启提示词优化
    }

    try:
        print(f"正在请求 MiniMax API 生成图片... (模型: {model}, 比例: {aspect_ratio})")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("base_resp", {}).get("status_code") != 0:
            error_msg = result.get("base_resp", {}).get("status_msg", "未知错误")
            raise Exception(f"API 返回错误: {error_msg}")

        image_urls = result.get("data", {}).get("image_urls", [])
        if not image_urls:
            raise Exception("API 未返回任何图片 URL。")

        image_url = image_urls[0]
        return download_image(image_url, output_dir)

    except Exception as e:
        print(f"生成图片时发生错误: {e}")
        return None

def download_image(url, output_dir):
    """
    从指定 URL 下载图片并保存到本地目录。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 使用时间戳生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"gen_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    try:
        print(f"正在从 URL 下载图片: {url}")
        img_response = requests.get(url, stream=True, timeout=30)
        img_response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in img_response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        abs_path = os.path.abspath(filepath)
        print(f"图片已保存至: {abs_path}")
        return abs_path

    except Exception as e:
        print(f"下载图片时发生错误: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MiniMax 图片生成工具")
    parser.add_argument("--prompt", required=True, help="图片的文本描述")
    # 修改为支持多个比例，使用 nargs='+'
    parser.add_argument("--aspect_ratio", nargs='+', default=["1:1"], 
                        help="图片比例列表，用空格隔开 (例如: 1:1 16:9 4:3)。可选值: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9")
    parser.add_argument("--model", default="image-01", choices=["image-01", "image-01-live"], help="API 模型名称")
    parser.add_argument("--output_dir", default="./outputs", help="图片保存目录")

    args = parser.parse_args()

    final_paths = []
    print(f"收到请求，准备为以下比例生成图片: {', '.join(args.aspect_ratio)}")

    for ratio in args.aspect_ratio:
        path = generate_image(
            prompt=args.prompt,
            aspect_ratio=ratio,
            model=args.model,
            output_dir=args.output_dir
        )
        if path:
            final_paths.append(path)

    if final_paths:
        print("\n" + "="*30)
        print("所有图片生成完毕:")
        for p in final_paths:
            print(f"RESULT_FILE_PATH: {p}")
        print("="*30)
    else:
        print("未能成功生成任何图片。")
        exit(1)
