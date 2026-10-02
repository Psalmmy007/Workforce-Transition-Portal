import os
import base64
import time
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from skill_engine import get_career_recommendations, ROLE_SKILL_PROFILES, clean_skill_label
from job_risk_reference import get_external_risk_tier, get_external_risk_basis

# ---------------------------------------------------------
# Asset Loading & Brand Logo Setup
# ---------------------------------------------------------
LOGO_PATH = os.path.join(os.path.dirname(__file__), "career_gps_logo.png")

def get_logo_base64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

LOGO_B64 = get_logo_base64()
FAVICON_IMG = Image.open(LOGO_PATH) if os.path.exists(LOGO_PATH) else None

# ---------------------------------------------------------
# Page Setup & Enterprise Design System
# ---------------------------------------------------------
st.set_page_config(
    page_title="CareerGPS | Enterprise Workforce Mobility",
    page_icon=FAVICON_IMG if FAVICON_IMG else "🌐",
    layout="wide"
)

# ---------------------------------------------------------
# Sidebar Navigation & Single Toggle Theme Control
# ---------------------------------------------------------
if LOGO_B64:
    st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.35rem;">
        <img src="data:image/png;base64,{LOGO_B64}" style="width: 36px; height: 36px; border-radius: 50%; box-shadow: 0 2px 6px rgba(0,0,0,0.12); flex-shrink: 0;" alt="CareerGPS Logo"/>
        <div class="sidebar-brand" style="margin: 0; line-height: 1.1;"><span style="color: var(--ink);">Career</span><span style="color: #2563EB;">GPS</span></div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div class="sidebar-brand"><span style="color: var(--ink);">Career</span><span style="color: #2563EB;">GPS</span></div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-caption">Enterprise Workforce Mobility Intelligence</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="section-label" style="margin-bottom: 0.4rem;">Navigation</div>', unsafe_allow_html=True)
nav_choice = st.sidebar.radio(
    "Navigation Menu",
    ["Workforce Mobility Portal", "Talent Analytics Dashboard", "Methodology & Audited Benchmarks"],
    label_visibility="collapsed"
)

st.sidebar.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="section-label" style="margin-bottom: 0.3rem;">Appearance</div>', unsafe_allow_html=True)
dark_mode = st.sidebar.toggle("Dark mode", value=False)

# Theme-specific design tokens aligned with Brand Identity & Logo
if dark_mode:
    theme_vars = """
        --ink: #F8FAFC;
        --ink-light: #CBD5E1;
        --paper: #0B0F19;
        --paper-raised: #131B2E;
        --paper-card: #182234;
        --line: #293548;
        --line-strong: #3B4B64;
        --signal: #F59E0B;
        --signal-tint: #261E10;
        --slate: #3B82F6;
        --slate-tint: #132238;
        --moss: #10B981;
        --moss-tint: #0D261E;
        --brick: #EF4444;
        --brick-tint: #281414;
        --muted: #94A3B8;
        --btn-bg: #2563EB;
        --btn-text: #FFFFFF;
        --btn-border: #3B82F6;
        --btn-hover-bg: #1D4ED8;
        --btn-hover-border: #60A5FA;
        --btn-hover-text: #FFFFFF;
        --tag-match-bg: #1E293B;
        --tag-match-text: #F8FAFC;
        --tag-match-border: #3B4B64;
        --tag-gap-bg: #132238;
        --tag-gap-text: #60A5FA;
        --tag-gap-border: #3B82F6;
        --banner-warn-bg: #261E10;
        --banner-warn-border: #5C4318;
        --banner-warn-text: #FDE68A;
        --banner-succ-bg: #0D261E;
        --banner-succ-border: #1F533D;
        --banner-succ-text: #A7F3D0;
        --card-border-high: #5C2424;
        --card-border-med: #5C4318;
        --card-border-low: #1F533D;
    """
    chart_font_color = "#F8FAFC"
    chart_grid_color = "#1E293B"
    chart_line_color = "#334155"
    chart_muted_color = "#94A3B8"
    color_high = "#EF4444"
    color_med = "#F59E0B"
    color_low = "#10B981"
