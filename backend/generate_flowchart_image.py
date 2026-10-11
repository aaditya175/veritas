"""
High-Resolution Flowchart Generator for Veritas Project Presentation
Generates both Light Theme and Dark Theme presentation-ready images (PNG & SVG).
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIGHT_PNG = os.path.join(ROOT_DIR, "veritas_flowchart_presentation.png")
DARK_PNG = os.path.join(ROOT_DIR, "veritas_flowchart_dark.png")
SVG_PATH = os.path.join(ROOT_DIR, "veritas_flowchart.svg")


def create_flowchart(dark_mode=False, output_path="flowchart.png"):
    fig, ax = plt.subplots(figsize=(18, 12), dpi=300)

    bg_color = "#0f172a" if dark_mode else "#ffffff"
    text_primary = "#f8fafc" if dark_mode else "#0f172a"
    text_secondary = "#94a3b8" if dark_mode else "#475569"
    border_default = "#334155" if dark_mode else "#cbd5e1"

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Box styles
    c_input_bg = "#1e293b" if dark_mode else "#f8fafc"
    c_input_edge = "#475569" if dark_mode else "#94a3b8"

    c_causal_bg = "#064e3b" if dark_mode else "#ecfdf5"
    c_causal_edge = "#10b981" if dark_mode else "#059669"
    c_causal_text = "#a7f3d0" if dark_mode else "#065f46"

    c_human_bg = "#78350f" if dark_mode else "#fef3c7"
    c_human_edge = "#f59e0b" if dark_mode else "#d97706"
    c_human_text = "#fde68a" if dark_mode else "#92400e"

    c_gen_bg = "#1e3a8a" if dark_mode else "#eff6ff"
    c_gen_edge = "#3b82f6" if dark_mode else "#2563eb"
    c_gen_text = "#bfdbfe" if dark_mode else "#1e40af"

    c_eval_bg = "#831843" if dark_mode else "#fdf2f8"
    c_eval_edge = "#ec4899" if dark_mode else "#db2777"
    c_eval_text = "#fbcfe8" if dark_mode else "#9d174d"

    c_out_bg = "#0d4734" if dark_mode else "#0d4734"
    c_out_edge = "#34d399" if dark_mode else "#06291d"

    def draw_box(x, y, w, h, title, subtitle="", bg=c_input_bg, edge=c_input_edge, txt_col=text_primary, rad=0.03):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0.2,rounding_size={rad*10}",
            facecolor=bg, edgecolor=edge, linewidth=1.8, zorder=2
        )
        ax.add_patch(box)
        if subtitle:
            ax.text(x + w/2, y + h*0.62, title, ha="center", va="center", fontsize=10, fontweight="bold", color=txt_col, zorder=3)
            ax.text(x + w/2, y + h*0.30, subtitle, ha="center", va="center", fontsize=8, color=text_secondary, zorder=3)
        else:
            ax.text(x + w/2, y + h*0.5, title, ha="center", va="center", fontsize=10, fontweight="bold", color=txt_col, zorder=3)

    def draw_arrow(x1, y1, x2, y2, color=c_causal_edge, style="->", dashed=False):
        ls = "--" if dashed else "-"
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0, ls=ls, mutation_scale=15),
            zorder=1
        )

    # -------------------------------------------------------------
    # 1. Pipeline Title Header
    # -------------------------------------------------------------
    ax.text(50, 97, "VERITAS: END-TO-END CAUSAL SYNTHETIC DATA MECHANISM", ha="center", va="center",
            fontsize=16, fontweight="bold", color=text_primary)
    ax.text(50, 94.5, "Unified Pipeline: Continuous Structure Learning → Human-in-the-Loop SCM → Pearl Counterfactuals → SHAP XAI",
            ha="center", va="center", fontsize=9.5, color=text_secondary)

    # -------------------------------------------------------------
    # 2. Left / Main Column: Causal Pipeline
    # -------------------------------------------------------------
    # Box 1: Ingestion
    draw_box(16, 85, 26, 6, "1. Raw Observational Dataset", "CSV Upload (e.g. employee_data.csv)", bg=c_input_bg, edge=c_input_edge)
    draw_arrow(29, 85, 29, 79)

    # Box 2: Profiler
    draw_box(16, 73, 26, 6, "2. Automated Data Profiler", "Column Types, Nulls, Cardinality & Sensitive Flags", bg=c_input_bg, edge=c_input_edge)
    draw_arrow(29, 73, 29, 67)

    # Box 3: NOTEARS
    draw_box(14, 60, 30, 7, "3. Continuous Causal Discovery", "NOTEARS Algorithm: min 1/2n ||X - XW||² s.t. h(W)=0", bg=c_causal_bg, edge=c_causal_edge, txt_col=c_causal_text)
    draw_arrow(29, 60, 29, 54)

    # Box 4: Human-in-the-Loop
    draw_box(14, 47, 30, 7, "4. Human-in-the-Loop DAG Canvas", "Interactive UI: Add, Reverse, or Prune Directed Edges", bg=c_human_bg, edge=c_human_edge, txt_col=c_human_text)
    draw_arrow(29, 47, 29, 41)

    # Box 5: Mechanism Learning
    draw_box(14, 34, 30, 7, "5. SCM Mechanism Learning", "Per-Node Equations: Continuous (Ridge) & Categorical (CPT)", bg=c_causal_bg, edge=c_causal_edge, txt_col=c_causal_text)

    # Fork arrows from SCM Mechanism Learning
    draw_arrow(22, 34, 15, 27)  # to Path B (Counterfactuals)
    draw_arrow(36, 34, 43, 27)  # to Path A (Ancestral Sampling)

    # -------------------------------------------------------------
    # Branch B: Pearl Counterfactual Engine (Left)
    # -------------------------------------------------------------
    draw_box(5, 20, 22, 7, "PATH B: Pearl Counterfactuals", "Row-Level What-If Queries", bg=c_causal_bg, edge=c_causal_edge, txt_col=c_causal_text)
    draw_arrow(16, 20, 16, 14.5)

    # Step-by-step box for Pearl
    draw_box(3, 7.5, 26, 7, "Pearl's 3-Step Causal Engine", "1. Abduction (Noise ε*) → 2. Action do(X) → 3. Prediction", bg=c_causal_bg, edge=c_causal_edge, txt_col=c_causal_text)
    draw_arrow(16, 7.5, 16, 2)

    draw_box(5, 0.5, 22, 4.5, "Counterfactual Twin Row", "Exact Downstream Delta (Diff Table)", bg=c_out_bg, edge=c_out_edge, txt_col="#ffffff")

    # -------------------------------------------------------------
    # Branch A: Ancestral Generation (Center)
    # -------------------------------------------------------------
    draw_box(32, 20, 24, 7, "PATH A: Ancestral Generation", "Topological Kahn Sorting (Causes before Effects)", bg=c_gen_bg, edge=c_gen_edge, txt_col=c_gen_text)
    draw_arrow(44, 20, 44, 14.5)

    draw_box(32, 7.5, 24, 7, "Ancestral Sampling Engine", "Sample Root Noise → Evaluate Child Mechanisms", bg=c_gen_bg, edge=c_gen_edge, txt_col=c_gen_text)
    draw_arrow(44, 7.5, 44, 2)

    draw_box(33, 0.5, 22, 4.5, "Causal Synthetic Dataset", "Full Synthetic Table (No Invalid Pairings)", bg=c_out_bg, edge=c_out_edge, txt_col="#ffffff")

    # -------------------------------------------------------------
    # Right Column: Parallel Baselines & Multi-Metric Evaluation
    # -------------------------------------------------------------
    # Baseline Generative Models box
    draw_box(65, 83, 30, 9, "Baseline Generative Models", "• CTGAN (Conditional GAN)  • TVAE (Variational Autoencoder)\n• Gaussian Copula (Statistical)", bg=c_gen_bg, edge=c_gen_edge, txt_col=c_gen_text)

    # Connecting raw data to baselines
    draw_arrow(42, 88, 65, 88, color=c_gen_edge, dashed=True)

    # Arrow from baselines down to Evaluation
    draw_arrow(80, 83, 80, 71, color=c_gen_edge)

    # Evaluation Harness
    draw_box(64, 61, 32, 10, "Multi-Dimensional Evaluation", "Benchmark Scorecard across 4 Dimensions:\nFidelity (KS/Corr) • Utility (TSTR ML) • Privacy (DCR) • Fairness", bg=c_eval_bg, edge=c_eval_edge, txt_col=c_eval_text)

    # Also connect Ancestral Generation to Evaluation
    draw_arrow(56, 11, 70, 11, color=c_eval_edge)
    draw_arrow(70, 11, 70, 61, color=c_eval_edge)

    # C2ST + TreeSHAP Explainability
    draw_arrow(80, 61, 80, 48, color=c_eval_edge)
    draw_box(63, 37, 34, 11, "XAI Diagnostic Explainer", "Classifier Two-Sample Test (C2ST Discriminator: Real=0, Syn=1)\n+ TreeSHAP Feature Attributions (Diagnose Divergent Columns)", bg=c_eval_bg, edge=c_eval_edge, txt_col=c_eval_text)

    # Final Verified Platform Output Box
    draw_arrow(80, 37, 80, 22, color=c_out_edge)
    draw_box(62, 7, 36, 15, "VERITAS SYNTHETIC DATA & SCORECARD", "• High Fidelity & Generalization Utility\n• Strict Privacy Protection (Zero Memorization Leaks)\n• Interactive Row-Level Counterfactual What-Ifs\n• Game-Theoretic SHAP Interpretability", bg=c_out_bg, edge=c_out_edge, txt_col="#ffffff")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=bg_color, bbox_inches="tight")
    plt.close()
    print(f"Flowchart saved to: {output_path}")


if __name__ == "__main__":
    create_flowchart(dark_mode=False, output_path=LIGHT_PNG)
    create_flowchart(dark_mode=True, output_path=DARK_PNG)
    # Also save as SVG vector
    create_flowchart(dark_mode=False, output_path=SVG_PATH)
