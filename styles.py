import os
import base64
import streamlit as st
from config import UNIVERSITY_CONFIG


def get_custom_css(theme="dark"):
    """
    Generate custom CSS for ICARE Glassmorphism design system supporting Dark and Light modes.
    """
    if theme.lower() == "light":
        bg_color = "#F8FAFC"
        text_primary = "#0F172A"
        text_secondary = "#475569"
        card_bg = "rgba(255, 255, 255, 0.85)"
        card_border = "1px solid rgba(15, 23, 42, 0.08)"
        card_shadow = "0 8px 32px 0 rgba(31, 38, 135, 0.07)"
        sidebar_bg = "#FFFFFF"
        subtle_bg = "rgba(2, 132, 199, 0.05)"
        tab_bg = "#E2E8F0"
        tab_active = "#FFFFFF"
    else:  # Dark mode default
        bg_color = "#070D1E"
        text_primary = "#F8FAFC"
        text_secondary = "#94A3B8"
        card_bg = "rgba(14, 23, 42, 0.75)"
        card_border = "1px solid rgba(255, 255, 255, 0.08)"
        card_shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
        sidebar_bg = "#0B1329"
        subtle_bg = "rgba(2, 132, 199, 0.12)"
        tab_bg = "#0E172A"
        tab_active = "#1E293B"

    primary_blue = UNIVERSITY_CONFIG.get("primary_color", "#0284C7")
    accent_gold = UNIVERSITY_CONFIG.get("accent_color", "#F59E0B")

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap');

    html, body, [class*="st-"], .stApp {{
        font-family: 'Inter', sans-serif;
        background-color: {bg_color} !important;
        color: {text_primary} !important;
    }}

    .main .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 95% !important;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: {card_border} !important;
    }}

    /* Glassmorphism Cards */
    .glass-card {{
        background: {card_bg} !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: {card_border} !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: {card_shadow} !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        margin-bottom: 1.25rem;
    }}

    .glass-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 40px 0 rgba(2, 132, 199, 0.2) !important;
        border-color: rgba(2, 132, 199, 0.4) !important;
    }}

    /* KPI Metric Cards */
    .kpi-card {{
        background: {card_bg} !important;
        backdrop-filter: blur(12px) !important;
        border: {card_border} !important;
        border-radius: 14px !important;
        padding: 1.2rem 1rem !important;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }}

    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, {primary_blue}, {accent_gold});
    }}

    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.25);
    }}

    .kpi-value {{
        font-family: 'Outfit', sans-serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: {text_primary};
        line-height: 1.2;
        margin: 0.2rem 0;
    }}

    .kpi-label {{
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {text_secondary};
    }}

    .kpi-subtext {{
        font-size: 0.78rem;
        color: {primary_blue};
        font-weight: 500;
        margin-top: 0.3rem;
    }}

    /* ICARE Topbar Component */
    .icare-topbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: {card_bg};
        backdrop-filter: blur(14px);
        border: {card_border};
        border-radius: 14px;
        padding: 0.9rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: {card_shadow};
    }}

    .icare-logo-badge {{
        background: linear-gradient(135deg, #0284C7 0%, #06B6D4 100%);
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 0.9rem;
        padding: 0.35rem 0.85rem;
        border-radius: 8px;
        letter-spacing: 0.08em;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
    }}

    .icare-logo-img {{
        height: 32px;
        width: auto;
        max-width: 140px;
        object-fit: contain;
        border-radius: 6px;
        background: #FFFFFF;
        padding: 2px 6px;
        display: inline-block;
        vertical-align: middle;
    }}

    .icare-subtext {{
        font-size: 0.72rem;
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        padding: 0.15rem 0.45rem;
        border-radius: 4px;
        font-weight: 600;
        margin-left: 0.4rem;
    }}

    .univ-title {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: {text_primary};
        margin: 0;
        line-height: 1.3;
    }}

    .univ-subtitle {{
        font-size: 0.84rem;
        font-weight: 600;
        color: {primary_blue};
        margin: 0;
    }}

    /* Hero Dossier Banner */
    .hero-banner {{
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.15) 0%, rgba(15, 23, 42, 0.4) 100%);
        border: {card_border};
        border-left: 5px solid {primary_blue};
        border-radius: 18px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(12px);
    }}

    .hero-badges-wrapper {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 0.8rem;
    }}

    .hero-badge {{
        background: {subtle_bg};
        border: 1px solid rgba(2, 132, 199, 0.3);
        color: {text_primary};
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.3rem 0.75rem;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }}

    .hero-title {{
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, {text_primary} 30%, {primary_blue} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.3rem 0 0.8rem 0;
        line-height: 1.2;
    }}

    .rank-box {{
        background: {card_bg};
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 0.8rem 1.4rem;
        display: inline-flex;
        align-items: center;
        gap: 1.2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }}

    .rank-num {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: {accent_gold};
    }}

    .rank-label {{
        font-size: 0.78rem;
        color: {text_secondary};
        font-weight: 600;
        text-transform: uppercase;
    }}

    /* Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: {tab_bg};
        padding: 6px;
        border-radius: 12px;
        border: {card_border};
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 42px;
        border-radius: 8px;
        color: {text_secondary};
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0 16px;
        border: none !important;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {tab_active} !important;
        color: {primary_blue} !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        font-weight: 700;
    }}

    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {bg_color};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {primary_blue};
        border-radius: 4px;
    }}
    </style>
    """
    return css


def get_icare_logo_b64():
    logo_path = "ICARE - LOGO .jpeg"
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            pass
    return ""


def render_icare_topbar(theme="dark"):
    """
    Render Top Navigation Bar with ICARE Logo Image, University Name, and NIRF badge.
    """
    univ_name = UNIVERSITY_CONFIG.get("full_name", "Dr. Babasaheb Ambedkar Marathwada University")
    nirf_id = UNIVERSITY_CONFIG.get("nirf_id", "IR-O-U-0298")
    city = UNIVERSITY_CONFIG.get("city", "Chhatrapati Sambhajinagar, Maharashtra")

    logo_b64 = get_icare_logo_b64()
    if logo_b64:
        logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" alt="ICARE Logo" class="icare-logo-img">'
    else:
        logo_html = 'ICARE'

    html = f"""
    <div class="icare-topbar">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div class="icare-logo-badge">
                {logo_html} <span class="icare-subtext">PORTAL INTELLIGENCE</span>
            </div>
            <div>
                <h2 class="univ-title">{univ_name}</h2>
                <div class="univ-subtitle"><b>{nirf_id}</b> • {city}</div>
            </div>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.8rem; font-weight: 600; opacity: 0.8; display: inline-flex; align-items: center; gap: 0.4rem;">
                <span style="height: 9px; width: 9px; background-color: #10B981; border-radius: 50%; display: inline-block;"></span>
                Live Scopus API Engine Active
            </span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_icare_hero(total_pubs, total_cites, theme="dark"):
    """
    Render ICARE Hero Research Dossier Banner with badges, title, and rank statistics.
    """
    status_tag = UNIVERSITY_CONFIG.get("status_tag", "🏛 State Public University (Estd. 1958)")
    naac_badge = UNIVERSITY_CONFIG.get("naac_badge", "⭐ NAAC A+ (CGPA 3.38)")
    app_title = UNIVERSITY_CONFIG.get("app_title", "BAMU Live Scopus Intelligence Dashboard")

    html = f"""
    <div class="hero-banner">
        <div class="hero-badges-wrapper">
            <span class="hero-badge">🏆 Scopus Research Dossier</span>
            <span class="hero-badge">{status_tag}</span>
            <span class="hero-badge">{naac_badge}</span>
            <span class="hero-badge">📜 NIRF Category: University</span>
        </div>
        <h1 class="hero-title">{app_title}</h1>
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
            <p style="margin: 0; font-size: 0.95rem; opacity: 0.85; max-width: 650px;">
                Comprehensive institutional bibliometric analytics, faculty h-index tracking, Q1 publication trends, and international collaboration intelligence for Dr. Babasaheb Ambedkar Marathwada University.
            </p>
            <div class="rank-box">
                <div>
                    <div class="rank-num">#{total_pubs:,}</div>
                    <div class="rank-label">Indexed Papers</div>
                </div>
                <div style="height: 30px; width: 1px; background: rgba(255,255,255,0.15);"></div>
                <div>
                    <div class="rank-num" style="color: #0284C7;">{total_cites:,}</div>
                    <div class="rank-label">Total Citations</div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


if __name__ == "__main__":
    print("styles.py component ready.")
