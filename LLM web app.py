import streamlit as st
import requests
import base64
from PIL import Image
import io
import os

# ---------------- CONFIG ----------------
HF_API_URL = "https://api-inference.huggingface.co/models/llava-hf/llava-1.5-7b-hf"
HF_API_KEY = st.secrets["HF_API_KEY"]

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# ---------------- FUNCTIONS ----------------
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def vision_analysis(image_b64, domain, description):
    prompt = f"""
You are an expert engineer.

Domain: {domain}

User description:
{description}

Analyze the uploaded image and provide:
- Technical interpretation
- Engineering strengths
- Limitations
- Improvement suggestions
"""

    payload = {
        "inputs": {
            "image": image_b64,
            "text": prompt
        }
    }

    response = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=60)

    if response.status_code != 200:
        return f"❌ API Error: {response.text}"

    result = response.json()

    if isinstance(result, list):
        return result[0].get("generated_text", "No response")
    return result.get("generated_text", "No response")

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Engineering Analysis AI", layout="centered")

st.title("🔧 Engineering Analysis AI")
st.subheader("Vision-Language Analysis for Robotics & Design")

uploaded_image = st.file_uploader(
    "Upload a design image",
    type=["png", "jpg", "jpeg"]
)

domain = st.selectbox(
    "Select design domain",
    ["Robotics", "Product Design", "CAD / 3D Printing", "Electronics"]
)

description = st.text_area(
    "Describe the design",
    placeholder="Example: 4-DOF robotic arm with servo motors..."
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Design", use_column_width=True)

if st.button("Analyze Design") and uploaded_image and description:
    with st.spinner("Analyzing with AI..."):
        image_b64 = encode_image(image)
        result = vision_analysis(image_b64, domain, description)

    st.success("Analysis Complete")
    st.markdown("### 🔍 Engineering Analysis")
    st.write(result)
