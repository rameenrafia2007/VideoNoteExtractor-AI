"""
app.py
------
Streamlit web interface for the Video Note Extractor with Soft Glassmorphism.
"""

import os
import streamlit as st
# from dotenv import load_dotenv
from pipeline import run_pipeline

# load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Video Note Extractor",
    page_icon="📝",
    layout="centered",
)

# ── Premium Soft Glassmorphism & Custom Input Styling ─────────────────────────
st.markdown(
    """
    <style>
    /* Clean White Main Background */
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main .block-container {
        max-width: 800px;
        padding-top: 2rem;
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    /* Beautiful Center Rectangle with Glass Effect */
    .glass-header-card {
        background: rgba(115, 84, 93, 0.08) !important; 
        backdrop-filter: blur(12px) saturate(160%);
        -webkit-backdrop-filter: blur(12px) saturate(160%);
        border: 1px solid rgba(115, 84, 93, 0.15);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(115, 84, 93, 0.05);
        margin-bottom: 2.5rem;
    }

    /* Soft Dark Aesthetic Sidebar */
    [data-testid="stSidebar"] {
        background-color: #513B43 !important; 
        border-right: none;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #F4F1EE !important; 
    }
    
    /* Compact Sidebar Spacing Adjustments */
    [data-testid="stSidebar"] .stElementContainer {
        margin-bottom: 0.5rem !important;
        padding-bottom: 0px !important;
    }
    [data-testid="stSidebar"] hr {
        margin-top: 0.8rem !important;
        margin-bottom: 0.8rem !important;
        opacity: 0.15;
    }
    
    /* High-Visibility Custom Inputs with User Requested Plum Shadow (#70526E) */
    [data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #FFFFFF !important; /* Pure white inside container */
        border: 1px solid rgba(112, 82, 110, 0.3) !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="input"]:focus-within {
        border-color: #70526E !important; /* Elegant Plum Shadow Focus Ring */
        box-shadow: 0 0 0 3px rgba(112, 82, 110, 0.25) !important;
    }
    [data-testid="stSidebar"] input {
        color: #2B2B2A !important; /* Rich Dark Text - Perfectly Visible */
    }
    [data-testid="stSidebar"] input::placeholder {
        color: #737982 !important;
    }
    
    /* Button Matching the Sidebar Color Scheme */
    .stButton > button {
        width: 100%;
        background: #513B43 !important; 
        color: #FFFFFF !important;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(81, 59, 67, 0.15);
    }
    .stButton > button:hover {
        background: #3F2E34 !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(81, 59, 67, 0.25);
    }
    
    /* Secondary Action Button - Clear Button */
    div[data-testid="stColumn"]:nth-of-type(2) .stButton > button {
        background: rgba(81, 59, 67, 0.12) !important;
        color: #513B43 !important;
        border: 1px solid rgba(81, 59, 67, 0.2) !important;
        box-shadow: none !important;
    }
    div[data-testid="stColumn"]:nth-of-type(2) .stButton > button:hover {
        background: rgba(81, 59, 67, 0.2) !important;
        transform: none;
    }

    /* Content Preview Area Note Box */
    .note-box {
        background: #FFFFFF !important;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.03);
        margin: 1.5rem 0;
        border: 1px solid #E5E7EB;
        border-left: 6px solid #513B43 !important;
    }
    
    /* Solid Soft Green Active Badge */
    .badge-active {
        background: #2E7D32 !important; 
        color: #FFFFFF !important;
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-future {
        background: rgba(255, 255, 255, 0.08);
        color: #D1C7BD !important;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
    }
    
    .platform-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        padding: 2px 0;
    }
    .platform-name-clean {
        font-style: normal !important; 
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Glassmorphism Header Panel ────────────────────────────────────────────────
st.markdown(
    """
    <div class="glass-header-card">
        <div style="margin-bottom: 15px;">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="3" width="18" height="18" rx="4" stroke="#513B43" stroke-width="2.5"/>
                <path d="M7 8H17" stroke="#513B43" stroke-width="2.5" stroke-linecap="round"/>
                <path d="M7 13H17" stroke="#513B43" stroke-width="2.5" stroke-linecap="round"/>
                <path d="M7 17H13" stroke="#513B43" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
        </div>
        <h1 style='color: #513B43; font-weight: 800; font-size: 2.5rem; margin: 0px; padding: 0px;'>Video Note Extractor</h1>
        <p style='color: #513B43; opacity: 0.85; font-size: 1.05rem; max-width: 560px; margin: 8px auto 0px auto; font-weight: 400; line-height: 1.5;'>
            Convert global video transmissions into comprehensive, academic-grade structured notes via automated whisper speech models.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ── Sidebar settings (Custom Soft Dark Theme Controls with Compressed Gaps) ───
with st.sidebar:
    st.markdown("<h2 style='margin-bottom: 1rem; font-weight:700;'>⚙️ Settings</h2>",
                unsafe_allow_html=True)

    groq_key = os.getenv("GROQ_API_KEY", "")

    st.markdown("---")

    whisper_model = st.selectbox(
        "Whisper Model Strength",
        options=["tiny", "base", "small", "medium"],
        index=1,
    )

    frame_interval = st.slider(
        "Visual Frame Extraction (secs)",
        min_value=10,
        max_value=120,
        value=30,
        step=10,
    )

    st.markdown("---")

    st.markdown("<h3 style='font-size: 1.1rem; font-weight:600; margin-bottom: 0.5rem;'>🌐 Supported Platforms</h3>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="platform-row">
            <span style="display:flex; align-items:center; gap:8px;">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="#FF0000"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                <b style="color: #FFFFFF;">YouTube Engine</b>
            </span>
            <span class="badge-active">Active</span>
        </div>
        <div class="platform-row">
            <span class="platform-name-clean">📹 Vimeo Indexer</span>
            <span class="badge-future">Soon</span>
        </div>
        <div class="platform-row">
            <span class="platform-name-clean">🎓 Coursera Link</span>
            <span class="badge-future">Soon</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.caption("⚡ Core Stack: Whisper Core · LLaMA 3.3 · OpenCV")

# ── Main Action Form Target Input ─────────────────────────────────────────────
st.markdown("<h4 style='color: #513B43; font-weight: 600; margin-bottom: 8px; font-size:1rem;'>🔗 Video Target Endpoint</h4>", unsafe_allow_html=True)
video_url = st.text_input(
    label="Video URL Input",
    label_visibility="collapsed",
    placeholder="Paste YouTube lecture or context link here...",
)

st.write("")

col1, col2 = st.columns([3.2, 1])
with col1:
    run_btn = st.button("🚀 Generate AI Notes", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

if clear_btn:
    st.rerun()

# ── Pipeline Architecture Execution ───────────────────────────────────────────
if run_btn:
    if not video_url.strip():
        st.warning("Please specify an active stream target URL.")
    elif not os.getenv("GROQ_API_KEY"):
        st.error(
            "Missing Environment Token: Update Groq Cloud Access inside configuration.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(msg, pct):
            progress_bar.progress(pct)
            status_text.markdown(f"⏳ **{msg}**")

        try:
            result = run_pipeline(
                video_url=video_url.strip(),
                output_dir="outputs",
                frame_interval=frame_interval,
                whisper_model=whisper_model,
                progress_callback=update_progress,
            )

            progress_bar.progress(100)
            status_text.markdown("✅ **Processing completed successfully!**")

            st.success(f"📺 **Target Title:** {result['title']}")

            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Language", result["language"].upper())
            col_b.metric("Extracted Visuals", result["visual_frames_found"])
            col_c.metric("Format Channels", "MD / PDF")

            st.divider()

            st.subheader("📄 Generated Academic Notes")
            st.markdown(
                f'<div class="note-box">{result["notes_text"]}</div>', unsafe_allow_html=True)

            st.divider()

            st.subheader("⬇️ Document Export Options")
            dl_col1, dl_col2 = st.columns(2)
            pdf_path = result["pdf_path"].replace(".md", ".pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    dl_col2.download_button(
                        label="📕 Download PDF Report",
                        data=f,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        use_container_width=True,
                    )

            with st.expander("🎙️ View Complete Audio Transcript"):
                st.text(result["transcript"])

        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Execution Failure: {str(e)}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align: center; color: #513B43; opacity: 0.7; font-size: 0.8rem; font-weight: 500; letter-spacing: 0.3px;'>"
    "Developed by Rameen"
    "</p>",
    unsafe_allow_html=True
)
