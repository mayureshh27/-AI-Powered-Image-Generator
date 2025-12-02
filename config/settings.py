MODEL_CONFIG = {
    "model_id": "runwayml/stable-diffusion-v1-5",
    "torch_dtype": "float16",
    "enable_attention_slicing": True,
    "enable_vae_slicing": True,
}

GENERATION_CONFIG = {
    "default_steps": 50,
    "default_cfg_scale": 7.5,
    "default_height": 768,
    "default_width": 768,
    "max_images": 4,
    "negative_prompt_default": "blurry, low quality, distorted, ugly, bad anatomy, extra limbs, watermark, text, signature"
}

ARTICLE_CONFIG = {
    "max_concepts_per_article": 3,
    "min_text_length": 100,
    "quality_keywords": ["highly detailed", "8k", "photorealistic", "professional photography", "crisp", "sharp focus"],
}

PATHS = {
    "articles_dir": "Articles",
    "output_dir": "generated_images",
    "models_cache": ".cache/models"
}
