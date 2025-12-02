# 📰 Article-Based AI Image Generator

A production-grade, article-to-image generation system built with **PyTorch 2.9.1**, **CUDA 13.0**, and **Stable Diffusion 2.1**. This application reads articles from `.docx` files, understands their context, and generates high-resolution, photorealistic images based on the article content.

## 🚀 Features

### Article Processing
- **Automatic Article Reading**: Reads `.docx` files from the `Articles/` directory
- **Intelligent Concept Extraction**: Analyzes article content to identify key visual concepts
- **Context-Aware Processing**: Understands article themes and generates relevant prompts

### High-Quality Image Generation
- **Stable Diffusion 2.1**: Advanced model for photorealistic, high-resolution images
- **GPU Acceleration**: Optimized for NVIDIA RTX 4050 (6GB VRAM) with CUDA 13.0
- **Multiple Styles**: Photorealistic, artistic, and cinematic styles
- **Crisp & Clear Output**: 768x768 native resolution with upscaling support
- **Memory Optimized**: Attention slicing, VAE slicing, and XFormers support

### Dual Generation Modes
1. **Article-Based Mode**: Automatically process articles and generate contextual images
2. **Manual Mode**: Traditional text-to-image generation with custom prompts

### User Interface
- **Streamlit Web UI**: Clean, intuitive interface
- **Batch Processing**: Generate images from multiple articles at once
- **Real-time Preview**: View concepts and prompts before generation
- **Download Support**: Save individual images or entire batches

## 🛠️ Technology Stack

- **Language**: Python 3.11+
- **Deep Learning**: PyTorch 2.9.1 with CUDA 13.0
- **ML Framework**: Diffusers, Transformers, Accelerate
- **Model**: Stable Diffusion 2.1 (stabilityai/stable-diffusion-2-1)
- **UI**: Streamlit
- **Document Processing**: python-docx, spaCy
- **Environment**: UV package manager

## 📋 Requirements

### Hardware
- **GPU**: NVIDIA RTX 4050 or better (6GB+ VRAM)
- **RAM**: 16GB+ recommended
- **Storage**: ~15GB free space for models and dependencies

### Software
- **OS**: Windows 10/11 (Linux/Mac compatible with minor script changes)
- **Python**: 3.11 or higher
- **CUDA**: 13.0 (installed with PyTorch)
- **UV**: Package manager (will be installed)

## ⚙️ Installation & Setup

### Option 1: Automated Setup (Recommended)

1. **Run the setup script**:
   ```bash
   setup.bat
   ```
   This will:
   - Create a UV virtual environment
   - Install PyTorch 2.9.1 with CUDA 13.0
   - Install all dependencies

2. **Verify installation**:
   ```bash
   TEST_SETUP.bat
   ```
   Watch the terminal output to confirm:
   - ✓ PyTorch 2.9.1 installed
   - ✓ CUDA 13.0 available
   - ✓ GPU detected
   - ✓ All modules loaded

### Option 2: Manual Setup

1. **Install UV** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Create virtual environment**:
   ```bash
   uv venv
   ```

3. **Activate environment**:
   ```bash
   .venv\Scripts\activate
   ```

4. **Install PyTorch with CUDA 13.0**:
   ```bash
   uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
   ```

5. **Install other dependencies**:
   ```bash
   uv pip install diffusers transformers accelerate streamlit python-docx spacy sentencepiece protobuf safetensors huggingface-hub
   ```

6. **Verify setup**:
   ```bash
   python test_setup.py
   ```

## 🏃‍♂️ Usage

### Running the Application

**Quick Start**:
```bash
RUN_APP.bat
```

**Manual Start**:
```bash
.venv\Scripts\activate
streamlit run app_article.py
```

The app will open in your browser at `http://localhost:8501`

### Article-Based Generation

