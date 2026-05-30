$code = @'
import os
import json
import torch
from pathlib import Path
from diffusers import AutoPipelineForText2Image

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

    print("🤖 Initializing Local On-Device AI Engine...")
    
    # Auto-detect hardware acceleration (CUDA for NVIDIA, CPU for standard machines)
    if torch.cuda.is_available():
        device = "cuda"
        torch_dtype = torch.float16
        print("🚀 NVIDIA Graphics Core Detected! Enabling GPU acceleration.")
    else:
        device = "cpu"
        torch_dtype = torch.float32
        print("💻 Standard Hardware Detected. Running engine via system processor safely.")

    try:
        # Load a highly efficient, single-step local AI pipeline
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", 
            torch_dtype=torch_dtype, 
            variant="fp16" if device == "cuda" else None
        ).to(device)
        print("✅ AI Model Loaded into hardware memory successfully!\n")
    except Exception as e:
        print(f"💥 Failed to load model framework: {e}")
        return

    print(f"📦 Database Loaded: Processing {len(paintings)} prompts completely offline...\n")

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

        print(f"🎨 [{i}/{len(paintings)}] Rendering local AI art for: \"{title}\"...")

        try:
            # Generate the image locally using 1 single super-step
            result = pipe(
                prompt=painting_prompt, 
                num_inference_steps=1, 
                guidance_scale=0.0,
                width=512,
                height=512
            )
            
            image = result.images[0]
            image.save(target)
            print(f"   ✅ Saved locally -> public/images/{file_name}")
                
        except Exception as e:
            print(f"   ❌ Generation failed for this item: {e}")

    print("\n🚀 All AI assets have been successfully created locally on your machine!")

if __name__ == "__main__":
    main()
'@

Out-File -FilePath .\image_generation.py -InputObject $code -Encoding utf8