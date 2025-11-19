import torch
from diffusers import StableDiffusionPipeline
import os
from datetime import datetime
import json
from PIL import Image

class ImageGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device=None):
        self.model_id = model_id
        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Initializing model on {self.device}...")
        
        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id, 
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            self.pipe.to(self.device)
            # Enable attention slicing for lower memory usage if on CUDA
            if self.device == "cuda":
                self.pipe.enable_attention_slicing()
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e

    def generate(self, prompt, negative_prompt=None, num_images=1, steps=50, cfg_scale=7.5, height=512, width=512):
        """
        Generates images based on the prompt.
        """
        if self.device == "cpu":
            # MPS for Mac M1/M2 if available, but standard fallback is CPU
            # Note: float16 is not always supported on CPU, so we used float32 above
            pass

        images = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=cfg_scale,
            height=height,
            width=width,
            num_images_per_prompt=num_images
        ).images
        
        return images

    def save_image(self, image, prompt, params, output_dir="generated_images"):
        """
        Saves the image and metadata.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create a safe filename
        safe_prompt = "".join([c for c in prompt[:20] if c.isalnum() or c in (' ', '_')]).strip().replace(" ", "_")
        base_filename = f"{timestamp}_{safe_prompt}"
        
        image_path = os.path.join(output_dir, f"{base_filename}.png")
        image.save(image_path)
        
        metadata = {
            "prompt": prompt,
            "timestamp": timestamp,
            "parameters": params,
            "image_path": image_path
        }
        
        metadata_path = os.path.join(output_dir, f"{base_filename}.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)
            
        return image_path, metadata_path
