"""
Article-Based Image Generation UI
Streamlit interface for generating images from article content
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.models.image_generator import ImageGenerator
from src.utils.article_processor import ArticleProcessor
from src.utils.prompt_engineer import PromptEngineer
from config.settings import GENERATION_CONFIG, ARTICLE_CONFIG, PATHS

# Page configuration
st.set_page_config(
    page_title="Article-Based AI Image Generator",
    page_icon="📰",
    layout="wide"
)

# Initialize components (cached to avoid reloading)
@st.cache_resource
def get_generator():
    return ImageGenerator()

@st.cache_resource
def get_article_processor():
    return ArticleProcessor(PATHS["articles_dir"])

@st.cache_resource
def get_prompt_engineer():
    return PromptEngineer()

# Load components
try:
    with st.spinner("🚀 Loading AI models... This may take a minute on first run."):
        generator = get_generator()
        article_processor = get_article_processor()
        prompt_engineer = get_prompt_engineer()
    st.success("✅ Models loaded successfully!")
except Exception as e:
    st.error(f"❌ Failed to load models: {e}")
    st.stop()

# Sidebar settings
st.sidebar.header("⚙️ Generation Settings")

# Image quality settings
st.sidebar.subheader("Quality Settings")
steps = st.sidebar.slider("Inference Steps", min_value=20, max_value=100, value=50, 
                          help="More steps = better quality but slower")
cfg_scale = st.sidebar.slider("Guidance Scale (CFG)", min_value=1.0, max_value=15.0, value=7.5,
                              help="How closely to follow the prompt (7-9 recommended)")
height = st.sidebar.select_slider("Height", options=[512, 768, 1024], value=768)
width = st.sidebar.select_slider("Width", options=[512, 768, 1024], value=768)

# Style selection
style = st.sidebar.selectbox(
    "Image Style",
    ["photorealistic", "artistic", "cinematic"],
    help="Style of generated images"
)

# Number of concepts per article
max_concepts = st.sidebar.slider(
    "Images per Article",
    min_value=1,
    max_value=5,
    value=ARTICLE_CONFIG["max_concepts_per_article"],
    help="Number of images to generate per article"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Higher steps and resolution produce better quality but take longer to generate.")

# Main interface
st.title("📰 Article-Based AI Image Generator")
st.markdown("""
Generate high-quality, contextual images from article content using **Stable Diffusion 2.1** with GPU acceleration.
Upload articles or process existing ones from the `Articles/` directory.
""")

# Create tabs
tab1, tab2 = st.tabs(["📂 Process Articles", "🎨 Manual Generation"])

# Tab 1: Article-based generation
with tab1:
    st.header("Process Articles from Directory")
    
    # Get available articles
    articles = article_processor.get_all_articles()
    
    if not articles:
        st.warning(f"⚠️ No articles found in `{PATHS['articles_dir']}/` directory. Please add .docx files.")
    else:
        st.success(f"✅ Found {len(articles)} article(s)")
        
        # Display articles
        for i, article_path in enumerate(articles):
            article_name = os.path.basename(article_path)
            with st.expander(f"📄 {article_name}", expanded=(i == 0)):
                st.write(f"**Path**: `{article_path}`")
                
                # Process button for individual article
                if st.button(f"🔍 Preview Concepts", key=f"preview_{i}"):
                    with st.spinner(f"Processing {article_name}..."):
                        result = article_processor.process_article(article_path, max_concepts)
                        
                        if "error" in result:
                            st.error(result["error"])
                        else:
                            st.write(f"**Extracted {result['num_concepts']} concept(s):**")
                            for j, concept in enumerate(result["concepts"], 1):
                                st.write(f"{j}. {concept}")
                            
                            # Generate prompts
                            prompts = prompt_engineer.create_prompts_from_concepts(
                                result["concepts"], style=style
                            )
                            
                            st.write("\n**Generated Prompts:**")
                            for j, prompt_data in enumerate(prompts, 1):
                                st.code(prompt_data["enhanced_prompt"], language="text")
        
        st.markdown("---")
        
        # Process all articles button
        col1, col2 = st.columns([1, 3])
        with col1:
            process_all = st.button("🚀 Generate Images from All Articles", type="primary")
        
        if process_all:
            st.markdown("### 🎨 Generating Images...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            all_results = []
            total_articles = len(articles)
            
            for idx, article_path in enumerate(articles):
                article_name = os.path.basename(article_path).replace(".docx", "")
                status_text.write(f"📄 Processing: **{article_name}** ({idx+1}/{total_articles})")
                
                # Process article
                article_data = article_processor.process_article(article_path, max_concepts)
                
                if "error" not in article_data and article_data["concepts"]:
                    # Generate prompts
                    prompts = prompt_engineer.create_prompts_from_concepts(
                        article_data["concepts"], style=style
                    )
                    
                    # Generate images
                    try:
                        results = generator.generate_from_article_concepts(
                            concepts=article_data["concepts"],
                            prompts_data=prompts,
                            article_name=article_name,
                            steps=steps,
                            cfg_scale=cfg_scale,
                            height=height,
                            width=width
                        )
                        
                        all_results.append({
                            "article": article_name,
                            "results": results
                        })
                        
                    except Exception as e:
                        st.error(f"Error generating images for {article_name}: {e}")
                
                progress_bar.progress((idx + 1) / total_articles)
            
            status_text.write("✅ **All articles processed!**")
            
            # Display results
            st.markdown("---")
            st.header("📸 Generated Images")
            
            for article_result in all_results:
                st.subheader(f"📄 {article_result['article']}")
                
                # Display images in columns
                cols = st.columns(min(len(article_result['results']), 3))
                
                for i, result in enumerate(article_result['results']):
                    col_idx = i % 3
                    with cols[col_idx]:
                        st.image(result["image_path"], use_container_width=True)
                        st.caption(f"Concept: {result['concept'][:100]}...")
                        
                        # Download button
                        with open(result["image_path"], "rb") as file:
                            st.download_button(
                                label="⬇️ Download",
                                data=file,
                                file_name=os.path.basename(result["image_path"]),
                                mime="image/png",
                                key=f"download_{article_result['article']}_{i}"
                            )

# Tab 2: Manual generation (original functionality)
with tab2:
    st.header("Manual Text-to-Image Generation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        prompt = st.text_area(
            "Enter your prompt:",
            height=100,
            placeholder="A futuristic city at sunset, cyberpunk style, highly detailed, 8k..."
        )
        negative_prompt = st.text_input(
            "Negative Prompt (Optional):",
            value=prompt_engineer.get_negative_prompt(),
            placeholder="blurry, low quality, distorted..."
        )
    
    num_images = st.slider("Number of Images", min_value=1, max_value=4, value=1)
    
    generate_btn = st.button("🎨 Generate Images", type="primary")
    
    if generate_btn and prompt:
        with st.spinner("🎨 Generating images... This may take a moment."):
            try:
                # Generate images
                images = generator.generate(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_images=num_images,
                    steps=steps,
                    cfg_scale=cfg_scale,
                    height=height,
                    width=width
                )
                
                # Display and save images
                st.subheader("Generated Images")
                
                cols = st.columns(num_images)
                
                for idx, (col, img) in enumerate(zip(cols, images)):
                    # Save locally
                    params = {
                        "steps": steps,
                        "cfg_scale": cfg_scale,
                        "height": height,
                        "width": width,
                        "style": style
                    }
                    img_path, meta_path = generator.save_image(img, prompt, params)
                    
                    with col:
                        st.image(img, use_container_width=True)
                        
                        # Download button
                        with open(img_path, "rb") as file:
                            st.download_button(
                                label=f"⬇️ Download {idx+1}",
                                data=file,
                                file_name=os.path.basename(img_path),
                                mime="image/png",
                                key=f"manual_download_{idx}"
                            )
                
                st.success(f"✅ Successfully generated {num_images} image(s)!")
                
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
    
    elif generate_btn and not prompt:
        st.warning("⚠️ Please enter a prompt to generate images.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>AI-Powered Article Image Generator</strong></p>
    <p>Built with PyTorch 2.9.1 + CUDA 13.0 | Stable Diffusion 2.1</p>
    <p><em>Talrn Remote ML Internship Task Assessment</em></p>
</div>
""", unsafe_allow_html=True)
