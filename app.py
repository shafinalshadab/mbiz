"""
app.py — mBiz by Zorted Labs
=============================
Cute & Playful UI — AI Content Writing Engine
- Soft pastel aesthetic with kawaii-inspired design
- Warm gradient background with floating sparkles
- Bouncy, bubbly glassmorphic cards
- Playful animations and micro-interactions
- Dual-language font support (English + Bangla)
- Password-protected access gate
- Language selection: Banglish, Bangla, or English
"""

import os
import json
import asyncio
import streamlit as st
from dotenv import load_dotenv
from ai_engine import generate_facebook_content, LANGUAGE_OPTIONS

load_dotenv()

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="mBiz by Zorted Labs",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Inject Custom CSS (Cute Pastel Theme) ───────────────────────────────────

CUSTOM_CSS = """
<style>
    /* ── Reset Streamlit Defaults ── */
    #root > div:nth-child(1) > div > div > div > div > section,
    .stApp, .stApp > header {
        background: #fff5f7 !important;
    }
    .stApp {
        background: #fff5f7;
    }
    div[data-testid="stToolbar"] { display: none; }
    div[data-testid="stDecoration"] { display: none; }
    header[data-testid="stHeader"] { display: none; }
    .stApp > header { display: none !important; }
    #MainMenu { display: none; }

    /* ── Remove Streamlit default block padding ── */
    .stApp .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
    }
    .stApp .main > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    .stApp .element-container:has(> div:empty),
    .stApp .element-container:has(> .stMarkdown:empty) {
        display: none !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* ── Cute Animated Background ── */
    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background:
            radial-gradient(ellipse 70% 50% at 0% 10%, rgba(255, 182, 193, 0.25) 0%, transparent 60%),
            radial-gradient(ellipse 60% 50% at 100% 90%, rgba(216, 180, 254, 0.2) 0%, transparent 60%),
            radial-gradient(ellipse 50% 40% at 50% 50%, rgba(147, 197, 253, 0.12) 0%, transparent 50%),
            radial-gradient(ellipse 40% 30% at 80% 20%, rgba(252, 165, 165, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse 30% 40% at 20% 80%, rgba(167, 139, 250, 0.1) 0%, transparent 50%);
        animation: softDrift 25s ease-in-out infinite alternate;
    }
    @keyframes softDrift {
        0% { transform: scale(1) rotate(0deg); opacity: 0.8; }
        50% { transform: scale(1.05) rotate(1deg); opacity: 1; }
        100% { transform: scale(1) rotate(-0.5deg); opacity: 0.85; }
    }

    /* ── Floating Sparkles ── */
    body::after {
        content: '✨ 🌸 ✨ 🌷 ✨ 🌺 ✨ 🌻 ✨';
        position: fixed;
        top: -5%;
        left: -5%;
        width: 110%;
        height: 110%;
        font-size: 2rem;
        letter-spacing: 8vw;
        color: transparent;
        text-shadow:
            0 0 0 rgba(255, 182, 193, 0),
            10vw 20vh 0 rgba(255, 182, 193, 0.08),
            30vw 40vh 0 rgba(216, 180, 254, 0.06),
            50vw 15vh 0 rgba(147, 197, 253, 0.07),
            70vw 60vh 0 rgba(252, 165, 165, 0.05),
            20vw 70vh 0 rgba(167, 139, 250, 0.06),
            80vw 30vh 0 rgba(255, 182, 193, 0.07),
            45vw 80vh 0 rgba(216, 180, 254, 0.05),
            90vw 50vh 0 rgba(147, 197, 253, 0.06);
        z-index: -1;
        pointer-events: none;
        animation: sparkleFloat 30s linear infinite;
    }
    @keyframes sparkleFloat {
        0% { transform: translateY(0) rotate(0deg); }
        100% { transform: translateY(-30vh) rotate(10deg); }
    }

    /* ── Typography Base (Dual-Language) ── */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Hind Siliguri', 'Poppins', sans-serif;
        color: #4a4a5a;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    * {
        line-height: 1.7;
    }

    /* ── Main Container ── */
    .main-container {
        max-width: 820px;
        margin: 0 auto;
        padding: 0.5rem 1.5rem 3rem;
        position: relative;
        z-index: 1;
    }

    /* ── Cute Brand Header ── */
    .brand-header {
        text-align: center;
        margin-bottom: 2rem;
        padding-top: 1.5rem;
        animation: bounceIn 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3) translateY(-30px); }
        50% { opacity: 1; transform: scale(1.05) translateY(5px); }
        70% { transform: scale(0.95) translateY(-2px); }
        100% { transform: scale(1) translateY(0); }
    }
    .brand-header .logo-wrapper {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.6rem;
        margin-bottom: 0.3rem;
        position: relative;
    }
    .brand-header .logo-icon {
        font-size: 2.5rem;
        display: inline-block;
        animation: wiggle 3s ease-in-out infinite;
    }
    @keyframes wiggle {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(-8deg); }
        75% { transform: rotate(8deg); }
    }
    .brand-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f472b6 0%, #a78bfa 50%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
        margin-bottom: 0.15rem;
        background-size: 200% 200%;
        animation: softGradient 5s ease-in-out infinite;
        text-shadow: none;
    }
    @keyframes softGradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    .brand-header .subtitle {
        font-size: 0.95rem;
        color: #a78ba0;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    .brand-header .subtitle span {
        background: linear-gradient(135deg, #f472b6, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    .brand-header .tagline {
        font-size: 0.78rem;
        color: #c4a8b8;
        margin-top: 0.4rem;
        letter-spacing: 0.3px;
    }
    .brand-header .tagline span {
        color: #a78bfa;
        font-weight: 600;
    }

    /* ── Cute Decorative Divider ── */
    .cute-divider {
        text-align: center;
        font-size: 1.2rem;
        color: #e8d0dc;
        margin: 0.5rem 0 1.2rem;
        letter-spacing: 6px;
        animation: fadeSlideDown 0.6s ease-out;
    }

    /* ── Cute Glassmorphic Card ── */
    .cute-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 2px solid rgba(255, 182, 193, 0.25);
        border-radius: 28px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.25rem;
        box-shadow:
            0 4px 24px rgba(244, 114, 182, 0.08),
            0 2px 8px rgba(0, 0, 0, 0.03),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }
    .cute-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255, 182, 193, 0.08) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .cute-card:hover {
        transform: translateY(-4px) scale(1.01);
        border-color: rgba(255, 182, 193, 0.45);
        box-shadow:
            0 12px 40px rgba(244, 114, 182, 0.12),
            0 4px 12px rgba(0, 0, 0, 0.04);
    }

    /* ── Cute Form Labels ── */
    .cute-label {
        font-size: 0.8rem;
        font-weight: 700;
        color: #c084a8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.5rem;
        display: block;
    }
    .cute-label .label-icon {
        margin-right: 0.3rem;
    }

    /* ── Streamlit Input Overrides (Cute Style) ── */
    div[data-testid="stTextInput"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextArea"] label {
        display: none !important;
    }
    div[data-testid="stTextInput"] > div,
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stTextArea"] > div {
        margin-top: 0 !important;
    }
    .stTextInput input, .stTextArea textarea, div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.85) !important;
        border: 2px solid rgba(244, 114, 182, 0.15) !important;
        border-radius: 18px !important;
        color: #4a4a5a !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(244, 114, 182, 0.04) !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #f472b6 !important;
        box-shadow: 0 0 0 4px rgba(244, 114, 182, 0.1) !important;
    }
    .stTextArea textarea {
        min-height: 80px !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #d4b8c8 !important;
        font-weight: 400;
    }

    /* ── Selectbox / Dropdown (Cute) ── */
    div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.85) !important;
    }
    div[data-baseweb="select"] > div > div {
        color: #4a4a5a !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="select"] span {
        color: #4a4a5a !important;
    }
    div[data-baseweb="select"] svg {
        fill: #f472b6 !important;
    }
    div[data-baseweb="popover"] {
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(20px);
        border: 2px solid rgba(244, 114, 182, 0.2) !important;
        border-radius: 18px !important;
        box-shadow: 0 16px 48px rgba(244, 114, 182, 0.1) !important;
    }
    div[data-baseweb="popover"] li {
        color: #4a4a5a !important;
        padding: 0.6rem 1rem !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="popover"] li:hover {
        background: rgba(244, 114, 182, 0.08) !important;
    }
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background: rgba(244, 114, 182, 0.15) !important;
        color: #d9467a !important;
        font-weight: 600 !important;
    }

    /* ── Cute Button ── */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #f472b6, #a78bfa, #60a5fa) !important;
        background-size: 200% 200% !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.85rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: 0.02em;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 4px 20px rgba(244, 114, 182, 0.25), 0 2px 8px rgba(0, 0, 0, 0.05) !important;
        position: relative;
        overflow: hidden;
        animation: btnShimmer 4s ease-in-out infinite;
    }
    @keyframes btnShimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    div.stButton > button::after {
        content: '✨';
        position: absolute;
        top: -10px;
        right: 20px;
        font-size: 1.2rem;
        opacity: 0.6;
        animation: sparkle 2s ease-in-out infinite;
        pointer-events: none;
    }
    @keyframes sparkle {
        0%, 100% { opacity: 0.4; transform: scale(0.8) rotate(0deg); }
        50% { opacity: 1; transform: scale(1.2) rotate(20deg); }
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(244, 114, 182, 0.35), 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    }
    div.stButton > button:active {
        transform: translateY(0px) scale(0.98) !important;
    }

    /* ── Cute Variation Cards ── */
    .var-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 2px solid rgba(244, 114, 182, 0.12);
        border-radius: 24px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
        animation: popIn 0.5s ease-out forwards;
        opacity: 0;
        transform: scale(0.9);
    }
    .var-card:nth-child(1) { animation-delay: 0.1s; }
    .var-card:nth-child(2) { animation-delay: 0.2s; }
    .var-card:nth-child(3) { animation-delay: 0.3s; }
    @keyframes popIn {
        0% { opacity: 0; transform: scale(0.9) translateY(15px); }
        70% { opacity: 1; transform: scale(1.02) translateY(-3px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }
    .var-card:hover {
        transform: translateY(-3px) scale(1.01);
        border-color: rgba(244, 114, 182, 0.3);
        box-shadow: 0 8px 32px rgba(244, 114, 182, 0.1);
    }

    /* Variation A — Pink */
    .var-card.var-a {
        border-left: 5px solid #f472b6;
    }
    .var-card.var-a .var-badge {
        background: rgba(244, 114, 182, 0.12);
        color: #db2777;
        border: 1px solid rgba(244, 114, 182, 0.2);
    }

    /* Variation B — Purple */
    .var-card.var-b {
        border-left: 5px solid #a78bfa;
    }
    .var-card.var-b .var-badge {
        background: rgba(167, 139, 250, 0.12);
        color: #7c3aed;
        border: 1px solid rgba(167, 139, 250, 0.2);
    }

    /* Variation C — Blue */
    .var-card.var-c {
        border-left: 5px solid #60a5fa;
    }
    .var-card.var-c .var-badge {
        background: rgba(96, 165, 250, 0.12);
        color: #2563eb;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }

    .var-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        padding: 0.3rem 0.85rem;
        border-radius: 50px;
        margin-bottom: 0.6rem;
    }

    .var-headline {
        font-size: 1.1rem;
        font-weight: 700;
        color: #3b3b4a;
        margin-bottom: 0.4rem;
        line-height: 1.4;
    }
    .var-body {
        font-size: 0.9rem;
        color: #6b6b7a;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    /* ── Cute Copy Button ── */
    .cute-copy-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: rgba(244, 114, 182, 0.08) !important;
        border: 1.5px solid rgba(244, 114, 182, 0.15) !important;
        border-radius: 50px !important;
        color: #db2777 !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        padding: 0.35rem 1rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        font-family: inherit !important;
    }
    .cute-copy-btn:hover {
        background: rgba(244, 114, 182, 0.15) !important;
        border-color: rgba(244, 114, 182, 0.3) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(244, 114, 182, 0.12);
    }

    /* ── Copy All Button ── */
    .copy-all-btn-cute {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(167, 139, 250, 0.1) !important;
        border: 1.5px solid rgba(167, 139, 250, 0.2) !important;
        border-radius: 50px !important;
        color: #7c3aed !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.8rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        font-family: inherit !important;
    }
    .copy-all-btn-cute:hover {
        background: rgba(167, 139, 250, 0.18) !important;
        border-color: rgba(167, 139, 250, 0.35) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(167, 139, 250, 0.12);
    }

    /* ── Score Badge (Cute) ── */
    .score-badge-cute {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.8);
        border: 2px solid rgba(244, 114, 182, 0.15);
        border-radius: 50px;
        padding: 0.5rem 1.4rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: #db2777;
        margin-bottom: 1.2rem;
        animation: popIn 0.5s ease-out;
        box-shadow: 0 2px 12px rgba(244, 114, 182, 0.06);
    }
    .score-badge-cute .score-num {
        font-size: 1.4rem;
        font-weight: 800;
    }

    /* ── Cute Loading Animation ── */
    .loading-cute {
        text-align: center;
        padding: 1.5rem 0;
        animation: fadeIn 0.3s ease-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .loading-cute .loading-text {
        color: #a78ba0;
        font-size: 0.9rem;
        margin-bottom: 1.2rem;
    }
    .loading-cute .loading-text .highlight {
        color: #f472b6;
        font-weight: 700;
    }
    .loading-cute .loading-emoji {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        animation: bounce 1.5s ease-in-out infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-12px); }
    }
    .loading-bar-cute {
        width: 240px;
        height: 6px;
        background: rgba(244, 114, 182, 0.1);
        border-radius: 10px;
        margin: 0 auto 1rem;
        overflow: hidden;
        position: relative;
    }
    .loading-bar-fill-cute {
        height: 100%;
        width: 40%;
        background: linear-gradient(90deg, #f472b6, #a78bfa, #60a5fa);
        border-radius: 10px;
        animation: loadingSweep 1.8s ease-in-out infinite;
    }
    @keyframes loadingSweep {
        0% { transform: translateX(-100%); width: 40%; }
        50% { width: 60%; }
        100% { transform: translateX(350%); width: 40%; }
    }
    .loading-dots-cute {
        display: flex;
        justify-content: center;
        gap: 8px;
    }
    .loading-dots-cute div {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #f472b6;
        animation: cuteBounce 1.4s infinite ease-in-out both;
    }
    .loading-dots-cute div:nth-child(1) { animation-delay: -0.32s; background: #f472b6; }
    .loading-dots-cute div:nth-child(2) { animation-delay: -0.16s; background: #a78bfa; }
    .loading-dots-cute div:nth-child(3) { animation-delay: 0s; background: #60a5fa; }
    @keyframes cuteBounce {
        0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
        40% { transform: scale(1.2); opacity: 1; }
    }

    /* ── Password Wall ── */
    .password-wall-cute {
        text-align: center;
        padding: 2rem 1rem;
    }
    .password-wall-cute .lock-icon {
        font-size: 3.5rem;
        margin-bottom: 0.8rem;
        display: block;
        animation: wiggle 3s ease-in-out infinite;
    }
    .password-wall-cute h2 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #3b3b4a;
        margin-bottom: 0.4rem;
    }
    .password-wall-cute p {
        color: #a78ba0;
        margin-bottom: 1.2rem;
        font-size: 0.9rem;
    }

    /* ── Error / Info Messages ── */
    div[data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.85) !important;
        border: 2px solid rgba(244, 114, 182, 0.15) !important;
        border-radius: 18px !important;
        color: #4a4a5a !important;
        padding: 0.75rem 1rem !important;
    }
    div[data-testid="stAlert"] svg {
        fill: #f472b6 !important;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-color: #f472b6 !important;
        border-top-color: transparent !important;
        border-width: 3px !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.7) !important;
        border-radius: 16px !important;
        border: 2px solid rgba(244, 114, 182, 0.1) !important;
        color: #c084a8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: rgba(244, 114, 182, 0.25) !important;
        background: rgba(255, 255, 255, 0.85) !important;
    }
    .streamlit-expanderContent {
        border: none !important;
        background: transparent !important;
    }

    /* ── Cute Footer ── */
    .footer-cute {
        text-align: center;
        padding: 2rem 0 0.5rem;
        font-size: 0.78rem;
        color: #c4a8b8;
        border-top: 2px solid rgba(244, 114, 182, 0.06);
        margin-top: 0.5rem;
    }
    .footer-cute span {
        background: linear-gradient(135deg, #f472b6, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    .footer-cute .footer-links {
        margin-top: 0.4rem;
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        font-size: 0.72rem;
    }
    .footer-cute .footer-links a {
        color: #c4a8b8;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    .footer-cute .footer-links a:hover {
        color: #f472b6;
    }

    /* ── Responsive ── */
    @media (max-width: 640px) {
        .main-container { padding: 0.5rem 0.75rem 2.5rem; }
        .brand-header h1 { font-size: 2rem; }
        .brand-header { padding-top: 0.5rem; }
        .cute-card { padding: 1.1rem 1.2rem; border-radius: 22px; }
        .var-card { padding: 1rem 1.1rem; border-radius: 20px; }
    }
</style>
"""


