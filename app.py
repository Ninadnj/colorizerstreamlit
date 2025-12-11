import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from skimage import color
import base64, io, os

from cat_colorizer import models


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="COLORIZER",
    page_icon="🐈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# LOAD HERO IMAGE
# =========================================================
hero_image_path = "/Users/ninadoinjashvili/code/Nina_new_colorizer/assets/cool-cat.webp"


def load_hero_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


hero_bg = load_hero_base64(hero_image_path)


# =========================================================
# GLOBAL CSS — CLEAN WHITE + EDITORIAL
# =========================================================
st.markdown(
    f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;600&family=Playfair+Display:wght@400;600;700&display=swap');

.stApp {{
    background: #ffffff !important;
    font-family: 'Inter', sans-serif;
    color: #1a1a1a;
}}

header[data-testid="stHeader"], footer, #MainMenu {{
    display: none !important;
}}

.block-container {{
    padding-top: 0.5rem !important;
    max-width: 1600px !important;
}}

/* HERO */
.hero-box {{
    background: url("data:image/webp;base64,{hero_bg}") no-repeat right center;
    background-size: cover;
    padding: 160px 40px;
    border-bottom: 1px solid #eee;
    margin-bottom: 50px;
}}

.hero-title {{
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    text-transform: uppercase;
    margin-bottom: 8px;
    color: #111;
}}

.hero-sub {{
    font-size: 1rem;
    color: #666;
}}

/* CARDS */
.card {{
    background: white;
    padding: 22px;
    border-radius: 6px;
    border: 1px solid #eaeaea;
    box-shadow: 0 4px 18px rgba(0,0,0,0.04);
    margin-bottom: 22px;
}}

.card-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    margin-bottom: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.steps-row {{
    display: flex;
    gap: 16px;
}}

.step-card {{
    flex: 1;
    border: 1px solid #eaeaea;
    border-radius: 6px;
    padding: 18px;
    background: #fff;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
}}

.step-num-h {{
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    margin-bottom: 6px;
    color: #111;
}}

.step-text-h {{
    font-size: 0.9rem;
    color: #666;
}}

/* UPLOADER */
[data-testid="stFileUploader"] {{
    border: 1px dashed #dcdcdc !important;
    background: #fafafa !important;
    padding: 20px !important;
}}

[data-testid="stFileUploader"] button {{
    background: white !important;
    border: 1px solid #ccc;
    color: #111 !important;
}}

/* RESULTS */
.result-frame {{
    border: 1px solid #eaeaea;
    padding: 6px;
    border-radius: 6px;
    background: white;
    box-shadow: 0 4px 18px rgba(0,0,0,0.04);
}}

.result-label {{
    text-align: center;
    font-size: 0.85rem;
    color: #444;
    margin-bottom: 6px;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

/* LOADING OVERLAY */
.loading-overlay {{
    position: fixed;
    top:0; left:0;
    width:100%; height:100%;
    backdrop-filter: blur(12px) brightness(1.1);
    background: rgba(255,255,255,0.75);
    z-index: 9999;
    display:flex;
    align-items:center;
    justify-content:center;
}}

.loading-text {{
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    color: #111;
    animation: pulse 1.2s ease-in-out infinite;
}}

@keyframes pulse {{
    0% {{ opacity:0.25; }}
    50% {{ opacity:1; }}
    100% {{ opacity:0.25; }}
}}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# MODEL LOADING
# =========================================================
@st.cache_resource
def load_model(checkpoint_dir="./training_checkpoints"):
    generator = models.Generator()
    ckpt = tf.train.Checkpoint(generator=generator)
    latest = tf.train.latest_checkpoint(checkpoint_dir)
    if latest:
        ckpt.restore(latest).expect_partial()
    return generator


model = load_model()
IMG_SIZE = 256


# =========================================================
# FUNCTIONS — PREPROCESS / POSTPROCESS
# =========================================================
def preprocess(img: Image.Image):
    img = img.resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS).convert("RGB")
    arr = np.array(img) / 255.0
    lab = color.rgb2lab(arr).astype(np.float32)
    L = (lab[..., 0] / 50.0) - 1.0
    return tf.expand_dims(tf.expand_dims(L, -1), 0)


def postprocess(L_input, AB_output):
    L = (L_input[0].numpy() + 1) * 50
    AB = AB_output[0].numpy() * 128
    rgb = color.lab2rgb(np.concatenate([L, AB], axis=-1))
    return np.clip(rgb, 0, 1)


def to_png(rgb):
    buf = io.BytesIO()
    Image.fromarray((rgb * 255).astype(np.uint8)).save(buf, format="PNG")
    return buf.getvalue()


# =========================================================
# HERO SECTION
# =========================================================
st.markdown(
    """
<div class="hero-box">
    <div class="hero-title">COLORIZER</div>
    <div class="hero-sub"> #batch2130Paris</div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# STEPS
# =========================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">How It Works</div>', unsafe_allow_html=True)

st.markdown(
    """
<div class="steps-row">
    <div class="step-card">
        <div class="step-num-h">01</div>
        <div class="step-text-h">Upload a grayscale cat photo.</div>
    </div>
    <div class="step-card">
        <div class="step-num-h">02</div>
        <div class="step-text-h">Our ML model colorizes it instantly.</div>
    </div>
    <div class="step-card">
        <div class="step-num-h">03</div>
        <div class="step-text-h">Download the editorial version.</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# UPLOADER
# =========================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">Upload Your Cat</div>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Drop your image here", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# PROCESS IMAGE
# =========================================================
if uploaded:
    img = Image.open(uploaded)

    # Cinematic overlay
    overlay = st.empty()
    overlay.markdown(
        """
    <div class="loading-overlay">
        <div class="loading-text">Processing…</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    L = preprocess(img)
    AB = model(L, training=False)
    result = postprocess(L, AB)

    overlay.empty()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="result-frame"><div class="result-label">Original</div>',
            unsafe_allow_html=True,
        )
        st.image(img, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="result-frame"><div class="result-label">Colorized — Editorial</div>',
            unsafe_allow_html=True,
        )
        st.image(result, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        "Download Editorial PNG",
        data=to_png(result),
        file_name="Colorizer.png",
        mime="image/png",
    )
