---
name: imagegen
description: Generates and edits images using Google Gemini API based on content, style, size, aspect ratio, and editing specifications.
---

# ImageGen: Gemini Image Generator

Generate images using the Google Gemini API for use in slide presentations or other assets.

## Authentication

The skill automatically uses the `GEMINI_API_KEY` from your system environment. No manual configuration needed.

**Default Model:** `gemini-2.5-flash-image` (free tier)

## Model Comparison

| Model | Size Options | Notes |
|-------|--------------|-------|
| `gemini-2.5-flash-image` | 1K, 2K, 4K | Free tier, default. **512 not supported** |
| `gemini-3.1-flash-image-preview` | 512, 1K, 2K, 4K | Preview model, supports smaller sizes |

Switch models using the `--model` flag:
```bash
python3 skills/imagegen/scripts/generate.py \
  --prompt "..." --model gemini-3.1-flash-image-preview
```

## Setup

### 1. Create Virtual Environment (Recommended)

```bash
cd /path/to/SlideGen
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows
pip install requests
```

### 2. Set API Key (if not already in environment)

```bash
export GEMINI_API_KEY="your-api-key-here"
```

## When to Use

Use this skill when:
- You need a custom illustration for a slide deck
- You want to generate visual assets matching the BPDU style
- You need images in specific aspect ratios or resolutions
- You need style-consistent imagery for presentations
- **You want to edit an existing image** (add/remove elements, change colors, modify style)

## Input Parameters

| Parameter | Description | Options |
|-----------|-------------|---------|
| `prompt` | Description of what to generate or edit | Required, be specific about content, style, mood |
| `size` | Resolution | `"1K"`, `"2K"`, `"4K"` (512 not supported on 2.5) |
| `aspectRatio` | Image dimensions | `"1:1"` (square), `"16:9"` (landscape), `"9:16"` (portrait), `"4:3"`, `"3:2"` |
| `style` | Visual style | `"flat illustration"`, `"cartoon"`, `"photorealistic"`, `"minimalist"`, etc. |
| `outputPath` | Where to save the image | Relative path from project root |
| `imagePath` | Path to existing image for editing | Required for edit operations |
| `model` | Gemini model to use | `"gemini-2.5-flash-image"` (default), `"gemini-3.1-flash-image-preview"` |

## API Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent
Header: x-goog-api-key: $GEMINI_API_KEY
```

## Request Format

### Generate New Image
```json
{
  "contents": [{
    "parts": [{
      "text": "YOUR_PROMPT_HERE"
    }]
  }],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {
      "imageSize": "1K",
      "aspectRatio": "16:9"
    }
  }
}
```

### Edit Existing Image
```json
{
  "contents": [{
    "parts": [
      {"text": "Add a red bow tie to the character"},
      {
        "inline_data": {
          "mime_type": "image/png",
          "data": "BASE64_ENCODED_IMAGE"
        }
      }
    ]
  }],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {
      "imageSize": "1K",
      "aspectRatio": "16:9"
    }
  }
}
```

For editing, include both the text prompt describing the changes AND the original image in the `parts` array.

## Implementation Script

Create a script to generate and edit images programmatically:

```python
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

def generate_image(prompt: str, size: str = "1K", aspect_ratio: str = "16:9", output: str = "output.png", image_path: str = None):
    """Generate or edit an image using Gemini API."""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment")
        sys.exit(1)
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"
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
                "imageSize": size,
                "aspectRatio": aspect_ratio
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
    
    args = parser.parse_args()
    
    if args.image:
        print(f"Editing image: {args.image}")
        print(f"Edit instructions: {args.prompt}")
    else:
        print(f"Generating new image: {args.prompt}")
    
    generate_image(args.prompt, args.size, args.aspect, args.output, args.image)
```

## BPDU Style Guidelines

When generating images for BPDU presentations:

- **Style:** Warm, flat-cartoon illustrations
- **Colors:** Friendly, intellectual aesthetic with warm tones
- **Avoid:** Cold blues, harsh contrast, corporate/sterile looks
- **Match:** The style of `BPDU_theme_image.png` (illustrated group portrait)

### Example Prompts for BPDU

```
"Warm flat cartoon illustration of diverse students debating in a university seminar room, 
friendly intellectual atmosphere, soft colors, BPDU brand style"

"Minimalist flat illustration of a brain with lightning bolt, light teal background, 
BPDU logo style, clean vector art"

"Cartoon illustration of a podium and microphone on a stage, warm amber and white 
color scheme, friendly educational style"
```

## Usage Examples

### Generate a title slide illustration
```bash
cd /path/to/SlideGen
python3 skills/imagegen/scripts/generate.py \
  --prompt "Warm flat cartoon illustration of diverse debate team members, BPDU style" \
  --size 1K \
  --aspect 16:9 \
  --output title-illustration.png
```

### Generate a square icon (use 3.1 for 512px)
```bash
python3 skills/imagegen/scripts/generate.py \
  --prompt "Simple flat icon of a lightbulb, warm yellow, minimalist style" \
  --size 512 \
  --aspect 1:1 \
  --model gemini-3.1-flash-image-preview \
  --output assets/lightbulb-icon.png
```

### Generate a portrait for speaker bio
```bash
python3 skills/imagegen/scripts/generate.py \
  --prompt "Professional cartoon avatar of a teacher, friendly expression, warm colors" \
  --size 1K \
  --aspect 9:16 \
  --output speaker-avatar.png
```

### Edit an existing image (add element)
```bash
python3 skills/imagegen/scripts/generate.py \
  --prompt "Add a red bow tie to the character" \
  --image speaker-avatar.png \
  --output speaker-avatar-with-bowtie.png
```

### Modify image style
```bash
python3 skills/imagegen/scripts/generate.py \
  --prompt "Change to flat minimalist style with BPDU warm color palette" \
  --image photo-reference.jpg \
  --output illustration-version.png
```

### Create a variation
```bash
python3 skills/imagegen/scripts/generate.py \
  --prompt "Same composition but with different people and background" \
  --image title-illustration.png \
  --output title-illustration-v2.png
```

## Output

- Saves the generated image to the specified path
- Image is base64-decoded PNG format
- Ready to reference in HTML slides with relative paths
