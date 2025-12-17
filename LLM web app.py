import streamlit as st
import requests
import json
import base64
from PIL import Image
import io
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50;
    }
    
    /* Cards */
    .analysis-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #3498db;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.markdown("---")
    st.subheader("🔗 Ollama Settings")
    
    # Allow users to input their Ollama URL (for advanced users)
    ollama_url = st.text_input(
        "Ollama Server URL",
        value="http://localhost:11434",
        help="For local use: http://localhost:11434"
    )
    
    st.markdown("---")
    st.subheader("ℹ️ About This App")
    
    st.info("""
    **Engineering Analysis AI** provides:
    
    - 🤖 Technical design analysis
    - 🔍 Engineering recommendations
    - ⚙️ Manufacturing considerations
    - 🎯 Improvement suggestions
    
    *For full AI functionality, run the local version.*
    """)
    
    st.markdown("---")
    st.caption("Assignment 4 - LLM Web Application Deployment")

# ==================== MAIN CONTENT ====================
# Title
st.title("🔧 Engineering Analysis AI")
st.markdown("**Upload your design and get expert AI-powered engineering analysis**")

# Demo/Info banner
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.info("""
        ⚠️ **Streamlit Cloud Demo Mode** - This version demonstrates the interface and workflow. 
        For full AI functionality with Ollama, use the local HTML version included in this repository.
        """)
    with col2:
        if st.button("📥 Local Version"):
            st.markdown("[Download Local HTML Version](https://github.com/yourusername/engineering-analysis-ai/raw/main/local-version/index.html)")

# ==================== FORM INPUTS ====================
st.markdown("---")

# Domain Selection
domain_options = {
    "": "-- Select the domain --",
    "robotics": "🤖 Robotics / Mechanical Systems",
    "product": "📱 Product Design", 
    "cad": "💻 CAD Model / 3D Design",
    "mechanism": "⚙️ Mechanical Mechanism",
    "electronics": "🔌 Electronics / PCB Design",
    "other": "🔍 Other Engineering Design"
}

selected_key = st.selectbox(
    "🏷️ **What type of design is this?**",
    options=list(domain_options.keys()),
    format_func=lambda x: domain_options[x]
)

# Image Upload
uploaded_file = st.file_uploader(
    "📁 **Upload your design image**",
    type=["jpg", "jpeg", "png", "gif", "bmp"],
    help="Supported formats: JPG, PNG, GIF, BMP"
)

# Description Input
description = st.text_area(
    "📝 **Describe what you see in the image:**",
    height=120,
    placeholder="Example: 'This is a 4-degree-of-freedom robotic arm with servo motors, aluminum frame, and a gripper mechanism...'",
    help="Be specific about components, materials, mechanisms, and intended function"
)

