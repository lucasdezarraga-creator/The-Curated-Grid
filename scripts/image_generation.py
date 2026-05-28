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

        # Smart Skip: This will safely skip painting-01, 02, and 03 since you already have them!
        if target.exists():
            print(f"⏩ [{i}/{len(paintings)}] Skipping '{file_name}' (File already exists).")
            continue

        print(f"🎨 [{i}/{len(paintings)}] Generating asset for \"{item.get('title', painting_id)}\"...")
        prompt = urllib.parse.quote(painting_prompt)
        
        # Using the standard, completely unrestricted default engine path
        image_url = f"https://image.pollinations.ai/p/{prompt}?width=1024&height=1024&nologo=true"

        try:
            response = requests.get(image_url, timeout=45)
            if response.status_code == 200:
                with open(target, "wb") as img_file:
                    img_file.write(response.content)
                print(f"   ✅ Saved -> public/images/{file_name}")
                
                # Take a breath for 3 seconds so the server stays happy
                print("   ⏳ Pausing briefly to avoid rate limits...")
                time.sleep(3)
            else:
                print(f"   ❌ Server Issue: Couldn't render {file_name}. Status: {response.status_code}")
                print("   ⏳ Pausing longer to clear server flags...")
                time.sleep(5)
        except Exception as e:
            print(f"   💥 Connection Error on {file_name}: {e}")
            time.sleep(5)

    print("\n🚀 Asset sync complete! Your React frontend is now fully populated.")

if __name__ == "__main__":
    main()