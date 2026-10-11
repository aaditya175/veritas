# Veritas: A Causally-Grounded, Explainable Synthetic Data Platform

**BE Major Project: "Comparative Study of Deep Generative Models for Synthetic Data Generation Using Explainable AI"**

Veritas is a full-stack, multimodal synthetic data generation platform that integrates deep generative models with causal reasoning and Explainable AI (XAI). Unlike standard black-box generators, Veritas treats causal structure and interpretability as integral parts of the synthesis process rather than post-hoc metrics.

---

## 🌟 Key Architecture & Features

### 1. Tabular / CSV Module
- **Pluggable Generator Registry (`core/registry.py`)**:
  - **Causal SCM Generator (Novel Contribution)**:
    - Continuous DAG structure learning via the **NOTEARS** algorithm ($\min \frac{1}{2n}\|X - XW\|_F^2 + \lambda \|W\|_1 \text{ s.t. } \text{Tr}(e^{W \circ W}) - d = 0$).
    - Interactive **Human-in-the-Loop DAG Canvas**: inspect, add, remove, and reverse causal directed edges before synthesis.
    - **Mechanism Learning**: per-node structural equations ($X_i = f_i(\text{Pa}_i) + \epsilon_i$).
    - **Ancestral Sampling**: topological generation evaluating causes before effects.
    - **Pearl's 3-Step Counterfactual Engine**: given any factual row and an intervention $do(X = v)$, performs **Abduction** (infers row's latent noise $\epsilon^*$), **Action** (severs incoming edges), and **Prediction** (re-propagates strictly through downstream causal descendants, keeping non-descendants invariant).
  - **GAN Baseline**: CTGAN (Conditional Tabular GAN with mode-specific normalization).
  - **VAE Baseline**: TVAE (Tabular Variational Autoencoder).
  - **Statistical Baseline**: Multivariate Gaussian Copula.
- **Evaluation Harness (`tabular/evaluator.py`)**:
  - **Fidelity**: Column-wise distribution similarity (Kolmogorov-Smirnov test for numeric, Total Variation Distance for categorical), correlation matrix difference (Frobenius norm).
  - **Utility**: Train-on-Synthetic-Test-on-Real (**TSTR**) downstream ML accuracy/F1 compared against Train-Real-Test-Real (**TRTR**).
  - **Privacy**: Distance-to-Closest-Record (**DCR**) normalized Euclidean nearest-neighbor distances and zero-leakage duplicate checks.
  - **Fairness & Performance**: Demographic parity consistency and generation training time.
- **XAI Diagnostics (`tabular/explainer.py`)**:
  - **SHAP Feature Importance**: Game-theoretic Shapley attributions on a Classifier Two-Sample Test (**C2ST**) real-vs-synthetic discriminator diagnosing which features trigger divergence.

### 2. Text Corpus Module
- **Pluggable Text Engine (`text/`)**:
  - **Corpus Profiler**: Character and word length distributions, vocabulary size, tone/sentiment estimation, and category proportions.
  - **Generation Backends**:
    - **Veritas Local Engine**: Zero-configuration offline Markovian and stylistic recombination (runs 100% locally with zero API key required).
    - **Groq Cloud API**: Fast Llama 3.1 8B inference on Groq LPUs.
    - **Google Gemini API**: Gemini 1.5 Flash free tier.
  - **Text Explainability**: Real vs synthetic vocabulary overlap (**Jaccard similarity**), length distribution alignment, and top keyword overlap.

### 3. Future Multimodal Scope (Image & Video)
- **Decoupled Architecture**: Abstract base classes `BaseImageGenerator` and `BaseVideoGenerator` defined in `core/base_generator.py` and registered in `core/registry.py`.
- **Placeholder UI & Blueprints**: Dedicated Multimodal Hub and sidebar entries marked **"Coming soon"** detailing planned Phase 4 **CausalVAE** (latent factor intervention on lighting, pose, viewpoint) and Phase 5 **Causal Video Diffusion** (spatiotemporal physical dynamics). Adding these modules requires zero refactoring.

---

## 🖥️ UI & Visual Design