# ==================== ANALYSIS FUNCTION ====================
def generate_mock_analysis(domain, description):
    """Generate realistic mock analysis for demonstration"""
    
    domain_titles = {
        "robotics": "Robotics System Analysis",
        "product": "Product Design Review",
        "cad": "3D Model Evaluation",
        "mechanism": "Mechanical Mechanism Analysis",
        "electronics": "Electronics Design Assessment",
        "other": "Engineering Design Analysis"
    }
    
    mock_responses = {
        "robotics": f"""
**🤖 {domain_titles.get(domain, 'Engineering Analysis')}**

Based on your description: *"{description[:80]}..."*

**🔧 TECHNICAL SPECIFICATIONS:**
- **Mechanism Type**: Articulated robotic system
- **Degrees of Freedom**: 4-6 (based on visible joints)
- **Actuation Method**: Servo motors with gear reduction
- **Frame Material**: Aluminum alloy (6061-T6 suggested)
- **End-Effector**: Gripper mechanism with force sensing

**⚙️ DESIGN CONSIDERATIONS:**
- **Applications**: Pick-and-place operations, assembly automation
- **Strengths**: Good range of motion, modular construction
- **Limitations**: Cable management needed, requires position feedback
- **Safety**: Implement emergency stop and limit switches

**🚀 RECOMMENDATIONS:**
1. Add absolute encoders for position feedback
2. Implement ROS (Robot Operating System) for control
3. Consider harmonic drives for smoother motion
4. Add cable management channels

**📈 NEXT STEPS:**
- Perform kinematic analysis
- Test with maximum payload
- Implement collision detection
""",

        "product": f"""
**📱 {domain_titles.get(domain, 'Engineering Analysis')}**

Based on your description: *"{description[:80]}..."*

**🎯 PRODUCT ANALYSIS:**
- **Target Users**: Professional/hobbyist users
- **Key Features**: Ergonomic design, durable construction
- **Materials**: ABS plastic with rubberized coating
- **Manufacturing**: Injection molding suitable

**🏭 MANUFACTURING & COST:**
- **Process**: 2-shot injection molding
- **Cost Estimate**: $12-18 per unit at scale
- **Assembly**: Minimal part count for easy assembly
- **Sustainability**: Recyclable materials recommended

**💡 DESIGN IMPROVEMENTS:**
1. Add anti-slip texture to grip surfaces
2. Consider modular attachments
3. Implement wear indicators
4. Add smart features (IoT connectivity optional)

**📊 MARKET POSITIONING:**
- Competitive advantage in ergonomics
- Target mid-range price point
- Focus on durability and user comfort
""",

        "cad": f"""
**💻 {domain_titles.get(domain, 'Engineering Analysis')}**

Based on your description: *"{description[:80]}..."*

**📐 DESIGN EVALUATION:**
- **Complexity**: Moderate with organic surfaces
- **Features**: Parametric design with assembly constraints
- **Manufacturability**: Suitable for 3D printing and CNC
- **Tolerances**: Standard ±0.1mm recommended

**🛠️ ENGINEERING RECOMMENDATIONS:**
- Add fillets (R3-R5) to reduce stress concentrations
- Implement proper draft angles (1-2°) for molding
- Consider thermal expansion in tolerance calculations
- Optimize wall thickness for strength/weight ratio

**🔧 PROTOTYPING PLAN:**
1. 3D print functional prototype (FDM/SLA)
2. Conduct FEA stress analysis
3. Test with real-world loads
4. Iterate based on feedback

**⚙️ PRODUCTION READINESS:**
- Design for manufacturing (DFM) review complete
- Tooling considerations identified
- Assembly sequence defined
- Quality control points established
"""
    }
    
    # Default response if domain not in mock_responses
    default_response = f"""
**🔍 {domain_titles.get(domain, 'Engineering Analysis')}**

Based on your description: *"{description[:80]}..."*

**📋 ANALYSIS SUMMARY:**
This design shows good engineering principles with attention to functionality and manufacturability.

**✅ STRENGTHS:**
- Clear functional purpose
- Consideration of materials and construction
- Appropriate scale and proportions
- Good aesthetic integration

**⚠️ AREAS FOR IMPROVEMENT:**
1. Consider alternative materials for cost/performance
2. Implement design for assembly principles
3. Add safety features where applicable
4. Consider environmental impact

**🚀 RECOMMENDATIONS:**
- Build a proof-of-concept prototype
- Conduct user testing sessions
- Refine based on feedback
- Plan for manufacturing at scale

**📞 NEXT ACTIONS:**
1. Detailed CAD modeling
2. Material selection optimization
3. Manufacturing process planning
4. Cost analysis and budgeting
"""
    
    return mock_responses.get(domain, default_response)

# ==================== ANALYSIS BUTTON ====================
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button(
        "🚀 **Generate Engineering Analysis**",
        type="primary",
        use_container_width=True,
        disabled=not (selected_key and description and uploaded_file)
    )

# ==================== ANALYSIS RESULTS ====================
if analyze_button:
    with st.spinner("🤖 AI is analyzing your design... (Demo Mode)"):
        # Simulate processing time
        time.sleep(2)
        
        # Show uploaded image
        st.subheader("📷 Uploaded Design")
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Design", use_column_width=True)
        
        # Show description summary
        st.subheader("📝 Your Description")
        st.info(f"*{description}*")
        
        # Generate and display mock analysis
        st.subheader("📊 Engineering Analysis Results")
        
        analysis = generate_mock_analysis(selected_key, description)
        
        with st.container():
            st.markdown("""
            <div class="analysis-card">
            """, unsafe_allow_html=True)
            
            st.markdown(analysis)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
        
        # Download button
        st.download_button(
            label="📥 Download Analysis Report",
            data=analysis,
            file_name=f"engineering_analysis_{selected_key}.md",
            mime="text/markdown",
            use_container_width=True
        )
        
        # Local version reminder
        st.info("""
        💡 **For Real AI Analysis**: 
        Download and run the local HTML version with Ollama for actual AI-powered analysis 
        using TinyLlama and vision models.
        """)

# ==================== FOOTER ====================
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("**Assignment 4** - LLM Web App Deployment")
with col2:
    st.caption("**Course**: Large Language Models")
with col3:
    st.caption("**Student**: [Your Name]")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 1rem;">
    <p><strong>Engineering Analysis AI</strong> | Streamlit Cloud Deployment</p>
    <p><small>Demo Version - For educational purposes</small></p>
</div>
""", unsafe_allow_html=True)
