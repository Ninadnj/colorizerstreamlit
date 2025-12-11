import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO

# ---------------------------------------------------------
#   PAGE CONFIG — DIOR EDITION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Colorizer — Haute Couture Edition",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
#   STYLE VARIABLES — COUTURE PALETTE
# ---------------------------------------------------------
bg = "#FAFAFA"                  # Dior white
card = "#FFFFFF"                # Pure white
border = "rgba(0,0,0,0.08)"     # Soft, elegant outline
accent = "#111111"              # Almost-black ink
frost = "rgba(180, 200, 220, 0.55)"  # Cold ice-blue glow
shadow_soft = "0 4px 30px rgba(0,0,0,0.06)"
shadow_strong = "0 28px 60px rgba(0,0,0,0.18)"


# ---------------------------------------------------------
#   CUSTOM COUTURE CSS — CLEAN, LUXE, EDITORIAL
# ---------------------------------------------------------
st.markdown(
    f"""
<style>

    /* GLOBAL — DIOR CLEAN */
    body, html {{
        background: {bg};
        color: {accent};
        font-family: 'Inter', -apple-system, sans-serif;
    }}

    /* FILE UPLOADER — WHITE-ON-WHITE LUXURY */
    .stFileUploader label {{
        background: {card};
        padding: 32px;
        border-radius: 18px;
        border: 1px solid {border};
        box-shadow: {shadow_soft};
        transition: all 0.25s ease;
        text-align: center;
        font-weight: 500;
        letter-spacing: 0.3px;
    }}
    .stFileUploader label:hover {{
        transform: translateY(-3px);
        border-color: {frost};
        box-shadow: {shadow_strong};
    }}

    /* RESULT FRAME — COLD SHADOWS, EDITORIAL EDGE */
    .result-frame {{
        margin-top: 28px;
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid {border};
        box-shadow: {shadow_soft};
        transition: 0.35s ease;
        position: relative;
    }}
    .result-frame:hover {{
        transform: scale(1.012);
        border-color: {frost};
        box-shadow: {shadow_strong};
    }}
    .result-frame img {{
        width: 100%;
        border-radius: inherit;
        transition: transform 0.4s ease;
    }}
    .result-frame:hover img {{
        transform: scale(1.028);
    }}

    /* DOWNLOAD BUTTON — HAUTE MINIMALISM */
    .download-btn {{
        display: inline-flex;
        padding: 14px 36px;
        background: {card};
        border-radius: 14px;
        border: 1px solid {border};
        font-weight: 600;
        letter-spacing: 0.5px;
        color: {accent};
        text-decoration: none;
        transition: all 0.25s ease;
        box-shadow: {shadow_soft};
    }}
    .download-btn:hover {{
        transform: translateY(-3px);
        border-color: {frost};
        box-shadow: {shadow_strong};
    }}

</style>
""",
    unsafe_allow_html=True
)

# ---------------------------------------------------------
#   PAGE TITLE — EDITORIAL MINIMAL
# ---------------------------------------------------------
st.markdown(
    """
    <h1 style='text-align:center; font-weight:600; letter-spacing:1px; margin-bottom:6px;'>
        Colorizer — Haute Couture Edition
    </h1>
    <p style='text-align:center; opacity:0.7; margin-top:-8px; font-size:14px;'>
        Black-and-white? Very vintage. Let's fix that.
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
#   FILE UPLOAD — CLEAN
# ---------------------------------------------------------
uploaded = st.file_uploader("Upload your grayscale image", type=["jpg", "jpeg", "png"])

# ---------------------------------------------------------
#   PROCESS & DISPLAY
# ---------------------------------------------------------
if uploaded:

    img = Image.open(uploaded).convert("RGB")

    # Fake colorization placeholder — integrate your model here
    colorized = img  # replace with YOUR OUTPUT

    st.markdown("<div class='result-frame'>", unsafe_allow_html=True)
    st.image(colorized, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Prepare download
    buf = BytesIO()
    colorized.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.markdown(
        f"""
        <a href="data:file/png;base64,{str(np.base64.b64encode(byte_im),'utf-8')}"
           download="colorized.png"
           class="download-btn">
            Download Image
        </a>
        """,
        unsafe_allow_html=True
    )
