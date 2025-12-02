import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import os
from datetime import datetime
import json
from PIL import Image
from typing import List, Optional
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import MODEL_CONFIG, GENERATION_CONFIG, PATHS


class ImageGenerator:
    
    def __init__(self, model_id: Optional[str] = None, device: Optional[str] = None):
        self.model_id = model_id or MODEL_CONFIG["model_id"]
        
        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"🚀 Initializing {self.model_id} on {self.device}...")
        print(f"   CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   CUDA Version: {torch.version.cuda}")
        
        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
            )
            
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            self.pipe.to(self.device)
            
            if self.device == "cuda":
                self.pipe.enable_attention_slicing()
                self.pipe.enable_vae_slicing()
                try:
                    self.pipe.enable_xformers_memory_efficient_attention()
                    print("   ✓ XFormers enabled for better performance")
                except Exception:
                    print("   ⚠ XFormers not available, using standard attention")
            
            print("✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise e
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        num_images: int = 1,
        steps: int = 50,
        cfg_scale: float = 7.5,
        height: int = 768,
        width: int = 768,
        seed: Optional[int] = None
    ) -> List[Image.Image]:
        
        if negative_prompt is None:
            negative_prompt = GENERATION_CONFIG["negative_prompt_default"]
        
        safety_negative = "nsfw, nude, naked, sexual, explicit, adult content, inappropriate, vulgar, offensive, violence, gore, disturbing"
        negative_prompt = f"{negative_prompt}, {safety_negative}"
        
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        
        print(f"\n🎨 Generating {num_images} image(s)...")
        print(f"   Prompt: {prompt[:100]}...")
        print(f"   Steps: {steps}, CFG: {cfg_scale}, Size: {width}x{height}")
        
        try:
            images = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                guidance_scale=cfg_scale,
                height=height,
                width=width,
                num_images_per_prompt=num_images,
                generator=generator
            ).images
            
            print(f"✅ Generated {len(images)} image(s) successfully!")
            return images
            
        except Exception as e:
            print(f"❌ Error during generation: {e}")
            raise e
    
    def save_image(
        self,
        image: Image.Image,
        prompt: str,
        params: dict,
        output_dir: Optional[str] = None,
        article_name: Optional[str] = None
    ) -> tuple:
        
        if output_dir is None:
            output_dir = PATHS["output_dir"]
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if article_name:
            safe_name = "".join([c for c in article_name[:30] if c.isalnum() or c in (' ', '_')]).strip().replace(" ", "_")
            base_filename = f"{timestamp}_{safe_name}"
        else:
            safe_prompt = "".join([c for c in prompt[:20] if c.isalnum() or c in (' ', '_')]).strip().replace(" ", "_")
            base_filename = f"{timestamp}_{safe_prompt}"
        
        image_path = os.path.join(output_dir, f"{base_filename}.png")
        image.save(image_path, quality=95)
        
        metadata = {
            "prompt": prompt,
            "timestamp": timestamp,
            "parameters": params,
            "image_path": image_path,
            "model_id": self.model_id,
            "article_source": article_name
        }
        
        metadata_path = os.path.join(output_dir, f"{base_filename}.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        
        return image_path, metadata_path
    
    def generate_from_article_concepts(
        self,
        concepts: List[str],
        prompts_data: List[dict],
        article_name: str,
        **generation_kwargs
    ) -> List[dict]:
        
        results = []
        
        for i, prompt_data in enumerate(prompts_data):
            print(f"\n📄 Processing concept {i+1}/{len(prompts_data)} from '{article_name}'")
            
            images = self.generate(
                prompt=prompt_data["enhanced_prompt"],
                negative_prompt=prompt_data["negative_prompt"],
                num_images=1,
                **generation_kwargs
            )
            
            params = {
                **generation_kwargs,
                "concept": prompt_data["original_concept"],
                "style": prompt_data["style"]
            }
            
            img_path, meta_path = self.save_image(
                images[0],
                prompt_data["enhanced_prompt"],
                params,
                article_name=article_name
            )
            
            results.append({
                "concept_index": i,
                "concept": prompt_data["original_concept"],
                "prompt": prompt_data["enhanced_prompt"],
                "image_path": img_path,
                "metadata_path": meta_path
            })
        
        return results
