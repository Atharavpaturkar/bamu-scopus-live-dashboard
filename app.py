import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import base64
import io
import streamlit.components.v1 as components

from config import UNIVERSITY_CONFIG
from scopus_api import get_scopus_publications
from mock_data import load_or_generate_mock_data, BAMU_DEPARTMENTS
from data_processor import (
    calculate_top_10_kpis,
    get_publications_by_year,
    get_publications_by_month,
    get_top_authors_leaderboard,
    get_author_profile_metrics,
    filter_publications,
    export_to_bibtex,
    generate_author_print_html
)
from ai_copilot import query_ai_copilot
from styles import get_custom_css, render_icare_topbar, render_icare_hero

# Page Configuration
st.set_page_config(
    page_title=UNIVERSITY_CONFIG['app_title'],
    page_icon="🏛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Responsive Sidebar JavaScript Injection (Desktop expanded, Mobile collapsed)
js_responsive_sidebar = """
<script>
(function() {
    function adjustSidebar() {
        try {
            const parentDoc = (window.parent && window.parent.document) ? window.parent.document : document;
            const width = parentDoc.documentElement.clientWidth || window.innerWidth;
            const sidebar = parentDoc.querySelector('[data-testid="stSidebar"]');
            if (!sidebar) return;
            if (width > 768) {
                sidebar.setAttribute('aria-expanded', 'true');
            } else {
                sidebar.setAttribute('aria-expanded', 'false');
            }
        } catch(e) {}
    }
    setTimeout(adjustSidebar, 200);
    window.addEventListener('resize', adjustSidebar);
})();
</script>
"""
components.html(js_responsive_sidebar, height=0, width=0)

# Sidebar Branding & Scopus Gateway
st.sidebar.markdown(f"""
<div style="background: rgba(2, 132, 199, 0.12); border: 1px solid rgba(2, 132, 199, 0.3); border-radius: 12px; padding: 1rem; margin-bottom: 1.2rem; text-align: center;">
    <div style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.05rem; color: #0284C7;">
        🏛 BAMU PORTAL
    </div>
    <div style="font-size: 0.8rem; font-weight: 600; opacity: 0.9; margin-top: 0.2rem;">
        Live Scopus Intelligence [{UNIVERSITY_CONFIG.get('nirf_id', 'IR-O-U-0298')}]
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 0.6rem 0.8rem; font-size: 0.78rem; font-weight: 600; color: #10B981; margin-bottom: 1.2rem; text-align: center;">
    🟢 Live Scopus Feed • Auto-synced every 60m
</div>
""", unsafe_allow_html=True)

# Theme Selection Buttons
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

c_t1, c_t2 = st.sidebar.columns(2)
with c_t1:
    dark_btn_type = "primary" if st.session_state.theme == "Dark" else "secondary"
    if st.button("🌙 Dark Mode", use_container_width=True, type=dark_btn_type, key="btn_theme_dark"):
        st.session_state.theme = "Dark"
        st.rerun()

with c_t2:
    light_btn_type = "primary" if st.session_state.theme == "Light" else "secondary"
    if st.button("☀️ Light Mode", use_container_width=True, type=light_btn_type, key="btn_theme_light"):
        st.session_state.theme = "Light"
        st.rerun()

theme = st.session_state.theme

# Apply CSS Theme
st.markdown(get_custom_css(theme), unsafe_allow_html=True)

# Scopus Gateway Panel & Controls
data_mode = st.sidebar.radio(
    "📡 Data Engine Mode",
    ["Live Scopus API (Auto-Sync)", "Benchmark Offline Demo (~2,500 Papers)"],
    index=0
)

# Manual Sync Button in Scopus Gateway Panel
force_refresh = st.sidebar.button("🔄 Sync Scopus Now", use_container_width=True, type="primary")

# Load Dataset
@st.cache_data(ttl=1800, show_spinner=False)
def load_dashboard_data(mode_name, refresh_flag):
    if "Live" in mode_name:
        pubs = get_scopus_publications(force_refresh=refresh_flag)
    else:
        pubs = load_or_generate_mock_data()
    return pd.DataFrame(pubs)


with st.spinner("Connecting to Scopus Intelligence Engine..."):
    df_raw = load_dashboard_data(data_mode, force_refresh)

if df_raw.empty:
    st.error("No publication data available. Please check Scopus API key or connection.")
    st.stop()

# Sidebar Navigation & Filter Section Header
st.sidebar.markdown('<div class="sidebar-nav-header">🔍 NAVIGATE & FILTER</div>', unsafe_allow_html=True)

# Subheader: Evaluation Period
st.sidebar.markdown('<div class="sidebar-section-title">📅 Evaluation Period</div>', unsafe_allow_html=True)

# Year Range Slider & Inputs
data_min_yr = int(df_raw['year'].min()) if not df_raw.empty else 1950
slider_min_yr = min(1950, data_min_yr)
slider_max_yr = 2026

if "start_year" not in st.session_state:
    st.session_state.start_year = 1950
if "end_year" not in st.session_state:
    st.session_state.end_year = 2026

slider_yr = st.sidebar.slider(
    "Evaluation Period Range",
    min_value=slider_min_yr,
    max_value=slider_max_yr,
    value=(st.session_state.start_year, st.session_state.end_year),
    label_visibility="collapsed"
)

# Start Year & End Year side-by-side inputs
c_y1, c_y2 = st.sidebar.columns(2)
with c_y1:
    st.markdown("<div class='sidebar-label-title'>Start Year</div>", unsafe_allow_html=True)
    input_start_val = st.number_input("Start Year Input", min_value=slider_min_yr, max_value=slider_max_yr, value=slider_yr[0], step=1, label_visibility="collapsed")

with c_y2:
    st.markdown("<div class='sidebar-label-title'>End Year</div>", unsafe_allow_html=True)
    input_end_val = st.number_input("End Year Input", min_value=slider_min_yr, max_value=slider_max_yr, value=slider_yr[1], step=1, label_visibility="collapsed")

# Apply Year Range Button
apply_yr_btn = st.sidebar.button("🔄 Apply Year Range", use_container_width=True, type="primary", key="btn_apply_yr")
if apply_yr_btn:
    st.session_state.start_year = int(input_start_val)
    st.session_state.end_year = int(input_end_val)
    st.rerun()

selected_year_range = (min(input_start_val, input_end_val), max(input_start_val, input_end_val))

# Dropdown Filter 1: Department / School
st.sidebar.markdown('<div class="sidebar-section-title">🏢 Department / School</div>', unsafe_allow_html=True)
available_depts = sorted(list(df_raw['department'].dropna().unique()))
selected_depts = st.sidebar.multiselect(
    "Department Filter",
    options=available_depts,
    default=[],
    placeholder="Choose options",
    label_visibility="collapsed"
)

# Dropdown Filter 2: Journal Quartile (Q1-Q4)
st.sidebar.markdown('<div class="sidebar-section-title">🏆 Journal Quartile (Q1-Q4)</div>', unsafe_allow_html=True)
available_quartiles = ["Q1", "Q2", "Q3", "Q4"]
selected_quartiles = st.sidebar.multiselect(
    "Quartile Filter",
    options=available_quartiles,
    default=[],
    placeholder="Choose options",
    label_visibility="collapsed"
)

# Dropdown Filter 3: Collaboration Scope
st.sidebar.markdown('<div class="sidebar-section-title">🌐 Collaboration Scope</div>', unsafe_allow_html=True)
available_collabs = ["International Collaboration", "Industry Collaboration", "Institutional / National"]
selected_collabs = st.sidebar.multiselect(
    "Collaboration Scope Filter",
    options=available_collabs,
    default=[],
    placeholder="Choose options",
    label_visibility="collapsed"
)

# Apply Filtered Dataset
df_filtered = filter_publications(
    df_raw,
    year_range=selected_year_range,
    depts=selected_depts,
    quartiles=selected_quartiles,
    collab_types=selected_collabs
)

# Render Topbar & Hero Banner
render_icare_topbar(theme)
kpi_data = calculate_top_10_kpis(df_filtered)
render_icare_hero(kpi_data["total_output"], kpi_data["total_citations"], theme)

# 10 Executive KPI Cards Grid
st.markdown("### 📊 Executive Research Metrics")
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Indexed</div>
        <div class="kpi-value">{kpi_data['total_output']:,}</div>
        <div class="kpi-subtext">Scopus Output</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">2026 Volume</div>
        <div class="kpi-value">{kpi_data['volume_2026']:,}</div>
        <div class="kpi-subtext">Current Year</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Citations</div>
        <div class="kpi-value" style="color: #0284C7;">{kpi_data['total_citations']:,}</div>
        <div class="kpi-subtext">Citations Sum</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">2025 Volume</div>
        <div class="kpi-value">{kpi_data['volume_2025']:,}</div>
        <div class="kpi-subtext">Previous Year</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Citations / Paper</div>
        <div class="kpi-value" style="color: #F59E0B;">{kpi_data['citations_per_paper']}</div>
        <div class="kpi-subtext">CPP Impact</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Active Authors</div>
        <div class="kpi-value">{kpi_data['active_authors_count']:,}</div>
        <div class="kpi-subtext">Contributors</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Q1 Publications</div>
        <div class="kpi-value" style="color: #10B981;">{kpi_data['q1_count']:,}</div>
        <div class="kpi-subtext">{kpi_data['q1_percentage']}% of Total</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Intl. Collab</div>
        <div class="kpi-value">{kpi_data['international_collab_pct']}%</div>
        <div class="kpi-subtext">Global Share</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Industry Collab</div>
        <div class="kpi-value">{kpi_data['industry_collab_pct']}%</div>
        <div class="kpi-subtext">R&D Share</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">30-Day Velocity</div>
        <div class="kpi-value" style="color: #38BDF8;">+{kpi_data['last_30_days_velocity']}</div>
        <div class="kpi-subtext">Recent Output</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Helper function for Plotly Theme adaptation
def get_plotly_layout(theme_mode="dark"):
    is_dark = theme_mode.lower() == "dark"
    paper_bg = "rgba(14, 23, 42, 0.5)" if is_dark else "#FFFFFF"
    plot_bg = "rgba(0, 0, 0, 0)"
    font_color = "#F8FAFC" if is_dark else "#0F172A"
    sub_font_color = "#94A3B8" if is_dark else "#475569"
    grid_color = "rgba(255, 255, 255, 0.14)" if is_dark else "rgba(15, 23, 42, 0.12)"
    zeroline_color = "rgba(56, 189, 248, 0.3)" if is_dark else "rgba(2, 132, 199, 0.3)"
    hover_bg = "#0E172A" if is_dark else "#FFFFFF"
    hover_border = "#38BDF8" if is_dark else "#0284C7"
    hover_text = "#F8FAFC" if is_dark else "#0F172A"
    land_color = "#1E293B" if is_dark else "#E2E8F0"
    ocean_color = "#0B1329" if is_dark else "#F1F5F9"

    return {
        "paper_bgcolor": paper_bg,
        "plot_bgcolor": plot_bg,
        "font": dict(family="Inter, sans-serif", color=font_color, size=12),
        "title": dict(font=dict(family="Outfit, sans-serif", color=font_color, size=16)),
        "xaxis": dict(
            gridcolor=grid_color,
            zerolinecolor=zeroline_color,
            tickfont=dict(color=font_color, family="Inter, sans-serif", size=11),
            title=dict(font=dict(color=font_color, family="Inter, sans-serif", size=12))
        ),
        "yaxis": dict(
            gridcolor=grid_color,
            zerolinecolor=zeroline_color,
            tickfont=dict(color=font_color, family="Inter, sans-serif", size=11),
            title=dict(font=dict(color=font_color, family="Inter, sans-serif", size=12))
        ),
        "legend": dict(
            font=dict(color=font_color, family="Inter, sans-serif", size=11),
            bgcolor="rgba(0,0,0,0)"
        ),
        "hoverlabel": dict(
            bgcolor=hover_bg,
            bordercolor=hover_border,
            font=dict(color=hover_text, family="Inter, sans-serif", size=12)
        ),
        "geo": dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor=grid_color,
            showland=True,
            landcolor=land_color,
            showocean=True,
            oceancolor=ocean_color,
            projection_type="natural earth",
            bgcolor=paper_bg
        ),
        "polar": dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=grid_color, tickfont=dict(color=font_color, size=10)),
            angularaxis=dict(gridcolor=grid_color, tickfont=dict(color=font_color, size=11, family="Inter, sans-serif")),
            bgcolor=paper_bg
        ),
        "coloraxis_colorbar": dict(
            tickfont=dict(color=font_color, family="Inter, sans-serif", size=11),
            title=dict(font=dict(color=font_color, family="Inter, sans-serif", size=12))
        ),
        "annotation_font": dict(color=font_color, family="Inter, sans-serif", size=11),
        "margin": dict(l=40, r=40, t=50, b=40)
    }