# ── Font Configuration ─────────────────────────────────────────────────────

FONT_OPTIONS = {
    "🌸 Soft & Sweet (Inter + Hind Siliguri)": {
        "name": "Inter + Hind Siliguri",
        "url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Hind+Siliguri:wght@300;400;500;600;700&display=swap",
        "css": "font-family: 'Inter', 'Hind Siliguri', sans-serif;",
    },
    "🎀 Playful Vibe (Space Grotesk + Hind Siliguri)": {
        "name": "Space Grotesk + Hind Siliguri",
        "url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Hind+Siliguri:wght@300;400;500;600;700&display=swap",
        "css": "font-family: 'Space Grotesk', 'Hind Siliguri', sans-serif;",
    },
    "💖 Cute & Cozy (Outfit + Hind Siliguri)": {
        "name": "Outfit + Hind Siliguri",
        "url": "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Hind+Siliguri:wght@300;400;500;600;700&display=swap",
        "css": "font-family: 'Outfit', 'Hind Siliguri', sans-serif;",
    },
    "🌈 Friendly Duo (Poppins + Hind Siliguri)": {
        "name": "Poppins + Hind Siliguri",
        "url": "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Hind+Siliguri:wght@300;400;500;600;700&display=swap",
        "css": "font-family: 'Poppins', 'Hind Siliguri', sans-serif;",
    },
}


