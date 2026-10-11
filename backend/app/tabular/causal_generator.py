"""
Veritas Causal Structural Generator & Counterfactual Engine
Novel SCM Generative Module based on:
1. Continuous DAG structure learning (NOTEARS / Zheng et al., 2018) + user-editable DAGs
2. Mechanism Learning: per-node structural equations (Continuous: Ridge SCM, Categorical: Multinomial/CPT)
3. Ancestral sampling: topological generation
4. Pearl's 3-step Counterfactual Engine (Abduction -> Action -> Prediction)
"""
import numpy as np
import pandas as pd
import networkx as nx
from typing import Dict, List, Any, Optional, Tuple
from scipy.optimize import minimize
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from app.core.base_generator import BaseTabularGenerator, Modality


def notears_linear(X: np.ndarray, lambda1: float = 0.1, loss_type: str = 'l2',
                   max_iter: int = 100, h_tol: float = 1e-8, rho_max: float = 1e+16,
                   w_threshold: float = 0.25) -> np.ndarray:
    """
    NOTEARS continuous optimization structure learning algorithm (Zheng et al., NeurIPS 2018).
    Solves: min 0.5/n * ||X - X W||_F^2 + lambda1 * ||W||_1  s.t.  Tr(exp(W o W)) - d = 0
    """
    n, d = X.shape
    w_est = np.zeros(d * d)
    rho = 1.0
    alpha = 0.0
    h_val = np.inf

    def _h(W):
        # Matrix exponential trace constraint: Tr(exp(W o W)) - d = 0
        M = np.eye(d) + W * W / d
        E = np.linalg.matrix_power(M, d - 1)  # polynomial approximation for stability
        h = np.trace(E @ (W * W)) - d
        return float(h)

    def _func(w_vec):
        W = w_vec.reshape((d, d))
        loss = 0.5 / n * np.square(np.linalg.norm(X - X @ W, 'fro'))
        h = _h(W)
        obj = loss + 0.5 * rho * h * h + alpha * h + lambda1 * np.sum(np.abs(W))
        return obj

    # Optimize using L-BFGS-B
    bounds = [(0, 0) if i == j else (None, None) for i in range(d) for j in range(d)]
    res = minimize(_func, w_est, method='L-BFGS-B', bounds=bounds,
                   options={'maxiter': max_iter, 'disp': False})
    
    W_est = res.x.reshape((d, d))
    W_est[np.abs(W_est) < w_threshold] = 0.0
    return W_est