1. **Place your articles** in the `Articles/` directory (`.docx` format)
2. **Open the app** and go to the "📂 Process Articles" tab
3. **Preview concepts** by clicking "🔍 Preview Concepts" for any article
4. **Generate images** by clicking "🚀 Generate Images from All Articles"
5. **Download** individual images or view them in the gallery

### Manual Generation

1. Go to the "🎨 Manual Generation" tab
2. Enter your custom prompt
3. Adjust settings in the sidebar (steps, CFG scale, resolution, style)
4. Click "🎨 Generate Images"
5. Download your generated images

## 📁 Project Structure

```
d:\Talrn assignment\
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration settings
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── image_generator.py   # Enhanced SD 2.1 generator
│   └── utils/
│       ├── __init__.py
│       ├── article_processor.py # Article reading & concept extraction
│       └── prompt_engineer.py   # Prompt optimization
├── Articles/                     # Place your .docx articles here
│   ├── article1.docx
│   ├── article2.docx
│   └── article3.docx
├── generated_images/            # Output directory for generated images
├── app_article.py               # Main Streamlit application
├── test_setup.py                # Environment verification script
├── pyproject.toml               # UV project configuration
├── requirements.txt             # Python dependencies
├── setup.bat                    # Automated setup script
├── RUN_APP.bat                  # Quick start script
├── TEST_SETUP.bat               # Test verification script
└── README.md                    # This file
```

## 🎨 Generation Tips

### For Best Quality
- Use **50-75 inference steps** for high quality
- Set **CFG scale to 7-9** for balanced results
- Use **768x768 resolution** (SD 2.1 native)
- Enable **photorealistic style** for realistic images

### Prompt Engineering
The system automatically enhances prompts with:
- Quality keywords: "highly detailed", "8k", "photorealistic"
- Lighting modifiers: "cinematic lighting", "natural lighting"
- Camera angles: "wide shot", "close-up", etc.

### Memory Management
For 6GB VRAM:
- Stick to 768x768 or lower resolution
- Generate 1-2 images at a time
- The system automatically enables memory optimizations

## 🔧 Configuration

Edit `config/settings.py` to customize:
- **Model selection**: Change to SDXL or other models
- **Default parameters**: Steps, CFG, resolution
- **Article processing**: Number of concepts per article
- **Output paths**: Where images are saved

## 📊 Example Workflow

1. **Add articles** to `Articles/` directory
2. **Run** `RUN_APP.bat`
3. **Navigate** to "Process Articles" tab
4. **Preview** extracted concepts
5. **Generate** images from all articles
6. **Review** generated images in gallery
7. **Download** desired images

## ⚠️ Troubleshooting

### CUDA Not Available
- Ensure NVIDIA drivers are up to date
- Verify CUDA toolkit installation
- Check GPU compatibility

### Out of Memory Errors
- Reduce resolution (512x512)
- Lower number of inference steps
- Generate fewer images at once

### Model Download Issues
- First run downloads ~5GB model (SD 2.1)
- Ensure stable internet connection
- Models cached in `.cache/` directory

## 🤝 Ethical Use

- Generate responsible, appropriate content
- Respect copyright and intellectual property
- Use for educational and creative purposes
- Generated images may contain AI watermarks

## 📝 Technical Details

### Optimizations Implemented
- ✅ Attention slicing for memory efficiency
- ✅ VAE slicing for large images
- ✅ XFormers memory-efficient attention
- ✅ DPM++ scheduler for better quality
- ✅ Float16 precision on GPU
- ✅ Model caching for faster subsequent runs

### Article Processing Pipeline
1. Read `.docx` files using python-docx
2. Clean and normalize text
3. Extract key sentences using scoring algorithm
4. Generate visual concepts from sentences
5. Enhance concepts with quality keywords
6. Create optimized prompts for SD 2.1

---

**Built for Talrn Remote ML Internship Task Assessment**

*Developed with PyTorch 2.9.1 + CUDA 13.0 | Stable Diffusion 2.1*
