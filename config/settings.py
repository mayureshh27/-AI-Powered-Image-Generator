MODEL_CONFIG = {
    "model_id": "SG161222/Realistic_Vision_V6.0_B1_noVAE",
    "torch_dtype": "float16",
    "enable_attention_slicing": True,
    "enable_vae_slicing": True,
}

GENERATION_CONFIG = {
    "default_steps": 40,
    "default_cfg_scale": 5.0,
    "default_height": 768,
    "default_width": 512,
    "max_images": 4,
    "negative_prompt_default": "cartoon, 3d, disfigured, bad art, deformed, poorly drawn, extra limbs, close up, b&w, weird colors, blurry"
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
