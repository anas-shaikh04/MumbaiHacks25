"""
Streamlit UI for Veritas Guardian
User-friendly interface for misinformation verification
"""

import streamlit as st
import os
from pathlib import Path
from datetime import datetime
from loguru import logger

from pipeline import VeritasGuardianPipeline

# Page configuration
st.set_page_config(
    page_title="Veritas Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1a73e8;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #5f6368;
        margin-bottom: 2rem;
    }
    .verdict-true {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
    }
    .verdict-false {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
    }
    .verdict-neutral {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
    }
    .risk-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.875rem;
    }
    .risk-low { background-color: #d4edda; color: #155724; }
    .risk-medium { background-color: #fff3cd; color: #856404; }
    .risk-high { background-color: #f8d7da; color: #721c24; }
    .risk-critical { background-color: #dc3545; color: white; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if 'results' not in st.session_state:
    st.session_state.results = None

# Initialize pipeline (cached)
@st.cache_resource
def get_pipeline():
    return VeritasGuardianPipeline()


# Header
st.markdown('<div class="main-header">🛡️ VERITAS GUARDIAN</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-Agent Misinformation Verification System</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **Veritas Guardian** uses 6 AI agents to verify any content:
    
    1. 🎬 **Ingestion** - Extract text from any media
    2. 🌍 **Claims** - Detect language & extract facts
    3. 🔍 **Evidence** - Search reliable sources
    4. ✅ **Verification** - AI-powered fact-checking
    5. 📊 **Virality** - Assess spread & risk
    6. 📄 **Synthesis** - Generate reports
    
    **Supported Languages:**
    - English, Hindi, Marathi (full support)
    - Other Indian languages (partial)
    """)
    
    st.divider()
    
    st.header("⚙️ Settings")
    show_workflow = st.checkbox("Show Agent Workflow", value=False)
    show_evidence = st.checkbox("Show All Evidence", value=True)

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Text", "🔗 URL", "🖼️ Image", "🎥 Video", "📄 PDF"])

# Text verification
with tab1:
    st.subheader("Verify Text Content")
    
    text_input = st.text_area(
        "Enter text to verify:",
        height=150,
        placeholder="Paste any text, WhatsApp message, tweet, or claim here..."
    )
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        views = st.number_input("Views (optional)", min_value=0, value=1000, step=100)
    with col2:
        likes = st.number_input("Likes (optional)", min_value=0, value=100, step=10)
    with col3:
        shares = st.number_input("Shares (optional)", min_value=0, value=50, step=10)
    with col4:
        comments = st.number_input("Comments (optional)", min_value=0, value=20, step=5)
    
    if st.button("🔍 Verify Text", type="primary", use_container_width=True):
        if not text_input:
            st.error("Please enter some text to verify")
        else:
            with st.spinner("🤖 AI agents are working..."):
                try:
                    pipeline = get_pipeline()
                    
                    metadata = {
                        "views": views,
                        "likes": likes,
                        "shares": shares,
                        "comments": comments
                    }
                    
                    results = pipeline.process(text_input, "text", metadata)
                    st.session_state.results = results
                    
                    st.success("✅ Verification complete!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    logger.error(f"Verification error: {e}")

# URL verification
with tab2:
    st.subheader("Verify URL Content")
    
    url_input = st.text_input(
        "Enter URL:",
        placeholder="https://example.com/article or YouTube URL"
    )
    
    if st.button("🔍 Verify URL", type="primary", use_container_width=True):
        if not url_input:
            st.error("Please enter a URL")
        else:
            with st.spinner("🤖 Fetching and analyzing content..."):
                try:
                    pipeline = get_pipeline()
                    results = pipeline.process(url_input, "url")
                    st.session_state.results = results
                    st.success("✅ Verification complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Image verification
with tab3:
    st.subheader("Verify Image Content")
    
    image_file = st.file_uploader(
        "Upload image:",
        type=["png", "jpg", "jpeg"],
        help="Upload screenshots, memes, or any image with text"
    )
    
    if image_file:
        st.image(image_file, caption="Uploaded Image", use_container_width=True)
        
        if st.button("🔍 Verify Image", type="primary", use_container_width=True):
            with st.spinner("🤖 Extracting text and analyzing..."):
                try:
                    # Save temporarily
                    temp_path = Path("temp") / f"upload_{datetime.now().timestamp()}_{image_file.name}"
                    temp_path.parent.mkdir(exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(image_file.getbuffer())
                    
                    pipeline = get_pipeline()
                    results = pipeline.process(str(temp_path), "image")
                    st.session_state.results = results
                    
                    # Cleanup
                    temp_path.unlink()
                    
                    st.success("✅ Verification complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Video verification
with tab4:
    st.subheader("Verify Video Content")
    
    video_file = st.file_uploader(
        "Upload video:",
        type=["mp4", "avi", "mov", "mkv"],
        help="First 30 seconds will be analyzed"
    )
    
    if video_file:
        st.video(video_file)
        
        if st.button("🔍 Verify Video", type="primary", use_container_width=True):
            with st.spinner("🤖 Transcribing and analyzing... (this may take a moment)"):
                try:
                    temp_path = Path("temp") / f"upload_{datetime.now().timestamp()}_{video_file.name}"
                    temp_path.parent.mkdir(exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(video_file.getbuffer())
                    
                    pipeline = get_pipeline()
                    results = pipeline.process(str(temp_path), "video")
                    st.session_state.results = results
                    
                    temp_path.unlink()
                    
                    st.success("✅ Verification complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# PDF verification
with tab5:
    st.subheader("Verify PDF Content")
    
    pdf_file = st.file_uploader(
        "Upload PDF:",
        type=["pdf"],
        help="Extract and verify text from PDF documents"
    )
    
    if pdf_file:
        st.info(f"📄 {pdf_file.name} ({pdf_file.size // 1024} KB)")
        
        if st.button("🔍 Verify PDF", type="primary", use_container_width=True):
            with st.spinner("🤖 Extracting and analyzing text..."):
                try:
                    temp_path = Path("temp") / f"upload_{datetime.now().timestamp()}_{pdf_file.name}"
                    temp_path.parent.mkdir(exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(pdf_file.getbuffer())
                    
                    pipeline = get_pipeline()
                    results = pipeline.process(str(temp_path), "pdf")
                    st.session_state.results = results
                    
                    temp_path.unlink()
                    
                    st.success("✅ Verification complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# Display results
if st.session_state.results:
    st.divider()
    st.header("📊 Verification Results")
    
    results = st.session_state.results
    
    # Summary
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Claims", results['summary']['total_claims'])
    with col2:
        st.metric("✅ True", results['summary']['true_count'])
    with col3:
        st.metric("❌ False", results['summary']['false_count'])
    with col4:
        st.metric("⚠️ Neutral", results['summary']['neutral_count'])
    with col5:
        risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
        st.metric(
            "Risk Level",
            f"{risk_emoji.get(results['summary']['highest_risk'], '⚪')} {results['summary']['highest_risk'].upper()}"
        )
    
    st.divider()
    
    # Language info
    if results['language_support'] == 'partial':
        st.info(f"ℹ️ Detected {results['language_name']}. Explanation shown in English due to limited local-language support.")
    
    # Visual forensics
    if results.get('visual_forensics', {}).get('suspicion_level') != 'none':
        suspicion = results['visual_forensics']['suspicion_level']
        if suspicion in ['medium', 'high']:
            st.warning(f"⚠️ Visual Forensics: {suspicion.upper()} suspicion of image manipulation detected")
    
    # Individual claims
    for idx, claim in enumerate(results['results'], 1):
        st.subheader(f"Claim #{idx}")
        
        # Verdict box
        verdict_class = f"verdict-{claim['user_label'].lower()}"
        
        st.markdown(f'<div class="{verdict_class}">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{claim['claim']}**")
        
        with col2:
            st.markdown(f"**Verdict:** {claim['user_label']}")
            st.markdown(f"**Confidence:** {claim['confidence']}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Explanation
        st.write("**Explanation:**")
        if results['primary_language'] != 'en' and results['language_support'] == 'full':
            st.info(f"🌍 {results['language_name']}: {claim['short_explain_local']}")
        st.write(f"🇬🇧 English: {claim['short_explain_en']}")
        
        # Risk & Virality
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Virality Score", f"{claim['virality_score']}/100")
        with col2:
            risk_colors = {
                "low": "risk-low",
                "medium": "risk-medium",
                "high": "risk-high",
                "critical": "risk-critical"
            }
            risk_class = risk_colors.get(claim['combined_risk_level'], 'risk-low')
            st.markdown(
                f'<span class="risk-badge {risk_class}">{claim["combined_risk_level"].upper()}</span>',
                unsafe_allow_html=True
            )
        
        # Evidence
        if show_evidence and claim.get('evidence'):
            with st.expander("🔍 Evidence Sources"):
                for ev_idx, evidence in enumerate(claim['evidence'][:5], 1):
                    st.markdown(f"""
                    **{ev_idx}. [{evidence['source_type'].upper()}] {evidence['title']}**
                    - Credibility: {evidence['credibility_score']}/100
                    - URL: {evidence['url']}
                    """)
        
        # PDF download
        if claim.get('receipt_pdf_path') and os.path.exists(claim['receipt_pdf_path']):
            with open(claim['receipt_pdf_path'], 'rb') as f:
                st.download_button(
                    label="📄 Download Verification Receipt (PDF)",
                    data=f.read(),
                    file_name=f"verification_{claim['claim_id']}.pdf",
                    mime="application/pdf"
                )
        
        if claim.get('needs_human_review'):
            st.warning("⚠️ This claim requires human review due to sensitivity or low confidence.")
        
        st.divider()
    
    # Agent workflow
    if show_workflow:
        st.header("🤖 Agent Workflow")
        pipeline = get_pipeline()
        workflow = pipeline.get_agent_workflow(results)
        
        for step in workflow['workflow']:
            st.success(f"✅ **{step['agent']}**: {step['action']}")
    
    # Clear button
    if st.button("🔄 Clear Results"):
        st.session_state.results = None
        st.rerun()
