import streamlit as st
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.models.image_generator import ImageGenerator
from src.utils.article_processor import ArticleProcessor
from config.settings import PATHS

st.set_page_config(
    page_title="Talrn AI Assignment - Image Generator",
    page_icon="📰",
    layout="wide"
)

if "current_images" not in st.session_state:
    st.session_state.current_images = []
if "prompts" not in st.session_state:
    st.session_state.prompts = []
if "current_article" not in st.session_state:
    st.session_state.current_article = None

@st.cache_resource
def load_core():
    return ImageGenerator(), ArticleProcessor(PATHS["articles_dir"])

try:
    generator, processor = load_core()
    st.success("✅ AI Models loaded: Realistic Vision V6.0 + Groq Llama 3.3")
except Exception as e:
    st.error(f"❌ System Error: {e}")
    st.info("💡 Make sure your GROQ_API_KEY is set in the .env file")
    st.stop()

with st.sidebar:
    st.header("⚙️ Generation Settings")
    
    st.subheader("🎨 Quality Presets")
    preset = st.selectbox(
        "Choose Preset",
        ["Custom", "Photorealistic (Recommended)", "High Detail", "Balanced", "Fast"],
        help="Professional presets optimized for different use cases"
    )
    
    if preset == "Photorealistic (Recommended)":
        steps = 40
        cfg = 5.0
        height, width = 768, 512
    elif preset == "High Detail":
        steps = 50
        cfg = 6.0
        height, width = 1024, 768
    elif preset == "Balanced":
        steps = 35
        cfg = 5.5
        height, width = 768, 512
    elif preset == "Fast":
        steps = 30
        cfg = 5.0
        height, width = 512, 512
    else:
        st.markdown("---")
        st.subheader("Custom Settings")
        
        steps = st.slider(
            "Inference Steps",
            min_value=20,
            max_value=100,
            value=40,
            step=5,
            help="More steps = better quality but slower. Recommended: 40-50"
        )
        
        st.markdown("**CFG Scale (Guidance)**")
        cfg_preset = st.radio(
            "CFG Preset",
            ["Professional (5.0)", "Detailed (6.0)", "Artistic (7.5)", "Custom"],
            horizontal=True,
            help="How closely the model follows your prompt"
        )
        
        if cfg_preset == "Professional (5.0)":
            cfg = 5.0
        elif cfg_preset == "Detailed (6.0)":
            cfg = 6.0
        elif cfg_preset == "Artistic (7.5)":
            cfg = 7.5
        else:
            cfg = st.slider(
                "Custom CFG",
                min_value=1.0,
                max_value=15.0,
                value=5.0,
                step=0.5,
                help="Lower = more creative, Higher = more literal. Sweet spot: 5.0-7.0"
            )
        
        st.markdown("**Resolution**")
        res_preset = st.radio(
            "Aspect Ratio",
            ["Portrait (512x768)", "Square (768x768)", "Landscape (768x512)", "Custom"],
            help="Choose aspect ratio for your images"
        )
        
        if res_preset == "Portrait (512x768)":
            width, height = 512, 768
        elif res_preset == "Square (768x768)":
            width, height = 768, 768
        elif res_preset == "Landscape (768x512)":
            width, height = 768, 512
        else:
            col1, col2 = st.columns(2)
            with col1:
                width = st.selectbox("Width", [512, 768, 1024], index=0)
            with col2:
                height = st.selectbox("Height", [512, 768, 1024], index=1)
    
    st.markdown("---")
    st.subheader("🎲 Advanced Options")
    
    use_seed = st.checkbox("Use Fixed Seed", help="Enable for reproducible results")
    seed = None
    if use_seed:
        seed = st.number_input("Seed", min_value=0, max_value=999999, value=42, help="Same seed = same image")
    
    st.markdown("---")
    st.info(f"""
    **Current Settings:**
    - Steps: {steps}
    - CFG: {cfg}
    - Resolution: {width}x{height}
    - Seed: {"Fixed (" + str(seed) + ")" if seed is not None else "Random"}
    
    **Estimated Time:** {steps // 3}-{steps // 2}s per image
    """)
    
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.caption("""
    **Model:** Realistic Vision V6.0  
    **LLM:** Groq Llama 3.3 (70B)  
    **GPU:** CUDA-accelerated
    
    **Safety:** All content filtered for professional use.
    """)
    
    if st.button("🗑️ Clear Session", width="stretch"):
        st.session_state.current_images = []
        st.session_state.prompts = []
        st.session_state.current_article = None
        st.rerun()

st.title("📰 AI Article-to-Image Generator")
st.markdown("""
**Talrn Internship Assignment:** Context-aware, photorealistic image generation from articles using AI.

This tool analyzes article content and generates professional-quality images that accurately represent the text.
""")

col_input, col_output = st.columns([1, 2])

