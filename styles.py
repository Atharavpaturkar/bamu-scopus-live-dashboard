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
        text_secondary = "#334155"
        card_bg = "#FFFFFF"
        card_border = "1px solid #CBD5E1"
        card_border_hover = "1px solid #0284C7"
        card_shadow = "0 4px 20px 0 rgba(15, 23, 42, 0.08)"
        sidebar_bg = "#FFFFFF"
        subtle_bg = "rgba(2, 132, 199, 0.08)"
        tab_bg = "#F1F5F9"
        tab_active = "#FFFFFF"
        hero_bg = "linear-gradient(135deg, rgba(2, 132, 199, 0.08) 0%, rgba(241, 245, 249, 0.95) 100%)"
        badge_bg = "rgba(2, 132, 199, 0.12)"
        badge_text = "#0284C7"
        input_bg = "#FFFFFF"
        input_border = "1.5px solid #94A3B8"
        radio_bg = "#FFFFFF"
    else:  # Dark mode default
        bg_color = "#070D1E"
        text_primary = "#F8FAFC"
        text_secondary = "#94A3B8"
        card_bg = "rgba(14, 23, 42, 0.85)"
        card_border = "1px solid rgba(2, 132, 199, 0.35)"
        card_border_hover = "1px solid #38BDF8"
        card_shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.45)"
        sidebar_bg = "#0B1329"
        subtle_bg = "rgba(2, 132, 199, 0.15)"
        tab_bg = "#0E172A"
        tab_active = "#1E293B"
        hero_bg = "linear-gradient(135deg, rgba(2, 132, 199, 0.15) 0%, rgba(15, 23, 42, 0.4) 100%)"
        badge_bg = "rgba(56, 189, 248, 0.15)"
        badge_text = "#38BDF8"
        input_bg = "#111C35"
        input_border = "1.5px solid #38BDF8"
        radio_bg = "rgba(14, 23, 42, 0.7)"

    primary_blue = UNIVERSITY_CONFIG.get("primary_color", "#0284C7")
    accent_gold = UNIVERSITY_CONFIG.get("accent_color", "#F59E0B")

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&family=Material+Icons&display=block');

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

    /* Sidebar Styling & Background Layering */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: {card_border} !important;
        padding-top: 1rem !important;
    }}

    /* Custom Sidebar Scrollbar */
    [data-testid="stSidebar"]::-webkit-scrollbar {{
        width: 6px;
    }}
    [data-testid="stSidebar"]::-webkit-scrollbar-track {{
        background: {sidebar_bg};
    }}
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {{
        background: {"rgba(2, 132, 199, 0.4)" if theme.lower()=="dark" else "#CBD5E1"};
        border-radius: 4px;
    }}

    /* ==========================================================================
       SIDEBAR TOGGLE CONTROL (COLLAPSE / EXPAND) - PROFESSIONAL UI STYLING
       ========================================================================== */

    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="collapsedControl"] *,
    [data-testid="stSidebarToggle"] *,
    [data-testid="stSidebarHeader"] button *,
    [data-testid="stHeader"] button *,
    button[aria-label="Collapse sidebar"] *,
    button[aria-label="Expand sidebar"] *,
    button[data-testid="stHeaderActionElements"] * {{
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons', sans-serif !important;
    }}

    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarToggle"] button,
    [data-testid="stSidebarHeader"] button,
    [data-testid="collapsedControl"],
    button[aria-label="Collapse sidebar"],
    button[aria-label="Expand sidebar"],
    button[data-testid="stBaseButton-header"],
    button[data-testid="stBaseButton-headerNoPadding"] {{
        background: {"rgba(14, 23, 42, 0.85)" if theme.lower() == "dark" else "#FFFFFF"} !important;
        border: {"1px solid rgba(56, 189, 248, 0.35)" if theme.lower() == "dark" else "1px solid #CBD5E1"} !important;
        border-radius: 10px !important;
        color: {primary_blue} !important;
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        max-width: 36px !important;
        max-height: 36px !important;
        padding: 0 !important;
        margin: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: {"0 4px 14px rgba(0, 0, 0, 0.35)" if theme.lower() == "dark" else "0 2px 8px rgba(15, 23, 42, 0.08)"} !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        backdrop-filter: blur(12px) !important;
    }}

    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="collapsedControl"] button:hover,
    [data-testid="collapsedControl"]:hover,
    [data-testid="stSidebarToggle"] button:hover,
    [data-testid="stSidebarHeader"] button:hover,
    button[aria-label="Collapse sidebar"]:hover,
    button[aria-label="Expand sidebar"]:hover,
    button[data-testid="stBaseButton-header"]:hover,
    button[data-testid="stBaseButton-headerNoPadding"]:hover {{
        background: {"rgba(2, 132, 199, 0.22)" if theme.lower() == "dark" else "rgba(2, 132, 199, 0.12)"} !important;
        border-color: {primary_blue} !important;
        color: {primary_blue} !important;
        transform: translateY(-1px) scale(1.05) !important;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.45) !important;
    }}

    [data-testid="stSidebarCollapseButton"] button:active,
    [data-testid="collapsedControl"] button:active,
    [data-testid="collapsedControl"]:active,
    [data-testid="stSidebarToggle"] button:active,
    button[aria-label="Collapse sidebar"]:active,
    button[aria-label="Expand sidebar"]:active {{
        transform: scale(0.95) !important;
    }}

    /* CRITICAL FIX: Hide raw text string "keyboard_double_arrow_..." */
    [data-testid="stSidebarCollapseButton"] button p,
    [data-testid="collapsedControl"] button p,
    [data-testid="collapsedControl"] p,
    [data-testid="stSidebarToggle"] button p,
    [data-testid="stSidebarHeader"] button p,
    button[aria-label="Collapse sidebar"] p,
    button[aria-label="Expand sidebar"] p,
    [data-testid="stSidebarCollapseButton"] button span,
    [data-testid="collapsedControl"] button span,
    [data-testid="collapsedControl"] span,
    [data-testid="stSidebarToggle"] button span,
    [data-testid="stSidebarHeader"] button span {{
        font-size: 0 !important;
        line-height: 0 !important;
        color: transparent !important;
        opacity: 0 !important;
        display: inline-block !important;
    }}

    /* Icon Pseudo-element fallback for Sidebar OPEN (Collapse button) */
    button[aria-label="Collapse sidebar"]::after,
    [data-testid="stSidebarCollapseButton"] button::after,
    [data-testid="stSidebarHeader"] button::after {{
        content: "‹" !important;
        font-family: 'Outfit', 'Inter', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: {primary_blue} !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* Icon Pseudo-element fallback for Sidebar COLLAPSED (Expand button) */
    button[aria-label="Expand sidebar"]::after,
    [data-testid="collapsedControl"] button::after,
    [data-testid="collapsedControl"]::after {{
        content: "›" !important;
        font-family: 'Outfit', 'Inter', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: {primary_blue} !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* Segmented Theme Control Wrapper */
    .theme-segmented-wrapper {{
        background-color: {"#0E172A" if theme.lower()=="dark" else "#F1F5F9"};
        border: 1px solid {"rgba(56, 189, 248, 0.35)" if theme.lower()=="dark" else "#CBD5E1"};
        border-radius: 12px;
        padding: 4px;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }}

    /* GLOBAL FIX: All Buttons & Download Buttons styling & Remove Inner Dark/Light Paragraph Rectangle */
    [data-testid="stButton"] button,
    [data-testid="stDownloadButton"] button {{
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 0.65rem 1.25rem !important;
        margin: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }}

    /* CRITICAL FIX: Eliminate inner dark paragraph rectangle inside ALL buttons */
    [data-testid="stButton"] button *,
    [data-testid="stDownloadButton"] button * {{
        background: transparent !important;
        background-color: transparent !important;
        color: inherit !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }}

    /* Active / Primary Theme Button (Solid Filled Blue Gradient) */
    button[kind="primary"],
    button[data-testid="baseButton-primary"],
    [data-testid="stButton"] button[kind="primary"],
    [data-testid="stButton"] button[data-testid="baseButton-primary"],
    [data-testid="stDownloadButton"] button[kind="primary"],
    [data-testid="stDownloadButton"] button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #38BDF8 !important;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.45) !important;
    }}

    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    [data-testid="stButton"] button[kind="primary"]:hover,
    [data-testid="stButton"] button[data-testid="baseButton-primary"]:hover,
    [data-testid="stDownloadButton"] button[kind="primary"]:hover,
    [data-testid="stDownloadButton"] button[data-testid="baseButton-primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(2, 132, 199, 0.7) !important;
        border-color: #7DD3FC !important;
        background: linear-gradient(135deg, #0369A1 0%, #0284C7 100%) !important;
    }}

    /* Inactive / Secondary Theme Button */
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"],
    [data-testid="stButton"] button[kind="secondary"],
    [data-testid="stButton"] button[data-testid="baseButton-secondary"],
    [data-testid="stDownloadButton"] button[kind="secondary"],
    [data-testid="stDownloadButton"] button[data-testid="baseButton-secondary"] {{
        background: {"rgba(14, 23, 42, 0.6)" if theme.lower()=="dark" else "#FFFFFF"} !important;
        color: {"#94A3B8" if theme.lower()=="dark" else "#475569"} !important;
        border: 1px solid {"rgba(56, 189, 248, 0.3)" if theme.lower()=="dark" else "#CBD5E1"} !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }}

    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    [data-testid="stButton"] button[kind="secondary"]:hover,
    [data-testid="stButton"] button[data-testid="baseButton-secondary"]:hover,
    [data-testid="stDownloadButton"] button[kind="secondary"]:hover,
    [data-testid="stDownloadButton"] button[data-testid="baseButton-secondary"]:hover {{
        background: {subtle_bg} !important;
        color: {primary_blue} !important;
        border-color: {primary_blue} !important;
        transform: translateY(-1px) !important;
    }}

    /* Sidebar Section Headers */
    .sidebar-nav-header {{
        font-family: 'Outfit', sans-serif;
        font-size: 0.88rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: {"#38BDF8" if theme.lower()=="dark" else "#0284C7"};
        text-transform: uppercase;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid {"rgba(56, 189, 248, 0.25)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.15)"};
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }}

    .sidebar-section-title {{
        font-size: 0.9rem;
        font-weight: 700;
        color: {text_primary};
        margin-top: 1.1rem;
        margin-bottom: 0.45rem;
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }}

    .sidebar-label-title {{
        font-size: 0.84rem;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 0.35rem;
    }}

    /* CRITICAL FIX: Sidebar Control Borders & Outlines (Dark/Light High Visibility) */
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="select"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"],
    [data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid="stSidebar"] [data-baseweb="select"],
    [data-testid="stSidebar"] [data-baseweb="input"],
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="input"] > div,
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label,
    div[data-baseweb="select"] > div {{
        background-color: {"#111C35" if theme.lower()=="dark" else "#FFFFFF"} !important;
        border: {"2px solid #38BDF8" if theme.lower()=="dark" else "2px solid #0284C7"} !important;
        box-shadow: {"0 0 0 2px #38BDF8, 0 4px 12px rgba(56, 189, 248, 0.35)" if theme.lower()=="dark" else "0 0 0 2px #0284C7, 0 2px 8px rgba(2, 132, 199, 0.2)"} !important;
        border-radius: 10px !important;
        transition: all 0.25s ease !important;
    }}

    [data-testid="stSidebar"] [data-baseweb="select"]:hover,
    [data-testid="stSidebar"] [data-baseweb="select"] > div:hover,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="select"]:hover,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"]:hover,
    [data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"]:hover,
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover,
    div[data-baseweb="select"] > div:hover {{
        border-color: {"#7DD3FC" if theme.lower()=="dark" else "#0369A1"} !important;
        box-shadow: {"0 0 0 2px #7DD3FC, 0 0 16px rgba(56, 189, 248, 0.6)" if theme.lower()=="dark" else "0 0 0 2px #0369A1, 0 0 12px rgba(2, 132, 199, 0.3)"} !important;
    }}

    [data-testid="stSidebar"] [data-testid="stRadio"] label {{
        color: {text_primary} !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }}

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {{
        padding: 0.4rem 0.65rem !important;
        margin-bottom: 0.35rem !important;
    }}

    [data-testid="stSidebar"] [data-testid="stNumberInput"] input {{
        color: {text_primary} !important;
        font-weight: 700 !important;
        font-size: 0.94rem !important;
        text-align: center !important;
    }}

    [data-testid="stSidebar"] [data-testid="stNumberInput"] button {{
        display: none !important;
    }}

    div[data-baseweb="select"] > div:hover {{
        border-color: {"#38BDF8" if theme.lower()=="dark" else "#0284C7"} !important;
        box-shadow: 0 0 12px {"rgba(2, 132, 199, 0.35)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.2)"} !important;
    }}

    div[data-baseweb="select"] span {{
        color: {text_primary} !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
    }}

    div[data-baseweb="select"] [data-aria-hidden="true"] {{
        color: {"#94A3B8" if theme.lower()=="dark" else "#64748B"} !important;
        font-weight: 500 !important;
    }}

    div[data-baseweb="select"] svg {{
        fill: {"#38BDF8" if theme.lower()=="dark" else "#0284C7"} !important;
        color: {"#38BDF8" if theme.lower()=="dark" else "#0284C7"} !important;
    }}

    /* FIX: Multiselect Tag Chips */
    [data-baseweb="tag"] {{
        background-color: {"rgba(2, 132, 199, 0.22)" if theme.lower()=="dark" else "#E2E8F0"} !important;
        border: 1px solid {"rgba(56, 189, 248, 0.4)" if theme.lower()=="dark" else "#CBD5E1"} !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }}

    [data-baseweb="tag"] span {{
        color: {text_primary} !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
    }}

    /* FIX: Slider Track Red Accent Override */
    [data-testid="stSidebar"] [data-testid="stSlider"] {{
        padding-top: 0.25rem !important;
        padding-bottom: 0.25rem !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stTickBar"] {{
        display: none !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] > div {{
        background: {"#1E293B" if theme.lower()=="dark" else "#E2E8F0"} !important;
        height: 6px !important;
        border-radius: 4px !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] div[style*="background"] {{
        background: #0284C7 !important;
        background-color: #0284C7 !important;
        height: 6px !important;
        border-radius: 4px !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {{
        background-color: #0284C7 !important;
        border: 2px solid #38BDF8 !important;
        box-shadow: 0 0 12px rgba(2, 132, 199, 0.85) !important;
        width: 18px !important;
        height: 18px !important;
        top: -6px !important;
        transition: transform 0.2s ease !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"]:hover {{
        transform: scale(1.25) !important;
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
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 1.25rem;
    }}

    .glass-card:hover {{
        transform: translateY(-3px) scale(1.002);
        box-shadow: 0 12px 35px -5px rgba(2, 132, 199, 0.3) !important;
        border: {card_border_hover} !important;
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
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
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
        border: {card_border_hover} !important;
        box-shadow: 0 12px 30px -5px rgba(2, 132, 199, 0.35) !important;
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
        font-weight: 600;
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
        background: {badge_bg};
        color: {badge_text};
        padding: 0.15rem 0.45rem;
        border-radius: 4px;
        font-weight: 700;
        margin-left: 0.4rem;
    }}

    .univ-title {{
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: {text_primary} !important;
        -webkit-text-fill-color: {text_primary} !important;
        margin: 0 !important;
        line-height: 1.3 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    .univ-subtitle {{
        font-size: 0.84rem;
        font-weight: 600;
        color: {primary_blue};
        margin: 0;
    }}

    /* Hero Dossier Banner */
    .hero-banner {{
        background: {hero_bg};
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
        font-family: 'Outfit', 'Inter', sans-serif !important;
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        color: {text_primary} !important;
        -webkit-text-fill-color: {text_primary} !important;
        background: none !important;
        margin: 0.4rem 0 0.2rem 0 !important;
        line-height: 1.25 !important;
        display: block !important;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    .hero-subtitle-tag {{
        font-family: 'Outfit', 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: {primary_blue} !important;
        -webkit-text-fill-color: {primary_blue} !important;
        margin: 0 0 0.8rem 0 !important;
        display: block !important;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    .rank-box {{
        background: {card_bg};
        border: 1px solid rgba(245, 158, 11, 0.35);
        border-radius: 12px;
        padding: 0.8rem 1.4rem;
        display: inline-flex;
        align-items: center;
        gap: 1.2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
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

    /* Streamlit Metric Styling */
    [data-testid="stMetric"] {{
        background: {card_bg} !important;
        border: {card_border} !important;
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
        box-shadow: {card_shadow} !important;
    }}

    [data-testid="stMetricLabel"] {{
        color: {text_secondary} !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {text_primary} !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* Streamlit Containers, DataFrames & Expanders Borders */
    [data-testid="stDataFrame"], .stExpander {{
        background: {card_bg} !important;
        border: {card_border} !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }}

    .stExpander summary span {{
        color: {text_primary} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stDataFrame"]:hover, .stExpander:hover {{
        border: {card_border_hover} !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.2) !important;
    }}

    /* Buttons Styling (Main Area) */
    .stButton button[kind="primary"],
    button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #38BDF8 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
        transition: all 0.25s ease !important;
    }}

    .stButton button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.6) !important;
    }}

    .stButton button[kind="secondary"],
    button[data-testid="baseButton-secondary"] {{
        background: {card_bg} !important;
        color: {text_primary} !important;
        border: 1px solid {input_border} !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }}

    .stButton button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {{
        border-color: {primary_blue} !important;
        color: {primary_blue} !important;
        background: {subtle_bg} !important;
    }}

    /* Streamlit Tabs Navigation Styling & Unified Container Card */
    .stTabs {{
        background: {card_bg} !important;
        border: {card_border} !important;
        border-radius: 18px !important;
        box-shadow: {card_shadow} !important;
        padding: 0 !important;
        margin-bottom: 1.8rem !important;
        overflow: hidden !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px !important;
        background-color: {tab_bg} !important;
        padding: 10px 14px !important;
        border: none !important;
        border-bottom: {card_border} !important;
        border-radius: 18px 18px 0 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        margin-bottom: 0 !important;
        box-shadow: none !important;
    }}

    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 38px !important;
        line-height: 38px !important;
        border-radius: 10px !important;
        color: {text_secondary} !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0 16px !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        transition: all 0.2s ease-in-out !important;
        white-space: nowrap !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: {primary_blue} !important;
        border: {card_border_hover} !important;
        background: {subtle_bg} !important;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {tab_active} !important;
        color: {primary_blue} !important;
        border: {card_border_hover} !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
        font-weight: 700 !important;
    }}

    /* Tab Content Padding & Alignment Inside Container */
    [data-testid="stTabContent"] {{
        background: transparent !important;
        border: none !important;
        border-radius: 0 0 18px 18px !important;
        padding: 1.4rem 1.6rem !important;
        box-shadow: none !important;
    }}

    /* AI Copilot Chat Inputs & Messages Styling */
    [data-testid="stChatInput"] {{
        background: {input_bg} !important;
        border: 1px solid {input_border} !important;
        border-radius: 14px !important;
    }}

    [data-testid="stChatInput"] textarea {{
        color: {text_primary} !important;
    }}

    [data-testid="stChatMessage"] {{
        background: {subtle_bg} !important;
        border: {card_border} !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
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
            <span style="font-size: 0.8rem; font-weight: 600; opacity: 0.85; display: inline-flex; align-items: center; gap: 0.4rem;">
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
    full_name = UNIVERSITY_CONFIG.get("full_name", "Dr. Babasaheb Ambedkar Marathwada University")
    divider_bg = "rgba(255, 255, 255, 0.15)" if theme.lower() == "dark" else "rgba(15, 23, 42, 0.15)"

    html = f"""
    <div class="hero-banner">
        <div class="hero-badges-wrapper">
            <span class="hero-badge">🏆 Scopus Research Dossier</span>
            <span class="hero-badge">{status_tag}</span>
            <span class="hero-badge">{naac_badge}</span>
            <span class="hero-badge">📜 NIRF Category: University</span>
        </div>
        <div class="hero-title">{full_name}</div>
        <div class="hero-subtitle-tag">{app_title}</div>
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
            <p style="margin: 0; font-size: 0.95rem; opacity: 0.85; max-width: 650px;">
                Comprehensive institutional bibliometric analytics, faculty h-index tracking, Q1 publication trends, and international collaboration intelligence for Dr. Babasaheb Ambedkar Marathwada University.
            </p>
            <div class="rank-box">
                <div>
                    <div class="rank-num">#{total_pubs:,}</div>
                    <div class="rank-label">Indexed Papers</div>
                </div>
                <div style="height: 30px; width: 1px; background: {divider_bg};"></div>
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

