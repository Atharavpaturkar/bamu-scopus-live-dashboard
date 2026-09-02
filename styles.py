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
        color: {text_primary} !important;
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

    /* Premium Evaluation Period Header Card */
    .eval-period-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: {subtle_bg};
        border: 1px solid {"rgba(56, 189, 248, 0.25)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.2)"};
        border-radius: 10px;
        padding: 0.45rem 0.75rem;
        margin-top: 1rem;
        margin-bottom: 0.65rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        backdrop-filter: blur(8px);
    }}

    .eval-period-title {{
        font-family: 'Outfit', sans-serif;
        font-size: 0.88rem;
        font-weight: 700;
        color: {text_primary};
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }}

    .eval-period-badge {{
        font-family: 'Outfit', sans-serif;
        font-size: 0.76rem;
        font-weight: 800;
        color: {primary_blue};
        background: {badge_bg};
        border: 1px solid {"rgba(56, 189, 248, 0.3)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.25)"};
        padding: 0.18rem 0.55rem;
        border-radius: 6px;
        letter-spacing: 0.04em;
        white-space: nowrap;
    }}

    .sidebar-label-title {{
        font-family: 'Inter', sans-serif;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: {text_secondary};
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
        border: {"1.5px solid #38BDF8" if theme.lower()=="dark" else "1.5px solid #0284C7"} !important;
        box-shadow: {"0 0 0 1px #38BDF8, 0 3px 10px rgba(56, 189, 248, 0.25)" if theme.lower()=="dark" else "0 0 0 1px #0284C7, 0 2px 8px rgba(2, 132, 199, 0.15)"} !important;
        border-radius: 9px !important;
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
        box-shadow: {"0 0 0 1.5px #7DD3FC, 0 0 14px rgba(56, 189, 248, 0.5)" if theme.lower()=="dark" else "0 0 0 1.5px #0369A1, 0 0 10px rgba(2, 132, 199, 0.25)"} !important;
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
        font-family: 'Outfit', sans-serif !important;
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

    /* CHANGE 5: Multiselect Tag Chips (Light Mode Blue Tint & Dark Mode High Contrast) */
    [data-baseweb="tag"] {{
        background-color: {"rgba(2, 132, 199, 0.22)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.12)"} !important;
        border: 1px solid {"rgba(56, 189, 248, 0.4)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.3)"} !important;
        border-radius: 6px !important;
        padding: 2px 7px !important;
    }}

    [data-baseweb="tag"] span {{
        color: {text_primary if theme.lower()=="dark" else "#0284C7"} !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
    }}

    /* FIX: Premium Slider Track & Glow Handle for Evaluation Period */
    [data-testid="stSidebar"] [data-testid="stSlider"] {{
        padding-top: 0.3rem !important;
        padding-bottom: 0.4rem !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stTickBar"] {{
        display: none !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] > div {{
        background: {"rgba(30, 41, 59, 0.8)" if theme.lower()=="dark" else "#E2E8F0"} !important;
        height: 7px !important;
        border-radius: 6px !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] div[style*="background"] {{
        background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important;
        background-color: #0284C7 !important;
        height: 7px !important;
        border-radius: 6px !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.4) !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {{
        background-color: {"#38BDF8" if theme.lower()=="dark" else "#0284C7"} !important;
        border: 2.5px solid {"#070D1E" if theme.lower()=="dark" else "#FFFFFF"} !important;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.75), 0 2px 6px rgba(0, 0, 0, 0.3) !important;
        width: 20px !important;
        height: 20px !important;
        top: -6.5px !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        cursor: grab !important;
    }}

    [data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"]:hover {{
        transform: scale(1.25) !important;
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.95), 0 4px 10px rgba(0, 0, 0, 0.4) !important;
    }}

    /* Glassmorphism Cards & Container Cleanup */
    .glass-card {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        margin-bottom: 1.25rem;
    }}

    .glass-card:hover {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        transform: none !important;
    }}

    /* CRITICAL FIX: Completely eliminate empty rounded container boxes/bars throughout dashboard */
    .glass-card:empty,
    div.glass-card:empty,
    [data-testid="stMarkdownContainer"] > div.glass-card:empty,
    [data-testid="stMarkdownContainer"]:empty,
    .element-container:has(> [data-testid="stMarkdownContainer"] > div.glass-card:empty),
    .element-container:has(> [data-testid="stMarkdownContainer"]:empty) {{
        display: none !important;
        height: 0 !important;
        max-height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
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
        border-radius: 12px;
        padding: 0.45rem 1.1rem;
        margin-bottom: 0.85rem;
        box-shadow: {card_shadow};
    }}

    .icare-logo-badge {{
        background: {subtle_bg};
        border: 1px solid {"rgba(56, 189, 248, 0.25)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.2)"};
        border-radius: 9px;
        padding: 0.28rem 0.65rem;
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
    }}

    .icare-logo-img {{
        height: 34px;
        width: auto;
        max-width: 140px;
        object-fit: contain;
        border-radius: 5px;
        background: #FFFFFF;
        padding: 3px 7px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
        display: inline-block;
        vertical-align: middle;
    }}

    .icare-subtext {{
        font-family: 'Outfit', sans-serif;
        font-size: 0.70rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: {primary_blue};
        text-transform: uppercase;
        white-space: nowrap;
        padding: 0.15rem 0.45rem;
        background: {badge_bg};
        border-radius: 4px;
        border: 1px solid {"rgba(56, 189, 248, 0.2)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.15)"};
    }}

    .univ-header-card {{
        background: {subtle_bg};
        border: 1px solid {"rgba(56, 189, 248, 0.2)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.15)"};
        border-left: 3px solid {primary_blue};
        border-radius: 8px;
        padding: 0.25rem 0.75rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        backdrop-filter: blur(8px);
    }}

    .univ-title {{
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.02rem !important;
        font-weight: 700 !important;
        color: {text_primary} !important;
        -webkit-text-fill-color: {text_primary} !important;
        margin: 0 !important;
        line-height: 1.25 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    .univ-subtitle {{
        font-size: 0.78rem;
        font-weight: 600;
        color: {primary_blue};
        margin: 0.1rem 0 0 0;
    }}

    .live-status-pill {{
        font-size: 0.75rem;
        font-weight: 600;
        color: #10B981;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.25);
        padding: 0.3rem 0.7rem;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        white-space: nowrap;
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

    /* Streamlit Containers, DataFrames & Expanders Borders & Layout */
    [data-testid="stDataFrame"], .stExpander {{
        background: {card_bg} !important;
        border: {card_border} !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }}

    /* Faculty Leaderboard Expander - title alignment */
    .stExpander summary {{
        color: {text_primary} !important;
    }}

    .stExpander summary [data-testid="stIcon"],
    .stExpander summary i,
    .stExpander summary svg,
    [data-testid="stExpanderToggleIcon"] {{
        flex-shrink: 0 !important;
    }}

    .stExpander summary span {{
        color: {text_primary} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stDataFrame"]:hover, .stExpander:hover {{
        border: {card_border_hover} !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.2) !important;
    }}

    [data-testid="stDataFrame"] *,
    [data-testid="stTable"] * {{
        color: {text_primary} !important;
    }}

    [data-testid="stDataFrame"] a,
    [data-testid="stTable"] a {{
        color: {"#38BDF8" if theme.lower()=="dark" else "#0284C7"} !important;
        font-weight: 700 !important;
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

    /* ==========================================================================
       SCOPUS RESEARCH ANALYTICS SECTION HEADER & ZONE IDENTITY
       ========================================================================== */
    /* ==========================================================================
       SCOPUS RESEARCH ANALYTICS SECTION HEADER & ZONE IDENTITY (CHANGE 6)
       ========================================================================== */
    .analytics-section-header {{
        margin-top: 2.4rem !important;
        margin-bottom: 1.25rem !important;
        padding-top: 1.6rem !important;
        border-top: 2px solid {"rgba(56, 189, 248, 0.3)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.2)"} !important;
    }}

    .analytics-section-badge {{
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.45rem !important;
        padding: 0.35rem 0.85rem !important;
        border-radius: 20px !important;
        font-size: 0.76rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        background: {badge_bg} !important;
        color: {badge_text} !important;
        border: 1px solid {"rgba(56, 189, 248, 0.35)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.28)"} !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }}

    .analytics-section-title {{
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        color: {text_primary} !important;
        margin: 0.45rem 0 0.2rem 0 !important;
        letter-spacing: -0.01em !important;
    }}

    .analytics-section-subtitle {{
        font-size: 0.88rem !important;
        color: {text_secondary} !important;
        font-weight: 500 !important;
        line-height: 1.4 !important;
    }}

    /* Streamlit Tabs Navigation Styling & Container */
    .stTabs {{
        background: {card_bg} !important;
        border: {card_border} !important;
        border-radius: 18px !important;
        box-shadow: {card_shadow} !important;
        padding: 0 !important;
        margin-bottom: 1.8rem !important;
        overflow: hidden !important;
    }}

    /* CHANGE 2: Tab Navigation Overflow & Hidden Browser Scrollbar */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px !important;
        background-color: {tab_bg} !important;
        padding: 8px 14px 0 14px !important;
        border: none !important;
        border-bottom: {card_border} !important;
        border-radius: 18px 18px 0 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
        margin-bottom: 0 !important;
        box-shadow: none !important;
    }}

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
        display: none !important;
        height: 0 !important;
        width: 0 !important;
    }}

    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}

    /* CHANGE 4: Dark Mode Inactive Tab Readability (#CBD5E1) */
    .stTabs [data-baseweb="tab"] {{
        height: 44px !important;
        line-height: 44px !important;
        border: none !important;
        border-bottom: 2.5px solid transparent !important;
        border-radius: 0 !important;
        color: {"#CBD5E1" if theme.lower()=="dark" else text_secondary} !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 0 16px !important;
        background: transparent !important;
        box-shadow: none !important;
        transition: color 0.2s ease, border-color 0.2s ease !important;
        white-space: nowrap !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: {"#38BDF8" if theme.lower()=="dark" else primary_blue} !important;
        border: none !important;
        border-bottom: 2.5px solid {"rgba(56, 189, 248, 0.4)" if theme.lower()=="dark" else "rgba(2, 132, 199, 0.4)"} !important;
        background: transparent !important;
        box-shadow: none !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: transparent !important;
        color: {"#38BDF8" if theme.lower()=="dark" else primary_blue} !important;
        font-weight: 800 !important;
        border: none !important;
        border-bottom: 2.5px solid {"#38BDF8" if theme.lower()=="dark" else primary_blue} !important;
        box-shadow: none !important;
    }}

    /* Tab Content Padding & Alignment Inside Container */
    [data-testid="stTabContent"] {{
        background: transparent !important;
        border: none !important;
        border-radius: 0 0 18px 18px !important;
        padding: 1.4rem 1.6rem !important;
        box-shadow: none !important;
    }}

    /* CHANGE 1: Subsection Headings & Visual Grouping inside Analytics Tabs */
    [data-testid="stTabContent"] h3,
    [data-testid="stTabContent"] .stMarkdown:has(> h3) {{
        margin-top: 1.4rem !important;
        margin-bottom: 0.45rem !important;
        padding-left: 0.65rem !important;
        border-left: 3.5px solid {primary_blue} !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: {text_primary} !important;
        line-height: 1.3 !important;
    }}

    [data-testid="stTabContent"] h4,
    [data-testid="stTabContent"] .stMarkdown:has(> h4) {{
        margin-top: 1.1rem !important;
        margin-bottom: 0.35rem !important;
        color: {text_primary} !important;
        font-weight: 700 !important;
    }}

    /* CHANGE 3: Responsive AI Copilot Action Chips Container */
    .copilot-action-bar [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.5rem !important;
    }}

    .copilot-action-bar [data-testid="column"] {{
        flex: 1 1 140px !important;
        min-width: 130px !important;
        max-width: 100% !important;
    }}

    /* ISSUE 2 FIX: Live Feed Search Input Placeholder Contrast (Dark Mode scoped) */
    [data-testid="stTextInput"] input::placeholder {{
        color: {"rgba(248, 250, 252, 0.65)" if theme.lower() == "dark" else "rgba(15, 23, 42, 0.55)"} !important;
        opacity: 1 !important;
    }}

    /* ISSUE 3 FIX: AI Copilot Chat Inputs & Messages Avatar Overlap & Placeholder Contrast */
    [data-testid="stChatMessageAvatar"],
    [data-testid="stChatMessageAvatar"] *,
    [data-testid="stChatMessage"] [data-testid="stIcon"],
    [data-testid="stChatMessage"] div[data-testid="stChatMessageAvatar"] span {{
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons', sans-serif !important;
    }}

    [data-testid="stChatMessage"] {{
        background: {subtle_bg} !important;
        border: {card_border} !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
        display: flex !important;
        align-items: flex-start !important;
        gap: 0.8rem !important;
    }}

    [data-testid="stChatMessageContent"] {{
        color: {text_primary} !important;
    }}

    [data-testid="stChatInput"] {{
        background: {input_bg} !important;
        border: 1px solid {input_border} !important;
        border-radius: 14px !important;
    }}

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] input {{
        color: {text_primary} !important;
    }}

    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInput"] input::placeholder,
    div[data-testid="stChatInput"] [data-baseweb="base-input"] ::placeholder {{
        color: {"rgba(248, 250, 252, 0.65)" if theme.lower() == "dark" else "rgba(15, 23, 42, 0.55)"} !important;
        opacity: 1 !important;
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


def get_bamu_logo_b64():
    for logo_path in ["bamu_logo_transparent.png", "bamu_logo.png", "bamu_logo.jpeg"]:
        if os.path.exists(logo_path):
            try:
                with open(logo_path, "rb") as f:
                    mime = "image/png" if logo_path.endswith(".png") else "image/jpeg"
                    return f"data:{mime};base64," + base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return ""


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
        <div style="display: flex; align-items: center; gap: 0.85rem;">
            <div class="icare-logo-badge">
                {logo_html}
                <span class="icare-subtext">PORTAL INTELLIGENCE</span>
            </div>
            <div class="univ-header-card">
                <h2 class="univ-title">{univ_name}</h2>
                <div class="univ-subtitle"><b>{nirf_id}</b> • {city}</div>
            </div>
        </div>
        <div style="text-align: right;">
            <span class="live-status-pill">
                <span style="height: 8px; width: 8px; background-color: #10B981; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #10B981;"></span>
                Live Scopus API Engine Active
            </span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_icare_hero(total_pubs, total_cites, theme="dark"):
    """
    Render ICARE Hero Research Dossier Banner with BAMU logo, badges, title, and rank statistics.
    """
    status_tag = UNIVERSITY_CONFIG.get("status_tag", "🏛 State Public University (Estd. 1958)")
    naac_badge = UNIVERSITY_CONFIG.get("naac_badge", "⭐ NAAC A+ (CGPA 3.38)")
    app_title = UNIVERSITY_CONFIG.get("app_title", "BAMU Live Scopus Intelligence Dashboard")
    full_name = UNIVERSITY_CONFIG.get("full_name", "Dr. Babasaheb Ambedkar Marathwada University")
    divider_bg = "rgba(255, 255, 255, 0.15)" if theme.lower() == "dark" else "rgba(15, 23, 42, 0.15)"

    hero_logo_filter = "drop-shadow(0 0 1.5px rgba(255, 255, 255, 0.9)) drop-shadow(0 4px 12px rgba(56, 189, 248, 0.5))" if theme.lower() == "dark" else "drop-shadow(0 3px 10px rgba(15, 23, 42, 0.2))"

    bamu_b64 = get_bamu_logo_b64()
    if bamu_b64:
        hero_logo_html = f'<img src="{bamu_b64}" alt="BAMU Logo" style="height: 76px; width: auto; max-width: 82px; object-fit: contain; background: transparent !important; background-color: transparent !important; border: none; flex-shrink: 0; filter: {hero_logo_filter};">'
    else:
        hero_logo_html = ''

    html = f"""
    <div class="hero-banner">
        <div class="hero-badges-wrapper">
            <span class="hero-badge">🏆 Scopus Research Dossier</span>
            <span class="hero-badge">{status_tag}</span>
            <span class="hero-badge">{naac_badge}</span>
            <span class="hero-badge">📜 NIRF Category: University</span>
        </div>
        <div style="display: flex; align-items: center; gap: 1.2rem; margin: 0.6rem 0;">
            {hero_logo_html}
            <div>
                <div class="hero-title" style="margin: 0;">{full_name}</div>
                <div class="hero-subtitle-tag" style="margin-top: 0.2rem;">{app_title}</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; margin-top: 0.8rem;">
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

