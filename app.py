"""
Youth Unemployment Explorer — ACC102 Track 4
An interactive Streamlit app for exploring global youth unemployment trends.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Youth Unemployment Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    [data-testid="stSidebar"] * { color: #e0f2f1 !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stMultiSelect label { color: #80cbc4 !important; font-weight: 600; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #f0f7ff;
        border: 1px solid #cce0ff;
        border-radius: 12px;
        padding: 16px;
    }
    [data-testid="metric-container"] label { color: #1a4a7a !important; font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #0d47a1 !important; font-size: 2rem !important; font-weight: 700; }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 0.85rem; }

    /* Page header */
    .app-header {
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 40%, #0288d1 100%);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 28px;
        color: white;
    }
    .app-header h1 { margin: 0; font-size: 2rem; font-weight: 700; color: white; letter-spacing: -0.02em; }
    .app-header p  { margin: 6px 0 0; font-size: 1rem; color: #bbdefb; }

    /* Section headings */
    .section-title {
        font-size: 1.05rem; font-weight: 700; color: #0d47a1;
        border-left: 4px solid #0288d1; padding-left: 10px;
        margin: 8px 0 16px;
    }

    /* Insight box */
    .insight-box {
        background: #e3f2fd; border-left: 4px solid #1976d2;
        border-radius: 0 10px 10px 0; padding: 14px 18px; margin: 12px 0;
        font-size: 0.93rem; color: #0d47a1;
    }

    /* Warning box */
    .warn-box {
        background: #fff3e0; border-left: 4px solid #f57c00;
        border-radius: 0 10px 10px 0; padding: 12px 16px; margin: 8px 0;
        font-size: 0.88rem; color: #5d3a00;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0 !important;
        background: #e3f2fd !important;
        color: #1565c0 !important;
        font-weight: 600;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] { background: #1565c0 !important; color: white !important; }

    /* Footer */
    .footer { text-align:center; color:#90a4ae; font-size:0.78rem; margin-top:40px; padding-top:16px; border-top:1px solid #eceff1; }
</style>
""", unsafe_allow_html=True)

# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    youth_raw = pd.read_csv("youth_unemployment_global.csv")
    gdp_raw   = pd.read_csv("Employment_Unemployment_GDP_data.csv")

    youth = youth_raw.dropna(subset=["YouthUnemployment"])
    youth = youth[youth["Year"].between(1991, 2022)]

    df = youth.merge(
        gdp_raw,
        left_on=["Country", "Year"],
        right_on=["Country Name", "Year"],
        how="inner"
    )

    df["GDP_bn"]    = df["GDP (in USD)"] / 1e9
    df["GDP_log"]   = np.log10(df["GDP (in USD)"])
    df["Youth_Gap"] = df["YouthUnemployment"] - df["Unemployment Rate"]

    df["Dom_Sector"] = (
        df[["Employment Sector: Agriculture",
            "Employment Sector: Industry",
            "Employment Sector: Services"]]
        .idxmax(axis=1)
        .str.replace("Employment Sector: ", "", regex=False)
    )

    region_map = {
        "Afghanistan":"South Asia","Bangladesh":"South Asia","India":"South Asia",
        "Nepal":"South Asia","Pakistan":"South Asia","Sri Lanka":"South Asia",
        "Albania":"Eastern Europe","Armenia":"Eastern Europe","Azerbaijan":"Eastern Europe",
        "Belarus":"Eastern Europe","Bosnia and Herzegovina":"Eastern Europe",
        "Bulgaria":"Eastern Europe","Croatia":"Eastern Europe","Czech Republic":"Eastern Europe",
        "Estonia":"Eastern Europe","Georgia":"Eastern Europe","Hungary":"Eastern Europe",
        "Kazakhstan":"Eastern Europe","Kosovo":"Eastern Europe","Latvia":"Eastern Europe",
        "Lithuania":"Eastern Europe","Moldova":"Eastern Europe","Montenegro":"Eastern Europe",
        "North Macedonia":"Eastern Europe","Poland":"Eastern Europe","Romania":"Eastern Europe",
        "Russia":"Eastern Europe","Serbia":"Eastern Europe","Slovak Republic":"Eastern Europe",
        "Slovenia":"Eastern Europe","Tajikistan":"Eastern Europe","Turkey":"Eastern Europe",
        "Turkmenistan":"Eastern Europe","Ukraine":"Eastern Europe","Uzbekistan":"Eastern Europe",
        "Australia":"Asia-Pacific","China":"Asia-Pacific","Indonesia":"Asia-Pacific",
        "Japan":"Asia-Pacific","Korea, Rep.":"Asia-Pacific","Malaysia":"Asia-Pacific",
        "Myanmar":"Asia-Pacific","New Zealand":"Asia-Pacific","Philippines":"Asia-Pacific",
        "Thailand":"Asia-Pacific","Vietnam":"Asia-Pacific","Cambodia":"Asia-Pacific",
        "Austria":"Western Europe","Belgium":"Western Europe","Denmark":"Western Europe",
        "Finland":"Western Europe","France":"Western Europe","Germany":"Western Europe",
        "Greece":"Western Europe","Iceland":"Western Europe","Ireland":"Western Europe",
        "Italy":"Western Europe","Luxembourg":"Western Europe","Netherlands":"Western Europe",
        "Norway":"Western Europe","Portugal":"Western Europe","Spain":"Western Europe",
        "Sweden":"Western Europe","Switzerland":"Western Europe","United Kingdom":"Western Europe",
        "Algeria":"Middle East & Africa","Angola":"Middle East & Africa",
        "Bahrain":"Middle East & Africa","Egypt, Arab Rep.":"Middle East & Africa",
        "Ethiopia":"Middle East & Africa","Ghana":"Middle East & Africa",
        "Iran, Islamic Rep.":"Middle East & Africa","Iraq":"Middle East & Africa",
        "Jordan":"Middle East & Africa","Kenya":"Middle East & Africa",
        "Kuwait":"Middle East & Africa","Lebanon":"Middle East & Africa",
        "Morocco":"Middle East & Africa","Nigeria":"Middle East & Africa",
        "Saudi Arabia":"Middle East & Africa","South Africa":"Middle East & Africa",
        "Tunisia":"Middle East & Africa","United Arab Emirates":"Middle East & Africa",
        "Yemen, Rep.":"Middle East & Africa",
        "Argentina":"Latin America","Bolivia":"Latin America","Brazil":"Latin America",
        "Chile":"Latin America","Colombia":"Latin America","Costa Rica":"Latin America",
        "Ecuador":"Latin America","Mexico":"Latin America","Peru":"Latin America",
        "Uruguay":"Latin America","Venezuela, RB":"Latin America",
        "Canada":"North America","United States":"North America",
    }
    df["Region"] = df["Country"].map(region_map).fillna("Other")
    df = df.sort_values(["Country","Year"]).reset_index(drop=True)
    return df

REGION_COLOURS = {
    "Western Europe":       "#1565c0",
    "Eastern Europe":       "#2e7d32",
    "Latin America":        "#c62828",
    "Asia-Pacific":         "#e65100",
    "Middle East & Africa": "#6a1b9a",
    "South Asia":           "#4e342e",
    "North America":        "#00838f",
    "Other":                "#9e9e9e",
}

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "#f5f9ff",
    "axes.grid": True, "grid.color": "white", "grid.linewidth": 1.2,
    "font.family": "DejaVu Sans",
    "axes.spines.top": False, "axes.spines.right": False,
})

# ── Load ──────────────────────────────────────────────────────────────────────
with st.spinner("Loading data…"):
    df = load_data()

