# AI Article-to-Image Generator

**Talrn Internship Assignment** - Context-aware, photorealistic image generation from articles using AI.

## Overview

This application uses advanced AI models to analyze article content and generate professional-quality, photorealistic images that accurately represent the text. It combines:
- **Groq Llama 3.3 (70B)** for intelligent article understanding
- **Realistic Vision V6.0** for photorealistic image generation
- **Streamlit** for an intuitive web interface

## Features

✅ **Context-Aware**: AI reads and understands article content  
✅ **Photorealistic**: Generates crisp, clear, high-resolution images  
✅ **Safe Content**: Filters ensure professional, workplace-appropriate imagery  
✅ **Customizable**: Adjustable quality settings (steps, CFG, resolution)  
✅ **User-Friendly**: Simple 4-step workflow with regeneration options

## Requirements

- Python 3.12+
- NVIDIA GPU with 6GB+ VRAM (CUDA 13.0)
- Groq API Key (free from console.groq.com)

## Installation

1. **Clone or download this repository**

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

5. **Get Groq API Key**:
   - Visit: https://console.groq.com
   - Sign up (free)
   - Create API key
   - Add to `.env` file

## Usage

1. **Start the application**:
   ```bash
   streamlit run app_article.py
   ```

2. **Open in browser**: http://localhost:8501

3. **Generate images**:
   - Select an article from the dropdown
   - Click "Generate Prompts" to analyze the article
   - Review AI-generated prompts (or regenerate if needed)
   - Click "Render All Images" to create photorealistic images
   - Download individual images

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

## Configuration

### Generation Settings (Sidebar)
- **Inference Steps**: 30-60 (default: 40)
- **Guidance Scale**: 4.0-9.0 (default: 5.0)
- **Resolution**: 512x768 (recommended for portrait)

### Model Configuration (`config/settings.py`)
- Model: Realistic Vision V6.0
- Default CFG: 5.0 (optimized for realism)
- Default Steps: 40
- Resolution: 512x768 portrait

## Safety Features

- **Content Filtering**: LLM instructions ensure professional, workplace-appropriate prompts
- **Negative Prompts**: Automatically filters NSFW/inappropriate content
- **Context-Only**: Images generated strictly from article content

## Technical Specifications

- **Image Model**: SG161222/Realistic_Vision_V6.0_B1_noVAE
- **LLM**: Groq Llama 3.3-70B-Versatile
- **Framework**: PyTorch 2.9.1 + CUDA 13.0
- **UI**: Streamlit 1.42.0
- **GPU**: Optimized for 6GB VRAM

## Troubleshooting

### "GROQ_API_KEY not found"
- Ensure `.env` file exists with valid API key
- Format: `GROQ_API_KEY=gsk_your_key_here`

### Out of memory
- Lower resolution to 512x512
- Reduce batch size to 1 image at a time
- Close other GPU applications

### Slow generation
- Expected: 30-60 seconds per image on RTX 4050
- Verify GPU is being used (check terminal output)

## License

This project was created for the Talrn internship assignment.

## Contact

For questions or issues, please contact the development team.
