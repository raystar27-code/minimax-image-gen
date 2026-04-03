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

def generate_images(prompt, aspect_ratio=None, model="image-01", n=1, 
                    style=None, style_weight=0.8, seed=None, width=None, height=None, 
                    prompt_optimizer=True, output_dir="./outputs"):
    """
    调用 MiniMax API 生成多张图片并归档。
    """
    if not MINIMAX_API_KEY:
        print("错误: 未找到 MINIMAX_API_KEY，请检查环境变量或 .env 文件。")
        return []

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "response_format": "url",
        "n": n,
        "prompt_optimizer": prompt_optimizer
    }

    # 比例与宽高逻辑：比例优先级更高
    if aspect_ratio:
        payload["aspect_ratio"] = aspect_ratio
    elif width and height:
        # 仅针对 image-01 有效
        if model == "image-01":
            payload["width"] = width
            payload["height"] = height
        else:
            print(f"警告: 自定义宽高仅在 image-01 模型下有效，当前模型为 {model}。已跳过宽高设置。")

    # 风格设置：仅针对 image-01-live 有效
    if style:
        if model == "image-01-live":
            # style 应该是一个对象，包含 style_type 和 style_weight
            payload["style"] = {
                "style_type": style,
                "style_weight": style_weight if style_weight is not None else 0.8
            }
        else:
            print(f"警告: style 属性仅在 image-01-live 模型下有效。已跳过 style 设置。")

    # 随机种子
    if seed is not None:
        payload["seed"] = seed

    try:
        print(f"正在向 MiniMax 提交任务... (模型: {model}, 数量: {n}, 比例/尺寸: {aspect_ratio or f'{width}x{height}'})")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("base_resp", {}).get("status_code") != 0:
            error_msg = result.get("base_resp", {}).get("status_msg", "未知错误")
            raise Exception(f"API 返回错误: {error_msg}")

        image_urls = result.get("data", {}).get("image_urls", [])
        if not image_urls:
            raise Exception("API 未返回任何图片 URL。")

        # 循环下载所有图片
        saved_paths = []
        for i, url in enumerate(image_urls):
            path = download_image(url, output_dir, suffix=f"_{i+1}" if n > 1 else "")
            if path:
                saved_paths.append(path)
        
        return saved_paths

    except Exception as e:
        print(f"生成过程发生错误: {e}")
        return []

def download_image(url, output_dir, suffix=""):
    """
    下载图片并保存。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"gen_{timestamp}{suffix}.png"
    filepath = os.path.join(output_dir, filename)

    try:
        print(f"正在下载: {url}")
        img_response = requests.get(url, stream=True, timeout=30)
        img_response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in img_response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return os.path.abspath(filepath)
    except Exception as e:
        print(f"下载失败: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MiniMax 全功能图片生成工具")
    parser.add_argument("--prompt", required=True, help="提示词")
    parser.add_argument("--aspect_ratio", nargs='+', help="比例列表 (1:1等)")
    parser.add_argument("--model", default="image-01", choices=["image-01", "image-01-live"])
    parser.add_argument("--n", type=int, default=1, help="单次请求生成的图片数量 (1-9)")
    parser.add_argument("--style", help="风格 (仅限 image-01-live，如：漫画, 元气, 中世纪, 水彩)")
    parser.add_argument("--style_weight", type=float, default=0.8, help="风格权重 (0.0 到 1.0 之间)")
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument("--width", type=int, help="自定义宽度 (仅限 image-01)")
    parser.add_argument("--height", type=int, help="自定义高度 (仅限 image-01)")
    parser.add_argument("--no_optimizer", action="store_true", help="关闭提示词优化")
    parser.add_argument("--output_dir", default="./outputs")

    args = parser.parse_args()

    all_results = []
    
    # 如果用户没提供 aspect_ratio 也没提供宽高，默认使用 1:1
    ratios = args.aspect_ratio if args.aspect_ratio else ([None] if args.width and args.height else ["1:1"])

    for r in ratios:
        paths = generate_images(
            prompt=args.prompt,
            aspect_ratio=r,
            model=args.model,
            n=args.n,
            style=args.style,
            style_weight=args.style_weight,
            seed=args.seed,
            width=args.width,
            height=args.height,
            prompt_optimizer=not args.no_optimizer,
            output_dir=args.output_dir
        )
        all_results.extend(paths)

    if all_results:
        print("\n" + "="*30)
        print(f"成功生成 {len(all_results)} 张图片:")
        for res in all_results:
            print(f"RESULT_FILE_PATH: {res}")
        print("="*30)
    else:
        exit(1)