else:
    theme_vars = """
        --ink: #0F172A;
        --ink-light: #334155;
        --paper: #F8FAFC;
        --paper-raised: #F1F5F9;
        --paper-card: #FFFFFF;
        --line: #E2E8F0;
        --line-strong: #CBD5E1;
        --signal: #D97706;
        --signal-tint: #FFFBEB;
        --slate: #2563EB;
        --slate-tint: #EFF6FF;
        --moss: #059669;
        --moss-tint: #ECFDF5;
        --brick: #DC2626;
        --brick-tint: #FEF2F2;
        --muted: #64748B;
        --btn-bg: #0F172A;
        --btn-text: #FFFFFF;
        --btn-border: #0F172A;
        --btn-hover-bg: #2563EB;
        --btn-hover-border: #2563EB;
        --btn-hover-text: #FFFFFF;
        --tag-match-bg: #F1F5F9;
        --tag-match-text: #0F172A;
        --tag-match-border: #CBD5E1;
        --tag-gap-bg: #EFF6FF;
        --tag-gap-text: #2563EB;
        --tag-gap-border: #3B82F6;
        --banner-warn-bg: #FFFBEB;
        --banner-warn-border: #FDE68A;
        --banner-warn-text: #92400E;
        --banner-succ-bg: #ECFDF5;
        --banner-succ-border: #A7F3D0;
        --banner-succ-text: #065F46;
        --card-border-high: #FECACA;
        --card-border-med: #FDE68A;
        --card-border-low: #A7F3D0;
    """
    chart_font_color = "#0F172A"
    chart_grid_color = "#E2E8F0"
    chart_line_color = "#CBD5E1"
    chart_muted_color = "#64748B"
    color_high = "#DC2626"
    color_med = "#D97706"
    color_low = "#059669"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {{
        {theme_vars}
    }}

    /* Clear Streamlit fixed header toolbar and prevent title clipping */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        z-index: 10 !important;
    }}

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: var(--ink) !important;
        background-color: var(--paper) !important;
    }}

    /* Ensure text colors across all containers inherit the active theme */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] div,
    [data-testid="stMarkdownContainer"] li {{
        color: var(--ink);
    }}

    /* Main container padding: generous top clearance so headings are fully visible */
    .block-container {{
        padding-top: 4.75rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2.75rem !important;
        padding-right: 2.75rem !important;
        max-width: 1360px !important;
    }}

    /* Editorial Masthead */
    .brand-header {{
        border-bottom: 1px solid var(--line);
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
    }}
    .brand-eyebrow {{
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        color: var(--slate);
        margin-bottom: 0.35rem;
    }}
    .brand-title {{
        font-family: 'Newsreader', Georgia, serif;
        font-size: 2.35rem;
        font-weight: 500;
        letter-spacing: -0.02em;
        line-height: 1.2;
        color: var(--ink) !important;
        margin-bottom: 0.45rem;
    }}
    .brand-title em {{
        font-style: italic;
        font-weight: 400;
        color: var(--slate);
    }}
    .brand-subtitle {{
        font-size: 0.98rem;
        color: var(--muted) !important;
        max-width: 74ch;
        line-height: 1.55;
    }}

    /* Section Labels */
    .section-label {{
        font-size: 0.84rem;
        font-weight: 600;
        color: var(--slate) !important;
        letter-spacing: 0.01em;
        margin-bottom: 0.65rem;
    }}

    /* Form Container Panels */
    .form-panel-header {{
        border-bottom: 1px solid var(--line);
        padding-bottom: 0.65rem;
        margin-bottom: 1.1rem;
        font-family: 'Newsreader', Georgia, serif;
        font-size: 1.08rem;
        font-weight: 600;
        color: var(--ink) !important;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: var(--paper-raised) !important;
        border-right: 1px solid var(--line) !important;
    }}
    [data-testid="stSidebar"] .block-container {{
        padding: 4.5rem 1.4rem 2rem 1.4rem !important;
    }}
    .sidebar-brand {{
        font-family: 'Newsreader', Georgia, serif;
        font-size: 1.55rem;
        font-weight: 600;
        color: var(--ink) !important;
        letter-spacing: -0.01em;
        margin-bottom: 0.2rem;
    }}
    .sidebar-caption {{
        font-size: 0.8rem;
        color: var(--muted) !important;
        margin-bottom: 1.5rem;
        line-height: 1.4;
    }}
    .sidebar-client-tag {{
        border: 1px solid var(--line);
        background-color: var(--paper-card);
        border-radius: 3px;
        padding: 0.75rem 0.9rem;
        font-size: 0.8rem;
        color: var(--muted) !important;
        margin-top: 2rem;
        line-height: 1.45;
    }}

    /* Sidebar Radio Navigation Labels - Explicit Visibility */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {{
        color: var(--ink) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        padding: 0.35rem 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label p {{
        color: var(--ink) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.92rem !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover p {{
        color: var(--slate) !important;
    }}

    /* Sidebar Toggle Styling */
    [data-testid="stToggle"] label p {{
        color: var(--ink) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }}

    /* Form Inputs */
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
    [data-testid="stNumberInput"] div[data-baseweb="input"] {{
        background-color: var(--paper-card) !important;
        border: 1px solid var(--line) !important;
        border-radius: 3px !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.9rem !important;
        color: var(--ink) !important;
        box-shadow: none !important;
        min-height: 42px !important;
    }}
    [data-testid="stNumberInput"] input {{
        background-color: var(--paper-card) !important;
        color: var(--ink) !important;
        border: none !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.92rem !important;
    }}
    [data-testid="stNumberInput"] button {{
        background-color: var(--paper-raised) !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
        border-radius: 2px !important;
    }}
    [data-testid="stNumberInput"] button:hover {{
        background-color: var(--slate) !important;
        color: #FFFFFF !important;
    }}
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div:hover,
    [data-testid="stNumberInput"] div[data-baseweb="input"]:hover {{
        border-color: var(--line-strong) !important;
    }}
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within,
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div:focus-within,
    [data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {{
        border-color: var(--slate) !important;
        outline: none !important;
    }}
    /* Form Widget Labels & Help Tooltip Alignment */
    [data-testid="stWidgetLabel"] {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.45rem !important;
        width: 100% !important;
        margin-bottom: 0.35rem !important;
    }}
    [data-testid="stWidgetLabel"] > label,
    [data-testid="stWidgetLabelWrapper"] {{
        margin-bottom: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        width: auto !important;
        flex-shrink: 0 !important;
    }}
    [data-testid="stWidgetLabel"] p {{
        font-size: 0.84rem !important;
        font-weight: 500 !important;
        color: var(--ink) !important;
        margin: 0 !important;
        white-space: normal !important;
    }}
    [data-testid="stSelectbox"] svg,
    [data-testid="stMultiSelect"] svg {{
        fill: var(--ink-light) !important;
        color: var(--ink-light) !important;
    }}

    /* Tooltip Hover Icon */
    [data-testid="stTooltipIcon"],
    [data-testid="stTooltipHoverTarget"],
    button[data-testid="stTooltipHoverTarget"] {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: var(--muted) !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        cursor: pointer !important;
        outline: none !important;
        box-shadow: none !important;
    }}
    [data-testid="stTooltipHoverTarget"] svg,
    [data-testid="stTooltipIcon"] svg {{
        stroke: var(--muted) !important;
        color: var(--muted) !important;
        fill: none !important;
        width: 14px !important;
        height: 14px !important;
        transition: stroke 0.15s ease, color 0.15s ease !important;
    }}
    [data-testid="stTooltipHoverTarget"]:hover svg,
    [data-testid="stTooltipIcon"]:hover svg,
    [data-testid="stTooltipHoverTarget"]:focus svg {{
        stroke: var(--slate) !important;
        color: var(--slate) !important;
    }}

    /* Tooltips (Hover Only) */
    div[data-testid="stTooltipContent"],
    div[data-baseweb="tooltip"],
    div[data-baseweb="tooltip"] > div,
    div[role="tooltip"] {{
        background-color: var(--paper-card) !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
        border-radius: 4px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.82rem !important;
        line-height: 1.45 !important;
        padding: 0.55rem 0.8rem !important;
        max-width: 320px !important;
    }}
    div[data-testid="stTooltipContent"] *,
    div[data-baseweb="tooltip"] *,
    div[role="tooltip"] * {{
        color: var(--ink) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.82rem !important;
    }}

    /* Selectbox & MultiSelect Dropdown Menus (Single Clean Surface, Native Sizing, No White Bleed) */
    div[data-baseweb="popover"] {{
        background-color: var(--paper-card) !important;
        border: 1px solid var(--line) !important;
        border-radius: 4px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
        overflow: hidden !important;
        padding: 0 !important;
        margin: 0 !important;
        max-width: none !important;
    }}
    div[data-baseweb="popover"] div,
    div[data-baseweb="menu"],
    ul[role="listbox"] {{
        background-color: var(--paper-card) !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    li[role="option"] {{
        background-color: var(--paper-card) !important;
        color: var(--ink) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 400 !important;
        padding: 0.6rem 0.95rem !important;
        cursor: pointer !important;
        border: none !important;
        transition: background-color 0.12s ease, color 0.12s ease !important;
    }}
    li[role="option"] * {{
        color: var(--ink) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.88rem !important;
    }}
    li[role="option"]:hover,
    li[role="option"]:hover *,
    li[role="option"][aria-selected="true"],
    li[role="option"][aria-selected="true"] *,
    li[role="option"]:focus,
    li[role="option"]:focus * {{
        background-color: var(--paper-raised) !important;
        color: var(--ink) !important;
    }}

    /* Selected Tags in MultiSelect */
    [data-testid="stMultiSelect"] [data-baseweb="tag"] {{
        background-color: var(--paper-raised) !important;
        border: 1px solid var(--line) !important;
        border-radius: 2px !important;
        color: var(--ink) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.82rem !important;
    }}

    /* Primary & Standard Action Buttons */
    [data-testid="stButton"] button,
    .stButton button,
    button[kind="primary"],
    button[kind="secondary"],
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-secondary"] {{
        background-color: var(--btn-bg) !important;
        color: var(--btn-text) !important;
        border: 1px solid var(--btn-border) !important;
        border-radius: 3px !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.94rem !important;
        padding: 0.72rem 1.75rem !important;
        box-shadow: none !important;
        letter-spacing: 0.02em !important;
        cursor: pointer !important;
        transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease !important;
    }}
    [data-testid="stButton"] button *,
    .stButton button *,
    button[kind="primary"] *,
    button[kind="secondary"] *,
    button[data-testid="baseButton-primary"] *,
    button[data-testid="baseButton-secondary"] * {{
        color: var(--btn-text) !important;
        font-weight: 600 !important;
    }}
    [data-testid="stButton"] button:hover,
    .stButton button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {{
        background-color: var(--btn-hover-bg) !important;
        border-color: var(--btn-hover-border) !important;
        color: var(--btn-hover-text) !important;
    }}
    [data-testid="stButton"] button:hover *,
    .stButton button:hover *,
    button[kind="primary"]:hover *,
    button[kind="secondary"]:hover *,
    button[data-testid="baseButton-primary"]:hover *,
    button[data-testid="baseButton-secondary"]:hover * {{
        color: var(--btn-hover-text) !important;
    }}
    [data-testid="stButton"] button:focus,
    .stButton button:focus {{
        outline: 2px solid var(--slate) !important;
        outline-offset: 1px !important;
    }}

    /* Diagnostic Readout Panels */
    .reading {{
        background-color: var(--paper-card);
        border: 1px solid var(--line);
        border-left: 4px solid var(--ink);
        border-radius: 3px;
        padding: 1.15rem 1.25rem;
        height: 100%;
        box-sizing: border-box;
    }}
    .reading-high {{ border-left-color: var(--brick) !important; background-color: var(--brick-tint); border-color: var(--card-border-high); }}
    .reading-medium {{ border-left-color: var(--signal) !important; background-color: var(--signal-tint); border-color: var(--card-border-med); }}
    .reading-low {{ border-left-color: var(--moss) !important; background-color: var(--moss-tint); border-color: var(--card-border-low); }}

    .reading-label {{
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--muted) !important;
        letter-spacing: 0.02em;
        margin-bottom: 0.3rem;
    }}
    .reading-value {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2.1rem;
        font-weight: 600;
        line-height: 1.15;
        margin-bottom: 0.4rem;
    }}
    .reading-high .reading-value {{ color: var(--brick) !important; }}
    .reading-medium .reading-value {{ color: var(--signal) !important; }}
    .reading-low .reading-value {{ color: var(--moss) !important; }}
    .reading-subtext {{
        font-size: 0.84rem;
        color: var(--ink-light) !important;
        line-height: 1.45;
    }}

    /* Metric Card */
    .metric-card {{
        background-color: var(--paper-card);
        border: 1px solid var(--line);
        border-radius: 3px;
        padding: 1.15rem 1.25rem;
        height: 100%;
        box-sizing: border-box;
    }}
    .metric-label {{
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--muted) !important;
        letter-spacing: 0.02em;
        margin-bottom: 0.35rem;
    }}
    .metric-value {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.85rem;
        font-weight: 600;
        color: var(--ink) !important;
        line-height: 1.15;
        margin-bottom: 0.35rem;
    }}
    .metric-subtext {{
        font-size: 0.82rem;
        color: var(--muted) !important;
        line-height: 1.4;
    }}

    /* Flat Alert Banners */
    .status-banner {{
        border-radius: 3px;
        border: 1px solid var(--line);
        padding: 1rem 1.25rem;
        margin-bottom: 1.4rem;
        font-size: 0.9rem;
        line-height: 1.55;
    }}
    .status-banner-info {{
        background-color: var(--paper-card);
        border-left: 4px solid var(--slate);
        color: var(--ink) !important;
    }}
    .status-banner-success {{
        background-color: var(--banner-succ-bg);
        border: 1px solid var(--banner-succ-border);
        border-left: 4px solid var(--moss);
        color: var(--banner-succ-text) !important;
    }}
    .status-banner-warning {{
        background-color: var(--banner-warn-bg);
        border: 1px solid var(--banner-warn-border);
        border-left: 4px solid var(--signal);
        color: var(--banner-warn-text) !important;
    }}

    /* Flat Panel for General Content */
    .flat-panel {{
        background-color: var(--paper-card);
        border: 1px solid var(--line);
        border-radius: 3px;
        padding: 1.35rem 1.5rem;
        margin-bottom: 1.25rem;
    }}

    /* Competency Tag Badges */
    .skill-tag-match, .skill-tag-gap {{
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 2px;
        font-size: 0.82rem;
        font-weight: 500;
        margin-right: 0.45rem;
        margin-bottom: 0.5rem;
        font-family: 'IBM Plex Sans', sans-serif;
        line-height: 1.3;
    }}
    .skill-tag-match {{
        background-color: var(--tag-match-bg);
        color: var(--tag-match-text) !important;
        border: 1px solid var(--tag-match-border);
    }}
    .skill-tag-gap {{
        background-color: var(--tag-gap-bg);
        color: var(--tag-gap-text) !important;
        border: 1px dashed var(--tag-gap-border);
    }}

    /* Tabs Styling */
    [data-testid="stTabs"] button[role="tab"] {{
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: var(--muted) !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 3px 3px 0 0 !important;
    }}
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
        color: var(--ink) !important;
        font-weight: 600 !important;
        border-bottom: 2px solid var(--ink) !important;
    }}

    /* Progress Bar */
    [data-testid="stProgressBar"] > div {{
        background-color: var(--paper-raised) !important;
        border: 1px solid var(--line) !important;
        border-radius: 2px !important;
        height: 9px !important;
    }}
    [data-testid="stProgressBar"] > div > div {{
        background-color: var(--slate) !important;
        border-radius: 1px !important;
    }}

    /* Hairline Divider */
    .divider {{
        height: 1px;
        background-color: var(--line);
        margin: 2rem 0;
    }}

    /* Responsive Adjustments */
    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 1.15rem !important;
            padding-right: 1.15rem !important;
            padding-top: 4.25rem !important;
        }}
        .brand-title {{
            font-size: 1.8rem;
        }}
        .reading-value {{
            font-size: 1.65rem;
        }}
        .metric-value {{
            font-size: 1.45rem;
        }}
    }}

    @keyframes bounce {{
        0%, 20%, 50%, 80%, 100% {{
            transform: translateY(0);
        }}
        40% {{
            transform: translateY(-5px);
        }}
        60% {{
            transform: translateY(-2.5px);
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Load Data & Model
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df_raw = pd.read_csv("ai_job_market_insights.csv")
    df_raw.columns = [c.strip() for c in df_raw.columns]
    return df_raw

@st.cache_resource
def load_model():
    return joblib.load("automation_risk_model.pkl")

try:
    df = load_data()
    model = load_model()
except Exception as e:
    st.error(f"Initialization failure: {e}. Check dataset and 'automation_risk_model.pkl' paths.")
    st.stop()

# Precomputed static lookups for zero-latency selectbox rendering
ROLE_LIST = sorted(list(ROLE_SKILL_PROFILES.keys()))
INDUSTRY_LIST = sorted(df["Industry"].unique().tolist())
LOCATION_LIST = sorted(df["Location"].unique().tolist())
ALL_KNOWN_SKILLS = sorted(list(set([clean_skill_label(skill) for sublist in ROLE_SKILL_PROFILES.values() for skill in sublist])))

@st.cache_data
def get_macro_kpis():
    total = len(df)
    high_count = int((df["Automation_Risk"] == "High").sum())
    high_pct = (high_count / total) * 100
    mean_sal = float(df["Salary_USD"].mean())
    return total, high_count, high_pct, mean_sal

@st.cache_data
def build_risk_chart(f_col, l_col, g_col, m_col, c_high, c_med, c_low):
    risk_order = ["High", "Medium", "Low"]
    risk_counts = df["Automation_Risk"].value_counts().reindex(risk_order).fillna(0).reset_index()
    risk_counts.columns = ["Risk Tier", "Roles"]
    fig_risk = px.bar(
        risk_counts,
        x="Risk Tier",
        y="Roles",
        color="Risk Tier",
        color_discrete_map={"High": c_high, "Medium": c_med, "Low": c_low},
        text="Roles"
    )
    fig_risk.update_traces(
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=13, color=f_col),
        marker_line_width=0
    )
    fig_risk.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans", size=12, color=f_col),
        margin=dict(l=15, r=15, t=30, b=25),
        showlegend=False,
        height=330,
        xaxis=dict(
            title="",
            showgrid=False,
            linecolor=l_col,
            tickfont=dict(family="IBM Plex Sans", size=13, color=f_col)
        ),
        yaxis=dict(
            title="Monitored roles",
            gridcolor=g_col,
            zeroline=False,
            showgrid=True,
            tickfont=dict(family="IBM Plex Mono", size=11, color=m_col)
        )
    )
    return fig_risk

@st.cache_data
def build_industry_chart(f_col, l_col, g_col, m_col, c_high, c_med, c_low):
    ind_risk = df.groupby(["Industry", "Automation_Risk"]).size().reset_index(name="Volume")
    fig_ind = px.bar(
        ind_risk,
        x="Industry",
        y="Volume",
        color="Automation_Risk",
        barmode="group",
        color_discrete_map={"High": c_high, "Medium": c_med, "Low": c_low},
        category_orders={"Automation_Risk": ["High", "Medium", "Low"]}
    )
    fig_ind.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans", size=12, color=f_col),
        margin=dict(l=15, r=15, t=30, b=25),
        height=330,
        legend=dict(
            title=dict(text="Exposure Tier", font=dict(family="IBM Plex Sans", size=11, color=m_col)),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="IBM Plex Sans", size=11, color=f_col)
        ),
        xaxis=dict(
            title="",
            showgrid=False,
            linecolor=l_col,
            tickfont=dict(family="IBM Plex Sans", size=11, color=f_col)
        ),
        yaxis=dict(
            title="Volume",
            gridcolor=g_col,
            zeroline=False,
            showgrid=True,
            tickfont=dict(family="IBM Plex Mono", size=11, color=m_col)
        )
    )
    return fig_ind

