import os
import json
import urllib.parse
import requests
from pathlib import Path

def main():
    script_dir = (__file__).parent
    root_dir = script_dir.parent

    json_path = root_dir / "public" / "data" / "The_Curated_Grid_painting_data.json"
    output_image_dir = root_dir / "public" / "images"

    output_image_dir.mkdir(parents=True, exist_ok=True)

    if not json_path.exists():
        print(f"Couldn't find the .json file at: {json_path}. Make sure it's within public/data")
        return
    
    with open(json_path, "r", encoding="utf-8") as file:
        paintings = json.load(file)

    print(f"📦 Database Loaded: Found {len(paintings)} paintings waiting for artwork.\n")

    for i, item in enumerate(paintings, start=1):
        painting_id = item.get("id")
        painting_prompt = item.get("prompt")
        file_name = f"{painting_id}.png"
        target = output_image_dir / file_name

        if target.exists():
            print(f"⏩ [{i}/{len(paintings)}] Skipping '{file_name}' (File already exists).")
            continue

        prompt = urllib.parse.quote(painting_prompt)

        image_url = f"https://image.pollinations.ai/p/{prompt}?width=1024&height=1024&model=flux&nologo=true"

        try:
            response = requests.get(image_url, timeout=45)
            if response.status_code == 200:
                # Stream the raw image data directly onto your hard drive
                with open(target, "wb") as img_file:
                    img_file.write(response.content)
                print(f"   ✅ Saved -> public/images/{file_name}")
            else:
                print(f"   ❌ Server Issue: Couldn't render {file_name}. Status: {response.status_code}")
        except Exception as e:
            print(f"   💥 Connection Error on {file_name}: {e}")


if __name__ == "__main__":
    main()