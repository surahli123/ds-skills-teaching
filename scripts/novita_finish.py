#!/usr/bin/env python3
"""Finish generating the remaining slide images."""

import os
import sys

# Add parent so we can reuse the main script's functions
sys.path.insert(0, os.path.dirname(__file__))
from novita_image_gen import (
    generate_flux, generate_seedream, SLIDES, IMAGES_DIR
)

def main():
    # Check what's already done
    missing = []
    for slide in SLIDES:
        sid = slide["id"]
        flux_path = os.path.join(IMAGES_DIR, f"flux-pro-slide-{sid}.png")
        seed_path = os.path.join(IMAGES_DIR, f"seedream-slide-{sid}.png")

        # Check if file exists AND is non-empty
        if not os.path.exists(flux_path) or os.path.getsize(flux_path) < 100:
            missing.append(("flux", slide))
        if not os.path.exists(seed_path) or os.path.getsize(seed_path) < 100:
            missing.append(("seedream", slide))

    if not missing:
        print("All images already generated!")
        return

    print(f"Generating {len(missing)} missing images...\n")

    for model, slide in missing:
        sid = slide["id"]
        prompt = slide["prompt"]
        if model == "flux":
            generate_flux(prompt, sid)
        else:
            generate_seedream(prompt, sid)

    # Final check
    print("\n" + "=" * 50)
    print("Final image inventory:")
    for f in sorted(os.listdir(IMAGES_DIR)):
        path = os.path.join(IMAGES_DIR, f)
        if os.path.isfile(path):
            size_kb = os.path.getsize(path) / 1024
            status = "OK" if size_kb > 1 else "EMPTY"
            print(f"  {status:5s} {f} ({size_kb:.0f} KB)")

if __name__ == "__main__":
    main()
