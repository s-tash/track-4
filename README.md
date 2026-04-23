# Youth Unemployment Explorer 📊

**ACC102 Mini Assignment — Track 4: Interactive Data Analysis Tool**
Xi'an Jiaotong-Liverpool University · IBSS · 2nd Semester 2024–25

> An interactive Streamlit app for exploring global youth unemployment trends, regional disparities, country comparisons, and economic structural correlates — covering 100+ countries from 1991 to 2022.

---

## 🖥️ Demo Video

*[Insert your Mediasite / YouTube / Bilibili link here]*

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/acc102-youth-unemployment-explorer.git
cd acc102-youth-unemployment-explorer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser. Both CSV data files are included in the repository — no additional setup or API keys needed.

**Python version:** 3.9 or above recommended.

---

## 1. Problem & Intended User

**Question:** How has global youth unemployment evolved between 1991 and 2022 — and how do region, GDP, and economic sector structure relate to the youth–adult employment gap?

**Target user:** Economics and policy students, early-career researchers, and educators who want to explore the data interactively rather than read a static report. The app lets users filter by region, year range, and country so they can answer their own questions rather than just receive pre-packaged conclusions.

---

## 2. Data

| File | Source | Accessed | Key variables |
|------|--------|----------|---------------|
| `youth_unemployment_global.csv` | World Bank / ILO via Kaggle | April 2025 | Country, Year, YouthUnemployment (%) |
| `Employment_Unemployment_GDP_data.csv` | World Bank Open Data via Kaggle | April 2025 | Country, Year, GDP (USD), Unemployment Rate (%), sector employment shares |

Both files are under 25 MB and are included in the repository. Coverage: 100+ countries, 1991–2022.

---

## 3. App Features

The app has **four interactive tabs**, all controlled by a shared sidebar with year range, region, and country selectors:

| Tab | What it shows |
|-----|---------------|
| 🌍 **Global Trend** | Line chart of global average youth vs total unemployment over time, with crisis period shading and a summary insight |
| 📦 **Regional Breakdown** | Regional boxplot + multi-line trend chart + ranked top/bottom 5 country tables |
| 🔍 **Country Comparison** | Side-by-side trend chart, key metrics, and employment sector bar chart for any two user-selected countries |
| 📈 **GDP & Structure** | GDP vs youth unemployment scatter (log scale, r value shown) and youth–adult gap by dominant employment sector |

---

## 4. Key Findings

- Global average youth unemployment **peaked at 18.8% in 2020** (COVID-19 shock), recovering to **16.2% in 2022**.
- Youth unemployment runs **~2× the total adult rate** across all regions and time periods — the gap is structural, not merely cyclical.
- **Highest region (2022): Middle East & Africa (20.9%)** · **Lowest: Asia-Pacific (8.5%)**.
- **South Africa (61.1%)** and **Jordan (42.0%)** are the extreme outliers in 2022.
- GDP–youth unemployment correlation: **r = −0.26** — modest; structural factors matter as much as aggregate wealth.
- **Services-dominant economies** show a larger youth–adult gap (8.2 pp) than **agriculture-dominant** ones (3.4 pp).

---

## 5. Repository Structure

```
.
├── app.py                                   ← Streamlit app (entry point)
├── requirements.txt                         ← Python dependencies
├── README.md
├── youth_unemployment_global.csv            ← Dataset 1
├── Employment_Unemployment_GDP_data.csv     ← Dataset 2
└── reflection_report_track4.docx           ← Reflection report
```

---

## 6. Limitations & Next Steps

- Region labels are manually assigned; some smaller economies fall into "Other".
- The GDP scatter is cross-sectional (single year) — panel methods would give stronger causal insight.
- Future improvement: add a choropleth world map and a downloadable filtered CSV button.

---

*ACC102 · Track 4 · Interactive Data Analysis Tool · XJTLU IBSS 2024–25*
*Data: World Bank / ILO via Kaggle · Accessed April 2025*