with col_input:
    st.subheader("📄 Step 1: Select Article")
    articles = processor.get_all_articles()
    
    if not articles:
        st.warning(f"⚠️ No articles found in `{PATHS['articles_dir']}/` directory")
        st.info("💡 Add .docx files to the Articles folder and refresh the page")
        st.stop()
    
    st.caption(f"Found {len(articles)} article(s) in the Articles directory")
    
    selected_file = st.selectbox(
        "Choose an article:",
        articles,
        format_func=lambda x: os.path.basename(x),
        help="Select the article you want to generate images from"
    )
    
    article_name = os.path.basename(selected_file)
    
    st.markdown("---")
    st.subheader("🧠 Step 2: Generate Visual Prompts")
    st.caption("AI will read your article and create photorealistic scene descriptions")
    
    num_concepts = st.slider(
        "Number of images:",
        1, 5, 3,
        help="How many different scenes to generate from the article"
    )
    
    col_gen, col_regen = st.columns(2)
    
    with col_gen:
        if st.button("✨ Generate Prompts", type="primary", width="stretch"):
            st.session_state.current_images = []
            
            with st.spinner("🤖 AI is analyzing the article and creating visual prompts..."):
                data = processor.process_article(selected_file, max_concepts=num_concepts)
                
                if "error" in data:
                    st.error(f"❌ Error: {data['error']}")
                    st.info("💡 Check your GROQ_API_KEY in the .env file")
                else:
                    st.session_state.prompts = data["concepts"]
                    st.session_state.current_article = article_name
                    st.success(f"✅ Generated {len(data['concepts'])} contextual prompts!")
                    st.rerun()
    
    with col_regen:
        if st.session_state.prompts:
            if st.button("🔄 Regenerate", width="stretch", help="Generate different prompts if you don't like these"):
                st.session_state.current_images = []
                
                with st.spinner("🤖 Generating new prompts..."):
                    data = processor.process_article(selected_file, max_concepts=num_concepts)
                    
                    if "error" in data:
                        st.error(f"❌ Error: {data['error']}")
                    else:
                        st.session_state.prompts = data["concepts"]
                        st.success(f"✅ Regenerated {len(data['concepts'])} new prompts!")
                        st.rerun()
    
    if st.session_state.prompts and st.session_state.current_article:
        st.markdown("---")
        st.subheader("📝 Step 3: Review AI Prompts")
        st.caption(f"**Article:** {st.session_state.current_article}")
        st.info("These prompts are generated from your article content. If you don't like them, click 'Regenerate' above.")
        
        for i, prompt in enumerate(st.session_state.prompts):
            with st.expander(f"🎨 Scene {i+1}", expanded=True):
                st.write(prompt)
        
        st.markdown("---")
        st.subheader("🚀 Step 4: Generate Images")
        st.caption(f"This will create {len(st.session_state.prompts)} photorealistic image(s)")
        
        if st.button("🎨 Render All Images", type="primary", width="stretch"):
            st.session_state.current_images = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, prompt in enumerate(st.session_state.prompts):
                status_text.text(f"🎨 Rendering scene {idx+1}/{len(st.session_state.prompts)}... (30-60 seconds)")
                
                enhanced_prompt = f"{prompt}, raw photo, 8k uhd, dslr, soft lighting, high quality, film grain, photorealistic, professional photography"
                
                try:
                    imgs = generator.generate(
                        enhanced_prompt,
                        num_images=1,
                        steps=steps,
                        cfg_scale=cfg,
                        height=height,
                        width=width,
                        seed=seed
                    )
                    
                    path, meta_path = generator.save_image(
                        imgs[0],
                        prompt,
                        {
                            "source": st.session_state.current_article,
                            "steps": steps,
                            "cfg_scale": cfg,
                            "height": height,
                            "width": width
                        },
                        article_name=st.session_state.current_article.replace('.docx', '')
                    )
                    
                    st.session_state.current_images.append({
                        "image": imgs[0],
                        "path": path,
                        "prompt": prompt,
                        "article": st.session_state.current_article
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error generating image {idx+1}: {e}")
                
                progress_bar.progress((idx + 1) / len(st.session_state.prompts))
            
            status_text.text("✅ All images generated!")
            st.success(f"🎉 Successfully generated {len(st.session_state.prompts)} photorealistic images!")
            st.balloons()
            st.rerun()

with col_output:
    st.subheader("🖼️ Generated Images")
    
    if not st.session_state.current_images:
        st.info("""
        📸 **Generated images will appear here**
        
        **Quick Start Guide:**
        1. Select an article from the dropdown
        2. Click "✨ Generate Prompts" to analyze the article
        3. Review the AI-generated prompts (or regenerate if needed)
        4. Click "🎨 Render All Images" to create photorealistic images
        
        **Note:** Each image takes 30-60 seconds to generate. The AI ensures all images are:
        - ✅ Contextually accurate to the article
        - ✅ Professional and workplace-appropriate
        - ✅ Photorealistic quality
        - ✅ High resolution (512x768)
        """)
    else:
        st.success(f"**✅ Generated {len(st.session_state.current_images)} image(s)**")
        st.caption(f"**From Article:** {st.session_state.current_article}")
        
        for idx, img_data in enumerate(st.session_state.current_images):
            with st.container():
                st.markdown(f"### 🖼️ Image {idx + 1}")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(img_data["image"], width="stretch")
                    
                    with open(img_data["path"], "rb") as f:
                        st.download_button(
                            "⬇️ Download PNG",
                            f,
                            os.path.basename(img_data["path"]),
                            "image/png",
                            key=f"download_{idx}",
                            width="stretch"
                        )
                
                with col2:
                    st.markdown("**📝 AI-Generated Prompt:**")
                    st.info(img_data["prompt"])
                    
                    with st.expander("🔧 Technical Details"):
                        st.caption(f"""
                        **Enhanced Prompt:**  
                        {img_data['prompt']}, raw photo, 8k uhd, dslr, soft lighting, high quality, film grain, photorealistic, professional photography
                        
                        **Model:** Realistic Vision V6.0  
                        **Resolution:** {width}x{height}  
                        **Quality:** Photorealistic
                        """)
                
                st.divider()
        
        st.markdown("---")
        st.info("💡 **Tip:** To generate images from a different article, select it from the dropdown and click 'Generate Prompts' again.")