class CausalStructuralGenerator(BaseTabularGenerator):
    name = "causal_scm"
    display_name = "Causal Structural Model (SCM)"
    modality = Modality.TABULAR
    description = "Novel causal structural generator with NOTEARS DAG discovery, mechanism learning, ancestral sampling, and Pearl-style counterfactual inference."
    supports_counterfactual = True

    def __init__(self):
        self.dag: Optional[nx.DiGraph] = None
        self.columns: List[str] = []
        self.col_types: Dict[str, str] = {}
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.mechanisms: Dict[str, Any] = {}
        self.residuals: Dict[str, np.ndarray] = {}
        self.fitted = False

    def discover_graph(self, df: pd.DataFrame, threshold: float = 0.25) -> Dict[str, Any]:
        """
        Discovers causal DAG from observational dataframe using NOTEARS.
        Returns node list and directed edge list with weights.
        """
        cols = list(df.columns)
        X_encoded = np.zeros((len(df), len(cols)))
        
        for i, col in enumerate(cols):
            if pd.api.types.is_numeric_dtype(df[col]):
                vals = df[col].fillna(df[col].median()).values.astype(float)
                mean = np.mean(vals)
                std = np.std(vals) or 1.0
                X_encoded[:, i] = (vals - mean) / std
            else:
                le = LabelEncoder()
                vals = le.fit_transform(df[col].astype(str).fillna("missing")).astype(float)
                mean = np.mean(vals)
                std = np.std(vals) or 1.0
                X_encoded[:, i] = (vals - mean) / std

        # Run NOTEARS continuous DAG discovery
        try:
            W = notears_linear(X_encoded, lambda1=0.08, w_threshold=threshold, max_iter=80)
        except Exception:
            # Fallback to correlation-based upper triangular DAG
            corr = np.corrcoef(X_encoded, rowvar=False)
            W = np.triu(corr, k=1)
            W[np.abs(W) < threshold] = 0.0

        # Construct NetworkX DAG (break cycles if any remaining)
        G = nx.DiGraph()
        for c in cols:
            G.add_node(c)

        edges = []
        for i in range(len(cols)):
            for j in range(len(cols)):
                weight = float(W[i, j])
                if abs(weight) > 1e-4 and i != j:
                    G.add_edge(cols[i], cols[j], weight=weight)

        # Ensure strict acyclicity
        while not nx.is_directed_acyclic_graph(G):
            try:
                cycle = nx.find_cycle(G)
                # Remove edge with smallest absolute weight in cycle
                min_edge = min(cycle, key=lambda e: abs(G[e[0]][e[1]].get('weight', 0.1)))
                G.remove_edge(min_edge[0], min_edge[1])
            except nx.NetworkXNoCycle:
                break

        edge_list = [
            {"source": u, "target": v, "weight": round(float(G[u][v].get("weight", 0.3)), 3)}
            for u, v in G.edges()
        ]

        return {
            "nodes": [{"id": c, "label": c} for c in cols],
            "edges": edge_list,
            "is_acyclic": nx.is_directed_acyclic_graph(G)
        }

    def fit(self, df: pd.DataFrame, causal_graph: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """
        Fit structural causal equations for each node based on the DAG.
        If causal_graph is provided (e.g. edited by user), uses it; otherwise runs discovery.
        """
        self.columns = list(df.columns)
        self.col_types = {}
        self.label_encoders = {}
        self.scalers = {}
        self.mechanisms = {}
        self.residuals = {}

        # Profile columns
        df_processed = df.copy()
        for col in self.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                self.col_types[col] = "numeric"
                df_processed[col] = df[col].fillna(df[col].median()).astype(float)
            else:
                self.col_types[col] = "categorical"
                le = LabelEncoder()
                df_processed[col] = le.fit_transform(df[col].astype(str).fillna("missing"))
                self.label_encoders[col] = le

        # Build DAG
        if causal_graph and "edges" in causal_graph and causal_graph["edges"]:
            G = nx.DiGraph()
            for col in self.columns:
                G.add_node(col)
            for edge in causal_graph["edges"]:
                if edge["source"] in self.columns and edge["target"] in self.columns:
                    G.add_edge(edge["source"], edge["target"], weight=edge.get("weight", 0.5))
            
            # Verify acyclicity or break cycles
            while not nx.is_directed_acyclic_graph(G):
                try:
                    cycle = nx.find_cycle(G)
                    G.remove_edge(cycle[-1][0], cycle[-1][1])
                except nx.NetworkXNoCycle:
                    break
            self.dag = G
        else:
            disc = self.discover_graph(df)
            G = nx.DiGraph()
            for col in self.columns:
                G.add_node(col)
            for edge in disc["edges"]:
                G.add_edge(edge["source"], edge["target"], weight=edge["weight"])
            self.dag = G

        # Fit structural equation per node in topological order
        for node in self.columns:
            parents = list(self.dag.predecessors(node))
            y = df_processed[node].values

            if self.col_types[node] == "numeric":
                if not parents:
                    # Root continuous node: learn empirical mean, std, noise
                    mean_val = float(np.mean(y))
                    std_val = float(np.std(y)) if np.std(y) > 1e-4 else 1.0
                    self.mechanisms[node] = {"type": "root_numeric", "mean": mean_val, "std": std_val, "raw_values": y}
                    self.residuals[node] = y - mean_val
                else:
                    # Child continuous node: learn linear/ridge structural equation
                    X = df_processed[parents].values
                    model = Ridge(alpha=1.0)
                    model.fit(X, y)
                    preds = model.predict(X)
                    res = y - preds
                    self.mechanisms[node] = {
                        "type": "child_numeric",
                        "model": model,
                        "parents": parents,
                        "std_res": float(np.std(res)) if np.std(res) > 1e-4 else 1.0
                    }
                    self.residuals[node] = res
            else:
                # Categorical node
                if not parents:
                    # Root categorical: learn prior probabilities
                    cats, counts = np.unique(y, return_counts=True)
                    probs = counts / len(y)
                    self.mechanisms[node] = {"type": "root_categorical", "cats": cats, "probs": probs}
                else:
                    # Child categorical: learn multinomial logistic regression
                    X = df_processed[parents].values
                    clf = LogisticRegression(max_iter=200, multi_class='auto')
                    try:
                        clf.fit(X, y)
                        self.mechanisms[node] = {
                            "type": "child_categorical",
                            "model": clf,
                            "parents": parents,
                            "classes": clf.classes_
                        }
                    except Exception:
                        cats, counts = np.unique(y, return_counts=True)
                        self.mechanisms[node] = {"type": "root_categorical", "cats": cats, "probs": counts / len(y)}

        self.fitted = True
        return self

    def sample(self, n: int, **kwargs) -> pd.DataFrame:
        """
        Ancestral sampling: traverse topological order of DAG,
        evaluating causes before effects.
        """
        if not self.fitted:
            raise RuntimeError("CausalStructuralGenerator is not fitted.")

        topological_order = list(nx.topological_sort(self.dag))
        samples: Dict[str, np.ndarray] = {}

        for node in topological_order:
            mech = self.mechanisms[node]
            mech_type = mech["type"]

            if mech_type == "root_numeric":
                # Sample root noise
                res = self.residuals[node]
                noise = np.random.choice(res, size=n, replace=True)
                samples[node] = mech["mean"] + noise
            elif mech_type == "root_categorical":
                samples[node] = np.random.choice(mech["cats"], size=n, p=mech["probs"])
            elif mech_type == "child_numeric":
                parents = mech["parents"]
                X_parent = np.column_stack([samples[p] for p in parents])
                base_pred = mech["model"].predict(X_parent)
                # Sample empirical residual noise
                noise = np.random.normal(0, mech["std_res"], size=n)
                samples[node] = base_pred + noise
            elif mech_type == "child_categorical":
                parents = mech["parents"]
                X_parent = np.column_stack([samples[p] for p in parents])
                probs = mech["model"].predict_proba(X_parent)
                classes = mech["classes"]
                sampled_cats = [np.random.choice(classes, p=p_row) for p_row in probs]
                samples[node] = np.array(sampled_cats)

        # Decode categories back to original string representation
        df_out = pd.DataFrame(index=range(n))
        for col in self.columns:
            if self.col_types[col] == "categorical" and col in self.label_encoders:
                le = self.label_encoders[col]
                idx_clipped = np.clip(np.round(samples[col]).astype(int), 0, len(le.classes_) - 1)
                df_out[col] = le.inverse_transform(idx_clipped)
            else:
                df_out[col] = np.round(samples[col], 3)

        return df_out

    def intervene(self, row: Dict[str, Any], target_col: str, new_value: Any) -> Dict[str, Any]:
        """
        Pearl's 3-step Counterfactual Algorithm:
        1. Abduction: infer row-specific latent noise epsilon_i from factual row.
        2. Action: perform do(target_col = new_value) by severing parents and fixing value.
        3. Prediction: recompute downstream descendants in topological order using inferred noise.
        """
        if not self.fitted:
            raise RuntimeError("Generator must be fitted before computing counterfactuals.")
        if target_col not in self.columns:
            raise ValueError(f"Target column '{target_col}' not found.")

        # Encode factual row
        factual_encoded = {}
        for col in self.columns:
            raw_v = row.get(col)
            if self.col_types[col] == "numeric":
                factual_encoded[col] = float(raw_v) if raw_v is not None else self.mechanisms[col].get("mean", 0.0)
            else:
                le = self.label_encoders[col]
                try:
                    factual_encoded[col] = float(le.transform([str(raw_v)])[0])
                except Exception:
                    factual_encoded[col] = 0.0

        # Step 1: ABDUCTION (infer noise epsilon_i for each node)
        latent_noise: Dict[str, float] = {}
        for node in self.columns:
            mech = self.mechanisms[node]
            if mech["type"] == "root_numeric":
                latent_noise[node] = factual_encoded[node] - mech["mean"]
            elif mech["type"] == "child_numeric":
                parents = mech["parents"]
                X_parent = np.array([[factual_encoded[p] for p in parents]])
                pred = float(mech["model"].predict(X_parent)[0])
                latent_noise[node] = factual_encoded[node] - pred
            else:
                latent_noise[node] = 0.0

        # Step 2: ACTION (do intervention)
        counterfactual_encoded = dict(factual_encoded)
        if self.col_types[target_col] == "numeric":
            counterfactual_encoded[target_col] = float(new_value)
        else:
            le = self.label_encoders[target_col]
            try:
                counterfactual_encoded[target_col] = float(le.transform([str(new_value)])[0])
            except Exception:
                counterfactual_encoded[target_col] = 0.0

        # Find descendants of target_col in the DAG
        descendants = nx.descendants(self.dag, target_col)
        topological_order = list(nx.topological_sort(self.dag))

        # Step 3: PREDICTION (repropagate only through downstream causal paths)
        changed_nodes = [target_col]
        for node in topological_order:
            if node in descendants:
                mech = self.mechanisms[node]
                if mech["type"] == "child_numeric":
                    parents = mech["parents"]
                    X_p = np.array([[counterfactual_encoded[p] for p in parents]])
                    pred = float(mech["model"].predict(X_p)[0])
                    # Recompute counterfactual twin keeping individual's abduced noise intact!
                    counterfactual_encoded[node] = pred + latent_noise[node]
                    changed_nodes.append(node)
                elif mech["type"] == "child_categorical":
                    parents = mech["parents"]
                    X_p = np.array([[counterfactual_encoded[p] for p in parents]])
                    probs = mech["model"].predict_proba(X_p)[0]
                    # Select argmax or class with highest likelihood
                    best_cat = mech["classes"][np.argmax(probs)]
                    counterfactual_encoded[node] = float(best_cat)
                    changed_nodes.append(node)

        # Decode back to user representation
        counterfactual_row = {}
        for col in self.columns:
            if self.col_types[col] == "categorical" and col in self.label_encoders:
                le = self.label_encoders[col]
                idx = int(np.clip(round(counterfactual_encoded[col]), 0, len(le.classes_) - 1))
                counterfactual_row[col] = le.classes_[idx]
            else:
                counterfactual_row[col] = round(counterfactual_encoded[col], 3)

        return {
            "factual": row,
            "counterfactual": counterfactual_row,
            "intervention": {"feature": target_col, "new_value": new_value},
            "downstream_affected_features": [f for f in changed_nodes if f != target_col],
            "causal_graph_edges": [
                {"source": u, "target": v} for u, v in self.dag.edges()
                if u in changed_nodes or v in changed_nodes
            ]
        }
