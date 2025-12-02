# AI Article-to-Image Generator

## Overview

This application generates photorealistic images from article content using advanced AI models. It combines intelligent article understanding with state-of-the-art image generation to create crisp, clear, high-resolution, realistic images.

## Technologies

- **Groq Llama 3.3 (70B)** - Article understanding and prompt generation
- **Realistic Vision V6.0** - Photorealistic image generation
- **Python 3.12 + PyTorch 2.9.1 + CUDA 13.0** - Core framework
- **Streamlit 1.42.0** - Web interface

## Key Features

✅ **Context-Aware**: AI reads and understands article content  
✅ **Photorealistic**: Generates crisp, clear, high-resolution images  
✅ **Safe Content**: Double-layer filtering ensures professional imagery  
✅ **Customizable**: Professional presets and full manual control  
✅ **User-Friendly**: Simple 4-step workflow with regeneration options

## Task Requirements Met

| Requirement | Implementation | Status |
|------------|----------------|--------|
| **Understand article context** | Groq Llama 3.3 (70B) | ✅ |
| **Crisp and clear images** | 512x768 + Realistic Vision V6.0 | ✅ |
| **High resolution** | Configurable up to 1024x768 | ✅ |
| **Realistic images** | Realistic Vision V6.0 (photo-trained) | ✅ |
| **Safe content** | Double-layer safety filters | ✅ |

## Installation

### Requirements
- Python 3.12+
- NVIDIA GPU with 6GB+ VRAM (CUDA 13.0)
- Groq API Key (free from console.groq.com)

### Setup Steps

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

4. **Get Groq API Key**:
   - Visit: https://console.groq.com
   - Sign up (free)
   - Create API key
   - Add to `.env` file

5. **Run application**:
   ```bash
   streamlit run app_article.py
   ```

6. **Open browser**: http://localhost:8501

## Usage

### Simple 4-Step Workflow:

1. **Select Article** - Choose from dropdown menu
2. **Generate Prompts** - AI analyzes article content
3. **Review Prompts** - Check AI-generated descriptions (regenerate if needed)
4. **Render Images** - Create photorealistic images
5. **Download** - Save individual images

## Generation Settings

### Professional Presets:
- **Photorealistic (Recommended)**: 40 steps, CFG 5.0, 512x768 ⭐
- **High Detail**: 50 steps, CFG 6.0, 1024x768
- **Balanced**: 35 steps, CFG 5.5, 768x512
- **Fast**: 30 steps, CFG 5.0, 512x512

### Custom Settings:
- **Inference Steps**: 20-100 (recommended: 40-50)
- **CFG Scale**: 1.0-15.0 (professional: 5.0)
- **Resolution**: Up to 1024x1024
- **Fixed Seed**: Optional for reproducible results

## Project Structure

```
├── Articles/                 # Input articles (.docx files)
├── config/
│   └── settings.py          # Model and generation configuration
├── src/
│   ├── models/
│   │   └── image_generator.py  # Image generation logic
│   └── utils/
│       ├── article_processor.py  # Article analysis with Groq LLM
│       └── prompt_engineer.py    # Prompt enhancement utilities
├── generated_images/        # Output directory
├── .env                     # Environment variables (not committed)
├── .env.example            # Environment template
├── app_article.py          # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Safety Features

### 1. LLM Prompt Safety
- Strict instructions ensure context-only prompts
- Professional, workplace-appropriate content only
- No sensitive or controversial imagery

### 2. Image Generation Safety
- Comprehensive negative prompts filter NSFW content
- Blocks inappropriate, vulgar, or offensive imagery
- Double-layer protection (LLM + image generation)

## Technical Specifications

- **Image Model**: SG161222/Realistic_Vision_V6.0_B1_noVAE
- **LLM**: Groq Llama 3.3-70B-Versatile
- **Framework**: PyTorch 2.9.1 + CUDA 13.0
- **UI**: Streamlit 1.42.0
- **GPU**: Optimized for 6GB VRAM

### Performance (RTX 4050 Laptop, 6GB VRAM):

| Resolution | Steps | Time per Image | VRAM Usage |
|-----------|-------|----------------|------------|
| 512x512 | 30 | ~10s | ~3.5GB |
| 512x768 | 40 | ~15s | ~4.0GB |
| 768x768 | 40 | ~18s | ~5.0GB |
| 1024x768 | 50 | ~25s | ~5.8GB |


## License

This project was created for the Talrn internship assignment.


**Created by**: [Mayuresh Chavan]  
**Date**: December 3, 2025  

