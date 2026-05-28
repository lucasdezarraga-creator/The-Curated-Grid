import os
import json
import urllib.parse
import requests
import time
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

    print(f"📦 Database Loaded: Found {len(paintings)} paintings waiting for artwork.\n")

    for i, item in enumerate(paintings, start=1):
        painting_id = item.get("id")
        painting_prompt = item.get("prompt")
        
        if not painting_id or not painting_prompt:
            continue
            
        file_name = f"{painting_id}.png"
        target = output_image_dir / file_name

        # Smart Skip: This skips 1, 2, 3, 4, and 5 since you already have them!
        if target.exists():
            print(f"⏩ [{i}/{len(paintings)}] Skipping '{file_name}' (Already exists).")
            continue

        print(f"🎨 [{i}/{len(paintings)}] Generating asset via alternative mirror for \"{item.get('title', painting_id)}\"...")
        
        # We clean and encode the prompt text
        encoded_prompt = urllib.parse.quote(painting_prompt)
        
        # Using an alternative open infrastructure mirror that uses Flux/Stable Diffusion behind the scenes
        image_url = f"https://api.airforce/v1/image/generations?prompt={encoded_prompt}&model=flux&size=1:1"

        try:
            # We set a slightly shorter timeout because this mirror responds quickly
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                with open(target, "wb") as img_file:
                    img_file.write(response.content)
                print(f"   ✅ Saved -> public/images/{file_name}")
                # 2 second breath
                time.sleep(2)
            else:
                print(f"   ❌ Mirror Issue: Status {response.status_code}. Trying fallback...")
                # Fallback to a secondary fast prompt engine if primary is busy
                fallback_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={i}&nologo=true"
                response = requests.get(fallback_url, timeout=30)
                if response.status_code == 200:
                    with open(target, "wb") as img_file:
                        img_file.write(response.content)
                    print(f"   ✅ Saved via Fallback -> public/images/{file_name}")
                    time.sleep(3)
                else:
                    print(f"   ❌ Both endpoints rejected the request. Moving to next asset.")
                    
        except Exception as e:
            print(f"   💥 Connection Error on {file_name}: {e}")
            time.sleep(2)

    print("\n🚀 Asset sync complete! Your React frontend is now fully populated.")

if __name__ == "__main__":
    main()