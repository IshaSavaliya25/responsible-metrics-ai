# ResponsibleMetrics AI
> **An NLP-Based Multi-Level Framework for Responsible Use of Bibliometric Indicators**  
> *Final Year Capstone Project | Information Retrieval & Natural Language Processing (IRNLP)*

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![Sentence-Transformers](https://img.shields.io/badge/NLP-Sentence--Transformers-FFA500.svg)](https://sbert.net/)
[![KeyBERT](https://img.shields.io/badge/Keyphrases-KeyBERT-8A2BE2.svg)](https://maartengr.github.io/KeyBERT/)
[![OpenAlex](https://img.shields.io/badge/Bibliometrics-OpenAlex%20API-4169E1.svg)](https://openalex.org/)

---

## 📌 1. Project Overview & Problem Statement

Modern research evaluation increasingly relies on quantitative bibliometric indicators—such as **Citation Counts**, the **h-index**, and **Journal Impact Factor (JIF)**. However, uncritical and context-free reliance on these metrics creates severe systemic distortions in scientific evaluation:

* **Goodhart's Law in Academia:** *"When a measure becomes a target, it ceases to be a good measure."* Over-reliance leads to citation cartels, strategic self-citations, and publication slicing.
* **Misuse of Journal Metrics:** Using Journal Impact Factor (a journal-level metric) to assess individual researchers or paper quality violates the **San Francisco Declaration on Research Assessment (DORA)**.
* **Unnormalized Cross-Discipline Bias:** Comparing raw citations across disparate fields penalizes researchers in smaller or slower-citing disciplines (e.g., Mathematics vs. Biomedicine), violating the **Leiden Manifesto (Principle 6)**.
* **Career-Stage Inequity:** Evaluating early-career researchers using cumulative lifelong metrics (e.g., raw h-index) creates structural barriers.

**ResponsibleMetrics AI** addresses these challenges by introducing an **NLP-driven, automated, multi-level evaluation framework**. The system extracts scientific discourse from research papers (PDFs), queries live citation data via **OpenAlex**, classifies the contextual stance toward indicators, verifies compliance with **Leiden & DORA principles**, and calculates semantic novelty through literature gap clustering.

---

## 🏛️ 2. The Multi-Level Assessment Framework

The framework evaluates bibliometric usage across four distinct levels of scholarly aggregation:

```
┌─────────────────────────────────────────────────────────────┐
│               LEVEL 4: SYSTEM & POLICY LEVEL                │
│  - Transparency & Open Data (OpenAlex, Crossref)            │
│  - Governance, Goodhart gaming safeguards, systemic impacts │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│             LEVEL 3: INSTITUTIONAL / MESO LEVEL             │
│  - Field-weighted normalization (FWCI / MNCS)               │
│  - Alignment with institutional missions vs ranking tables  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│              LEVEL 2: RESEARCHER / MICRO LEVEL              │
│  - Career-stage context (m-quotient, early-career fairness) │
│  - Qualitative narrative portfolios & peer review primacy   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│              LEVEL 1: INDICATOR / METRIC LEVEL              │
│  - Multi-indicator diversity (avoiding single-metric silos) │
│  - Metric limitations awareness & avoidance of false precision
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 3. NLP & Machine Learning Architecture

1. **Contextual Keyphrase Extraction (`KeyBERT` + `SentenceTransformers`)**:
   * Uses `all-MiniLM-L6-v2` dense embeddings to extract multi-word scientometric keyphrases based on cosine similarity with the document representation.
2. **Metric Stance & Misuse Classifier (`MetricStanceClassifier`)**:
   * Analyzes author rhetoric around metric mentions to distinguish between:
     * `CRITICAL_AWARE` (Responsible contextualization, discussing limitations)
     * `NEUTRAL_DESCRIPTIVE` (Factual reporting of bibliometric metadata)
     * `UNCRITICAL_RELIANCE` (Prescriptive misuse, such as filtering applicants strictly by impact factor)
3. **Leiden Manifesto & DORA Rule Engine (`ResponsibleMetricsRules`)**:
   * Encodes the 10 Leiden Principles and DORA recommendations into formal pattern and semantic matching rules with actionable remediation instructions.
4. **Thematic Literature Clustering & Research Gap Projection (`ResearchClusteringService`)**:
   * Projects 384-dimensional dense paper representations down to a 2D space using **Principal Component Analysis (PCA)**.
   * Clusters literature into thematic groups via **K-Means**, plotting the target paper's coordinate distance from existing literature clusters to determine frontier novelty.
5. **Real-Time Scholarly Graph Integration (`OpenAlexService`)**:
   * Automated paper title disambiguation using fuzzy token-sort matching against the OpenAlex API to pull live citation counts, authors, venues, and open-access metadata.

### 📐 3.1 Mathematical Formulations & Score Derivations

The framework derives four core quantitative indicators to ensure explainable and mathematically grounded evaluation:

#### 1. Responsible Score ($S_{\text{resp}} \in [0, 100]$)
Measures the contextual and ethical maturity of bibliometric indicator discourse across 6 weighted scientometric dimensions:
$$S_{\text{resp}} = \min\left(100, \sum_{d=1}^{6} w_d \cdot D_d + B_{\text{biblio}}\right)$$
* **Dimensions & Weights ($w_d$)**:
  * **Contextual Evaluation ($w_1 = 20\%$)**: Context, tailored goals, appropriate usage scope.
  * **Limitations Awareness ($w_2 = 20\%$)**: Explicit caution, biases, gaming risks, indicator boundaries.
  * **Transparency & Openness ($w_3 = 15\%$)**: Open data, reproducible methodology, accessible records.
  * **Metric Diversity ($w_4 = 15\%$)**: Multi-metric portfolios, avoiding single-indicator reliance.
  * **Qualitative Evidence ($w_5 = 15\%$)**: Primacy of expert peer review, narrative portfolios.
  * **Disciplinary Context ($w_6 = 15\%$)**: Field variation awareness, cross-disciplinary normalization.
* **Bibliometric Bonus ($B_{\text{biblio}} \le 5$)**: OpenAlex verified metadata bonus (+2 citations, +1 pub year, +2 open access).

#### 2. Principle Compliance Score ($S_{\text{comp}} \in [0, 100]$)
Audits document compliance against the 10 Leiden Manifesto principles and DORA recommendations:
$$S_{\text{comp}} = \max\left(0, \min\left(100, 50 + 7 \cdot |P| - \sum_{m \in M} \text{penalty}(m)\right)\right)$$
* **Baseline Score**: Starts at a neutral baseline of 50.
* **Responsible Practice Reward ($+7$ per practice $|P|$)**: Awarded for explicit mentions of peer review primacy, multi-indicator evaluation, open data, and field normalization.
* **Misuse Deductions ($\text{penalty}(m)$)**:
  * **High Severity ($-15$ pts)**: DORA violations (evaluating individuals using Journal Impact Factor), single-metric filtering, unnormalized cross-discipline comparisons.
  * **Medium Severity ($-10$ pts)**: Arbitrary h-index thresholds, rigid ranking shortcuts.
  * **Low Severity ($-5$ pts)**: False precision / reporting metrics to misleading decimal places.

#### 3. Literature Similarity ($\text{Sim}_{\text{lit}}$)
Quantifies semantic proximity to foundational scientometric benchmark literature using dense SBERT embeddings ($\vec{v} \in \mathbb{R}^{384}$):
$$\text{Sim}(q, d_i) = \frac{\vec{v}_q \cdot \vec{v}_i}{\|\vec{v}_q\|_2 \|\vec{v}_i\|_2} \in [0.0, 1.0]$$
* **Nearest Match ($\text{Sim}_{\text{nearest}}$)**: Maximum cosine similarity against any single benchmark work.
* **Average Similarity ($\bar{S}$)**: Mean cosine similarity across the entire benchmark corpus ($N = 20$):
$$\bar{S} = \frac{1}{N} \sum_{i=1}^N \text{Sim}(q, d_i)$$

#### 4. Novelty Level & Novelty Index ($N_{\text{index}} \in [0\%, 100\%]$)
Evaluates whether the paper is incremental, a novel synthesis, or pioneering frontier research:
* **Prior Art Overlap**:
$$\text{Overlap} = 0.60 \cdot \text{Sim}_{\text{nearest}} + 0.40 \cdot \text{Sim}_{\text{top3}}$$
* **Composite Novelty Score**:
$$N_{\text{score}} = 0.70 \cdot (1.0 - \text{Overlap}) + 0.30 \cdot (1.0 - \text{Sim}_{\text{cluster}})$$
$$N_{\text{index}} = \text{round}(N_{\text{score}} \times 100, 1)$$
* **Categorical Rating**:
  * **High (Pioneering / Frontier)**: $N_{\text{index}} \ge 72.0\%$ (low prior art overlap)
  * **Medium (Novel Synthesis / Extension)**: $42.0\% \le N_{\text{index}} < 72.0\%$ (moderate overlap, builds upon existing principles)
  * **Low (Incremental Follow-up)**: $N_{\text{index}} < 42.0\%$ (high overlap with foundational prior art)

---

## 📂 4. Repository Structure

```text
responsible-metrics-ai/
├── backend/
│   ├── app/
│   │   ├── ml/                               # Advanced ML & NLP Module
│   │   │   ├── embeddings.py                 # Dense SentenceTransformer singleton
│   │   │   ├── classifier.py                 # Indicator stance & misuse classifier
│   │   │   └── clustering.py                 # K-Means clustering & 2D PCA projection
│   │   ├── rules/                            # Formalized Assessment Rules
│   │   │   └── responsible_metrics_rules.py  # Leiden & DORA rule definitions
│   │   ├── services/
│   │   │   ├── nlp_service.py                # Discourse parsing & KeyBERT extraction
│   │   │   ├── pdf_service.py                # PyMuPDF section extraction
│   │   │   ├── openalex_service.py           # Live OpenAlex API integration
│   │   │   ├── multi_level_framework_service.py # 4-Level evaluation logic
│   │   │   ├── responsible_metrics_service.py   # 6-Dimension responsible scoring
│   │   │   ├── principle_detection_service.py   # Leiden/DORA compliance auditor
│   │   │   └── research_gap_service.py       # Hybrid semantic novelty detector
│   │   ├── models/paper.py                   # SQLite / SQLAlchemy data model
│   │   ├── routers/                          # FastAPI endpoints
│   │   └── main.py                           # Application entry point
│   ├── data/literature/                      # Benchmark scientometric papers
│   └── requirements.txt
├── frontend/
│   ├── app.py                                # Streamlit homepage & health check
│   ├── pages/
│   │   ├── 1_Analyze_Paper.py                # PDF Upload & Pipeline execution
│   │   ├── 2_Dashboard.py                    # Analytics & multi-paper comparison
│   │   ├── 3_Analysis_History.py             # Paper archives & audit history
│   │   ├── 4_Analysis_Report.py              # Audit report & export (.md download)
│   │   └── 5_About_Project.py                # Academic problem statement & guide
│   └── utils/api.py                          # Backend HTTP client
├── requirements.txt                          # Unified dependency manifest
└── README.md                                 # Project documentation
```

---

## 🚀 5. Quickstart & Installation

### Prerequisites
* Python 3.10+ (Recommended: Python 3.11 or 3.12)
* Git

### Step 1: Clone Repository
```bash
git clone https://github.com/IshaSavaliya25/PGENAI-2026.git
cd responsible-metrics-ai
```

### Step 2: Set up Backend
```bash
cd backend
python -m venv venv

# Windows Powershell
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Launch FastAPI server
uvicorn app.main:app --reload --port 8000
```
* Backend interactive documentation is available at `http://127.0.0.1:8000/docs`.

### Step 3: Set up Frontend
Open a second terminal window:
```bash
cd frontend
# Windows Powershell
.\venv\Scripts\Activate.ps1

# Launch Streamlit interface
streamlit run app.py
```
* The web interface will open automatically at `http://localhost:8501`.

---

## 📚 6. Foundational References

* **Hicks, D., Wouters, P., Waltman, L., de Rijcke, S., & Rafols, I.** (2015). *Bibliometrics: The Leiden Manifesto for research metrics*. Nature, 520(7548), 429-431.
* **San Francisco Declaration on Research Assessment (DORA)** (2012). *DORA: Putting science into the assessment of research*.
* **Hirsch, J. E.** (2005). *An index to quantify an individual's scientific research output*. PNAS, 102(46), 16569-16572.
* **Priem, J., Taraborelli, D., Groth, P., & Neylon, C.** (2010). *Altmetrics: A manifesto*.
* **Wilsdon, J., et al.** (2015). *The Metric Tide: Report of the Independent Review of the Role of Metrics in Research Assessment and Management*. Higher Education Funding Council for England.

