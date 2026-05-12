#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["certifi"]
# ///
"""
Wiki 配图生成脚本
支持 OpenAI DALL-E 3 和 Google Gemini Imagen 3

用法:
  uv run generate.py --prompt "..." --output "assets/illust/xxx.png"
  uv run generate.py --prompt "..." --output "assets/illust/xxx.png" --provider google
"""

import argparse
import base64
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

import certifi


def ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context(cafile=certifi.where())
    return ctx


def load_env():
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())


def generate_openai(prompt: str, output_path: Path) -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("错误：未设置 OPENAI_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    print("[OpenAI DALL-E 3] 正在生成图片...")
    print(f"Prompt: {prompt[:80]}...")

    payload = json.dumps({
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1792x1024",
        "quality": "hd",
        "response_format": "b64_json"
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=60, context=ssl_context()) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"错误：OpenAI API 请求失败 ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)

    image_data = base64.b64decode(data["data"][0]["b64_json"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_data)
    print(f"✓ 图片已保存：{output_path}")


def generate_google(prompt: str, output_path: Path) -> None:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("错误：未设置 GOOGLE_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    print("[Google Imagen 4] 正在生成图片...")
    print(f"Prompt: {prompt[:80]}...")

    payload = json.dumps({
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9",
            "safetyFilterLevel": "block_few",
            "personGeneration": "allow_adult"
        }
    }).encode("utf-8")

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"imagen-4.0-generate-001:predict?key={api_key}"
    )

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=90, context=ssl_context()) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"错误：Google API 请求失败 ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)

    predictions = data.get("predictions", [])
    if not predictions:
        print("错误：Google API 未返回图片", file=sys.stderr)
        sys.exit(1)

    image_data = base64.b64decode(predictions[0]["bytesBase64Encoded"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_data)
    print(f"✓ 图片已保存：{output_path}")


def main():
    load_env()

    parser = argparse.ArgumentParser(description="Wiki 配图生成脚本")
    parser.add_argument("--prompt", required=True, help="图片描述 prompt（英文）")
    parser.add_argument("--output", required=True, help="输出路径，如 assets/illust/xxx.png")
    parser.add_argument(
        "--provider",
        choices=["openai", "google"],
        default=os.environ.get("ILLUST_PROVIDER", "openai"),
        help="生图服务商（默认读取 ILLUST_PROVIDER 环境变量，否则用 openai）"
    )

    args = parser.parse_args()
    output_path = Path(args.output)

    if output_path.exists():
        print(f"跳过：{output_path} 已存在（如需覆盖请手动删除）")
        sys.exit(0)

    if args.provider == "openai":
        generate_openai(args.prompt, output_path)
    elif args.provider == "google":
        generate_google(args.prompt, output_path)


if __name__ == "__main__":
    main()
