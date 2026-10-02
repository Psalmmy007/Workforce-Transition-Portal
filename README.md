# 🧭 CareerGPS — Predictive Workforce Transition Intelligence

> **Empirical AI Job Displacement Risk Classification & Career Reskilling Engine**  
> *Built for the 10Alytics × JengaGlobal Student's Hackathon 2026 — Track C: Data Science*  
> **Client Scenario:** StrataWork Global  

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E.svg)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75.svg)](https://plotly.com/)
[![Benchmark](https://img.shields.io/badge/Oxford-Frey%20%26%20Osborne%20(2013)-059669.svg)](#academic-benchmarking--validation)

---

## 📑 Table of Contents
- [Executive Summary & Problem Context](#-executive-summary--problem-context)
- [Strategic Rationale & Solution Pillars](#-strategic-rationale--solution-pillars)
- [System Architecture & Core Views](#-system-architecture--core-views)
- [Machine Learning Pipeline & Methodology](#-machine-learning-pipeline--methodology)
- [Skills Adjacency & Pathway Engine](#-skills-adjacency--pathway-engine)
- [Repository Structure](#-repository-structure)
- [Installation & Local Execution](#-installation--local-execution)
- [Deployment Guide](#-deployment-guide)
- [Project Deliverables & Submission Files](#-project-deliverables--submission-files)
- [The Team & Contributions](#-the-team--contributions)
- [References & Academic Grounding](#-references--academic-grounding)

---

## 📌 Executive Summary & Problem Context

Following aggressive adoption of generative AI agents across enterprise operations, **StrataWork Global** achieved unprecedented operational efficiency—automating **65% of entry-level and routine analytics tasks** and slashing turnaround times by **300%**. 

However, this technological leap created an acute human capital crisis:
1. **Sudden Redundancy:** Hundreds of junior and mid-level data analysts faced occupational displacement.
2. **Absence of Empirical Early Warning:** Management lacked quantitative forecasting to anticipate role exposure before organizational disruption.
3. **No Structured Reskilling Bridges:** Displaced personnel had no empirical guidance to map their existing skills into high-demand, resilient adjacent positions.

**CareerGPS** resolves this challenge by moving enterprise talent management from *reactive severance* to *proactive internal mobility and skill-based redeployment*.

---

## 🎯 Strategic Rationale & Solution Pillars

Modeled on modern executive workforce intelligence frameworks, CareerGPS addresses disruption across three strategic pillars:

```
┌─────────────────────────────────┐   ┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│  Predict Displacement Paths     │   │   Chart Reskilling Pathways     │   │  Preserve Human Capital Value   │
├─────────────────────────────────┤   ├─────────────────────────────────┤   ├─────────────────────────────────┤
│ Quantifies role-level automa-   │   │ Automated skill adjacency       │   │ Proactive talent redeployment   │
│ tion risk early using machine   │   │ mapping accelerates transition   │   │ preserves institutional domain  │
│ learning and Oxford benchmarks. │   │ into high-growth roles.         │   │ knowledge in the AI era.        │
└─────────────────────────────────┘   └─────────────────────────────────┘   └─────────────────────────────────┘
```

1. **Predict Displacement Trajectories:** Quantifies multi-factor automation exposure across 500 enterprise job titles to signal transition needs before layoffs occur.
2. **Chart Reskilling Pathways:** Computes competency overlaps to recommend 3 personalized transition pathways with prioritized skill acquisition targets.
3. **Preserve Human Capital Value:** Empowers HR leaders to retain domain knowledge and lower rehiring costs by cultivating internal talent pipelines.

---

## 🖥️ System Architecture & Core Views

CareerGPS is delivered as a production-ready, interactive Streamlit application structured into three specialized modules:

### View 1: Workforce Mobility Portal (Individual Transition Engine)
- **Role Profiling:** Users input their current occupation, functional domain, industry, and skills index.
- **Dynamic Risk Calibration:** Triggers real-time ML inference accompanied by UI loading calibration spinners.
- **Automated Results Scroll:** Automatically transitions the viewport directly to calibrated displacement risk metrics.
- **Pathway Recommendations:** Surfaces 3 high-probability adjacent career transitions with skill gap breakdowns, difficulty feasibility tiers, and prioritized learning steps.

### View 2: Talent Analytics Executive Dashboard (Macro Enterprise View)
- **Portfolio KPIs:** Summarizes total enterprise roles analyzed, high-risk role exposure, average risk distribution, and career transition coverage.
- **Interactive Visualizations:** Built with Plotly:
  - *Risk Category Breakdown:* Proportion of Low, Medium, and High susceptibility across surveyed sectors.
  - *Industry Vulnerability Hotspots:* Departmental comparison of automation probability vs. compensation levels.
  - *Experience vs. Risk Scatter Analysis:* Identifying where junior vs. senior talent clusters in vulnerability.

### View 3: Methodology & Audited Benchmarks (Governance & Transparency)
- **Model Card & Metrics:** Transparent presentation of 5-fold cross-validation accuracy, majority baseline lift, and hyperparameter choices.
- **Oxford Benchmark Comparison:** Direct cross-referencing against the Frey & Osborne (2013) Occupational Automation Index.
- **Limitation Disclosures:** Honest documentation of dataset size and model scope to build executive confidence.

---

## 🧠 Machine Learning Pipeline & Methodology

### 1. Data Ingestion & Preprocessing
- **Dataset:** 500 enterprise workforce records (`ai_job_market_insights.csv`) spanning cross-industry roles, compensation, automation probability, and skill indices.
- **Imputation & Cleaning:** Handled missing categorical values and standardized numerical metrics (`(Phase1)_EDA_and_Feature_Engineering.ipynb`).
- **Feature Encoding:** Label encoding for ordinal classifications and one-hot encoding for nominal domain attributes.

### 2. Modeling & Validation
- **Algorithm:** Multinomial Logistic Regression with L2 regularization (`automation_risk_model.pkl`).
- **Evaluation Strategy:** 5-Fold Stratified Cross-Validation to guarantee generalization across unbalanced role categories.
- **Statistical Results:**
  - **Mean 5-Fold CV Accuracy:** `36.0%`
  - **Majority-Class Baseline:** `34.6%`
  - **Empirical Model Lift:** `+1.4 pp` over random/majority assignment.

```
       [Raw Data: 500 Records]
                  │
                  ▼
       [Data Cleaning & Imputation]
                  │
                  ▼
       [Feature Engineering & Scaling]
                  │
                  ▼
       [Logistic Regression (5-Fold CV)] ──▶ Accuracy: 36.0% (vs 34.6% baseline)
                  │
                  ▼
       [Oxford Frey & Osborne Alignment] ──▶ Independent External Benchmark
```

### 3. Transparent Academic Disclosure
Rather than claiming unrealistic black-box accuracy on a 500-record dataset, CareerGPS honestly communicates its predictive boundaries. The primary business value is realized through the **skills graph adjacency engine** and **talent governance dashboard**, providing actionable reskilling intelligence.

---

## 🗺️ Skills Adjacency & Pathway Engine

The skill transition algorithm (`skill_engine.py`) matches competencies between source and candidate target roles using a multi-factor scoring mechanism:

$$\text{Pathway Compatibility Score} = w_1 \cdot \text{Skill Overlap} + w_2 \cdot \text{Industry Proximity} + w_3 \cdot (1 - \text{Target Automation Risk})$$

- **Skill Overlap:** Vectorized intersection between candidate roles to identify competencies already mastered.
- **Upskilling Gap Analysis:** Explicitly isolates the 2–4 critical missing skills required for transition.
- **Feasibility Ranking:** Filters target roles to ensure candidates transition toward lower automation risk profiles with viable career horizons.

---

## 📁 Repository Structure

```
Portal/
├── app.py                                   # Main Streamlit web application & routing
├── skill_engine.py                         # Skills adjacency matrix & pathway engine
├── job_risk_reference.py                   # Oxford Frey & Osborne benchmark lookup
├── automation_risk_model.pkl               # Trained & serialized scikit-learn model
├── ai_job_market_insights.csv              # Workforce dataset (500 enterprise records)
├── requirements.txt                        # Production dependency specifications
│
├── (Phase1)_EDA_and_Feature_Engineering.ipynb # Exploratory data analysis notebook
├── (Phase2)_Model_Building.ipynb           # Model experimentation & validation notebook
│
├── CareerGPS_Project_Documentation.pdf     # 3-Page formal PDF documentation
├── CareerGPS_Pitch_Deck_Final.pptx         # 8-Slide executive pitch deck (PowerPoint)
├── CareerGPS_Pitch_Deck.html               # Interactive SVG-based pitch deck (Browser)
├── career_gps_logo.png                      # Circular branding asset & favicon
│
├── icons_pro/                              # High-resolution vector icon badge assets
│   ├── compass.png                         # Predict displacement icon badge
│   ├── pathway.png                         # Chart reskilling icon badge
│   ├── briefcase.png                       # Preserve human capital icon badge
│   └── ...                                 # Technical architecture & UI badges
└── README.md                               # Project documentation & deployment manual
```

---

## ⚡ Installation & Local Execution

### Prerequisites
- **Python:** Version 3.10, 3.11, or 3.12
- **Package Manager:** `pip`

### 1. Clone or Navigate to Directory
```bash
cd Portal
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit Portal
```bash
streamlit run app.py
```
The application will launch automatically in your browser at `http://localhost:8501`.

---

## 🚀 Deployment Guide

### Deploying to Streamlit Community Cloud
1. Push this repository to GitHub.
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Select **"New app"**, point to your repository, set branch to `main`, and main file path to `app.py`.
4. Deploy! All dependencies in `requirements.txt` (including `Pillow` and `scikit-learn`) will install automatically.

### UI & Theme Configuration
The application is pre-configured with light and dark mode CSS tokens in `app.py`. The favicon and masthead branding automatically load from `career_gps_logo.png`.

---

## 📦 Project Deliverables & Submission Files

All competition requirements have been produced, packaged, and verified:

| Deliverable | Format | File Location | Description |
|---|---|---|---|
| **Working Application** | Python / Streamlit | [`app.py`](app.py) | Fully interactive 3-view workforce intelligence portal |
| **Technical Documentation** | PDF | [`CareerGPS_Project_Documentation.pdf`](CareerGPS_Project_Documentation.pdf) | 3-Page formal report with methodology & benchmark comparisons |
| **Pitch Presentation (PPTX)** | PowerPoint | [`CareerGPS_Pitch_Deck_Final.pptx`](CareerGPS_Pitch_Deck_Final.pptx) | 8-Slide executive deck with custom vector icon badges |
| **Pitch Presentation (HTML)** | HTML / Browser | [`CareerGPS_Pitch_Deck.html`](CareerGPS_Pitch_Deck.html) | Self-contained, print-to-PDF ready presentation deck |
| **Model & Data Files** | PKL & CSV | [`automation_risk_model.pkl`](automation_risk_model.pkl), [`ai_job_market_insights.csv`](ai_job_market_insights.csv) | Trained model and clean dataset |
| **Exploratory Notebooks** | Jupyter | [`(Phase1)...ipynb`](<(Phase1)_EDA_and_Feature_Engineering.ipynb>), [`(Phase2)...ipynb`](<(Phase2)_Model_Building.ipynb>) | Full data science exploration & training history |

---

## 👥 The Team & Contributions

**10Alytics × JengaGlobal Student's Hackathon 2026 — Track C: Data Science**

| Team Member | Role | Key Contributions |
|---|---|---|
| **Adeboyejo Adetoun Abigail** | **Team Lead** | Data Cleaning, Exploratory Data Analysis, Imputation, Quality Assurance |
| **Ikechukwu Augustine Okeke** | **Data Scientist** | Machine Learning Modeling, 5-Fold Cross-Validation, Statistical Testing |
| **Uket Samuel** | **Full-Stack Developer** | Streamlit Architecture, Skill Adjacency Engine, UI/UX Design & Branding |

---

## 📚 References & Academic Grounding

1. **Frey, C. B., & Osborne, M. A. (2013).** *The future of employment: How susceptible are jobs to computerisation?* Oxford Martin School, University of Oxford.
2. **World Economic Forum (2023).** *The Future of Jobs Report 2023.* Employment and Skills Dynamics in the Age of AI.
3. **Brynjolfsson, E., Li, D., & Raymond, L. R. (2023).** *Generative AI at Work.* National Bureau of Economic Research (NBER Working Paper No. 31161).