# Render Main Dashboard Tabs 1 to 7
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Trends & Output Velocity",
    "🎯 Research Impact & Landmark Papers",
    "🌐 Global & Industry Collaboration",
    "🏆 Quality Benchmarks & Quadrants",
    "👥 Faculty & Author Profiles",
    "📡 Live Feed & Data Export",
    "🤖 AI Research Copilot"
])

# -----------------------------------------------------------------------------
# TAB 1: 📈 TRENDS & OUTPUT VELOCITY
# -----------------------------------------------------------------------------
with tab1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📈 Annual Publication Growth & Cumulative Output")
    
    annual_df = get_publications_by_year(df_filtered)
    if not annual_df.empty:
        annual_df['cumulative_output'] = annual_df['publication_count'].cumsum()

        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

        # Primary Bar Chart - Annual Output
        fig_dual.add_trace(
            go.Bar(
                x=annual_df['year'],
                y=annual_df['publication_count'],
                name="Annual Publications",
                marker=dict(color="#0284C7", cornerradius=4),
                hovertemplate="<b>Year %{x}</b><br>Publications: %{y}<extra></extra>"
            ),
            secondary_y=False
        )

        # Secondary Line Chart - Cumulative Output
        fig_dual.add_trace(
            go.Scatter(
                x=annual_df['year'],
                y=annual_df['cumulative_output'],
                name="Cumulative Total",
                mode="lines+markers",
                line=dict(color="#F59E0B", width=3, shape="spline"),
                marker=dict(size=7, color="#F59E0B"),
                hovertemplate="<b>Year %{x}</b><br>Cumulative: %{y:,}<extra></extra>"
            ),
            secondary_y=True
        )

        layout_opts = get_plotly_layout(theme)
        fig_dual.update_layout(
            paper_bgcolor=layout_opts["paper_bgcolor"],
            plot_bgcolor=layout_opts["plot_bgcolor"],
            font=layout_opts["font"],
            height=420,
            hovermode="x unified",
            hoverlabel=layout_opts["hoverlabel"],
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=layout_opts["legend"]["font"]),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        fig_dual.update_xaxes(title_text="Publication Year", gridcolor=layout_opts["xaxis"]["gridcolor"], tickfont=layout_opts["xaxis"]["tickfont"], title_font=layout_opts["xaxis"]["title"]["font"])
        fig_dual.update_yaxes(title_text="Annual Output (Papers)", secondary_y=False, gridcolor=layout_opts["yaxis"]["gridcolor"], tickfont=layout_opts["yaxis"]["tickfont"], title_font=layout_opts["yaxis"]["title"]["font"])
        fig_dual.update_yaxes(title_text="Cumulative Output", secondary_y=True, showgrid=False, tickfont=layout_opts["yaxis"]["tickfont"], title_font=layout_opts["yaxis"]["title"]["font"])

        st.plotly_chart(fig_dual, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Monthly Velocity Breakdown
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.subheader("⚡ Monthly Publication Velocity Breakdown")
    with c2:
        available_years = sorted(list(df_filtered['year'].unique()), reverse=True)
        selected_m_year = st.selectbox("Select Target Year", available_years, index=0)

    month_df = get_publications_by_month(df_filtered, selected_m_year)
    if not month_df.empty:
        bar_color = "#0284C7" if theme.lower() == "light" else "#38BDF8"
        fig_month = go.Figure()
        fig_month.add_trace(
            go.Bar(
                x=month_df['month'],
                y=month_df['publication_count'],
                name="Monthly Papers",
                marker=dict(color=bar_color, cornerradius=4),
                hovertemplate="<b>%{x}</b><br>Publications: %{y}<extra></extra>"
            )
        )
        layout_opts = get_plotly_layout(theme)
        fig_month.update_layout(
            paper_bgcolor=layout_opts["paper_bgcolor"],
            plot_bgcolor=layout_opts["plot_bgcolor"],
            font=layout_opts["font"],
            height=340,
            hoverlabel=layout_opts["hoverlabel"],
            xaxis=dict(title="Month", gridcolor=layout_opts["xaxis"]["gridcolor"], tickfont=layout_opts["xaxis"]["tickfont"], title_font=layout_opts["xaxis"]["title"]["font"]),
            yaxis=dict(title="Indexed Publications", gridcolor=layout_opts["yaxis"]["gridcolor"], tickfont=layout_opts["yaxis"]["tickfont"], title_font=layout_opts["yaxis"]["title"]["font"]),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig_month, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 2: 🎯 RESEARCH IMPACT & LANDMARK PAPERS
# -----------------------------------------------------------------------------
with tab2:
    col_acc, col_dept = st.columns([1, 1])

    with col_acc:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📈 Annual Citation Accrual Curve")
        annual_df = get_publications_by_year(df_filtered)
        if not annual_df.empty:
            fig_acc = go.Figure()
            fig_acc.add_trace(
                go.Scatter(
                    x=annual_df['year'],
                    y=annual_df['total_citations'],
                    fill='tozeroy',
                    mode='lines+markers',
                    name='Annual Citations',
                    line=dict(color='#0284C7', width=3, shape='spline'),
                    fillcolor='rgba(2, 132, 199, 0.2)'
                )
            )
            layout_opts = get_plotly_layout(theme)
            fig_acc.update_layout(
                paper_bgcolor=layout_opts["paper_bgcolor"],
                plot_bgcolor=layout_opts["plot_bgcolor"],
                font=layout_opts["font"],
                height=360,
                hoverlabel=layout_opts["hoverlabel"],
                xaxis=dict(title="Year", gridcolor=layout_opts["xaxis"]["gridcolor"], tickfont=layout_opts["xaxis"]["tickfont"], title_font=layout_opts["xaxis"]["title"]["font"]),
                yaxis=dict(title="Citations Accrued", gridcolor=layout_opts["yaxis"]["gridcolor"], tickfont=layout_opts["yaxis"]["tickfont"], title_font=layout_opts["yaxis"]["title"]["font"]),
                margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig_acc, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_dept:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🏢 Department Citation Impact")
        dept_cites = df_filtered.groupby('department')['citations'].sum().reset_index()
        dept_cites = dept_cites.sort_values('citations', ascending=True).tail(10)
        
        fig_dept_bar = go.Figure()
        fig_dept_bar.add_trace(
            go.Bar(
                x=dept_cites['citations'],
                y=dept_cites['department'],
                orientation='h',
                marker=dict(color='#F59E0B', cornerradius=4),
                hovertemplate="<b>%{y}</b><br>Citations: %{x:,}<extra></extra>"
            )
        )
        layout_opts = get_plotly_layout(theme)
        fig_dept_bar.update_layout(
            paper_bgcolor=layout_opts["paper_bgcolor"],
            plot_bgcolor=layout_opts["plot_bgcolor"],
            font=layout_opts["font"],
            height=360,
            hoverlabel=layout_opts["hoverlabel"],
            xaxis=dict(title="Total Citations", gridcolor=layout_opts["xaxis"]["gridcolor"], tickfont=layout_opts["xaxis"]["tickfont"], title_font=layout_opts["xaxis"]["title"]["font"]),
            yaxis=dict(gridcolor=layout_opts["yaxis"]["gridcolor"], tickfont=layout_opts["yaxis"]["tickfont"]),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig_dept_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Landmark Papers Table with Live DOI Links
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("⭐ High-Impact Landmark Research Papers")

    top_cited = df_filtered.sort_values('citations', ascending=False).head(20).copy()

    if not top_cited.empty:
        top_cited['DOI Link'] = top_cited['doi'].apply(
            lambda d: f"https://doi.org/{d}" if d else "#"
        )
        
        display_df = top_cited[['title', 'primary_author', 'department', 'journal', 'year', 'citations', 'quartile', 'DOI Link']].copy()
        display_df.columns = ['Title', 'Primary Author', 'Department', 'Journal', 'Year', 'Citations', 'Quartile', 'DOI Link']

        st.dataframe(
            display_df,
            column_config={
                "DOI Link": st.column_config.LinkColumn("DOI Link", display_text="↗ View"),
                "Citations": st.column_config.NumberColumn("Citations", format="%d 📈"),
                "Year": st.column_config.NumberColumn("Year", format="%d")
            },
            use_container_width=True,
            hide_index=True
        )

        bib_text = export_to_bibtex(top_cited)
        st.download_button(
            label="📥 Export Top Papers to BibTeX",
            data=bib_text,
            file_name="BAMU_Landmark_Publications.bib",
            mime="text/plain"
        )

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 3: 🌐 GLOBAL & INDUSTRY COLLABORATION
# -----------------------------------------------------------------------------
with tab3:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🌍 International Research Collaboration Map")

    country_counts = {}
    for country_list in df_filtered['countries'].dropna():
        if isinstance(country_list, list):
            for c in country_list:
                c_clean = str(c).strip()
                if c_clean and c_clean.lower() != 'india':
                    country_counts[c_clean] = country_counts.get(c_clean, 0) + 1

    country_df = pd.DataFrame(list(country_counts.items()), columns=['Country', 'Publications']).sort_values('Publications', ascending=False)

    if not country_df.empty:
        fig_map = px.choropleth(
            country_df,
            locations="Country",
            locationmode="country names",
            color="Publications",
            hover_name="Country",
            color_continuous_scale="Tealgrn",
            labels={"Publications": "Co-Authored Papers"}
        )
        layout_opts = get_plotly_layout(theme)
        fig_map.update_layout(
            paper_bgcolor=layout_opts["paper_bgcolor"],
            plot_bgcolor=layout_opts["plot_bgcolor"],
            font=layout_opts["font"],
            hoverlabel=layout_opts["hoverlabel"],
            coloraxis_colorbar=layout_opts["coloraxis_colorbar"],
            geo=layout_opts["geo"],
            height=440,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No international collaboration records found in filtered dataset.")
    st.markdown("</div>", unsafe_allow_html=True)

    col_treemap, col_ind = st.columns([1, 1])

    with col_treemap:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🏢 Department & Journal Publication Hierarchy")
        if not df_filtered.empty:
            fig_tree = px.treemap(
                df_filtered,
                path=['department', 'journal'],
                values='citations',
                color='citations',
                color_continuous_scale='Blues'
            )
            layout_opts = get_plotly_layout(theme)
            fig_tree.update_layout(
                paper_bgcolor=layout_opts["paper_bgcolor"],
                font=layout_opts["font"],
                hoverlabel=layout_opts["hoverlabel"],
                height=380,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_tree, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ind:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🏭 Industry R&D Collaboration Share")
        ind_collab_count = int(df_filtered['is_industry_collab'].sum())
        non_ind_count = len(df_filtered) - ind_collab_count

        fig_ind = go.Figure(
            data=[go.Pie(
                labels=['Industry R&D Collaboration', 'Academic / Institutional'],
                values=[ind_collab_count, non_ind_count],
                hole=0.6,
                marker=dict(colors=['#F59E0B', '#0284C7'])
            )]
        )
        layout_opts = get_plotly_layout(theme)
        fig_ind.update_layout(
            paper_bgcolor=layout_opts["paper_bgcolor"],
            font=layout_opts["font"],
            hoverlabel=layout_opts["hoverlabel"],
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5, font=layout_opts["legend"]["font"])
        )
        st.plotly_chart(fig_ind, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 4: 🏆 QUALITY BENCHMARKS & QUADRANTS
# -----------------------------------------------------------------------------
with tab4:
    col_donut, col_quad = st.columns([1, 2])

    with col_donut:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("⭐ Quartile Share")
        q_counts = df_filtered['quartile'].value_counts().reindex(['Q1', 'Q2', 'Q3', 'Q4']).fillna(0)

        fig_q = go.Figure(
            data=[go.Pie(
                labels=q_counts.index,
                values=q_counts.values,
                hole=0.6,
                marker=dict(colors=['#10B981', '#3B82F6', '#F59E0B', '#EF4444']),
                textinfo='label+percent',
                hoverinfo='label+value+percent'
            )]
        )
        layout_opts = get_plotly_layout(theme)
        fig_q.update_layout(
            paper_bgcolor=layout_opts["paper_bgcolor"],
            font=layout_opts["font"],
            hoverlabel=layout_opts["hoverlabel"],
            height=380,
            margin=dict(l=10, r=10, t=30, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=layout_opts["legend"]["font"])
        )
        st.plotly_chart(fig_q, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_quad:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🎯 Impact vs. Volume Quadrant Bubble Chart")

        dept_summary = df_filtered.groupby('department').agg(
            volume=('scopus_id', 'count'),
            total_citations=('citations', 'sum'),
            avg_cpp=('citations', 'mean'),
            q1_papers=('quartile', lambda x: (x == 'Q1').sum())
        ).reset_index()

        dept_summary['avg_cpp'] = dept_summary['avg_cpp'].round(2)
        overall_avg_cpp = round(df_filtered['citations'].mean(), 2) if not df_filtered.empty else 0.0

        if not dept_summary.empty:
            fig_bubble = px.scatter(
                dept_summary,
                x='volume',
                y='avg_cpp',
                size='total_citations',
                color='department',
                hover_name='department',
                size_max=45,
                labels={
                    'volume': 'Publication Volume (Papers)',
                    'avg_cpp': 'Average CPP (Citations / Paper)',
                    'total_citations': 'Total Citations'
                }
            )

            layout_opts = get_plotly_layout(theme)
            fig_bubble.add_hline(
                y=overall_avg_cpp,
                line_dash="dash",
                line_color="#F59E0B",
                annotation_text=f"Univ Avg CPP ({overall_avg_cpp})",
                annotation_position="bottom right",
                annotation_font=layout_opts["annotation_font"]
            )

            fig_bubble.update_layout(
                paper_bgcolor=layout_opts["paper_bgcolor"],
                plot_bgcolor=layout_opts["plot_bgcolor"],
                font=layout_opts["font"],
                hoverlabel=layout_opts["hoverlabel"],
                height=380,
                margin=dict(l=40, r=40, t=40, b=40),
                showlegend=False
            )
            fig_bubble.update_xaxes(gridcolor=layout_opts["xaxis"]["gridcolor"], tickfont=layout_opts["xaxis"]["tickfont"], title_font=layout_opts["xaxis"]["title"]["font"])
            fig_bubble.update_yaxes(gridcolor=layout_opts["yaxis"]["gridcolor"], tickfont=layout_opts["yaxis"]["tickfont"], title_font=layout_opts["yaxis"]["title"]["font"])

            st.plotly_chart(fig_bubble, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Department Radar Benchmark Chart
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🕸️ Department Comparative Benchmark Radar Chart")

    top_depts = df_filtered['department'].value_counts().head(5).index.tolist()
    if top_depts:
        categories = ['Volume Share', 'Citation Share', 'Q1 Share', 'Intl Collab Share', 'Industry Collab Share']
        fig_radar = go.Figure()

        for d in top_depts:
            d_df = df_filtered[df_filtered['department'] == d]
            if d_df.empty:
                continue

            vol_pct = (len(d_df) / len(df_filtered)) * 100
            cite_pct = (d_df['citations'].sum() / max(1, df_filtered['citations'].sum())) * 100
            q1_pct = ((d_df['quartile'] == 'Q1').sum() / len(d_df)) * 100
            intl_pct = (d_df['is_international_collab'].sum() / len(d_df)) * 100
            ind_pct = (d_df['is_industry_collab'].sum() / len(d_df)) * 100

            r_vals = [vol_pct, cite_pct, q1_pct, intl_pct, ind_pct]
            r_vals.append(r_vals[0])

            fig_radar.add_trace(
                go.Scatterpolar(
                    r=r_vals,
                    theta=categories + [categories[0]],
                    fill='toself',
                    name=d.replace("Department of ", "")
                )
            )

        layout_opts = get_plotly_layout(theme)
        fig_radar.update_layout(
            paper_bgcolor=layout_opts["paper_bgcolor"],
            font=layout_opts["font"],
            hoverlabel=layout_opts["hoverlabel"],
            polar=layout_opts["polar"],
            height=440,
            margin=dict(l=40, r=40, t=40, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=layout_opts["legend"]["font"])
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 5: 👥 FACULTY & AUTHOR PROFILES
# -----------------------------------------------------------------------------
with tab5:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🏆 Top Faculty Leaderboard & Podium")

    leaderboard_df = get_top_authors_leaderboard(df_filtered, top_n=50)
    text_primary = "#F8FAFC" if theme.lower() == "dark" else "#0F172A"
    pod_stat_bg = "rgba(0, 0, 0, 0.25)" if theme.lower() == "dark" else "rgba(2, 132, 199, 0.08)"
    pod_r2_bg = "rgba(148, 163, 184, 0.12)" if theme.lower() == "dark" else "rgba(100, 116, 139, 0.08)"
    pod_r2_border = "#94A3B8" if theme.lower() == "dark" else "#64748B"

    if not leaderboard_df.empty:
        # Podium Cards for Top 3
        pod1, pod2, pod3 = st.columns(3)

        if len(leaderboard_df) >= 1:
            r1 = leaderboard_df.iloc[0]
            with pod1:
                st.markdown(f"""
                <div style="background: rgba(245, 158, 11, 0.12); border: 2px solid #F59E0B; border-radius: 16px; padding: 1.2rem; text-align: center; box-shadow: 0 8px 24px rgba(245, 158, 11, 0.2);">
                    <div style="font-size: 2.2rem; margin-bottom: 0.2rem;">🥇</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #F59E0B; text-transform: uppercase; letter-spacing: 0.08em;">RANK #1 PODIUM</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: {text_primary}; margin: 0.3rem 0;">{r1['author']}</div>
                    <div style="font-size: 0.82rem; color: #0284C7; font-weight: 600; margin-bottom: 0.8rem;">{r1['primary_department']}</div>
                    <div style="display: flex; justify-content: space-around; background: {pod_stat_bg}; padding: 0.6rem; border-radius: 10px;">
                        <div><span style="font-size: 0.75rem; opacity: 0.85;">Papers</span><br><b style="color: {text_primary};">{r1['paper_count']}</b></div>
                        <div><span style="font-size: 0.75rem; opacity: 0.85;">Citations</span><br><b style="color: #0284C7;">{r1['total_citations']:,}</b></div>
                        <div><span style="font-size: 0.75rem; opacity: 0.85;">h-Index</span><br><b style="color: #F59E0B;">h-{r1['h_index']}</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if len(leaderboard_df) >= 2:
            r2 = leaderboard_df.iloc[1]
            with pod2:
                st.markdown(f"""
                <div style="background: {pod_r2_bg}; border: 2px solid {pod_r2_border}; border-radius: 16px; padding: 1.2rem; text-align: center; box-shadow: 0 8px 24px rgba(148, 163, 184, 0.15);">
                    <div style="font-size: 2.2rem; margin-bottom: 0.2rem;">🥈</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: {pod_r2_border}; text-transform: uppercase; letter-spacing: 0.08em;">RANK #2 PODIUM</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: {text_primary}; margin: 0.3rem 0;">{r2['author']}</div>
                    <div style="font-size: 0.82rem; color: #0284C7; font-weight: 600; margin-bottom: 0.8rem;">{r2['primary_department']}</div>
                    <div style="display: flex; justify-content: space-around; background: {pod_stat_bg}; padding: 0.6rem; border-radius: 10px;">
                        <div><span style="font-size: 0.75rem; opacity: 0.85;">Papers</span><br><b style="color: {text_primary};">{r2['paper_count']}</b></div>
                        <div><span style="font-size: 0.75rem; opacity: 0.85;">Citations</span><br><b style="color: #0284C7;">{r2['total_citations']:,}</b></div>
                        <div><span style="font-size: 0.75rem; opacity: 0.85;">h-Index</span><br><b style="color: #F59E0B;">h-{r2['h_index']}</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if len(leaderboard_df) >= 3:
            r3 = leaderboard_df.iloc[2]
            with pod3:
                st.markdown(f"""
                <div style="background: rgba(217, 119, 6, 0.12); border: 2px solid #D97706; border-radius: 16px; padding: 1.2rem; text-align: center; box-shadow: 0 8px 24px rgba(217, 119, 6, 0.15);">
                    <div style="font-size: 2.2rem; margin-bottom: 0.2rem;">🥉</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #D97706; text-transform: uppercase; letter-spacing: 0.08em;">RANK #3 PODIUM</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: {text_primary}; margin: 0.3rem 0;">{r3['author']}</div>
                    <div style="font-size: 0.82rem; color: #0284C7; font-weight: 600; margin-bottom: 0.8rem;">{r3['primary_department']}</div>
                    <div style="display: flex; justify-content: space-around; background: {pod_stat_bg}; padding: 0.6rem; border-radius: 10px;">
                        <div><span style="font-size: 0.75rem; opacity: 0.85;">Papers</span><br><b style="color: {text_primary};">{r3['paper_count']}</b></div>
                        <div><span style="font-size: 0.75rem; opacity: 0.85;">Citations</span><br><b style="color: #0284C7;">{r3['total_citations']:,}</b></div>
                        <div><span style="font-size: 0.75rem; opacity: 0.85;">h-Index</span><br><b style="color: #F59E0B;">h-{r3['h_index']}</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📋 View Complete Faculty Leaderboard Table"):
            st.dataframe(
                leaderboard_df,
                column_config={
                    "author": "Faculty / Author Name",
                    "paper_count": st.column_config.NumberColumn("Publications", format="%d 📜"),
                    "total_citations": st.column_config.NumberColumn("Total Citations", format="%d 📈"),
                    "cpp": st.column_config.NumberColumn("CPP", format="%.2f"),
                    "h_index": st.column_config.NumberColumn("h-Index", format="h-%d 🏆"),
                    "primary_department": "Primary Department"
                },
                use_container_width=True,
                hide_index=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # Interactive Faculty Selector & Profile Deep Dive
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔍 Individual Faculty Scopus Dossier & Profile Deep Dive")

    if not leaderboard_df.empty:
        author_list = leaderboard_df['author'].tolist()
        selected_author = st.selectbox(
            "👤 Select Faculty Member / Author to Inspect",
            options=author_list,
            index=0
        )

        auth_profile = get_author_profile_metrics(df_filtered, selected_author)

        if auth_profile:
            # Header Card
            st.markdown(f"""
            <div style="background: rgba(2, 132, 199, 0.08); border: 1px solid rgba(2, 132, 199, 0.3); border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <h2 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.8rem; color: {text_primary};">{auth_profile['author_name']}</h2>
                        <div style="font-size: 0.95rem; font-weight: 600; color: #0284C7; margin-top: 0.2rem;">{auth_profile['primary_department']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 5 KPI Chips
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric("Publications", f"{auth_profile['total_papers']}")
            with c2:
                st.metric("Citations", f"{auth_profile['total_citations']:,}")
            with c3:
                st.metric("CPP Impact", f"{auth_profile['cpp']}")
            with c4:
                st.metric("h-Index", f"h-{auth_profile['h_index']}")
            with c5:
                st.metric("Q1 Ratio", f"{auth_profile['q1_percentage']}%", help=f"{auth_profile['q1_count']} Q1 Papers")

            st.markdown("<br>", unsafe_allow_html=True)

            # Badges & Co-authors
            co_list = ", ".join([a[0] for a in auth_profile['top_coauthors']]) or "None recorded"
            st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 0.8rem; margin-bottom: 1.5rem;">
                <span class="hero-badge">🌐 International Collaboration: <b>{auth_profile['international_collab_pct']}%</b></span>
                <span class="hero-badge">🏭 Industry Collaboration: <b>{auth_profile['industry_collab_pct']}%</b></span>
                <span class="hero-badge">🤝 Top Co-Authors: <b>{co_list}</b></span>
            </div>
            """, unsafe_allow_html=True)

            # Author Specific Publications DataFrame
            author_papers = df_filtered[df_filtered['authors'].apply(
                lambda authors: any(selected_author.lower() in str(a).lower() for a in (authors if isinstance(authors, list) else [authors]))
            )].copy()

            # Dual-Axis Trend & Quartile Donut for Author
            col_atrend, col_aquart = st.columns([1.5, 1])

            with col_atrend:
                st.markdown("#### 📈 Faculty Annual Output & Citations Trend")
                trend_data = auth_profile['yearly_trend']
                if not trend_data.empty:
                    fig_auth_trend = make_subplots(specs=[[{"secondary_y": True}]])
                    fig_auth_trend.add_trace(
                        go.Bar(x=trend_data['year'], y=trend_data['papers'], name="Papers", marker=dict(color="#0284C7")),
                        secondary_y=False
                    )
                    fig_auth_trend.add_trace(
                        go.Scatter(x=trend_data['year'], y=trend_data['citations'], name="Citations", mode="lines+markers", line=dict(color="#F59E0B", width=3)),
                        secondary_y=True
                    )
                    layout_opts = get_plotly_layout(theme)
                    fig_auth_trend.update_layout(
                        paper_bgcolor=layout_opts["paper_bgcolor"],
                        plot_bgcolor=layout_opts["plot_bgcolor"],
                        font=layout_opts["font"],
                        height=320,
                        margin=dict(l=30, r=30, t=30, b=30),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig_auth_trend, use_container_width=True)

            with col_aquart:
                st.markdown("#### ⭐ Journal Quality Profile")
                if not author_papers.empty:
                    q_counts = author_papers['quartile'].value_counts().reindex(['Q1', 'Q2', 'Q3', 'Q4']).fillna(0)
                    fig_auth_q = go.Figure(
                        data=[go.Pie(
                            labels=q_counts.index,
                            values=q_counts.values,
                            hole=0.5,
                            marker=dict(colors=['#10B981', '#3B82F6', '#F59E0B', '#EF4444'])
                        )]
                    )
                    layout_opts = get_plotly_layout(theme)
                    fig_auth_q.update_layout(
                        paper_bgcolor=layout_opts["paper_bgcolor"],
                        font=layout_opts["font"],
                        height=320,
                        margin=dict(l=10, r=10, t=30, b=10)
                    )
                    st.plotly_chart(fig_auth_q, use_container_width=True)

            # Top 5 Landmark Contributions
            st.markdown("#### 🌟 Top 5 Landmark Contributions")
            top_auth_pubs = auth_profile['top_publications'].copy()
            if not top_auth_pubs.empty:
                top_auth_pubs['DOI Link'] = top_auth_pubs['doi'].apply(lambda d: f"https://doi.org/{d}" if d else "#")
                st.dataframe(
                    top_auth_pubs[['title', 'journal', 'year', 'citations', 'quartile', 'DOI Link']],
                    column_config={
                        "DOI Link": st.column_config.LinkColumn("DOI Link", display_text="↗ View"),
                        "citations": st.column_config.NumberColumn("Citations", format="%d 📈")
                    },
                    use_container_width=True,
                    hide_index=True
                )

            # Full Papers Table for Selected Author
            st.markdown("#### 📚 Full Publication Record")
            if not author_papers.empty:
                author_papers_display = author_papers.copy()
                author_papers_display['DOI Link'] = author_papers_display['doi'].apply(lambda d: f"https://doi.org/{d}" if d else "#")
                st.dataframe(
                    author_papers_display[['title', 'journal', 'year', 'citations', 'quartile', 'DOI Link']],
                    column_config={
                        "DOI Link": st.column_config.LinkColumn("DOI Link", display_text="↗ View"),
                        "citations": st.column_config.NumberColumn("Citations", format="%d 📈")
                    },
                    use_container_width=True,
                    hide_index=True
                )

            st.markdown("<br>", unsafe_allow_html=True)
            # Targeted Print Capability
            print_btn = st.button("🖨️ Print Author Dossier / Save PDF", type="primary", use_container_width=False)
            if print_btn:
                print_html = generate_author_print_html(auth_profile, author_papers)
                b64_html = base64.b64encode(print_html.encode('utf-8')).decode('utf-8')
                
                js_print_code = f"""
                <script>
                (function() {{
                const b64 = "{b64_html}";
                const html = decodeURIComponent(escape(window.atob(b64)));
                const parentDoc = (window.parent && window.parent.document) ? window.parent.document : document;
                let frame = parentDoc.getElementById('author-print-isolated-frame');
                if (frame) frame.remove();
                frame = parentDoc.createElement('iframe');
                frame.id = 'author-print-isolated-frame';
                frame.style.position = 'fixed'; frame.style.right = '0'; frame.style.bottom = '0';
                frame.style.width = '0'; frame.style.height = '0'; frame.style.border = '0';
                parentDoc.body.appendChild(frame);
                const doc = frame.contentWindow.document;
                doc.open(); doc.write(html); doc.close();
                setTimeout(() => {{ frame.contentWindow.focus(); frame.contentWindow.print(); }}, 350);
                }})();
                </script>
                """
                components.html(js_print_code, height=0, width=0)
                st.success(f"Preparing official print dossier for {auth_profile['author_name']}...")

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 6: 📡 LIVE FEED & DATA EXPORT
# -----------------------------------------------------------------------------
with tab6:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📡 Live Scopus Indexed Feed & Multiformat Data Exporter")

    search_query = st.text_input(
        "🔎 Search Publications Feed",
        placeholder="Type keyword, title, author name, journal, department, or DOI..."
    )

    if search_query:
        sq = search_query.lower()
        df_feed = df_filtered[
            df_filtered['title'].str.lower().str.contains(sq, na=False) |
            df_filtered['primary_author'].str.lower().str.contains(sq, na=False) |
            df_filtered['department'].str.lower().str.contains(sq, na=False) |
            df_filtered['journal'].str.lower().str.contains(sq, na=False) |
            df_filtered['doi'].str.lower().str.contains(sq, na=False)
        ].copy()
    else:
        df_feed = df_filtered.copy()

    st.markdown(f"Displaying **{len(df_feed):,}** indexed publications matching current filters.")

    # Export Buttons Row
    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        # Excel Export
        excel_data = io.BytesIO()
        export_excel_df = df_feed[['scopus_id', 'title', 'primary_author', 'department', 'journal', 'year', 'citations', 'quartile', 'doi']].copy()
        export_excel_df.columns = ['Scopus ID', 'Title', 'Primary Author', 'Department', 'Journal', 'Year', 'Citations', 'Quartile', 'DOI']
        with pd.ExcelWriter(excel_data, engine='openpyxl') as writer:
            export_excel_df.to_excel(writer, index=False, sheet_name='BAMU Scopus Publications')
        
        st.download_button(
            label="📊 Export Excel (.xlsx)",
            data=excel_data.getvalue(),
            file_name="BAMU_Scopus_Publications.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with exp_col2:
        # BibTeX Export
        bib_data = export_to_bibtex(df_feed)
        st.download_button(
            label="📑 Export BibTeX (.bib)",
            data=bib_data,
            file_name="BAMU_Scopus_Publications.bib",
            mime="text/plain",
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Table
    if not df_feed.empty:
        df_feed_display = df_feed.copy()
        df_feed_display['DOI Link'] = df_feed_display['doi'].apply(lambda d: f"https://doi.org/{d}" if d else "#")

        st.dataframe(
            df_feed_display[['scopus_id', 'title', 'primary_author', 'department', 'journal', 'year', 'citations', 'quartile', 'DOI Link']],
            column_config={
                "scopus_id": "Scopus ID",
                "title": "Publication Title",
                "primary_author": "Primary Author",
                "department": "Department",
                "journal": "Journal",
                "year": st.column_config.NumberColumn("Year", format="%d"),
                "citations": st.column_config.NumberColumn("Citations", format="%d 📈"),
                "quartile": "Quartile",
                "DOI Link": st.column_config.LinkColumn("DOI Link", display_text="↗ View")
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No publications found matching search query.")

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 7: 🤖 AI RESEARCH COPILOT
# -----------------------------------------------------------------------------
with tab7:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🤖 BAMU Scopus AI Research Copilot")
    st.caption("Fast built-in Python/Pandas natural language research assistant. Zero external API keys required.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Hello! I am your **BAMU Scopus AI Research Copilot**. Select a prompt chip below or type any question to analyze BAMU's research output, top faculty, department rankings, or Q1 journal quality!"
            }
        ]

    # Action Bar: Prompt Chips & Clear History
    chip_col1, chip_col2, chip_col3, chip_col4, clear_col = st.columns([1, 1, 1, 1, 1])

    prompt_to_send = None

    with chip_col1:
        if st.button("📊 Executive Dossier", use_container_width=True):
            prompt_to_send = "Executive Dossier"
    with chip_col2:
        if st.button("🏛 Dept Rankings", use_container_width=True):
            prompt_to_send = "Dept Rankings"
    with chip_col3:
        if st.button("🏆 Q1 Quality Analysis", use_container_width=True):
            prompt_to_send = "Q1 Quality Analysis"
    with chip_col4:
        if st.button("👥 Top Authors", use_container_width=True):
            prompt_to_send = "Top Authors"
    with clear_col:
        if st.button("🗑 Clear Chat History", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "👋 Chat history cleared. Ask me any research question about BAMU!"
                }
            ]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input Box
    user_input = st.chat_input("Ask BAMU AI Copilot (e.g. 'Show department rankings', 'Top Q1 papers')...")

    if user_input:
        prompt_to_send = user_input

    if prompt_to_send:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt_to_send})
        with st.chat_message("user"):
            st.markdown(prompt_to_send)

        # Generate response using AI Copilot Pandas engine
        with st.spinner("AI Copilot analyzing research dataset..."):
            response_md = query_ai_copilot(df_filtered, prompt_to_send)

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response_md})
        with st.chat_message("assistant"):
            st.markdown(response_md)

    st.markdown("</div>", unsafe_allow_html=True)