The UI direction matches the clean, minimalist aesthetic with forest green primary accents (`#0d4734`):
1. **Landing Page**:
   - Hero headline: *"Generate Synthetic Data That Makes Sense"*
   - Pill badge: `• SYNTHETIC DATA • CAUSAL AI • EXPLAINABLE AI`
   - Call-to-actions: `Try Veritas ->` and `Watch Demo`
   - 4-feature icon bar: Multiple Generative Models, Causal Reasoning, Explainable Results, Privacy & Fairness Evaluation.
   - Interactive preview of the workspace laptop scene.
2. **App Dashboard**:
   - **Dataset Overview**: Upload CSV, view row/column counts, review the interactive NOTEARS DAG, model comparison bar chart, and scrollable synthetic data preview table.
   - **Causal Graph**: Full DAG editor with node-and-edge manipulation.
   - **Generate Data**: Model selector, sample size configuration, and live generation.
   - **Synthetic Preview**: Filterable, searchable data table with CSV export.
   - **Compare Models**: Multi-model benchmark scorecard.
   - **Counterfactual Explorer**: Pearl 3-step what-if query interface with side-by-side diff.
   - **Explainability**: SHAP attribution plots and diagnostic insights.
   - **Text Generation**: Corpus upload/paste, analysis, prompt synthesis, and Jaccard overlap metrics.
   - **Multimodal Architecture Hub**: Image & Video blueprints.
   - **Settings**: Local SQLite API key configuration.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+

### One-Click Launch (Windows)
Double-click:
```cmd
run_veritas.bat
```
or run in PowerShell:
```powershell
.\run_veritas.ps1
```

### Manual Launch
#### 1. Backend (Terminal 1):
```bash
python -m pip install -r backend/requirements.txt
python backend/run.py
```
Backend API will be running at: `http://127.0.0.1:8000` (Docs at `/docs`)

#### 2. Frontend (Terminal 2):
```bash
cd frontend
npm install
npm run dev
```
Frontend will be running at: `http://localhost:5173`

---

## 📂 Project Structure

```
Major project/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entrypoint
│   │   ├── database.py            # SQLite metadata DB
│   │   ├── core/
│   │   │   ├── base_generator.py  # Abstract multimodal generator interfaces
│   │   │   ├── registry.py        # Central generator registry
│   │   │   └── setup_registry.py  # Plugin registration
│   │   ├── tabular/
│   │   │   ├── causal_generator.py # NOTEARS DAG discovery + SCM + Pearl counterfactuals
│   │   │   ├── copula_generator.py # Gaussian Copula
│   │   │   ├── ctgan_generator.py  # CTGAN
│   │   │   ├── tvae_generator.py   # TVAE
│   │   │   ├── evaluator.py        # Fidelity, Utility (TSTR), Privacy (DCR)
│   │   │   └── explainer.py        # SHAP on C2ST discriminator
│   │   ├── text/
│   │   │   ├── corpus_analyzer.py  # Length, vocab, tone profiling
│   │   │   ├── local_generator.py  # Zero-key offline synthesizer
│   │   │   ├── groq_generator.py   # Groq Llama 3.1
│   │   │   └── gemini_generator.py # Google Gemini 1.5 Flash
│   │   ├── multimodal/
│   │   │   ├── image_generator.py  # Phase 4 CausalVAE blueprint
│   │   │   └── video_generator.py  # Phase 5 Causal Diffusion blueprint
│   │   ├── api/                   # REST API routes
│   │   └── sample_data/           # Preloaded employee_data.csv & customer_feedback.json
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/            # Navbar, Sidebar, CausalGraphCanvas
│   │   └── pages/                 # LandingPage, DashboardOverview, etc.
│   ├── public/hero_mockup.jpg
│   └── package.json
├── run_veritas.bat
├── run_veritas.ps1
└── README.md
```

---

## 📚 Annotated Academic Bibliography
1. **Zheng et al.** (NeurIPS 2018) — *"DAGs with NO TEARS: Continuous Optimization for Structure Learning"*
2. **Xu et al.** (NeurIPS 2019) — *"Modeling Tabular Data using Conditional GAN (CTGAN)"*
3. **Lundberg & Lee** (NeurIPS 2017) — *"A Unified Approach to Interpreting Model Predictions (SHAP)"*
4. **Pearl, J.** (2009) — *"Causality: Models, Reasoning, and Inference"* (Pearl's 3-step counterfactual recipe: Abduction–Action–Prediction)
5. **van Breugel et al.** (NeurIPS 2021) — *"DECAF: Generating Fair Synthetic Data Using Causally-Aware Generative Networks"*
