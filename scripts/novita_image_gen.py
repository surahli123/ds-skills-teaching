#!/usr/bin/env python3
"""
Novita AI Image Bake-off: FLUX 2 Pro vs Seedream 4.5
Generates slide images in Electric Studio style for comparison.

Electric Studio: electric blue/purple, bold, creative, high-contrast, dark background.
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

# FLUX 2 Pro: async API, size uses "*", range 256-1536 per dim
FLUX_ENDPOINT = "https://api.novita.ai/v3/async/flux-2-pro"
FLUX_POLL     = "https://api.novita.ai/v3/async/task-result"
FLUX_SIZE     = "1536*864"  # 16:9, within 256-1536 per-dim limit

# Seedream 4.5: sync API, size uses "x", min 3,686,400 total pixels
SEEDREAM_ENDPOINT = "https://api.novita.ai/v3/seedream-4.5"
SEEDREAM_SIZE     = "2560x1440"  # 16:9, exactly meets 3.6M pixel minimum

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

# ---------------------------------------------------------------------------
# Prompts — Electric Studio style adapted from AAAAAJ Cyberpunk + Neo-Brutalism
# ---------------------------------------------------------------------------
SLIDES = [
    {
        "id": "01-title",
        "prompt": (
            "Electric studio style PPT slide, dark navy-black background, "
            "bold title text 'Why You Re-Explain the Same Thing Every Session' "
            "in large white sans-serif font with electric blue glow, "
            "subtitle 'The Hidden Cost of Tribal Knowledge' in smaller purple text below, "
            "electric blue #0066FF and vivid purple #9933FF neon accent lines, "
            "geometric circuit-board decorations in corners, "
            "subtle grid pattern overlay, high contrast, bold creative energy, "
            "professional presentation slide, 16:9"
        ),
    },
    {
        "id": "04-what-is-skill",
        "prompt": (
            "Electric studio style PPT slide, dark navy-black background, "
            "bold title text 'What Is a Skill?' in large white sans-serif font "
            "with electric blue neon glow effect, "
            "subtitle 'A Reusable Folder: Prompt + Context + Examples' in light purple text, "
            "three glowing cards below showing 'SKILL.md' 'CONTEXT/' 'EXAMPLES/' "
            "each in rounded rectangles with electric blue #0066FF borders, "
            "purple #9933FF accent highlights, dark background with subtle hex grid, "
            "bold modern typography, high contrast neon design, "
            "professional presentation slide, 16:9"
        ),
    },
    {
        "id": "06-before-after",
        "prompt": (
            "Electric studio style PPT slide, dark navy-black background, "
            "bold title text 'Before vs After Skills' in large white font "
            "with electric blue glow, "
            "left side labeled 'BEFORE' in red #FF4444 showing chaotic scattered text "
            "'re-explain every time' 'lost context' 'inconsistent output', "
            "right side labeled 'AFTER' in electric green #00FF88 showing organized "
            "clean blocks 'reusable' 'consistent' 'scalable', "
            "vertical divider line in vivid purple #9933FF, "
            "electric blue #0066FF accent elements, neon glow effects, "
            "bold typography, high contrast, professional presentation slide, 16:9"
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
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"  HTTP {e.code}: {error_body}")
        return None


def download_image(url, filepath, max_retries=3):
    """Download an image from a URL to a local file with retry."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=300) as resp:
                with open(filepath, "wb") as f:
                    f.write(resp.read())
            size_kb = os.path.getsize(filepath) / 1024
            print(f"  Saved: {os.path.basename(filepath)} ({size_kb:.0f} KB)")
            return
        except Exception as e:
            print(f"  Download attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    print(f"  FAILED to download after {max_retries} attempts")


# ---------------------------------------------------------------------------
# FLUX 2 Pro — async: submit → poll → download
# ---------------------------------------------------------------------------
def generate_flux(prompt, slide_id):
    """Generate an image with FLUX 2 Pro (async API)."""
    print(f"\n[FLUX 2 Pro] Generating: {slide_id}")
    print(f"  Prompt: {prompt[:80]}...")

    payload = {
        "prompt": prompt,
        "size": FLUX_SIZE,
        "seed": 42,
    }

    # Submit task
    result = api_request(FLUX_ENDPOINT, payload)
    if not result or "task_id" not in result:
        print(f"  FAILED to submit task: {result}")
        return None

    task_id = result["task_id"]
    print(f"  Task submitted: {task_id}")

    # Poll for completion (max 120 seconds)
    for i in range(60):
        time.sleep(3)
        poll_url = f"{FLUX_POLL}?task_id={task_id}"
        status = api_request(poll_url, method="GET")

        if not status:
            print(f"  Poll failed at attempt {i+1}")
            continue

        task_status = status.get("task", {}).get("status", "")
        if task_status == "TASK_STATUS_SUCCEED":
            images = status.get("images", [])
            if images:
                img_url = images[0]["image_url"]
                filepath = os.path.join(IMAGES_DIR, f"flux-pro-slide-{slide_id}.png")
                download_image(img_url, filepath)
                return filepath
            else:
                print("  SUCCEEDED but no images returned")
                return None
        elif task_status == "TASK_STATUS_FAILED":
            reason = status.get("task", {}).get("reason", "unknown")
            print(f"  FAILED: {reason}")
            return None
        else:
            progress = status.get("task", {}).get("progress_percent", 0)
            if i % 5 == 0:
                print(f"  Polling... status={task_status} progress={progress}%")

    print("  TIMEOUT after 180 seconds")
    return None


# ---------------------------------------------------------------------------
# Seedream 4.5 — sync: submit → get images directly
# ---------------------------------------------------------------------------
def generate_seedream(prompt, slide_id):
    """Generate an image with Seedream 4.5 (sync API)."""
    print(f"\n[Seedream 4.5] Generating: {slide_id}")
    print(f"  Prompt: {prompt[:80]}...")

    payload = {
        "prompt": prompt,
        "size": SEEDREAM_SIZE,
        "watermark": False,
    }

    result = api_request(SEEDREAM_ENDPOINT, payload)
    if not result:
        print("  FAILED: no response")
        return None

    # Check for error
    if "code" in result and result["code"] != 200:
        print(f"  FAILED: {result.get('message', 'unknown error')}")
        return None

    images = result.get("images", [])
    if images:
        # Images may be URLs (strings) or objects with image_url
        img_data = images[0]
        if isinstance(img_data, str):
            img_url = img_data
        elif isinstance(img_data, dict):
            img_url = img_data.get("image_url", img_data.get("url", ""))
        else:
            print(f"  Unexpected image format: {type(img_data)}")
            return None

        filepath = os.path.join(IMAGES_DIR, f"seedream-slide-{slide_id}.png")
        download_image(img_url, filepath)
        return filepath
    else:
        print(f"  FAILED: no images in response. Keys: {list(result.keys())}")
        # Print first 500 chars for debugging
        print(f"  Response preview: {json.dumps(result)[:500]}")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Novita AI Image Bake-off: FLUX 2 Pro vs Seedream 4.5")
    print("Style: Electric Studio (blue/purple, bold, high-contrast)")
    print(f"FLUX size: {FLUX_SIZE} | Seedream size: {SEEDREAM_SIZE}")
    print("=" * 60)

    results = {"flux": [], "seedream": []}

    for slide in SLIDES:
        sid = slide["id"]
        prompt = slide["prompt"]

        # Generate with both models
        flux_path = generate_flux(prompt, sid)
        if flux_path:
            results["flux"].append(flux_path)

        seedream_path = generate_seedream(prompt, sid)
        if seedream_path:
            results["seedream"].append(seedream_path)

    # Summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"\nFLUX 2 Pro: {len(results['flux'])}/{len(SLIDES)} images generated")
    for p in results["flux"]:
        print(f"  ✓ {os.path.basename(p)}")

    print(f"\nSeedream 4.5: {len(results['seedream'])}/{len(SLIDES)} images generated")
    for p in results["seedream"]:
        print(f"  ✓ {os.path.basename(p)}")

    print(f"\nAll images saved to: {os.path.abspath(IMAGES_DIR)}/")
    return results


if __name__ == "__main__":
    main()
