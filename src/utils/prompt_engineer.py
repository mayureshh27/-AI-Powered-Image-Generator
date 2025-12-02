from typing import List, Dict
import random


class PromptEngineer:
    
    def __init__(self):
        self.quality_enhancers = [
            "highly detailed",
            "8k resolution",
            "photorealistic",
            "professional photography",
            "crisp and clear",
            "sharp focus",
            "high quality",
            "masterpiece",
            "ultra detailed"
        ]
        
        self.style_modifiers = [
            "cinematic lighting",
            "dramatic lighting",
            "natural lighting",
            "studio lighting",
            "golden hour",
        ]
        
        self.camera_angles = [
            "wide angle shot",
            "close-up",
            "medium shot",
            "establishing shot",
            "aerial view"
        ]
        
        self.negative_prompt = (
            "blurry, low quality, distorted, ugly, bad anatomy, "
            "extra limbs, watermark, text, signature, low resolution, "
            "pixelated, jpeg artifacts, out of focus"
        )
    
    def enhance_concept(self, concept: str, style: str = "photorealistic") -> str:
        quality = random.sample(self.quality_enhancers, 3)
        lighting = random.choice(self.style_modifiers)
        
        enhanced = f"{concept}, {', '.join(quality)}, {lighting}"
        
        if style == "photorealistic":
            enhanced += ", professional photography, realistic"
        elif style == "artistic":
            enhanced += ", digital art, concept art, trending on artstation"
        elif style == "cinematic":
            enhanced += ", cinematic composition, movie still, film grain"
        
        return enhanced
    
    def create_prompt(self, concept: str, style: str = "photorealistic", 
                     add_camera_angle: bool = False) -> str:
        prompt = self.enhance_concept(concept, style)
        
        if add_camera_angle:
            angle = random.choice(self.camera_angles)
            prompt = f"{prompt}, {angle}"
        
        return prompt
    
    def create_prompts_from_concepts(self, concepts: List[str], 
                                    style: str = "photorealistic") -> List[Dict]:
        prompts = []
        
        for i, concept in enumerate(concepts):
            prompt = self.create_prompt(concept, style, add_camera_angle=True)
            prompts.append({
                "concept_index": i,
                "original_concept": concept,
                "enhanced_prompt": prompt,
                "negative_prompt": self.negative_prompt,
                "style": style
            })
        
        return prompts
    
    def get_negative_prompt(self) -> str:
        return self.negative_prompt
