import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    export_to_bibtex
)
from styles import get_custom_css, render_icare_topbar, render_icare_hero

# Page Configuration
st.set_page_config(
    page_title=UNIVERSITY_CONFIG['app_title'],
    page_icon="🏛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Controls
st.sidebar.markdown("### ⚙️ Dashboard Controls")

theme = st.sidebar.radio(
    "🎨 Theme Mode",
    ["Dark", "Light"],
    index=0,
    horizontal=True
)

# Apply CSS Theme
st.markdown(get_custom_css(theme), unsafe_allow_html=True)

data_mode = st.sidebar.radio(
    "📡 Data Engine Mode",
    ["Live Scopus API (Auto-Sync)", "Benchmark Offline Demo (~2,500 Papers)"],
    index=0
)

# Force Refresh Button
force_refresh = st.sidebar.button("🔄 Force Scopus API Sync", use_container_width=True)

# Load Data based on selection
@st.cache_data(ttl=1800, show_spinner=False)
def load_dashboard_data(mode_name, refresh_flag):
    if "Live" in mode_name:
        pubs = get_scopus_publications(force_refresh=refresh_flag)
    else:
        pubs = load_or_generate_mock_data()
    return pd.DataFrame(pubs)


with st.spinner("Syncing Scopus Intelligence Engine..."):
    df_raw = load_dashboard_data(data_mode, force_refresh)

if df_raw.empty:
    st.error("No publication data available. Please check Scopus API key or connection.")
    st.stop()

# Sidebar Filters
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filter Intelligence")

# Year Range Filter
min_year = int(df_raw['year'].min())
max_year = int(df_raw['year'].max())
selected_year_range = st.sidebar.slider(
    "📅 Publication Years",
    min_value=min_year,
    max_value=max_year,
    value=(2015, max_year)
)

# Department Filter
available_depts = ["All Departments"] + sorted(list(df_raw['department'].dropna().unique()))
selected_depts = st.sidebar.multiselect(
    "🏢 Academic Department",
    options=available_depts,
    default=["All Departments"]
)

# Quartile Filter
available_quartiles = ["All Quartiles", "Q1", "Q2", "Q3", "Q4"]
selected_quartiles = st.sidebar.multiselect(
    "⭐ Journal Quartile",
    options=available_quartiles,
    default=["All Quartiles"]
)

# Collaboration Type Filter
available_collabs = ["All Types", "International Collaboration", "Industry Collaboration", "Institutional / National"]
selected_collabs = st.sidebar.multiselect(
    "🤝 Collaboration Scope",
    options=available_collabs,
    default=["All Types"]
)

# Apply Filters
df_filtered = filter_publications(
    df_raw,
    year_range=selected_year_range,
    depts=selected_depts,
    quartiles=selected_quartiles,
    collab_types=selected_collabs
)

# Render Executive Header & Hero Banner
render_icare_topbar(theme)
kpi_data = calculate_top_10_kpis(df_filtered)
render_icare_hero(kpi_data["total_output"], kpi_data["total_citations"], theme)

# KPI Cards Row (10 Executive Metrics)
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
    paper_bg = "rgba(14, 23, 42, 0.4)" if is_dark else "#FFFFFF"
    plot_bg = "rgba(0, 0, 0, 0)"
    font_color = "#F8FAFC" if is_dark else "#0F172A"
    grid_color = "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(15, 23, 42, 0.08)"

    return {
        "paper_bgcolor": paper_bg,
        "plot_bgcolor": plot_bg,
        "font": dict(family="Inter, sans-serif", color=font_color),
        "xaxis": dict(gridcolor=grid_color, zerolinecolor=grid_color),
        "yaxis": dict(gridcolor=grid_color, zerolinecolor=grid_color),
        "margin": dict(l=40, r=40, t=50, b=40)
    }

# Render Main Dashboard Tabs 1 to 4
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Trends & Output Velocity",
    "🎯 Research Impact & Landmark Papers",
    "🌐 Global & Industry Collaboration",
    "🏆 Quality Benchmarks & Quadrants"
])

# -----------------------------------------------------------------------------
# TAB 1: 📈 TRENDS
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
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        fig_dual.update_xaxes(title_text="Publication Year", gridcolor=layout_opts["xaxis"]["gridcolor"])
        fig_dual.update_yaxes(title_text="Annual Output (Papers)", secondary_y=False, gridcolor=layout_opts["yaxis"]["gridcolor"])
        fig_dual.update_yaxes(title_text="Cumulative Output", secondary_y=True, showgrid=False)

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
        fig_month = go.Figure()
        fig_month.add_trace(
            go.Bar(
                x=month_df['month'],
                y=month_df['publication_count'],
                name="Monthly Papers",
                marker=dict(color="#38BDF8", cornerradius=4),
                hovertemplate="<b>%{x}</b><br>Publications: %{y}<extra></extra>"
            )
        )
        layout_opts = get_plotly_layout(theme)
        fig_month.update_layout(
            paper_bgcolor=layout_opts["paper_bgcolor"],
            plot_bgcolor=layout_opts["plot_bgcolor"],
            font=layout_opts["font"],
            height=340,
            xaxis=dict(title="Month", gridcolor=layout_opts["xaxis"]["gridcolor"]),
            yaxis=dict(title="Indexed Publications", gridcolor=layout_opts["yaxis"]["gridcolor"]),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig_month, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 2: 🎯 IMPACT & LANDMARK PAPERS
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
                xaxis=dict(title="Year", gridcolor=layout_opts["xaxis"]["gridcolor"]),
                yaxis=dict(title="Citations Accrued", gridcolor=layout_opts["yaxis"]["gridcolor"]),
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
            xaxis=dict(title="Total Citations", gridcolor=layout_opts["xaxis"]["gridcolor"]),
            yaxis=dict(gridcolor=layout_opts["yaxis"]["gridcolor"]),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig_dept_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Landmark Papers Table with Live DOI Links
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("⭐ High-Impact Landmark Research Papers")

    top_cited = df_filtered.sort_values('citations', ascending=False).head(20).copy()

    if not top_cited.empty:
        # Create clickable DOI link
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

        # BibTeX Export Button
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
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth',
                bgcolor=layout_opts["paper_bgcolor"]
            ),
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
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_ind, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 4: 🏆 QUALITY & BENCHMARKS
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
            height=380,
            margin=dict(l=10, r=10, t=30, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
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

            # Benchmark Line: Average CPP across university
            fig_bubble.add_hline(
                y=overall_avg_cpp,
                line_dash="dash",
                line_color="#F59E0B",
                annotation_text=f"Univ Avg CPP ({overall_avg_cpp})",
                annotation_position="bottom right"
            )

            layout_opts = get_plotly_layout(theme)
            fig_bubble.update_layout(
                paper_bgcolor=layout_opts["paper_bgcolor"],
                plot_bgcolor=layout_opts["plot_bgcolor"],
                font=layout_opts["font"],
                height=380,
                margin=dict(l=40, r=40, t=40, b=40),
                showlegend=False
            )
            fig_bubble.update_xaxes(gridcolor=layout_opts["xaxis"]["gridcolor"])
            fig_bubble.update_yaxes(gridcolor=layout_opts["yaxis"]["gridcolor"])

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
            r_vals.append(r_vals[0])  # Close radar loop

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
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor=layout_opts["xaxis"]["gridcolor"]),
                angularaxis=dict(gridcolor=layout_opts["xaxis"]["gridcolor"]),
                bgcolor=layout_opts["paper_bgcolor"]
            ),
            height=440,
            margin=dict(l=40, r=40, t=40, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
