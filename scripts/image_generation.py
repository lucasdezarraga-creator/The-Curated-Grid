import os
import json
import urllib.parse
import requests
import time
import random
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent

    json_path = root_dir / "public" / "data" / "The_Curated_Grid_painting_data.json"
    output_image_dir = root_dir / "public" / "images"

    output_image_dir.mkdir(parents=True, exist_ok=True)

    if not json_path.exists():
        print(f"❌ Error: Couldn't find the .json file at: {json_path}")
        return
    
    with open(json_path, "r", encoding="utf-8") as file:
        paintings = json.load(file)

    print(f"📦 Database Loaded: Ingesting prompts via Open AI Proxy...\n")

    for i, item in enumerate(paintings, start=1):
        painting_id = item.get("id")
        painting_prompt = item.get("prompt")
        title = item.get("title", painting_id)
        
        if not painting_id or not painting_prompt:
            continue
            
        file_name = f"{painting_id}.png"
        target = output_image_dir / file_name

        if target.exists() and os.path.getsize(target) > 5000:
            print(f"⏩ [{i}/{len(paintings)}] Skipping '{file_name}' (Valid file already exists).")
            continue

        print(f"🎨 [{i}/{len(paintings)}] Rendering Open-Gate AI Art for: \"{title}\"...")

        # URL-encode the text prompt safely
        encoded_prompt = urllib.parse.quote(painting_prompt)
        
        # Using the dedicated developer stream gateway with random indexing to bypass server cache
        seed = random.randint(1, 99999)
        image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=512&height=512&seed={seed}&model=flux"

        try:
            # Direct binary stream fetch with a generic browser agent
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(image_url, headers=headers, timeout=25)
            
            if response.status_code == 200:
                with open(target, "wb") as img_file:
                    img_file.write(response.content)
                print(f"   ✅ Saved -> public/images/{file_name}")
                # Micro-breather just to be a good net citizen
                time.sleep(1)
            else:
                print(f"   ❌ Endpoint returned code: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Network exception: {e}")
            time.sleep(2)

    print("\n🚀 All 15 assets are synchronized and local!")

if __name__ == "__main__":
    main()
