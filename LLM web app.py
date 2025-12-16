import streamlit as st
import requests
import json
from PIL import Image
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .logo {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .analysis-result {
        background: #f8f9ff;
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    .demo-notice {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Title and header
st.markdown('<div class="logo">🔧</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header"><h1>Engineering Analysis AI</h1><p>Upload your design and get expert technical analysis</p></div>', unsafe_allow_html=True)

# Demo notice
st.markdown("""
<div class="demo-notice">
⚠️ <strong>DEMO MODE</strong> - This is a demonstration version. For full functionality with Ollama AI, run the local HTML version.
</div>
""", unsafe_allow_html=True)

# Mock AI responses based on domain
def get_mock_analysis(domain, description):
    mock_responses = {
        "robotics": f"""
🔧 TECHNICAL SPECIFICATIONS (Mock Analysis):
- Based on your description: "{description[:100]}..."
- Mechanism: Robotic arm with multiple degrees of freedom
- Components: Servo motors, aluminum frame, gripper mechanism
- Control: Microcontroller-based system with position feedback
- Power: 12V DC supply with current regulation

⚙️ DESIGN CONSIDERATIONS:
- Applications: Pick-and-place operations, assembly automation
- Strengths: Good range of motion, modular design
- Improvements: Add cable management, implement force sensing
- Safety: Include emergency stop and limit switches

📈 RECOMMENDATIONS:
1. Implement ROS (Robot Operating System) for advanced control
2. Add vision system for object recognition
3. Consider harmonic drives for smoother motion
4. Implement collision detection algorithms
""",
        
        "product": f"""
🎯 PRODUCT ANALYSIS (Mock Analysis):
- Based on: "{description[:100]}..."
- Function: Ergonomic tool/product design
- Target Users: Professionals and hobbyists
- Key Features: Comfortable grip, lightweight, durable materials

🏭 MANUFACTURING & COST:
- Materials: ABS plastic with rubberized coating
- Processes: Injection molding with overmolding
- Assembly: Minimal parts for easy manufacturing
- Cost Estimate: $15-25 per unit at scale

💡 DESIGN IMPROVEMENTS:
1. Add textured surface for better grip
2. Consider biodegradable materials
3. Implement modular design for customization
4. Add smart features (IoT connectivity)
""",
        
        "cad": f"""
📐 CAD ANALYSIS (Mock Analysis):
- Design: "{description[:100]}..."
- Complexity: Moderate with organic curves
- Features: Parametric design with assembly constraints
- Manufacturing: Suitable for 3D printing and CNC

🛠️ ENGINEERING RECOMMENDATIONS:
- Add fillets to reduce stress concentrations
- Implement proper draft angles for molding
- Consider thermal expansion in tolerances
- Optimize wall thickness for strength/weight

🔧 PROTOTYPING PLAN:
1. 3D print functional prototype
2. Conduct stress analysis simulation
3. Test with real-world loads
4. Iterate based on feedback
""",
        
        "mechanism": f"""
⚙️ MECHANICAL ANALYSIS (Mock Analysis):
- Mechanism: "{description[:100]}..."
- Type: Linkage system with multiple joints
- Motion: Rotary to linear conversion
- Efficiency: Estimated 85-90%

🔧 PERFORMANCE ANALYSIS:
- Load Capacity: Medium (10-50kg range)
- Wear Points: Joint bearings, sliding surfaces
- Maintenance: Regular lubrication needed
- Lifetime: 5+ years with proper care

🚀 OPTIMIZATION SUGGESTIONS:
1. Replace bushings with ball bearings
2. Add position feedback sensors
3. Implement self-lubricating materials
4. Consider alternative mechanism geometries
""",
        
        "electronics": f"""
🔌 ELECTRONICS ANALYSIS (Mock Analysis):
- Circuit: "{description[:100]}..."
- Components: Microcontroller, sensors, power regulation
- Power: 5V/3.3V mixed voltage system
- Communication: I2C/SPI/UART interfaces

⚡ DESIGN CONSIDERATIONS:
- PCB Layout: 2-layer with ground plane
- Thermal: Add heatsinks for power components
- EMI: Implement proper filtering and shielding
- Testing: In-circuit testing points recommended

💡 IMPROVEMENTS:
1. Add overvoltage/overcurrent protection
2. Implement sleep modes for power saving
3. Use surface mount for miniaturization
4. Add debugging interfaces (JTAG/SWD)
""",
        
        "other": f"""
🔍 ENGINEERING ANALYSIS (Mock Analysis):
- Design: "{description[:100]}..."
- Purpose: {description[:50]}...
- Principles: Mechanical/electrical integration
- Innovation: Novel approach to problem solving

💡 TECHNICAL ASSESSMENT:
- Functionality: Meets basic requirements
- Innovation: Shows creative engineering
- Feasibility: Technically achievable
- Market Potential: Niche application

🚀 DEVELOPMENT PATH:
1. Build proof-of-concept prototype
2. Conduct user testing
3. Refine design based on feedback
4. Plan for manufacturing at scale
"""
    }
    
    return mock_responses.get(domain, "Analysis not available for this domain.")

# Main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Upload Your Design")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png', 'gif'],
        help="Upload CAD models, robotics, mechanisms, products, etc."
    )
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Design", use_column_width=True)
            st.success("✅ Image uploaded successfully!")
        except:
            st.warning("📄 File uploaded (preview not available in demo mode)")

with col2:
    st.subheader("🎯 Analysis Settings")
    
    # Domain selection
    domain = st.selectbox(
        "🏷️ What type of design is this?",
        options=["robotics", "product", "cad", "mechanism", "electronics", "other"],
        format_func=lambda x: {
            "robotics": "🤖 Robotics / Mechanical Systems",
            "product": "📱 Product Design",
            "cad": "💻 CAD Model / 3D Design",
            "mechanism": "⚙️ Mechanical Mechanism",
            "electronics": "🔌 Electronics / PCB Design",
            "other": "🔍 Other Engineering Design"
        }[x]
    )
    
    # Description input
    description = st.text_area(
        "📝 Describe what you see in the image:",
        height=150,
        placeholder="Example: 'This is a 4-degree-of-freedom robotic arm with servo motors, aluminum frame, and a gripper mechanism...'",
        help="Be specific about components, materials, mechanisms, and intended function"
    )

# Analysis button
if st.button("🚀 Analyze Design", type="primary", use_container_width=True):
    if not description.strip():
        st.error("⚠️ Please describe your design!")
    else:
        with st.spinner("🤖 Generating AI analysis (Demo Mode)..."):
            # Simulate AI processing time
            time.sleep(2)
            
            # Get mock analysis
            analysis = get_mock_analysis(domain, description)
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Analysis Results")
            
            st.markdown(f"""
            <div class="analysis-result">
                <h3>🔍 Engineering Analysis Results (Demo)</h3>
                <div style="white-space: pre-wrap; line-height: 1.6; margin-top: 1rem;">
                    {analysis}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Download button
            st.download_button(
                label="📥 Download Analysis Report",
                data=analysis,
                file_name=f"engineering_analysis_{domain}.txt",
                mime="text/plain",
                use_container_width=True
            )

# Information section
with st.expander("ℹ️ About This Demo"):
    st.markdown("""
    ### How This Works
    
    **Local Version (Full Functionality):**
    1. Run Ollama locally: `ollama run tinyllama:latest`
    2. Use the HTML file with your browser
    3. Connects to local AI for real analysis
    
    **Streamlit Demo (This Version):**
    - Shows the user interface and workflow
    - Uses mock responses to demonstrate capabilities
    - Can be deployed on Streamlit Cloud
    
    ### For Your Assignment:
    - Submit both versions
    - HTML version for actual Ollama functionality
    - Streamlit version for deployment demonstration
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding-top: 2rem;">
    <p><strong>Engineering Analysis AI</strong> | Demo Version for Streamlit Cloud</p>
    <p><small>For full AI functionality, use the local HTML version with Ollama</small></p>
</div>
""", unsafe_allow_html=True)
