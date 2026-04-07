#!/usr/bin/env python3
"""Generate and edit images using Gemini API."""

import os
import sys
import base64
import requests
import argparse

def encode_image(path: str) -> tuple[str, str]:
    """Encode image to base64 and detect MIME type."""
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    ext = os.path.splitext(path)[1].lower()
    mime = mime_map.get(ext, "image/png")
    with open(path, "rb") as f:
        return mime, base64.b64encode(f.read()).decode("utf-8")

def generate_image(prompt: str, size: str = "1K", aspect_ratio: str = "16:9", output: str = "output.png", image_path: str = None, model: str = "gemini-2.5-flash-image"):
    """Generate or edit an image using Gemini API."""

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment")
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }

    # Build parts array - include image if editing
    parts = []
    if image_path:
        mime, data = encode_image(image_path)
        parts.append({"inline_data": {"mime_type": mime, "data": data}})
    parts.append({"text": prompt})

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": size
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"API Error: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)

    data = response.json()

    # Extract image from response
    if "candidates" in data and len(data["candidates"]) > 0:
        parts = data["candidates"][0].get("content", {}).get("parts", [])
        for part in parts:
            if "inlineData" in part:
                image_data = base64.b64decode(part["inlineData"]["data"])
                with open(output, "wb") as f:
                    f.write(image_data)
                print(f"Image saved to: {output}")
                return output

    print("No image generated in response")
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and edit images with Gemini API")
    parser.add_argument("--prompt", "-p", required=True, help="Image description or edit instructions")
    parser.add_argument("--size", "-s", default="1K", choices=["1K", "2K", "4K"])
    parser.add_argument("--aspect", "-a", default="16:9", choices=["1:1", "16:9", "9:16", "4:3", "3:2"])
    parser.add_argument("--output", "-o", default="generated.png")
    parser.add_argument("--image", "-i", default=None, help="Path to existing image for editing")
    parser.add_argument("--model", "-m", default="gemini-2.5-flash-image", help="Model to use (default: gemini-2.5-flash-image)")

    args = parser.parse_args()

    if args.image:
        print(f"Editing image: {args.image}")
        print(f"Edit instructions: {args.prompt}")
        print(f"Model: {args.model}")
    else:
        print(f"Generating new image: {args.prompt}")
        print(f"Model: {args.model}")

    generate_image(args.prompt, args.size, args.aspect, args.output, args.image, args.model)