# ---------------------------------------------------------
# Sidebar Client Tag
# ---------------------------------------------------------
st.sidebar.markdown("""
<div class="sidebar-client-tag">
    <div style="font-weight: 600; color: var(--ink); margin-bottom: 0.2rem;">Client Dossier</div>
    StrataWork Global Enterprise<br>
    <span style="color: var(--slate); font-size: 0.74rem;">Calibrated Baseline v2.4</span>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 1: WORKFORCE MOBILITY PORTAL (CONNECTED SYSTEM)
# ---------------------------------------------------------
if nav_choice == "Workforce Mobility Portal":
    logo_header_html = f'<img src="data:image/png;base64,{LOGO_B64}" style="width: 44px; height: 44px; border-radius: 50%; box-shadow: 0 2px 8px rgba(37,99,235,0.2); flex-shrink: 0;" alt="CareerGPS"/>' if LOGO_B64 else ''
    st.markdown(f"""
    <div class="brand-header">
        <div style="display: flex; align-items: center; gap: 0.85rem; margin-bottom: 0.45rem;">
            {logo_header_html}
            <div>
                <div class="brand-eyebrow">Individual Career Navigation</div>
                <div class="brand-title">Role Automation Risk & <em>Transition Pathways</em></div>
            </div>
        </div>
        <div class="brand-subtitle">Evaluate how artificial intelligence and automation could affect your current role, and discover personalized career pathways to protect and grow your career.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="form-panel-header">Your current role</div>
        """, unsafe_allow_html=True)
        job_title = st.selectbox("Job Title", ROLE_LIST)
        industry = st.selectbox("Industry", INDUSTRY_LIST)
        company_size = st.selectbox("Company Size", ["Small", "Medium", "Large"])
        location = st.selectbox("Location", LOCATION_LIST)
        
    with col2:
        st.markdown("""
        <div class="form-panel-header">Workplace and market setting</div>
        """, unsafe_allow_html=True)
        ai_adoption = st.selectbox("Company AI Adoption Level", ["Low", "Medium", "High"])
        growth_projection = st.selectbox("5-Year Job Growth Outlook", ["Growth", "Stable", "Decline"])
        remote_friendly = st.selectbox("Remote Work Friendly", ["Yes", "No"])
        salary_usd = st.number_input("Annual Salary (USD)", min_value=30000, max_value=250000, value=85000, step=5000)

    # Core Competencies selection
    default_skills = ROLE_SKILL_PROFILES.get(job_title, ["Communication"])
    
    st.markdown('<div style="margin-top: 0.5rem;"></div>', unsafe_allow_html=True)
    selected_skills = st.multiselect(
        "Your Core Skills",
        options=ALL_KNOWN_SKILLS,
        default=[clean_skill_label(s) for s in default_skills[:3]],
        help="Select the skills you use in your everyday work to find compatible career transitions."
    )

    st.markdown('<div style="margin-top: 0.85rem;"></div>', unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns([1.35, 1.65])
    with btn_col1:
        run_analysis = st.button("Analyze Career Risk & Find Pathways", type="primary", use_container_width=True)

    if run_analysis:
        with st.spinner("Calibrating AI automation risk model and mapping career pathways..."):
            time.sleep(0.45)

        primary_skill = selected_skills[0] if len(selected_skills) > 0 else "Communication"

        # Input record matching the audited model features (no artificial composite noise)
        input_df = pd.DataFrame([{
            'Salary_USD': float(salary_usd),
            'Job_Title': job_title,
            'Industry': industry,
            'Company_Size': company_size,
            'Location': location,
            'AI_Adoption_Level': ai_adoption,
            'Required_Skills': primary_skill,
            'Remote_Friendly': remote_friendly,
            'Job_Growth_Projection': growth_projection
        }])

        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
        prob_dict = dict(zip(model.classes_, probabilities))

        # Prominent Result Status Banner & Downward Action Indicator
        st.markdown(f"""
        <div id="results-anchor" style="margin-top: 1.4rem; padding: 0.95rem 1.25rem; background: var(--slate-tint); border: 1.5px solid var(--slate); border-radius: 4px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; color: var(--slate); font-weight: 600; font-size: 0.95rem;">
                <span style="font-size: 1.3rem; display: inline-block; animation: bounce 1.2s infinite ease-in-out;">↓</span>
                <span>Analysis Complete — Review Your Custom Risk Breakdown & Pathways Below</span>
            </div>
            <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.82rem; background: var(--paper-card); color: var(--ink); padding: 0.3rem 0.75rem; border-radius: 3px; border: 1px solid var(--line);">Profile: {job_title} · {industry}</span>
        </div>
        """, unsafe_allow_html=True)

        # Smooth auto-scroll to the anchor
        components.html("""
        <script>
            setTimeout(function() {
                const anchor = window.parent.document.getElementById('results-anchor');
                if (anchor) {
                    anchor.scrollIntoView({behavior: 'smooth', block: 'start'});
                }
            }, 80);
        </script>
        """, height=0)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Risk assessment summary</div>', unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        with r1:
            tier_class = {"High": "reading-high", "Medium": "reading-medium", "Low": "reading-low"}[prediction]
            tier_text = {
                "High": "High likelihood of routine daily task automation",
                "Medium": "Moderate potential for partial task automation",
                "Low": "Strong protection with high strategic and interpersonal demands"
            }[prediction]
            st.markdown(f'''
            <div class="reading {tier_class}">
                <div class="reading-label">Automation risk level</div>
                <div class="reading-value">{prediction}</div>
                <div class="reading-subtext">{tier_text}. Model confidence: <strong>{prob_dict.get(prediction, 0.0)*100:.1f}%</strong></div>
            </div>
            ''', unsafe_allow_html=True)

        with r2:
            st.markdown('''
            <div class="metric-card">
                <div class="metric-label">Market risk baseline</div>
                <div class="metric-value">34.6%</div>
                <div class="metric-subtext">Percentage of all surveyed workforce roles that fall into the average (Medium) risk category.</div>
            </div>
            ''', unsafe_allow_html=True)

        with r3:
            urgency_text = "Immediate Action" if prediction == "High" else ("Planned Transition" if prediction == "Medium" else "Proactive Growth")
            routing_sub = "Prioritizing resilient career pathways with strong skill overlap." if prediction in ["High", "Medium"] else "Prioritizing vertical advancement and specialization."
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Recommended action priority</div>
                <div class="metric-value">{urgency_text}</div>
                <div class="metric-subtext">{routing_sub}</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Independent research comparison</div>', unsafe_allow_html=True)
        ext_tier = get_external_risk_tier(job_title)
        ext_basis = get_external_risk_basis(job_title)

        st.markdown(f'''
        <div class="flat-panel">
            <div style="display: flex; flex-wrap: wrap; gap: 2rem; align-items: baseline;">
                <div style="min-width: 190px;">
                    <div class="reading-label">Published study rating</div>
                    <div style="font-family: 'IBM Plex Mono', monospace; font-size: 1.45rem; font-weight: 600; color: var(--ink);">{ext_tier}</div>
                </div>
                <div style="flex: 1; min-width: 280px;">
                    <div class="reading-label">About this benchmark (Frey & Osborne Oxford study)</div>
                    <div style="font-size: 0.88rem; color: var(--ink-light); line-height: 1.55;">Independent study on occupational automation. Key finding: {ext_basis}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        if ext_tier != prediction:
            st.markdown(f'''
            <div class="status-banner status-banner-warning">
                <strong>Note on Research vs. Model:</strong> Our AI model estimates this profile as <strong>{prediction}</strong> risk, while published academic research rates this occupational category as <strong>{ext_tier}</strong>. Because real-world impact varies by industry and specific company practices, consider both perspectives when planning your next career step.
            </div>
            ''', unsafe_allow_html=True)

        # Recommender: Directly passed the predicted risk
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Recommended career pathways</div>', unsafe_allow_html=True)
        
        if prediction in ["High", "Medium"]:
            st.markdown('''
            <div class="status-banner status-banner-info">
                <strong>Recommended Career Strategy:</strong> This role has elevated exposure to automation. The pathways below are prioritized for <strong>defensive career resilience</strong>, helping you transfer your current skills into safer lateral roles.
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="status-banner status-banner-success">
                <strong>Recommended Career Strategy:</strong> This role has strong protection against automation. The pathways below are prioritized for <strong>vertical career growth and leadership specialization</strong>.
            </div>
            ''', unsafe_allow_html=True)

        recommendations = get_career_recommendations(job_title, selected_skills, predicted_risk=prediction)

        if recommendations:
            tabs = st.tabs([f"Option {i+1}: {r['target_role']}" for i, r in enumerate(recommendations[:3])])
            for i, rec in enumerate(recommendations[:3]):
                with tabs[i]:
                    st.markdown(f'''
                    <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; margin-bottom: 0.6rem; margin-top: 0.35rem;">
                        <span style="font-size: 0.9rem; color: var(--ink);">Strategic focus: <code style="font-family: 'IBM Plex Mono', monospace; font-size: 0.84rem; background: var(--paper-raised); color: var(--ink); padding: 0.2rem 0.5rem; border-radius: 2px; border: 1px solid var(--line);">{rec['strategy']}</code></span>
                        <span style="font-size: 0.9rem; color: var(--muted); font-family: 'IBM Plex Mono', monospace;">Skill match: <strong style="color: var(--ink); font-size: 1.05rem;">{rec['match_score']}%</strong></span>
                    </div>
                    ''', unsafe_allow_html=True)
                    st.progress(float(rec['match_score']) / 100.0)

                    col_match, col_gap = st.columns(2)
                    with col_match:
                        st.markdown('<div class="section-label" style="color: var(--ink); margin-top: 1rem; margin-bottom: 0.45rem;">Skills you already have</div>', unsafe_allow_html=True)
                        if rec['matching_skills']:
                            tags_html = "".join([f"<span class='skill-tag-match'>{s}</span>" for s in rec['matching_skills']])
                            st.markdown(tags_html, unsafe_allow_html=True)
                        else:
                            st.caption("No direct skill overlap identified. Foundational training recommended.")
                            
                    with col_gap:
                        st.markdown('<div class="section-label" style="color: var(--slate); margin-top: 1rem; margin-bottom: 0.45rem;">Skills to learn</div>', unsafe_allow_html=True)
                        if rec['skills_to_learn']:
                            tags_gap_html = "".join([f"<span class='skill-tag-gap'>+ {s}</span>" for s in rec['skills_to_learn']])
                            st.markdown(tags_gap_html, unsafe_allow_html=True)
                        else:
                            st.caption("You already meet all primary skill requirements for this position.")

# ---------------------------------------------------------
# VIEW 2: TALENT ANALYTICS DASHBOARD
# ---------------------------------------------------------
elif nav_choice == "Talent Analytics Dashboard":
    logo_header_html = f'<img src="data:image/png;base64,{LOGO_B64}" style="width: 44px; height: 44px; border-radius: 50%; box-shadow: 0 2px 8px rgba(37,99,235,0.2); flex-shrink: 0;" alt="CareerGPS"/>' if LOGO_B64 else ''
    st.markdown(f"""
    <div class="brand-header">
        <div style="display: flex; align-items: center; gap: 0.85rem; margin-bottom: 0.45rem;">
            {logo_header_html}
            <div>
                <div class="brand-eyebrow">Macro Workforce Analytics</div>
                <div class="brand-title">Enterprise Exposure & <em>Workforce Distribution</em></div>
            </div>
        </div>
        <div class="brand-subtitle">Aggregated displacement exposure and structural risk distribution across 500 surveyed enterprise positions.</div>
    </div>
    """, unsafe_allow_html=True)

    total_staff, high_risk_count, high_risk_pct, avg_salary = get_macro_kpis()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total roles analyzed</div>
            <div class="metric-value">{total_staff:,}</div>
            <div class="metric-subtext">Total surveyed positions across industries</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High risk share</div>
            <div class="metric-value">{high_risk_pct:.1f}%</div>
            <div class="metric-subtext">{high_risk_count} roles classified in the high automation risk tier</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average annual compensation</div>
            <div class="metric-value">${avg_salary:,.0f}</div>
            <div class="metric-subtext">Annualized average salary across all surveyed verticals</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.markdown('<div class="section-label">Workforce distribution by risk tier</div>', unsafe_allow_html=True)
        fig_risk = build_risk_chart(chart_font_color, chart_line_color, chart_grid_color, chart_muted_color, color_high, color_med, color_low)
        st.plotly_chart(fig_risk, use_container_width=True, config={"displayModeBar": False})

    with chart_right:
        st.markdown('<div class="section-label">Automation risk across industry verticals</div>', unsafe_allow_html=True)
        fig_ind = build_industry_chart(chart_font_color, chart_line_color, chart_grid_color, chart_muted_color, color_high, color_med, color_low)
        st.plotly_chart(fig_ind, use_container_width=True, config={"displayModeBar": False})

# ---------------------------------------------------------
# VIEW 3: METHODOLOGY & AUDITED BENCHMARKS
# ---------------------------------------------------------
else:
    logo_header_html = f'<img src="data:image/png;base64,{LOGO_B64}" style="width: 44px; height: 44px; border-radius: 50%; box-shadow: 0 2px 8px rgba(37,99,235,0.2); flex-shrink: 0;" alt="CareerGPS"/>' if LOGO_B64 else ''
    st.markdown(f"""
    <div class="brand-header">
        <div style="display: flex; align-items: center; gap: 0.85rem; margin-bottom: 0.45rem;">
            {logo_header_html}
            <div>
                <div class="brand-eyebrow">Model Audit & Empirical Disclosures</div>
                <div class="brand-title">Validation Benchmarks & <em>Statistical Methodology</em></div>
            </div>
        </div>
        <div class="brand-subtitle">Transparent technical disclosures, cross-validation metrics, and feature selection documentation.</div>
    </div>
    """, unsafe_allow_html=True)

    # Executive Benchmark KPI strip
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Majority baseline accuracy</div>
            <div class="metric-value">34.6%</div>
            <div class="metric-subtext">Naive majority prediction baseline (Medium class)</div>
        </div>
        """, unsafe_allow_html=True)
    with b2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">5-fold cross-validation</div>
            <div class="metric-value">36.0%</div>
            <div class="metric-subtext">±5.0% standard deviation across 5 validation folds</div>
        </div>
        """, unsafe_allow_html=True)
    with b3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Audited training records</div>
            <div class="metric-value">500</div>
            <div class="metric-subtext">Cross-industry empirical survey observations</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Technical disclosures and validation record</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="flat-panel" style="margin-bottom: 1.15rem;">
        <div style="font-family: 'Newsreader', Georgia, serif; font-size: 1.2rem; font-weight: 600; color: var(--ink); margin-bottom: 0.5rem;">
            1. Empirical Signal Reality and Baseline Benchmark
        </div>
        <div style="font-size: 0.92rem; color: var(--ink-light); line-height: 1.65;">
            In a 3-class problem with 500 rows, a naive model that always predicts the majority class (<code>Medium</code>) scores <strong>34.6% accuracy</strong>.<br>
            Our regularized Logistic Regression pipeline achieves <strong>36.0% accuracy across 5-fold cross-validation (±5.0%)</strong>, which is only a small, not fully reliable edge over the 34.5% majority baseline. A single held-out test split can show a higher number (44%), but the 5-fold cross-validation figure is the honest one to quote, since it isn't dependent on one lucky split.
        </div>
    </div>

    <div class="flat-panel" style="margin-bottom: 1.15rem;">
        <div style="font-family: 'Newsreader', Georgia, serif; font-size: 1.2rem; font-weight: 600; color: var(--ink); margin-bottom: 0.5rem;">
            2. Feature Selection and Dimensionality Audit
        </div>
        <div style="font-size: 0.92rem; color: var(--ink-light); line-height: 1.65;">
            Statistical inspection proved that creating weighted composite indices from noisy survey responses (<code>AI_Pressure_Index</code>) failed to produce separable signal.<br>
            Redundant bucketed features (<code>Salary_Tier</code>) were dropped in favor of raw standardized numerical features (<code>Salary_USD</code>).
        </div>
    </div>

    <div class="flat-panel" style="margin-bottom: 1.15rem;">
        <div style="font-family: 'Newsreader', Georgia, serif; font-size: 1.2rem; font-weight: 600; color: var(--ink); margin-bottom: 0.5rem;">
            3. Independent Academic Reference (Frey & Osborne)
        </div>
        <div style="font-size: 0.92rem; color: var(--ink-light); line-height: 1.65;">
            An <code>External_Risk_Tier</code> feature was engineered from Frey & Osborne's published automation research, mapped to each job title.<br>
            Tested directly: it showed no significant relationship with our target (p=0.076) and, when added to the model, provided no accuracy improvement (35.25% vs. 36.00%), which is expected since it is fully derived from <code>Job_Title</code>, which the model already uses.<br>
            Rather than force it into the model, it is shown in the app as an independent, transparently sourced second opinion alongside the model's own prediction.
        </div>
    </div>

    <div class="flat-panel" style="margin-bottom: 1.15rem;">
        <div style="font-family: 'Newsreader', Georgia, serif; font-size: 1.2rem; font-weight: 600; color: var(--ink); margin-bottom: 0.5rem;">
            4. Skill Engine Architecture and Transition Routing
        </div>
        <div style="font-size: 0.92rem; color: var(--ink-light); line-height: 1.65;">
            Because the underlying dataset contains only one skill per worker, full role competency profiles were curated using occupational benchmarks rather than noisy statistical imputation.<br>
            The transition engine is connected to the predictive model: high-risk users are routed toward automation-resilient roles, while low-risk users receive vertical specialization pathways.
        </div>
    </div>
    """, unsafe_allow_html=True)