#!/usr/bin/env python3
"""
Novita AI v2 Image Generation — Electric Studio Style
Clean, bright, bold blue + white panels. NO dark mode, NO neon, NO cyberpunk.

Primary: Seedream 4.5 (sync, better text rendering)
Fallback: FLUX 2 Pro (async)
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

# Seedream 4.5: sync, size uses "x", min 3,686,400 pixels
SEEDREAM_ENDPOINT = "https://api.novita.ai/v3/seedream-4.5"
SEEDREAM_SIZE = "2560x1440"

# FLUX 2 Pro: async, size uses "*", max 1536 per dim
FLUX_ENDPOINT = "https://api.novita.ai/v3/async/flux-2-pro"
FLUX_POLL = "https://api.novita.ai/v3/async/task-result"
FLUX_SIZE = "1536*864"

# ---------------------------------------------------------------------------
# Electric Studio style — shared style block for all prompts
# Clean white bg, electric blue #4361ee accent, flat design, bold sans-serif
# ---------------------------------------------------------------------------
STYLE_BLOCK = (
    "Modern corporate presentation slide, clean white background, "
    "electric blue color #4361ee as accent, bold black sans-serif typography "
    "like Manrope or Inter, flat design, minimal geometric shapes, "
    "professional business aesthetic, crisp clean layout, "
    "no shadows, no gradients, no glow effects, no neon, "
    "no dark background, no circuit boards, no cyberpunk, "
    "no glassmorphism, no gradient text, 16:9"
)

# Negative prompt for models that support it (FLUX)
NEGATIVE_PROMPT = (
    "neon, glow, dark background, circuit board, cyberpunk, "
    "glassmorphism, gradient text, sci-fi, futuristic, "
    "purple, magenta, cyan neon, black background, tech grid"
)

# ---------------------------------------------------------------------------
# Slide prompts — Electric Studio style
# ---------------------------------------------------------------------------
SLIDES = [
    {
        "id": "01-title",
        "prompt": (
            f"{STYLE_BLOCK}, "
            "split-panel composition with white top half and electric blue #4361ee bottom half, "
            "large bold black title text 'Why You Re-Explain the Same Thing Every Session' "
            "centered in the white area, "
            "smaller light gray subtitle text 'The Hidden Cost of Tribal Knowledge' below the title, "
            "thin electric blue horizontal accent line separating title from subtitle, "
            "clean open whitespace, no decorative elements, no icons"
        ),
    },
    {
        "id": "04-what-is-skill",
        "prompt": (
            f"{STYLE_BLOCK}, "
            "white background with electric blue #4361ee accent bar on the left side, "
            "bold black title 'What Is a Skill?' at the top left, "
            "subtitle in gray 'A Reusable Folder with Prompt, Context, and Examples', "
            "three white rectangular cards in a row below with thin electric blue borders, "
            "card labels in bold black text: 'SKILL.md' and 'scripts/' and 'references/', "
            "cards evenly spaced with generous whitespace between them, "
            "flat solid colors only, no icons, no illustrations"
        ),
    },
    {
        "id": "06-before-after",
        "prompt": (
            f"{STYLE_BLOCK}, "
            "side-by-side two-column layout, "
            "bold black title 'Before vs After Skills' centered at top, "
            "left column labeled 'BEFORE' in bold red #e63946 text at top, "
            "left column has scattered messy text items 're-explain every time' "
            "'lost context' 'inconsistent output' on white background, "
            "right column labeled 'AFTER' in bold green #2a9d8f text at top, "
            "right column has clean organized blue-bordered cards "
            "'reusable' 'consistent' 'scalable', "
            "thin vertical electric blue #4361ee divider line between columns, "
            "clean flat design, no glow, no dark background"
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
    """Download an image from a URL to a local file with retry."""
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
                print(f"  Downloaded but file is empty, retrying...")
        except Exception as e:
            print(f"  Download attempt {attempt+1} failed: {e}")
        if attempt < max_retries - 1:
            time.sleep(3)
    print(f"  FAILED to download after {max_retries} attempts")
    return False


# ---------------------------------------------------------------------------
# Seedream 4.5 — sync API (primary)
# ---------------------------------------------------------------------------
def generate_seedream(prompt, slide_id):
    """Generate with Seedream 4.5 (sync). Returns filepath or None."""
    print(f"\n[Seedream 4.5] Generating: {slide_id}")
    print(f"  Prompt: {prompt[:100]}...")

    payload = {
        "prompt": prompt,
        "size": SEEDREAM_SIZE,
        "watermark": False,
    }

    result = api_request(SEEDREAM_ENDPOINT, payload)
    if not result:
        print("  FAILED: no response")
        return None

    if "code" in result and result["code"] != 200 and "images" not in result:
        print(f"  FAILED: {result.get('message', 'unknown error')}")
        return None

    images = result.get("images", [])
    if images:
        img_data = images[0]
        if isinstance(img_data, str):
            img_url = img_data
        elif isinstance(img_data, dict):
            img_url = img_data.get("image_url", img_data.get("url", ""))
        else:
            print(f"  Unexpected image format: {type(img_data)}")
            return None

        filepath = os.path.join(IMAGES_DIR, f"v2-seedream-slide-{slide_id}.png")
        if download_image(img_url, filepath):
            return filepath
    else:
        print(f"  No images in response. Keys: {list(result.keys())}")
    return None


# ---------------------------------------------------------------------------
# FLUX 2 Pro — async API (fallback)
# ---------------------------------------------------------------------------
def generate_flux(prompt, slide_id):
    """Generate with FLUX 2 Pro (async). Returns filepath or None."""
    print(f"\n[FLUX 2 Pro FALLBACK] Generating: {slide_id}")
    print(f"  Prompt: {prompt[:100]}...")

    payload = {
        "prompt": prompt,
        "size": FLUX_SIZE,
        "seed": 42,
    }

    result = api_request(FLUX_ENDPOINT, payload)
    if not result or "task_id" not in result:
        print(f"  FAILED to submit: {result}")
        return None

    task_id = result["task_id"]
    print(f"  Task submitted: {task_id}")

    # Poll for up to 120 seconds
    for i in range(40):
        time.sleep(3)
        poll_url = f"{FLUX_POLL}?task_id={task_id}"
        status = api_request(poll_url, method="GET")
        if not status:
            continue

        task_status = status.get("task", {}).get("status", "")
        if task_status == "TASK_STATUS_SUCCEED":
            images = status.get("images", [])
            if images:
                img_url = images[0]["image_url"]
                filepath = os.path.join(IMAGES_DIR, f"v2-flux-slide-{slide_id}.png")
                if download_image(img_url, filepath):
                    return filepath
            return None
        elif task_status == "TASK_STATUS_FAILED":
            reason = status.get("task", {}).get("reason", "unknown")
            print(f"  FAILED: {reason}")
            return None
        elif i % 5 == 0:
            print(f"  Polling... status={task_status}")

    print("  TIMEOUT")
    return None


# ---------------------------------------------------------------------------
# Main — Seedream first, FLUX fallback
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("v2 Image Generation — Electric Studio Style")
    print("Clean white bg + electric blue #4361ee + bold sans-serif")
    print("Primary: Seedream 4.5 | Fallback: FLUX 2 Pro")
    print("=" * 60)

    results = []

    for slide in SLIDES:
        sid = slide["id"]
        prompt = slide["prompt"]

        # Try Seedream first
        path = generate_seedream(prompt, sid)

        # Fallback to FLUX if Seedream fails
        if not path:
            print(f"  Seedream failed for {sid}, trying FLUX 2 Pro fallback...")
            path = generate_flux(prompt, sid)

        if path:
            results.append(path)
        else:
            print(f"  BOTH MODELS FAILED for {sid}")

    # Summary
    print("\n" + "=" * 60)
    print(f"v2 RESULTS: {len(results)}/{len(SLIDES)} images generated")
    print("=" * 60)
    for p in results:
        size_kb = os.path.getsize(p) / 1024
        print(f"  {os.path.basename(p)} ({size_kb:.0f} KB)")

    # List all v2 images
    print(f"\nAll v2 images in {os.path.abspath(IMAGES_DIR)}/:")
    for f in sorted(os.listdir(IMAGES_DIR)):
        if f.startswith("v2-"):
            path = os.path.join(IMAGES_DIR, f)
            size_kb = os.path.getsize(path) / 1024
            print(f"  {f} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
