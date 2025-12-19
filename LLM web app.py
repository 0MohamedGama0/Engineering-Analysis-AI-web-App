import streamlit as st
import io
from PIL import Image
from huggingface_hub import InferenceClient

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="centered"
)

# Get API key from Streamlit secrets
HF_API_KEY = st.secrets.get("HF_API_KEY", None)

# Model names
VISION_MODEL = "Salesforce/blip-image-captioning-base"
TEXT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"  # Use this instead of Mistral-Nemo

# Initialize the clients with specific models
vision_client = InferenceClient(model=VISION_MODEL, token=HF_API_KEY)
text_client = InferenceClient(model=TEXT_MODEL, token=HF_API_KEY)

# -----------------------------
# FUNCTIONS
# -----------------------------

def vision_caption(image: Image.Image) -> str:
    """Generate a caption for the uploaded image."""
    try:
        # Convert PIL Image to bytes for the API
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        image_bytes = buffer.getvalue()
        
        # Use image captioning API
        result = vision_client.image_to_text(image=image_bytes)
        
        # The result might be a dictionary, extract the text
        if isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        elif isinstance(result, list) and len(result) > 0:
            # Handle list response format
            if isinstance(result[0], dict) and "generated_text" in result[0]:
                return result[0]["generated_text"]
            else:
                return str(result[0])
        else:
            return str(result)
            
    except Exception as e:
        return f"Vision model error: {str(e)}"

def engineering_analysis(caption, user_description, domain):
    """Generate engineering analysis based on image caption and user description."""
    prompt = f"""You are an expert engineering AI.

DOMAIN:
{domain}

IMAGE UNDERSTANDING (AI Vision):
{caption}

USER DESCRIPTION:
{user_description if user_description else "No additional description provided by user."}

TASK:
Provide a structured engineering analysis including:
- System identification
- Key components
- Functionality
- Design strengths
- Weaknesses or risks
- Suggested improvements

Keep the analysis concise, technical, and focused on the {domain} domain.
"""
    
    try:
        # Use text generation with proper parameters
        result = text_client.text_generation(
            prompt,
            max_new_tokens=500,
            temperature=0.4,
            do_sample=True
        )
        return result
    except Exception as e:
        # Try alternative API method if text_generation fails
        try:
            # Use conversational API as fallback
            messages = [{"role": "user", "content": prompt}]
            result = text_client.chat_completion(
                messages=messages,
                max_tokens=500,
                temperature=0.4
            )
            return result.choices[0].message.content
        except Exception as e2:
            return f"Text model error: {str(e)}\nFallback also failed: {str(e2)}"

# -----------------------------
# UI
# -----------------------------
st.title("🔧 Engineering Analysis AI")
st.caption("Vision-Language AI for Robotics & Design Engineering")

uploaded_file = st.file_uploader(
    "Upload an engineering or design image",
    type=["png", "jpg", "jpeg"]
)

domain = st.selectbox(
    "Select domain",
    ["Robotics", "Product Design", "Mechanical", "Electronics", "CAD / 3D Printing"]
)

user_description = st.text_area(
    "Describe the design (optional but recommended)",
    height=120,
    placeholder="Example: 'This is a robotic arm prototype with 4 degrees of freedom...'"
)

if uploaded_file and st.button("Analyze Design"):
    if not HF_API_KEY:
        st.error("Hugging Face API key not found. Add it to Streamlit secrets.")
        st.stop()
    
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Design", use_container_width=True)
    
    with st.spinner("Analyzing design using AI..."):
        with st.status("Processing...", expanded=True) as status:
            status.update(label="📷 Generating image caption...", state="running")
            caption = vision_caption(image)
            
            status.update(label="🤖 Performing engineering analysis...", state="running")
            analysis = engineering_analysis(caption, user_description, domain)
            
            status.update(label="✅ Analysis complete!", state="complete")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 AI Image Understanding")
        st.info(caption)
    
    with col2:
        st.subheader("📊 Engineering Analysis")
        st.success(analysis)
