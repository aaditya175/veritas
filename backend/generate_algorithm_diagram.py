"""
High-Resolution Algorithm & Mathematical Framework Diagram for Veritas
Generates presentation-ready 300 DPI diagram (PNG & SVG) for Slide 1 (Analysis / Framework / Algorithm).
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PNG = os.path.join(ROOT_DIR, "veritas_algorithm_framework.png")
OUTPUT_DARK_PNG = os.path.join(ROOT_DIR, "veritas_algorithm_framework_dark.png")
OUTPUT_SVG = os.path.join(ROOT_DIR, "veritas_algorithm_framework.svg")


def generate_diagram(dark_mode=False, output_path="algorithm_framework.png"):
    fig, ax = plt.subplots(figsize=(20, 11.5), dpi=300)

    bg_color = "#0b1329" if dark_mode else "#ffffff"
    text_primary = "#f8fafc" if dark_mode else "#0f172a"
    text_secondary = "#94a3b8" if dark_mode else "#475569"
    border_color = "#334155" if dark_mode else "#cbd5e1"

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Card background colors
    c_card_bg = "#131f3d" if dark_mode else "#f8fafc"
    c_card_edge = "#1e293b" if dark_mode else "#e2e8f0"

    # Accents
    c_green_bg = "#064e3b" if dark_mode else "#ecfdf5"
    c_green_edge = "#10b981" if dark_mode else "#059669"
    c_green_txt = "#a7f3d0" if dark_mode else "#065f46"

    c_blue_bg = "#1e3a8a" if dark_mode else "#eff6ff"
    c_blue_edge = "#3b82f6" if dark_mode else "#2563eb"
    c_blue_txt = "#bfdbfe" if dark_mode else "#1e40af"

    c_amber_bg = "#78350f" if dark_mode else "#fef3c7"
    c_amber_edge = "#f59e0b" if dark_mode else "#d97706"
    c_amber_txt = "#fde68a" if dark_mode else "#92400e"

    c_pink_bg = "#831843" if dark_mode else "#fdf2f8"
    c_pink_edge = "#ec4899" if dark_mode else "#db2777"
    c_pink_txt = "#fbcfe8" if dark_mode else "#9d174d"

    c_brand = "#0d4734" if not dark_mode else "#059669"

    def draw_card(x, y, w, h, bg, edge, lw=1.5, rad=0.02):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0.2,rounding_size={rad*10}",
            facecolor=bg, edgecolor=edge, linewidth=lw, zorder=2
        )
        ax.add_patch(box)

    def draw_arrow(x1, y1, x2, y2, color=c_brand, lw=2.0, dashed=False):
        ls = "--" if dashed else "-"
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, mutation_scale=15),
            zorder=4
        )

    # -------------------------------------------------------------
    # Title Header
    # -------------------------------------------------------------
    ax.text(50, 97, "VERITAS: MATHEMATICAL FRAMEWORK & ALGORITHMIC ARCHITECTURE",
            ha="center", va="center", fontsize=15, fontweight="bold", color=text_primary)
    ax.text(50, 94.5, "Analysis & Algorithmic Formulation for Continuous Discovery, SCM Mechanism Learning, Counterfactuals & XAI",
            ha="center", va="center", fontsize=9, color=text_secondary)

    # -------------------------------------------------------------
    # MODULE 1: Continuous Causal Discovery (NOTEARS)
    # -------------------------------------------------------------
    draw_card(3, 53, 44, 38, c_green_bg, c_green_edge)
    ax.text(5.5, 88, "1. CONTINUOUS CAUSAL DISCOVERY (NOTEARS)", fontsize=11, fontweight="bold", color=c_green_txt)
    ax.text(5.5, 85.5, "Reformulates DAG search from combinatorial discrete graph space O(d!) into smooth optimization:", fontsize=8, color=text_secondary)

    # Math Box 1
    draw_card(5, 71, 40, 12, bg_color, c_green_edge, lw=1.2)
    ax.text(25, 80, r"$\min_{W \in \mathbb{R}^{d \times d}} \frac{1}{2n} \|X - XW\|_F^2 + \lambda \|W\|_1$",
            ha="center", va="center", fontsize=11, fontweight="bold", color=text_primary)
    ax.text(25, 74.5, r"$\text{subject to } \quad h(W) = \text{Tr}\left(e^{W \odot W}\right) - d = 0$",
            ha="center", va="center", fontsize=11, fontweight="bold", color=c_green_edge)

    ax.text(5.5, 68, "• Matrix Exponential Trace: counts closed walks of all lengths k via Tr((W o W)^k).", fontsize=7.8, color=text_primary)
    ax.text(5.5, 65.5, "• Exactly equals d if and only if the graph has ZERO directed cycles (Strict Acyclicity).", fontsize=7.8, color=text_primary)
    ax.text(5.5, 63, "• Optimization: Solved via Augmented Lagrangian with L-BFGS-B, followed by thresholding.", fontsize=7.8, color=text_primary)
    ax.text(5.5, 60.5, "• Human-in-the-Loop Integration: Domain expert reviews & corrects edge orientations via UI.", fontsize=7.8, fontweight="bold", color=c_green_txt)
    ax.text(5.5, 56.5, "Result: Verified Directed Acyclic Graph (DAG) G = (V, E) without exponential complexity.", fontsize=8, color=text_secondary)

    # -------------------------------------------------------------
    # MODULE 2: Structural Causal Model (SCM) Mechanism Learning
    # -------------------------------------------------------------
    draw_card(53, 53, 44, 38, c_blue_bg, c_blue_edge)
    ax.text(55.5, 88, "2. SCM MECHANISM LEARNING", fontsize=11, fontweight="bold", color=c_blue_txt)
    ax.text(55.5, 85.5, "Factorizes joint observational distribution according to verified causal DAG:", fontsize=8, color=text_secondary)

    # Math Box 2
    draw_card(55, 71, 40, 12, bg_color, c_blue_edge, lw=1.2)
    ax.text(75, 80, r"$P(X_1, \dots, X_d) = \prod_{i=1}^d P\left(X_i \mid \text{Parents}(X_i)\right)$",
            ha="center", va="center", fontsize=11, fontweight="bold", color=text_primary)
    ax.text(75, 74.5, r"$\text{Structural Equation: } X_i = f_i\left(\text{Parents}_i\right) + \epsilon_i$",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color=c_blue_edge)

    ax.text(55.5, 68, "• Root Continuous Nodes (No Parents): Empirical marginal priors N(mu_i, sigma_i^2) or KDE.", fontsize=7.8, color=text_primary)
    ax.text(55.5, 65.5, "• Child Continuous Nodes: Ridge structural regression; retains empirical residuals epsilon_i.", fontsize=7.8, color=text_primary)
    ax.text(55.5, 63, "• Child Categorical Nodes: Multinomial logistic regression P(X_i = c | Parents_i).", fontsize=7.8, color=text_primary)
    ax.text(55.5, 60.5, "• Decoupled Mechanisms: Invariance under interventions on other structural components.", fontsize=7.8, fontweight="bold", color=c_blue_txt)
    ax.text(55.5, 56.5, "Result: Fitted Structural Causal Model supporting both sampling and interventional calculus.", fontsize=8, color=text_secondary)

    # Connecting arrow between Module 1 & 2
    draw_arrow(47, 72, 53, 72, color=c_blue_edge)

    # Big fork arrows from top to bottom
    draw_arrow(25, 53, 20, 46, color=c_blue_edge)
    draw_arrow(75, 53, 50, 46, color=c_amber_edge)
    draw_arrow(75, 53, 80, 46, color=c_pink_edge)

    # -------------------------------------------------------------
    # MODULE 3: Path A - Ancestral Topological Generation
    # -------------------------------------------------------------
    draw_card(3, 4, 30, 40, c_blue_bg, c_blue_edge)
    ax.text(5, 41, "3. ANCESTRAL SAMPLING", fontsize=10, fontweight="bold", color=c_blue_txt)
    ax.text(5, 38.5, "Kahn's Topological Generation:", fontsize=7.8, color=text_secondary)

    draw_card(4.5, 27, 27, 9.5, bg_color, c_blue_edge, lw=1)
    ax.text(18, 33, r"$\text{Topological Order: } \{V_{(1)}, \dots, V_{(d)}\}$", ha="center", va="center", fontsize=8.5, color=text_primary)
    ax.text(18, 29.5, r"$\text{Sample causes before effects}$", ha="center", va="center", fontsize=8, color=c_blue_edge)

    ax.text(5, 23.5, "1. Kahn's algorithm extracts DAG order.", fontsize=7.5, color=text_primary)
    ax.text(5, 20.5, "2. Sample root noise epsilon_root ~ P_prior.", fontsize=7.5, color=text_primary)
    ax.text(5, 17.5, "3. Sequentially propagate downstream.", fontsize=7.5, color=text_primary)
    ax.text(5, 14.5, "4. Invert categorical encoders to text.", fontsize=7.5, color=text_primary)
    ax.text(5, 10.5, "• Guarantee: Zero invalid combinations", fontsize=7.5, fontweight="bold", color=c_blue_txt)
    ax.text(5, 8, "  (e.g. 19-yr-old with PhD is eliminated)", fontsize=7, color=text_secondary)

    # -------------------------------------------------------------
    # MODULE 4: Path B - Pearl's Counterfactual Engine
    # -------------------------------------------------------------
    draw_card(35, 4, 32, 40, c_amber_bg, c_amber_edge)
    ax.text(37, 41, "4. PEARL'S 3-STEP COUNTERFACTUALS", fontsize=10, fontweight="bold", color=c_amber_txt)
    ax.text(37, 38.5, "Row-Level What-If Causal Calculus:", fontsize=7.8, color=text_secondary)

    draw_card(36.5, 27, 29, 9.5, bg_color, c_amber_edge, lw=1)
    ax.text(51, 33, r"$\text{Intervention: } do(X_k = v')$", ha="center", va="center", fontsize=9, fontweight="bold", color=text_primary)
    ax.text(51, 29.5, r"$\epsilon_i^* = x_i^* - \hat{f}_i(\text{Parents}(x_i^*))$", ha="center", va="center", fontsize=8.5, color=c_amber_edge)

    ax.text(37, 23.5, "1. Abduction: Invert observed row noise epsilon^*", fontsize=7.5, fontweight="bold", color=c_amber_txt)
    ax.text(37, 20.5, "   (Preserves John's unique individual baseline).", fontsize=7, color=text_secondary)
    ax.text(37, 17.5, "2. Action: Sever parents of X_k; fix X_k = v'.", fontsize=7.5, fontweight="bold", color=c_amber_txt)
    ax.text(37, 14.5, "3. Prediction: Topologically recompute only", fontsize=7.5, fontweight="bold", color=c_amber_txt)
    ax.text(37, 12, "   downstream descendants with fixed epsilon^*.", fontsize=7, color=text_secondary)
    ax.text(37, 8.5, "• Invariant Ancestors: Causes (e.g. Age)", fontsize=7.5, fontweight="bold", color=c_amber_edge)
    ax.text(37, 6.5, "  remain strictly identical.", fontsize=7, color=text_secondary)

    # -------------------------------------------------------------
    # MODULE 5: Evaluation & XAI Attribution (TreeSHAP + C2ST)
    # -------------------------------------------------------------
    draw_card(69, 4, 28, 40, c_pink_bg, c_pink_edge)
    ax.text(71, 41, "5. XAI ATTRIBUTION (SHAP + C2ST)", fontsize=10, fontweight="bold", color=c_pink_txt)
    ax.text(71, 38.5, "Game-Theoretic Divergence Diagnosis:", fontsize=7.8, color=text_secondary)

    draw_card(70.5, 27, 25, 9.5, bg_color, c_pink_edge, lw=1)
    ax.text(83, 33, r"$\text{C2ST: } D(x) \to \{0, 1\}$", ha="center", va="center", fontsize=8.5, color=text_primary)
    ax.text(83, 29.5, r"$\phi_i = \sum_{S} \frac{|S|!(|F|-|S|-1)!}{|F|!} \Delta f$", ha="center", va="center", fontsize=8, color=c_pink_edge)

    ax.text(71, 23.5, "1. C2ST Discriminator: Real (0) vs Syn (1).", fontsize=7.5, color=text_primary)
    ax.text(71, 20.5, "2. Accuracy ~50% indicates gold fidelity.", fontsize=7.5, color=text_primary)
    ax.text(71, 17.5, "3. TreeSHAP computes Shapley values phi_i.", fontsize=7.5, color=text_primary)
    ax.text(71, 14.5, "4. Pinpoints exact features causing shift.", fontsize=7.5, color=text_primary)
    ax.text(71, 10.5, "• Actionable Diagnostics: Identifies weak", fontsize=7.5, fontweight="bold", color=c_pink_txt)
    ax.text(71, 8, "  mechanisms for targeted recalibration.", fontsize=7, color=text_secondary)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=bg_color, bbox_inches="tight")
    plt.close()
    print(f"Generated Algorithm Framework diagram at: {output_path}")


if __name__ == "__main__":
    generate_diagram(dark_mode=False, output_path=OUTPUT_PNG)
    generate_diagram(dark_mode=True, output_path=OUTPUT_DARK_PNG)
    generate_diagram(dark_mode=False, output_path=OUTPUT_SVG)