countries_all = sorted(df["Country"].unique().tolist())
regions_all   = [r for r in REGION_COLOURS if r != "Other"]
year_min, year_max = int(df["Year"].min()), int(df["Year"].max())

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Global Filters")
    st.markdown("---")

    year_range = st.slider(
        "Year range",
        min_value=year_min, max_value=year_max,
        value=(1995, 2022), step=1
    )
    selected_regions = st.multiselect(
        "Regions",
        options=regions_all,
        default=regions_all[:5]
    )
    st.markdown("---")
    st.markdown("### 🔍 Country Deep-Dive")
    country_a = st.selectbox("Country A", countries_all,
                              index=countries_all.index("South Africa") if "South Africa" in countries_all else 0)
    country_b = st.selectbox("Country B", countries_all,
                              index=countries_all.index("Germany") if "Germany" in countries_all else 1)
    st.markdown("---")
    st.markdown(
        "<small style='color:#80cbc4'>Data: World Bank / ILO via Kaggle · 1991–2022<br>"
        "ACC102 · Track 4 · XJTLU IBSS</small>",
        unsafe_allow_html=True
    )

# ── Filter data ───────────────────────────────────────────────────────────────
mask = (
    df["Year"].between(year_range[0], year_range[1]) &
    df["Region"].isin(selected_regions + ["Other"])
)
dff = df[mask].copy()
latest_year = min(2022, year_range[1])
latest = dff[dff["Year"] == latest_year]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <h1>📊 Youth Unemployment Explorer</h1>
  <p>An interactive analysis of global youth unemployment trends, regional disparities, and economic correlates · 1991–2022</p>