def inject_font(font_key: str) -> str:
    """Return the CSS <link> tag for the selected Google Font."""
    font = FONT_OPTIONS.get(font_key, FONT_OPTIONS["🌸 Soft & Sweet (Inter + Hind Siliguri)"])
    return f'<link href="{font["url"]}" rel="stylesheet">'


def get_font_css(font_key: str) -> str:
    """Return the CSS rule for the selected font."""
    font = FONT_OPTIONS.get(font_key, FONT_OPTIONS["🌸 Soft & Sweet (Inter + Hind Siliguri)"])
    return font["css"]


# ── Session State Init ─────────────────────────────────────────────────────

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "generated_content" not in st.session_state:
    st.session_state.generated_content = None
if "audit_log" not in st.session_state:
    st.session_state.audit_log = None
if "final_score" not in st.session_state:
    st.session_state.final_score = 0
if "selected_font" not in st.session_state:
    st.session_state.selected_font = "🌸 Soft & Sweet (Inter + Hind Siliguri)"
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "🌐 Banglish (Bengali + English Mix)"


# ── Render Functions ───────────────────────────────────────────────────────

def render_password_wall():
    """Render the password-protected access gate."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        f"""
        {inject_font(st.session_state.selected_font)}
        <style>
            html, body, [class*="css"] {{ {get_font_css(st.session_state.selected_font)} }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Brand header
    st.markdown(
        """
        <div class="brand-header">
            <div class="logo-wrapper">
                <span class="logo-icon">🌸</span>
                <h1>mBiz</h1>
            </div>
            <div class="subtitle">by <span>Zorted Labs</span> — AI Content Writing Engine</div>
            <div class="tagline">Powered by <span>2026 Meta Algorithm</span> • Made with 💖 for Bangladesh</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Password card
    st.markdown(
        """
        <div class="cute-card password-wall-cute">
            <span class="lock-icon">🔐</span>
            <h2>Hi there! 💕</h2>
            <p>Enter your secret password to unlock the magic ✨</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your APP_PASSWORD...",
        label_visibility="collapsed",
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌸 Unlock the Magic", use_container_width=True):
            app_password = os.getenv("APP_PASSWORD", "")
            if password == app_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Oops! That's not the right password. Try again! 💪")

    st.markdown("</div>", unsafe_allow_html=True)


def render_main_app():
    """Render the main application interface."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        f"""
        {inject_font(st.session_state.selected_font)}
        <style>
            html, body, [class*="css"] {{ {get_font_css(st.session_state.selected_font)} }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # ── Brand Header ──
    st.markdown(
        """
        <div class="brand-header">
            <div class="logo-wrapper">
                <span class="logo-icon">🌸</span>
                <h1>mBiz</h1>
            </div>
            <div class="subtitle">by <span>Zorted Labs</span> — AI Content Writing Engine</div>
            <div class="tagline">Powered by <span>2026 Meta Algorithm</span> • Made with 💖 for Bangladesh</div>
        </div>
        <div class="cute-divider">✿ ✿ ✿</div>
        """,
        unsafe_allow_html=True,
    )

    # ── Language Selector ──
    st.markdown('<div class="cute-card">', unsafe_allow_html=True)
    st.markdown('<span class="cute-label"><span class="label-icon">🌍</span> Caption Language</span>', unsafe_allow_html=True)
    selected_language = st.selectbox(
        "Caption Language",
        options=list(LANGUAGE_OPTIONS.keys()),
        index=list(LANGUAGE_OPTIONS.keys()).index(st.session_state.selected_language),
        label_visibility="collapsed",
    )
    if selected_language != st.session_state.selected_language:
        st.session_state.selected_language = selected_language
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Font Selector ──
    st.markdown('<div class="cute-card">', unsafe_allow_html=True)
    st.markdown('<span class="cute-label"><span class="label-icon">🎨</span> Output Presentation Style</span>', unsafe_allow_html=True)
    selected_font = st.selectbox(
        "Font Style",
        options=list(FONT_OPTIONS.keys()),
        index=list(FONT_OPTIONS.keys()).index(st.session_state.selected_font),
        label_visibility="collapsed",
    )
    if selected_font != st.session_state.selected_font:
        st.session_state.selected_font = selected_font
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Input Form ──
    st.markdown('<div class="cute-card">', unsafe_allow_html=True)
    st.markdown('<span class="cute-label"><span class="label-icon">📋</span> Tell Me About Your Product</span>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input(
            "Product Name",
            placeholder="e.g. LuxeFit Slim Blazer ✨",
            label_visibility="collapsed",
        )
    with col2:
        product_category = st.text_input(
            "Category",
            placeholder="e.g. Men's Fashion 👔",
            label_visibility="collapsed",
        )

    core_usp = st.text_input(
        "Core USP",
        placeholder="e.g. Stretch fabric, wrinkle-free, tailored for Bangladeshi men 🌟",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns(2)
    with col1:
        target_location = st.text_input(
            "Target Location",
            placeholder="e.g. Dhaka, Bangladesh 🏙️",
            label_visibility="collapsed",
        )
    with col2:
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g. Professional men 25-45 👨‍💼",
            label_visibility="collapsed",
        )

    additional_context = st.text_area(
        "Additional Context (optional)",
        placeholder="e.g. Office wear + casual dinner vibe. Price: ৳3,500 💫",
        label_visibility="collapsed",
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Generate Button ──
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_clicked = st.button(
            "✨ Generate Magical Content",
            use_container_width=True,
            type="primary",
        )

    # ── Generation Logic ──
    if generate_clicked:
        if not all([product_name, product_category, core_usp, target_location, target_audience]):
            st.error("⚠️ Oops! Please fill in all the required fields first! 💕")
        else:
            with st.spinner(""):
                # Show cute loading animation
                st.markdown(
                    """
                    <div class="loading-cute">
                        <div class="loading-emoji">🧠</div>
                        <div class="loading-text">
                            <span class="highlight">🌸 mBiz AI</span> is cooking up something amazing...
                        </div>
                        <div class="loading-bar-cute">
                            <div class="loading-bar-fill-cute"></div>
                        </div>
                        <div class="loading-dots-cute">
                            <div></div><div></div><div></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Get language code from selected language
                language_code = LANGUAGE_OPTIONS[st.session_state.selected_language]["code"]

                # Run async generation
                result = asyncio.run(
                    generate_facebook_content(
                        product_name=product_name.strip(),
                        product_category=product_category.strip(),
                        core_usp=core_usp.strip(),
                        target_location=target_location.strip(),
                        target_audience=target_audience.strip(),
                        additional_context=additional_context.strip(),
                        language_code=language_code,
                    )
                )

                if result["success"] and result["content"]:
                    st.session_state.generated_content = result["content"]
                    st.session_state.audit_log = result.get("audit_log", [])
                    st.session_state.final_score = result.get("final_score", 0)
                    st.rerun()
                else:
                    error_msg = result.get("error", "Unknown error occurred.")
                    st.error(f"❌ Oh no! Generation failed: {error_msg} 😢")

    # ── Display Results ──
    if st.session_state.generated_content:
        content = st.session_state.generated_content
        audit_log = st.session_state.audit_log
        final_score = st.session_state.final_score

        # Score badge
        score_color = "#db2777" if final_score >= 10 else "#f59e0b"
        st.markdown(
            f"""
            <div style="text-align:center;">
                <div class="score-badge-cute" style="border-color: {score_color}33; color: {score_color};">
                    🏆 Audit Score: <span class="score-num">{final_score}/10</span>
                    {'✅ Yay!' if final_score >= 10 else '🔄 Needs Work'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Audit log summary (collapsible)
        if audit_log:
            with st.expander("📊 Peek Behind the Scenes ✨", expanded=False):
                for entry in audit_log:
                    it = entry["iteration"]
                    score = entry["overall"]
                    passed = entry["passed"]
                    issues = entry.get("issues", [])
                    fix = entry.get("fix", "")
                    status_icon = "✅" if passed else "🔄"
                    st.markdown(
                        f"""
                        <div style="background:rgba(255,255,255,0.6);border-radius:16px;padding:0.75rem 1rem;margin-bottom:0.5rem;border:1px solid rgba(244,114,182,0.08);">
                            <strong style="color:#4a4a5a;">{status_icon} Round {it} — Score: {score}/10</strong>
                            {"<span style='color:#db2777;margin-left:0.5rem;'>✨ Passed!</span>" if passed else "<span style='color:#f59e0b;margin-left:0.5rem;'>🔄 Needed some tweaks</span>"}
                            {f"<br><span style='color:#f59e0b;font-size:0.85rem;'>Issues: {', '.join(issues)}</span>" if issues else ""}
                            {f"<br><span style='color:#a78ba0;font-size:0.85rem;'>Fix: {fix[:200]}{'...' if len(fix) > 200 else ''}</span>" if fix else ""}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # ── Variation A ──
        var_a = content.get("variation_a", {})
        st.markdown(
            f"""
            <div class="var-card var-a">
                <div class="var-badge">💕 Variation A — Hook-Story Matrix</div>
                <div class="var-headline">{var_a.get("headline", "")}</div>
                <div class="var-body">{var_a.get("body", "")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Variation B ──
        var_b = content.get("variation_b", {})
        st.markdown(
            f"""
            <div class="var-card var-b">
                <div class="var-badge">✨ Variation B — Lifestyle Flex</div>
                <div class="var-headline">{var_b.get("headline", "")}</div>
                <div class="var-body">{var_b.get("body", "")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Variation C ──
        var_c = content.get("variation_c", {})
        st.markdown(
            f"""
            <div class="var-card var-c">
                <div class="var-badge">🌟 Variation C — Value-Math Engine</div>
                <div class="var-headline">{var_c.get("headline", "")}</div>
                <div class="var-body">{var_c.get("body", "")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Copy All Button ──
        full_text = (
            f"💕 VARIATION A — Hook-Story Matrix\n\n{var_a.get('headline', '')}\n\n{var_a.get('body', '')}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"✨ VARIATION B — Lifestyle Flex\n\n{var_b.get('headline', '')}\n\n{var_b.get('body', '')}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🌟 VARIATION C — Value-Math Engine\n\n{var_c.get('headline', '')}\n\n{var_c.get('body', '')}"
        )
        json_text = json.dumps(full_text, ensure_ascii=False)

        st.markdown(
            f"""
            <div style="text-align:center;margin-top:0.5rem;">
                <button class="copy-all-btn-cute" id="copy-all-btn-cute"
                    style="background:rgba(167,139,250,0.1) !important;border:1.5px solid rgba(167,139,250,0.2) !important;border-radius:50px !important;color:#7c3aed !important;font-size:0.9rem !important;font-weight:600 !important;padding:0.6rem 1.8rem !important;cursor:pointer !important;transition:all 0.3s ease !important;font-family:inherit !important;">
                    📋 Copy All to Clipboard
                </button>
            </div>
            <script>
            (function() {{
                var btn = document.getElementById('copy-all-btn-cute');
                if (!btn) return;
                var text = {json_text};
                btn.onclick = function() {{
                    navigator.clipboard.writeText(text).then(function() {{
                        btn.textContent = '✅ Copied! 💕';
                        var self = btn;
                        setTimeout(function() {{
                            self.textContent = '📋 Copy All to Clipboard';
                        }}, 2000);
                    }}).catch(function() {{
                        btn.textContent = '❌ Failed 😢';
                    }});
                }};
            }})();
            </script>
            """,
            unsafe_allow_html=True,
        )

        # ── Generate Again ──
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Generate Fresh Content", use_container_width=True):
                st.session_state.generated_content = None
                st.session_state.audit_log = None
                st.session_state.final_score = 0
                st.rerun()

    # ── Footer ──
    st.markdown(
        """
        <div class="footer-cute">
            Made with 💖 by <span>Zorted Labs</span> • Powered by 2026 Meta Algorithm
            <div class="footer-links">
                <a href="#">Privacy</a>
                <a href="#">Terms</a>
                <a href="#">Contact</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ── Entry Point ────────────────────────────────────────────────────────────

if not st.session_state.authenticated:
    render_password_wall()
else:
    render_main_app()

