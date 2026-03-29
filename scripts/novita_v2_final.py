#!/usr/bin/env python3
"""
Novita AI v2 Final — Revised Electric Studio prompts from team lead.
Matches the HTML deck: Manrope 800 + DM Sans, #4361ee accent,
split-panel white/blue layouts, clean flat design.

Primary: Seedream 4.5 | Fallback: FLUX 2 Pro
"""

import os
import json
import time
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
API_KEY = os.environ.get("NOVITA_API_KEY")
if not API_KEY:
    raise RuntimeError("NOVITA_API_KEY not set — source ~/.zshrc first")

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

# Seedream 4.5: sync, min 3,686,400 pixels → 2560x1440 for 16:9
SEEDREAM_ENDPOINT = "https://api.novita.ai/v3/seedream-4.5"
SEEDREAM_SIZE = "2560x1440"

# FLUX 2 Pro: async, max 1536 per dim → 1536*864 for 16:9
FLUX_ENDPOINT = "https://api.novita.ai/v3/async/flux-2-pro"
FLUX_POLL = "https://api.novita.ai/v3/async/task-result"
FLUX_SIZE = "1536*864"

# ---------------------------------------------------------------------------
# Revised prompts from team lead — match the HTML deck exactly
# ---------------------------------------------------------------------------
SLIDES = [
    {
        "id": "01-title",
        "prompt": (
            'Modern minimalist presentation title slide, split panel design '
            'with white upper half and solid electric blue (#4361ee) lower half, '
            'bold black sans-serif heading "Why You Re-Explain the Same Thing '
            'Every Session" on the white section, smaller gray subtitle '
            '"The Hidden Cost of Tribal Knowledge" below, small blue circle '
            'brand mark in top right corner, clean flat design, no shadows '
            'no gradients no glow effects, professional corporate aesthetic, '
            'generous whitespace, 16:9 aspect ratio, 2048x1152'
        ),
    },
    {
        "id": "04-what-is-skill",
        "prompt": (
            'Clean corporate infographic slide, white background, bold black '
            'sans-serif heading "What Is a Skill?" at top, subtitle '
            '"A Reusable Folder: Prompt + Context + Examples" in gray, '
            'three flat rectangular cards in a row below showing "SKILL.md" '
            'and "scripts/" and "references/", cards have thin electric blue '
            '(#4361ee) left border accent, light gray card backgrounds (#f5f5f0), '
            'minimal flat design, no shadows no glow no dark background, '
            'professional business presentation style, 16:9 aspect ratio, 2048x1152'
        ),
    },
    {
        "id": "06-comparison",
        "prompt": (
            'Clean corporate comparison slide, white background, bold black '
            'sans-serif heading "Skills vs SubAgents" at top, two-column layout, '
            'left column labeled "Skills" with electric blue (#4361ee) accent bar '
            'and keywords "Depth, Reusable, Persistent Knowledge", right column '
            'labeled "SubAgents" with dark gray accent bar and keywords '
            '"Breadth, One-Shot, Parallel Execution", clean flat design with '
            'thin divider line between columns, no shadows no glow no dark '
            'background no neon, professional minimal aesthetic, 16:9 aspect '
            'ratio, 2048x1152'
        ),
    },
]


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------
def api_request(url, data=None, method="POST"):
    """Make an API request and return parsed JSON."""
    if data is not None:
        body = json.dumps(data).encode("utf-8")
    else:
        body = None
        method = "GET"

    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"  HTTP {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"  Request error: {e}")
        return None


def download_image(url, filepath, max_retries=3):
    """Download image with retry and longer timeout for large Seedream files."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=300) as resp:
                with open(filepath, "wb") as f:
                    f.write(resp.read())
            size_kb = os.path.getsize(filepath) / 1024
            if size_kb > 1:
                print(f"  Saved: {os.path.basename(filepath)} ({size_kb:.0f} KB)")
                return True
            else:
                print(f"  Empty file, retrying...")
        except Exception as e:
            print(f"  Download attempt {attempt+1} failed: {e}")
        if attempt < max_retries - 1:
            time.sleep(3)
    print(f"  FAILED to download after {max_retries} attempts")
    return False


# ---------------------------------------------------------------------------
# Seedream 4.5 — sync (primary)
# ---------------------------------------------------------------------------
def generate_seedream(prompt, slide_id):
    """Generate with Seedream 4.5. Returns filepath or None."""
    print(f"\n[Seedream 4.5] Generating: {slide_id}")

    payload = {
        "prompt": prompt,
        "size": SEEDREAM_SIZE,
        "watermark": False,
    }

    result = api_request(SEEDREAM_ENDPOINT, payload)
    if not result:
        return None

    if "code" in result and result["code"] != 200 and "images" not in result:
        print(f"  Error: {result.get('message', 'unknown')}")
        return None

    images = result.get("images", [])
    if images:
        img_data = images[0]
        img_url = img_data if isinstance(img_data, str) else img_data.get("image_url", "")
        filepath = os.path.join(IMAGES_DIR, f"v2-seedream-slide-{slide_id}.png")
        if download_image(img_url, filepath):
            return filepath
    else:
        print(f"  No images returned. Response keys: {list(result.keys())}")
    return None


# ---------------------------------------------------------------------------
# FLUX 2 Pro — async (fallback)
# ---------------------------------------------------------------------------
def generate_flux(prompt, slide_id):
    """Generate with FLUX 2 Pro (async). Returns filepath or None."""
    print(f"\n[FLUX 2 Pro FALLBACK] Generating: {slide_id}")

    payload = {"prompt": prompt, "size": FLUX_SIZE, "seed": 42}

    result = api_request(FLUX_ENDPOINT, payload)
    if not result or "task_id" not in result:
        print(f"  Submit failed: {result}")
        return None

    task_id = result["task_id"]
    print(f"  Task: {task_id}")

    for i in range(40):
        time.sleep(3)
        status = api_request(f"{FLUX_POLL}?task_id={task_id}", method="GET")
        if not status:
            continue
        task_status = status.get("task", {}).get("status", "")
        if task_status == "TASK_STATUS_SUCCEED":
            images = status.get("images", [])
            if images:
                filepath = os.path.join(IMAGES_DIR, f"v2-flux-slide-{slide_id}.png")
                if download_image(images[0]["image_url"], filepath):
                    return filepath
            return None
        elif task_status == "TASK_STATUS_FAILED":
            print(f"  Failed: {status.get('task', {}).get('reason', '?')}")
            return None
        elif i % 5 == 0:
            print(f"  Polling... {task_status}")

    print("  Timeout")
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("v2 FINAL — Revised Electric Studio Prompts")
    print("Primary: Seedream 4.5 | Fallback: FLUX 2 Pro")
    print("=" * 60)

    results = []
    for slide in SLIDES:
        sid = slide["id"]
        prompt = slide["prompt"]

        # Seedream primary
        path = generate_seedream(prompt, sid)
        # FLUX fallback
        if not path:
            print(f"  Seedream failed, trying FLUX fallback...")
            path = generate_flux(prompt, sid)

        if path:
            results.append(path)
        else:
            print(f"  BOTH MODELS FAILED for {sid}")

    # Summary
    print("\n" + "=" * 60)
    print(f"RESULTS: {len(results)}/{len(SLIDES)} images")
    print("=" * 60)
    for f in sorted(os.listdir(IMAGES_DIR)):
        if f.startswith("v2-"):
            p = os.path.join(IMAGES_DIR, f)
            print(f"  {f} ({os.path.getsize(p)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
