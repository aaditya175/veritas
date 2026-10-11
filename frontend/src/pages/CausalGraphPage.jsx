import React, { useState, useEffect } from 'react';
import { GitFork, Save, RotateCcw, Check, Sparkles, AlertCircle, Info } from 'lucide-react';
import CausalGraphCanvas from '../components/CausalGraphCanvas';

export default function CausalGraphPage({ dataset }) {
  const [graph, setGraph] = useState({ nodes: [], edges: [] });
  const [loading, setLoading] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    if (dataset) {
      loadGraph(dataset.id);
    }
  }, [dataset]);

  const loadGraph = async (id) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/causal/${id}/graph`);
      if (res.ok) {
        const data = await res.json();
        setGraph(data || { nodes: [], edges: [] });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateGraph = (newGraph) => {
    setGraph(newGraph);
    setSavedSuccess(false);
  };

  const handleSaveGraph = async () => {
    if (!dataset) return;
    setLoading(true);
    try {
      const res = await fetch(`/api/causal/${dataset.id}/graph`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(graph)
      });
      if (res.ok) {
        setSavedSuccess(true);
        setTimeout(() => setSavedSuccess(false), 3000);
      }
    } catch (e) {
      alert('Save failed: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-stone-950 tracking-tight">Causal Graph Discovery & Editor</h1>
          <p className="text-xs text-stone-500 mt-0.5">
            Continuous NOTEARS optimization proposes the initial DAG. Inspect and correct dependencies to enforce domain reality.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => loadGraph(dataset.id)}
            className="border border-stone-200 text-stone-700 hover:bg-stone-50 px-3.5 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset to NOTEARS</span>
          </button>

          <button
            onClick={handleSaveGraph}
            className="bg-forest-900 hover:bg-forest-950 text-white px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 shadow-xs transition"
          >
            {savedSuccess ? <Check className="w-4 h-4 text-emerald-300" /> : <Save className="w-4 h-4" />}
            <span>{savedSuccess ? 'Saved to SCM!' : 'Save & Update SCM'}</span>
          </button>
        </div>
      </div>

      {/* Causal Methodology Info Banner */}
      <div className="bg-forest-50 border border-forest-200/80 p-4 rounded-2xl flex items-start gap-3 text-xs text-forest-950">
        <Sparkles className="w-4 h-4 text-forest-800 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Human-in-the-Loop Causal Grounding:</span> Purely statistical algorithms (CTGAN, TVAE) frequently learn spurious correlations (e.g. reverse causation). By correcting directed edges here, the downstream Causal SCM generator respects exact ancestral dependencies <code>X_i = f(Parents_i) + &epsilon;_i</code> during ancestral sampling and counterfactual evaluation.
        </div>
      </div>

      {/* Interactive Editor Canvas */}
      <CausalGraphCanvas
        nodes={graph.nodes || []}
        edges={graph.edges || []}
        onUpdateGraph={handleUpdateGraph}
        readOnly={false}
      />
    </div>
  );
}
