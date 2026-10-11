"""
Veritas Tabular Explainability Service
Implements SHAP-based feature attribution on a Real-vs-Synthetic C2ST discriminator
to explain WHY and WHERE synthetic data deviates from real data.
"""
import numpy as np
import pandas as pd
import shap
from typing import Dict, Any, List
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


class TabularExplainer:
    @staticmethod
    def explain_divergence(real_df: pd.DataFrame, syn_df: pd.DataFrame, max_samples: int = 200) -> Dict[str, Any]:
        """
        Trains a Real vs Synthetic (C2ST) discriminator, runs SHAP feature attribution,
        and returns column-level divergence drivers with human-interpretable reasoning.
        """
        cols = [c for c in real_df.columns if c in syn_df.columns]
        
        # Subsample for snappy SHAP computation
        n_r = min(len(real_df), max_samples)
        n_s = min(len(syn_df), max_samples)
        r_sub = real_df[cols].sample(n=n_r, random_state=42)
        s_sub = syn_df[cols].sample(n=n_s, random_state=42)

        # Preprocess features
        combined_df = pd.concat([r_sub, s_sub], ignore_index=True)
        X_mat = np.zeros((len(combined_df), len(cols)))
        encoders = {}

        for i, col in enumerate(cols):
            if pd.api.types.is_numeric_dtype(combined_df[col]):
                vals = combined_df[col].fillna(combined_df[col].median()).values.astype(float)
                mean = np.mean(vals)
                std = np.std(vals) or 1.0
                X_mat[:, i] = (vals - mean) / std
            else:
                le = LabelEncoder()
                vals = le.fit_transform(combined_df[col].astype(str).fillna("missing")).astype(float)
                mean = np.mean(vals)
                std = np.std(vals) or 1.0
                X_mat[:, i] = (vals - mean) / std
                encoders[col] = le

        # Label: 0 = Real, 1 = Synthetic
        y = np.array([0] * n_r + [1] * n_s)

        # Train C2ST Discriminator
        clf = RandomForestClassifier(n_estimators=35, max_depth=5, random_state=42)
        clf.fit(X_mat, y)

        # Discriminator accuracy (0.50 = perfectly indistinguishable; 1.00 = easily distinguishable)
        c2st_acc = float(np.mean(clf.predict(X_mat) == y))

        # Compute SHAP values
        feature_importance_list = []
        try:
            explainer = shap.TreeExplainer(clf)
            shap_values = explainer.shap_values(X_mat[n_r:])  # Explain synthetic row predictions
            
            # If binary classifier returns list of 2 arrays [class_0, class_1]
            if isinstance(shap_values, list):
                vals_syn = shap_values[1]
            elif len(shap_values.shape) == 3:
                vals_syn = shap_values[:, :, 1]
            else:
                vals_syn = shap_values

            mean_abs_shap = np.mean(np.abs(vals_syn), axis=0)
            total_shap = np.sum(mean_abs_shap) or 1.0
            normalized_importance = (mean_abs_shap / total_shap).tolist()

            for idx, col in enumerate(cols):
                feature_importance_list.append({
                    "feature": col,
                    "importance": round(float(normalized_importance[idx]), 4),
                    "mean_shap": round(float(mean_abs_shap[idx]), 4)
                })

        except Exception as e:
            # Fallback to Gini importance if SHAP fails on edge case
            gini_imp = clf.feature_importances_
            for idx, col in enumerate(cols):
                feature_importance_list.append({
                    "feature": col,
                    "importance": round(float(gini_imp[idx]), 4),
                    "mean_shap": round(float(gini_imp[idx]), 4)
                })

        # Sort descending by importance
        feature_importance_list.sort(key=lambda x: x["importance"], reverse=True)

        # Generate human-readable diagnostics for the top distinguishing features
        diagnostics = []
        for item in feature_importance_list[:3]:
            feat = item["feature"]
            imp_pct = round(item["importance"] * 100, 1)
            if pd.api.types.is_numeric_dtype(real_df[feat]):
                r_m = float(real_df[feat].mean())
                s_m = float(syn_df[feat].mean())
                r_std = float(real_df[feat].std())
                s_std = float(syn_df[feat].std())
                diag = f"'{feat}' accounts for {imp_pct}% of real-vs-synthetic divergence (Real Mean={r_m:.2f}, Syn Mean={s_m:.2f}; Real Std={r_std:.2f}, Syn Std={s_std:.2f})."
            else:
                top_real = real_df[feat].mode()[0] if not real_df[feat].empty else "N/A"
                top_syn = syn_df[feat].mode()[0] if not syn_df[feat].empty else "N/A"
                diag = f"'{feat}' accounts for {imp_pct}% of divergence (Dominant real mode: '{top_real}', synthetic mode: '{top_syn}')."
            diagnostics.append(diag)

        return {
            "c2st_discriminator_accuracy": round(c2st_acc, 3),
            "fidelity_verdict": "High fidelity: data is difficult to distinguish from real" if c2st_acc < 0.65 else "Moderate divergence detected by classifier",
            "feature_attributions": feature_importance_list,
            "top_divergence_insights": diagnostics
        }
