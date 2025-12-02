import torch
import sys
from pathlib import Path

print("=" * 60)
print("🔍 ENVIRONMENT VERIFICATION")
print("=" * 60)

print(f"\n✓ Python Version: {sys.version.split()[0]}")
print(f"✓ PyTorch Version: {torch.__version__}")

cuda_available = torch.cuda.is_available()
print(f"✓ CUDA Available: {cuda_available}")

if cuda_available:
    print(f"✓ CUDA Version: {torch.version.cuda}")
    print(f"✓ GPU Device: {torch.cuda.get_device_name(0)}")
    print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    print(f"✓ Number of GPUs: {torch.cuda.device_count()}")
else:
    print("⚠ CUDA not available - will run on CPU (slower)")

print("\n" + "=" * 60)
print("📦 TESTING IMPORTS")
print("=" * 60)

try:
    from diffusers import StableDiffusionPipeline
    print("✓ Diffusers imported successfully")
except Exception as e:
    print(f"❌ Diffusers import failed: {e}")

try:
    from transformers import CLIPTextModel
    print("✓ Transformers imported successfully")
except Exception as e:
    print(f"❌ Transformers import failed: {e}")

try:
    import streamlit
    print(f"✓ Streamlit imported successfully (v{streamlit.__version__})")
except Exception as e:
    print(f"❌ Streamlit import failed: {e}")

try:
    from docx import Document
    print("✓ python-docx imported successfully")
except Exception as e:
    print(f"❌ python-docx import failed: {e}")

try:
    import spacy
    print(f"✓ spaCy imported successfully (v{spacy.__version__})")
except Exception as e:
    print(f"❌ spaCy import failed: {e}")

print("\n" + "=" * 60)
print("🔧 TESTING CUSTOM MODULES")
print("=" * 60)

sys.path.append(str(Path(__file__).parent))

try:
    from config.settings import MODEL_CONFIG, GENERATION_CONFIG
    print("✓ Config module loaded")
    print(f"  - Model: {MODEL_CONFIG['model_id']}")
    print(f"  - Default resolution: {GENERATION_CONFIG['default_height']}x{GENERATION_CONFIG['default_width']}")
except Exception as e:
    print(f"❌ Config module failed: {e}")

try:
    from src.utils.article_processor import ArticleProcessor
    processor = ArticleProcessor()
    articles = processor.get_all_articles()
    print(f"✓ ArticleProcessor loaded")
    print(f"  - Found {len(articles)} article(s) in Articles/ directory")
except Exception as e:
    print(f"❌ ArticleProcessor failed: {e}")

try:
    from src.utils.prompt_engineer import PromptEngineer
    engineer = PromptEngineer()
    print("✓ PromptEngineer loaded")
except Exception as e:
    print(f"❌ PromptEngineer failed: {e}")

print("\n" + "=" * 60)
print("✅ VERIFICATION COMPLETE")
print("=" * 60)
print("\n💡 Next steps:")
print("   1. Run: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux/Mac)")
print("   2. Run: streamlit run app_article.py")
print("   3. Open browser at http://localhost:8501")
print("\n")