</div>
""", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
global_avg_latest = df[df["Year"] == latest_year]["YouthUnemployment"].mean()
global_avg_prev   = df[df["Year"] == latest_year - 1]["YouthUnemployment"].mean()
worst_country     = latest.loc[latest["YouthUnemployment"].idxmax(), "Country"] if not latest.empty else "N/A"
worst_rate        = latest["YouthUnemployment"].max() if not latest.empty else 0
best_country      = latest.loc[latest["YouthUnemployment"].idxmin(), "Country"] if not latest.empty else "N/A"
best_rate         = latest["YouthUnemployment"].min() if not latest.empty else 0
avg_gap           = dff["Youth_Gap"].mean()

col1.metric(f"Global Avg Youth Unemp. ({latest_year})", f"{global_avg_latest:.1f}%",
            delta=f"{global_avg_latest - global_avg_prev:+.1f}pp vs prev yr",
            delta_color="inverse")
col2.metric("Highest in dataset", f"{worst_rate:.1f}%", worst_country, delta_color="off")
col3.metric("Lowest in dataset",  f"{best_rate:.1f}%",  best_country,  delta_color="off")
col4.metric("Avg Youth–Adult Gap", f"{avg_gap:.1f}pp", "youth rate above total")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Global Trend",
    "📦 Regional Breakdown",
    "🔍 Country Comparison",
    "📈 GDP & Structure"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GLOBAL TREND
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Global Average Youth vs Total Unemployment Over Time</div>', unsafe_allow_html=True)

    trend = (dff.groupby("Year")["YouthUnemployment"].mean().reset_index()
               .rename(columns={"YouthUnemployment": "AvgYouth"}))
    trend_tot = (dff.groupby("Year")["Unemployment Rate"].mean().reset_index()
                   .rename(columns={"Unemployment Rate": "AvgAll"}))
    trend = trend.merge(trend_tot, on="Year")

    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.fill_between(trend["Year"], trend["AvgYouth"], alpha=0.12, color="#1565c0")
    ax.plot(trend["Year"], trend["AvgYouth"], color="#1565c0", lw=2.5,
            marker="o", ms=4, label="Youth unemployment (avg)")
    ax.plot(trend["Year"], trend["AvgAll"],  color="#e53935", lw=2,
            ls="--", marker="s", ms=3, label="Total unemployment (avg)")
    if year_range[0] <= 2009 <= year_range[1]:
        ax.axvspan(2008, 2010, alpha=0.12, color="grey", label="Global financial crisis")
    if year_range[0] <= 2021 <= year_range[1]:
        ax.axvspan(2019.5, 2021, alpha=0.12, color="orange", label="COVID-19")
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Unemployment Rate (%)", fontsize=10)
    ax.set_title(f"Global Average Youth vs Total Unemployment ({year_range[0]}–{year_range[1]})",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    if not trend.empty:
        peak_row = trend.loc[trend["AvgYouth"].idxmax()]
        st.markdown(f"""
        <div class="insight-box">
        💡 <b>Insight:</b> Youth unemployment peaked at <b>{peak_row['AvgYouth']:.1f}%</b> in <b>{int(peak_row['Year'])}</b>
        within your selected date range. The youth rate consistently runs about
        <b>{(trend['AvgYouth'] - trend['AvgAll']).mean():.1f} percentage points</b> above the total rate —
        a gap that has persisted through booms and crises alike.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📋 Show underlying data table"):
        st.dataframe(trend.rename(columns={"AvgYouth":"Avg Youth Unemp (%)","AvgAll":"Avg Total Unemp (%)"})
                        .set_index("Year").round(2), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — REGIONAL BREAKDOWN
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown('<div class="section-title">Regional Distribution in Latest Year</div>', unsafe_allow_html=True)
        latest_filt = latest[latest["Region"].isin(selected_regions)]
        if latest_filt.empty:
            st.warning("No data for selected regions / year. Adjust the sidebar filters.")
        else:
            region_order = (latest_filt.groupby("Region")["YouthUnemployment"]
                            .median().sort_values(ascending=False).index.tolist())
            fig2, ax2 = plt.subplots(figsize=(7, 4.5))
            sns.boxplot(data=latest_filt, y="Region", x="YouthUnemployment",
                        order=region_order, palette=REGION_COLOURS,
                        width=0.5, linewidth=1.2, ax=ax2)
            ax2.set_xlabel("Youth Unemployment Rate (%)", fontsize=10)
            ax2.set_ylabel("")
            ax2.set_title(f"Youth Unemployment by Region ({latest_year})", fontsize=11, fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()

    with col_r:
        st.markdown('<div class="section-title">Regional Trends Over Time</div>', unsafe_allow_html=True)
        reg_trend = (dff[dff["Region"].isin(selected_regions)]
                     .groupby(["Year","Region"])["YouthUnemployment"].mean().reset_index())
        fig3, ax3 = plt.subplots(figsize=(7, 4.5))
        for reg in selected_regions:
            sub = reg_trend[reg_trend["Region"] == reg]
            if not sub.empty:
                ax3.plot(sub["Year"], sub["YouthUnemployment"],
                         label=reg, color=REGION_COLOURS.get(reg,"#999"),
                         lw=1.8, marker="o", ms=2.5)
        ax3.set_xlabel("Year", fontsize=10)
        ax3.set_ylabel("Avg Youth Unemployment (%)", fontsize=10)
        ax3.set_title("Regional Average Youth Unemployment Over Time", fontsize=11, fontweight="bold")
        ax3.legend(fontsize=7.5, loc="upper right")
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

    # Top/bottom 5 table
    st.markdown('<div class="section-title">Country Rankings</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        top5 = (latest[latest["Region"].isin(selected_regions)]
                .nlargest(5, "YouthUnemployment")[["Country","Region","YouthUnemployment"]]
                .rename(columns={"YouthUnemployment":"Youth Unemp (%)"})
                .round(1).reset_index(drop=True))
        st.markdown("**🔴 Top 5 Highest**")
        st.dataframe(top5, use_container_width=True, hide_index=True)
    with c2:
        bot5 = (latest[latest["Region"].isin(selected_regions)]
                .nsmallest(5, "YouthUnemployment")[["Country","Region","YouthUnemployment"]]
                .rename(columns={"YouthUnemployment":"Youth Unemp (%)"})
                .round(1).reset_index(drop=True))
        st.markdown("**🟢 Top 5 Lowest**")
        st.dataframe(bot5, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — COUNTRY COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Side-by-Side Country Comparison</div>', unsafe_allow_html=True)

    da = df[(df["Country"] == country_a) & df["Year"].between(*year_range)].copy()
    db = df[(df["Country"] == country_b) & df["Year"].between(*year_range)].copy()

    if da.empty or db.empty:
        st.warning("One or both countries have no data in the selected year range.")
    else:
        # Trend chart
        fig4, ax4 = plt.subplots(figsize=(12, 4.5))
        ax4.plot(da["Year"], da["YouthUnemployment"], color="#1565c0", lw=2.5,
                 marker="o", ms=4, label=f"{country_a} — Youth")
        ax4.plot(da["Year"], da["Unemployment Rate"],  color="#1565c0", lw=1.5,
                 ls="--", alpha=0.6, label=f"{country_a} — Total")
        ax4.plot(db["Year"], db["YouthUnemployment"], color="#c62828", lw=2.5,
                 marker="s", ms=4, label=f"{country_b} — Youth")
        ax4.plot(db["Year"], db["Unemployment Rate"],  color="#c62828", lw=1.5,
                 ls="--", alpha=0.6, label=f"{country_b} — Total")
        ax4.set_xlabel("Year", fontsize=10)
        ax4.set_ylabel("Unemployment Rate (%)", fontsize=10)
        ax4.set_title(f"Youth & Total Unemployment: {country_a} vs {country_b}", fontsize=12, fontweight="bold")
        ax4.legend(fontsize=9)
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

        # Stats side-by-side
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(f"{country_a} · Avg Youth", f"{da['YouthUnemployment'].mean():.1f}%")
        m2.metric(f"{country_a} · Avg Gap",   f"{da['Youth_Gap'].mean():.1f}pp")
        m3.metric(f"{country_b} · Avg Youth", f"{db['YouthUnemployment'].mean():.1f}%")
        m4.metric(f"{country_b} · Avg Gap",   f"{db['Youth_Gap'].mean():.1f}pp")

        # Employment sector bar comparison
        st.markdown('<div class="section-title">Average Employment Sector Mix</div>', unsafe_allow_html=True)
        sectors = ["Employment Sector: Agriculture", "Employment Sector: Industry", "Employment Sector: Services"]
        labels  = ["Agriculture", "Industry", "Services"]
        means_a = [da[s].mean() for s in sectors]
        means_b = [db[s].mean() for s in sectors]

        x = np.arange(len(labels))
        fig5, ax5 = plt.subplots(figsize=(7, 3.5))
        ax5.bar(x - 0.2, means_a, 0.38, label=country_a, color="#1565c0", alpha=0.85)
        ax5.bar(x + 0.2, means_b, 0.38, label=country_b, color="#c62828", alpha=0.85)
        ax5.set_xticks(x); ax5.set_xticklabels(labels, fontsize=10)
        ax5.set_ylabel("Share of Employment (%)", fontsize=10)
        ax5.set_title("Employment Sector Mix (period average)", fontsize=11, fontweight="bold")
        ax5.legend(fontsize=9)
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()

        with st.expander("📋 Raw data for selected countries"):
            show = pd.concat([
                da[["Country","Year","YouthUnemployment","Unemployment Rate","Youth_Gap","GDP_bn","Dom_Sector"]],
                db[["Country","Year","YouthUnemployment","Unemployment Rate","Youth_Gap","GDP_bn","Dom_Sector"]]
            ]).round(2)
            st.dataframe(show, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — GDP & STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    col_l4, col_r4 = st.columns([1, 1])

    with col_l4:
        st.markdown('<div class="section-title">GDP vs Youth Unemployment (log scale)</div>', unsafe_allow_html=True)
        scatter_data = latest[latest["Region"].isin(selected_regions)].dropna(subset=["GDP_log"])
        if scatter_data.empty:
            st.warning("No data available. Adjust filters.")
        else:
            fig6, ax6 = plt.subplots(figsize=(7, 4.5))
            for reg, grp in scatter_data.groupby("Region"):
                ax6.scatter(grp["GDP_log"], grp["YouthUnemployment"],
                            label=reg, color=REGION_COLOURS.get(reg,"#999"),
                            alpha=0.75, s=55, edgecolors="white", lw=0.5)
            # Trend line
            x_vals = scatter_data["GDP_log"].values
            y_vals = scatter_data["YouthUnemployment"].values
            z = np.polyfit(x_vals, y_vals, 1)
            p = np.poly1d(z)
            xs = np.linspace(x_vals.min(), x_vals.max(), 100)
            ax6.plot(xs, p(xs), "k--", lw=1.2, alpha=0.5, label="Trend line")
            r = np.corrcoef(x_vals, y_vals)[0, 1]
            ax6.text(0.05, 0.95, f"r = {r:.2f}", transform=ax6.transAxes,
                     fontsize=10, va="top", color="#333")
            ax6.set_xlabel("log₁₀ GDP (USD)", fontsize=10)
            ax6.set_ylabel("Youth Unemployment (%)", fontsize=10)
            ax6.set_title(f"GDP vs Youth Unemployment ({latest_year})", fontsize=11, fontweight="bold")
            ax6.legend(fontsize=7.5, loc="upper right")
            plt.tight_layout()
            st.pyplot(fig6)
            plt.close()

            st.markdown(f"""
            <div class="insight-box">
            💡 Pearson r = <b>{r:.2f}</b> — a <b>{'weak' if abs(r)<0.3 else 'moderate'} negative</b> association.
            Wealthier economies tend to have lower youth unemployment, but GDP alone explains little of the variation.
            </div>
            """, unsafe_allow_html=True)

    with col_r4:
        st.markdown('<div class="section-title">Youth–Adult Gap by Dominant Sector</div>', unsafe_allow_html=True)
        sector_data = dff[dff["Region"].isin(selected_regions)]
        if sector_data.empty:
            st.warning("No data available.")
        else:
            sector_gap = (sector_data.groupby("Dom_Sector")["Youth_Gap"]
                          .agg(["median","mean","count"]).reset_index()
                          .rename(columns={"Dom_Sector":"Sector","median":"Median Gap","mean":"Mean Gap","count":"Obs"}))
            sector_gap = sector_gap.sort_values("Median Gap", ascending=False)

            fig7, ax7 = plt.subplots(figsize=(7, 4.5))
            colors = {"Agriculture":"#2e7d32","Industry":"#1565c0","Services":"#e65100"}
            bars = ax7.barh(sector_gap["Sector"], sector_gap["Median Gap"],
                            color=[colors.get(s,"#999") for s in sector_gap["Sector"]],
                            alpha=0.85, height=0.5)
            for bar, val in zip(bars, sector_gap["Median Gap"]):
                ax7.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                         f"{val:.1f} pp", va="center", fontsize=10, fontweight="bold")
            ax7.set_xlabel("Median Youth–Adult Gap (percentage points)", fontsize=10)
            ax7.set_title("Youth–Adult Unemployment Gap\nby Dominant Employment Sector", fontsize=11, fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig7)
            plt.close()

            st.dataframe(sector_gap.set_index("Sector").round(2), use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Youth Unemployment Explorer · ACC102 Track 4 · Xi'an Jiaotong-Liverpool University · IBSS 2024–25<br>
  Data: World Bank / ILO via Kaggle · Accessed April 2025
</div>
""", unsafe_allow_html=True)
