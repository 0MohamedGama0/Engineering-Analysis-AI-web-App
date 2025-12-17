import streamlit as st
import requests
import base64
from PIL import Image
import io

# ---------------- CONFIG ----------------
HF_API_URL = "https://router.huggingface.co/hf-inference/models/llava-hf/llava-1.5-7b-hf"
HF_API_KEY = st.secrets["HF_API_KEY"]

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- FUNCTIONS ----------------
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def vision_analysis(image_b64, domain, description):
    prompt = f"""
You are an expert engineer specializing in robotics and design engineering.

Domain: {domain}

User description:
{description}

Analyze the uploaded image and provide:
1. Technical interpretation
2. Key components and mechanisms
3. Engineering strengths
4. Limitations
5. Suggested improvements
"""

    payload = {
        "inputs": {
            "image": image_b64,
            "text": prompt
        }
    }

    response = requests.post(
        HF_API_URL,
        headers=HEADERS,
        json=payload,
        timeout=90
    )

    if response.status_code != 200:
        return f"❌ API Error ({response.status_code}): {response.text}"

    result = response.json()

    # Hugging Face response handling
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]

    if "generated_text" in result:
        return result["generated_text"]

    return "⚠️ No analysis generated."

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Engineering Analysis AI", layout="centered")

st.title("🔧 Engineering Analysis AI")
st.subheader("Vision-Language Analysis for Robotics & Design Engineering")

uploaded_image = st.file_uploader(
    "Upload an engineering design image",
    type=["png", "jpg", "jpeg"]
)

domain = st.selectbox(
    "Select design domain",
    [
        "Robotics",
        "Product Design",
        "CAD / 3D Printing",
        "Electronics"
    ]
)

description = st.text_area(
    "Describe the design",
    placeholder="Example: 4-DOF robotic arm with servo motors and aluminum links..."
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Design", use_column_width=True)

if st.button("Analyze Design"):
    if not uploaded_image or not description:
        st.warning("Please upload an image and enter a description.")
    else:
        with st.spinner("Analyzing with AI..."):
            image_b64 = encode_image(image)
            analysis = vision_analysis(image_b64, domain, description)

        st.success("Analysis complete")
        st.markdown("### 🔍 Engineering Analysis Result")
        st.write(analysis)
