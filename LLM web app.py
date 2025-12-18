import streamlit as st
import requests
from PIL import Image
import io
import os

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="centered"
)

HF_API_KEY = st.secrets.get("HF_API_KEY", None)

VISION_MODEL = "Salesforce/blip-image-captioning-base"
TEXT_MODEL = "google/flan-t5-large"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# -----------------------------
# FUNCTIONS
# -----------------------------
def vision_caption(image: Image.Image) -> str:
    """Generate image caption using Hugging Face Vision model"""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{VISION_MODEL}",
        headers=HEADERS,
        data=buffer
    )

    if response.status_code != 200:
        return f"Vision model error: {response.text}"

    try:
        data = response.json()
    except Exception:
        return "Vision model returned invalid JSON."

    # Handle different HF response formats
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    if isinstance(data, dict) and "error" in data:
        return f"Vision model error: {data['error']}"

    return "Unable to generate image caption."


def engineering_analysis(caption: str, user_desc: str, domain: str) -> str:
    prompt = f"""
You are an expert engineering analyst.

DOMAIN:
{domain}

IMAGE DESCRIPTION:
{caption}

USER DESCRIPTION:
{user_desc}

Provide a structured engineering analysis including:
- Functionality
- Components
- Design strengths
- Limitations
- Improvement suggestions
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400,
            "temperature": 0.3
        }
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{TEXT_MODEL}",
        headers=HEADERS,
        json=payload
    )

    if response.status_code != 200:
        return f"Text model error: {response.text}"

    try:
        data = response.json()
    except Exception:
        return "Text model returned invalid JSON."

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    if isinstance(data, dict) and "error" in data:
        return f"Text model error: {data['error']}"

    return "Unable to generate engineering analysis."


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
    height=120
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Design", use_container_width=True)

    if st.button("Analyze Design"):
        if not HF_API_KEY:
            st.error("Hugging Face API key not found. Add it to Streamlit secrets.")
            st.stop()

        with st.spinner("Analyzing design using AI..."):
            caption = vision_caption(image)
            analysis = engineering_analysis(caption, user_description, domain)

        st.subheader("🧠 AI Image Understanding")
        st.write(caption)

        st.subheader("📊 Engineering Analysis")
        st.write(analysis)
