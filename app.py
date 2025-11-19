import streamlit as st
from generator import ImageGenerator
import os

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# Initialize generator (cached to avoid reloading model on every rerun)
@st.cache_resource
def get_generator():
    return ImageGenerator()

try:
    generator = get_generator()
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# Sidebar for settings
st.sidebar.header("Generation Settings")

model_id = st.sidebar.text_input("Model ID (HuggingFace)", value="runwayml/stable-diffusion-v1-5")
# Note: Changing model ID at runtime would require re-initializing the generator, 
# which is complex with st.cache_resource. For this demo, we stick to the default or allow restart.

num_images = st.sidebar.slider("Number of Images", min_value=1, max_value=4, value=1)
steps = st.sidebar.slider("Inference Steps", min_value=10, max_value=100, value=50)
cfg_scale = st.sidebar.slider("Guidance Scale (CFG)", min_value=1.0, max_value=20.0, value=7.5)
height = st.sidebar.select_slider("Height", options=[256, 512, 768, 1024], value=512)
width = st.sidebar.select_slider("Width", options=[256, 512, 768, 1024], value=512)

st.sidebar.markdown("---")
st.sidebar.info("Note: First generation may take longer as the model initializes.")

# Main interface
st.title("🎨 AI-Powered Image Generator")
st.markdown("Generate high-quality images from text descriptions using Stable Diffusion.")

col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_area("Enter your prompt:", height=100, placeholder="A futuristic city at sunset, cyberpunk style, highly detailed, 8k...")
    negative_prompt = st.text_input("Negative Prompt (Optional):", placeholder="blurry, low quality, distorted, ugly...")

    generate_btn = st.button("Generate Images", type="primary")

if generate_btn and prompt:
    with st.spinner("Generating images... This may take a moment depending on your hardware."):
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
            
            # Create columns for grid display
            cols = st.columns(num_images)
            
            for idx, (col, img) in enumerate(zip(cols, images)):
                # Save locally
                params = {
                    "steps": steps,
                    "cfg_scale": cfg_scale,
                    "height": height,
                    "width": width,
                    "model_id": generator.model_id
                }
                img_path, meta_path = generator.save_image(img, prompt, params)
                
                with col:
                    st.image(img, use_container_width=True)
                    
                    # Download button
                    with open(img_path, "rb") as file:
                        btn = st.download_button(
                            label=f"Download Image {idx+1}",
                            data=file,
                            file_name=os.path.basename(img_path),
                            mime="image/png"
                        )
                        
            st.success(f"Successfully generated {num_images} image(s)!")
            
        except Exception as e:
            st.error(f"An error occurred during generation: {e}")

elif generate_btn and not prompt:
    st.warning("Please enter a prompt to generate images.")

# Footer
st.markdown("---")
st.markdown("Built for Talrn Remote ML Internship Task Assessment")
