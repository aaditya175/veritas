import React, { useState, useEffect } from 'react';
import { 
  Sparkles, 
  ArrowRight, 
  RotateCw, 
  CheckCircle2, 
  Info, 
  GitFork, 
  Layers, 
  ArrowRightLeft,
  ChevronRight,
  ShieldCheck
} from 'lucide-react';

export default function CounterfactualPage({ dataset }) {
  const [rows, setRows] = useState([]);
  const [selectedRowIndex, setSelectedRowIndex] = useState(0);
  const [targetFeature, setTargetFeature] = useState('Education');
  const [newValue, setNewValue] = useState("Master's");
  const [counterfactualResult, setCounterfactualResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (dataset) {
      loadSampleRows(dataset.id);
    }
  }, [dataset]);

  const loadSampleRows = async (dsId) => {
    try {
      const res = await fetch(`/api/datasets/${dsId}`);
      if (res.ok) {
        const data = await res.json();
        const pRows = data.preview_rows || [];
        setRows(pRows);
        if (pRows.length > 0) {
          // Set sensible default intervention
          const firstRow = pRows[0];
          if (firstRow.Education) {
            setTargetFeature('Education');
            setNewValue(firstRow.Education === "Bachelor's" ? "Master's" : "PhD");
          }
        }
      }
    } catch (e) {
      console.error(e);
    }
  };

  const currentFactualRow = rows[selectedRowIndex] || {
    Education: "Bachelor's",
    Age: 24,
    Experience: 2.0,
    Occupation: "Developer",
    HoursPerWeek: 40,
    Department: "Engineering",
    Income: 65000,
    PerformanceScore: 4.2
  };

  const handleRunCounterfactual = async () => {
    if (!dataset || !currentFactualRow) return;
    setLoading(true);

    try {
      const res = await fetch(`/api/causal/${dataset.id}/counterfactual`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          row: currentFactualRow,
          target_feature: targetFeature,
          new_value: newValue
        })
      });

      if (res.ok) {
        const data = await res.json();
        setCounterfactualResult(data);
      } else {
        const err = await res.json();
        alert('Counterfactual calculation failed: ' + (err.detail || 'Error'));
      }
    } catch (e) {
      alert('Error: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  // Feature choices based on row keys
  const availableFeatures = Object.keys(currentFactualRow);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-stone-950 tracking-tight">Counterfactual "What-If" Explorer</h1>
          <p className="text-xs text-stone-500 mt-0.5">
            Intervene on an individual record using Pearl's 3-step causal calculus: Abduction → Action → Prediction.
          </p>
        </div>
      </div>

      {/* Pearl's 3-step banner */}
      <div className="bg-forest-50/80 border border-forest-200/90 p-4 rounded-2xl grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div className="flex items-start gap-2.5">
          <div className="w-5 h-5 rounded-full bg-forest-900 text-white flex items-center justify-center font-bold text-[10px] shrink-0">1</div>
          <div>
            <span className="font-bold text-forest-950">Step 1: Abduction</span>
            <p className="text-stone-600 mt-0.5">Infers the individual's latent background noise ε_i from factual observations.</p>
          </div>
        </div>
        <div className="flex items-start gap-2.5">
          <div className="w-5 h-5 rounded-full bg-forest-900 text-white flex items-center justify-center font-bold text-[10px] shrink-0">2</div>
          <div>
            <span className="font-bold text-forest-950">Step 2: Action</span>
            <p className="text-stone-600 mt-0.5">Performs intervention do(X = v) by severing parental incoming edges.</p>
          </div>
        </div>
        <div className="flex items-start gap-2.5">
          <div className="w-5 h-5 rounded-full bg-forest-900 text-white flex items-center justify-center font-bold text-[10px] shrink-0">3</div>
          <div>
            <span className="font-bold text-forest-950">Step 3: Prediction</span>
            <p className="text-stone-600 mt-0.5">Propagates downstream causal mechanisms while keeping non-descendants invariant.</p>
          </div>
        </div>
      </div>

      {/* Configuration Box */}
      <div className="bg-white p-5 rounded-2xl border border-stone-200/90 shadow-2xs space-y-4">
        <div className="text-sm font-bold text-stone-900">Configure Intervention Query</div>
        
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {/* Select Factual Row */}
          <div>
            <label className="block text-xs font-semibold text-stone-700 mb-1.5">
              1. Choose Factual Row from Real Data:
            </label>
            <select
              value={selectedRowIndex}
              onChange={e => {
                const idx = Number(e.target.value);
                setSelectedRowIndex(idx);
                setCounterfactualResult(null);
              }}
              className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3 py-2 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900"
            >
              {rows.map((r, i) => (
                <option key={i} value={i}>
                  Row #{i + 1} — {r.Occupation || 'Profile'} ({r.Education || 'Degree'}, Age {r.Age || 30})
                </option>
              ))}
            </select>
          </div>

          {/* Select Feature to Intervene On */}
          <div>
            <label className="block text-xs font-semibold text-stone-700 mb-1.5">
              2. Feature to Intervene on (do(X)):
            </label>
            <select
              value={targetFeature}
              onChange={e => {
                setTargetFeature(e.target.value);
                setCounterfactualResult(null);
              }}
              className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3 py-2 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900"
            >
              {availableFeatures.map(f => (
                <option key={f} value={f}>{f}</option>
              ))}
            </select>
          </div>

          {/* New Target Value */}
          <div>
            <label className="block text-xs font-semibold text-stone-700 mb-1.5">
              3. New Counterfactual Value:
            </label>
            <input
              type="text"
              value={newValue}
              onChange={e => setNewValue(e.target.value)}
              placeholder="e.g. PhD, Master's, 50, etc."
              className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3 py-2 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900"
            />
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            onClick={handleRunCounterfactual}
            disabled={loading}
            className="bg-forest-900 hover:bg-forest-950 disabled:opacity-50 text-white px-6 py-2.5 rounded-xl font-semibold text-xs flex items-center gap-2 shadow-xs transition cursor-pointer"
          >
            {loading ? (
              <>
                <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Abducing & Propagating...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Compute Counterfactual Twin</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Counterfactual Diff View */}
      {counterfactualResult && (
        <div className="bg-white p-6 rounded-2xl border border-emerald-300 shadow-sm space-y-5 animate-fade-in">
          <div className="flex items-center justify-between pb-3 border-b border-stone-100">
            <div>
              <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-full">
                Counterfactual Twin Recomputed
              </span>
              <h3 className="font-bold text-stone-900 text-lg mt-1.5 flex items-center gap-2">
                <span>Intervention:</span>
                <span className="text-forest-900 font-extrabold">do({targetFeature} = "{newValue}")</span>
              </h3>
            </div>

            <div className="text-xs text-stone-500 font-medium text-right">
              <div>Affected Downstream: <strong>{counterfactualResult.downstream_affected_features?.length || 0} features</strong></div>
              <div>Invariant Causes: <strong>{availableFeatures.length - 1 - (counterfactualResult.downstream_affected_features?.length || 0)} features</strong></div>
            </div>
          </div>

          {/* Side by side diff table */}
          <div className="overflow-x-auto border border-stone-100 rounded-xl">
            <table className="w-full text-left text-xs text-stone-700">
              <thead className="bg-stone-50/80 text-stone-500 font-semibold uppercase tracking-wider text-[10px] border-b border-stone-200">
                <tr>
                  <th className="py-3 px-4">Feature</th>
                  <th className="py-3 px-4">Factual (Observed)</th>
                  <th className="py-3 px-4">Counterfactual (Predicted Twin)</th>
                  <th className="py-3 px-4">Causal Mechanism State</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-stone-100">
                {availableFeatures.map(feat => {
                  const factualVal = counterfactualResult.factual?.[feat];
                  const counterVal = counterfactualResult.counterfactual?.[feat];
                  const isIntervened = feat === targetFeature;
                  const isAffected = counterfactualResult.downstream_affected_features?.includes(feat);
                  const isChanged = String(factualVal) !== String(counterVal);

                  return (
                    <tr 
                      key={feat} 
                      className={`transition ${
                        isIntervened 
                          ? 'bg-amber-50/50 font-semibold' 
                          : isAffected 
                          ? 'bg-emerald-50/40 font-medium' 
                          : 'hover:bg-stone-50/60'
                      }`}
                    >
                      <td className="py-3 px-4 font-bold text-stone-900">
                        {feat}
                      </td>
                      <td className="py-3 px-4 text-stone-600">
                        {typeof factualVal === 'number' ? factualVal.toLocaleString() : String(factualVal)}
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                          isIntervened
                            ? 'text-amber-800 bg-amber-100'
                            : isAffected
                            ? 'text-emerald-800 bg-emerald-100'
                            : 'text-stone-700'
                        }`}>
                          {typeof counterVal === 'number' ? counterVal.toLocaleString() : String(counterVal)}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        {isIntervened ? (
                          <span className="text-[11px] font-bold text-amber-700">
                            Intervened Target Node (Severed Parents)
                          </span>
                        ) : isAffected ? (
                          <span className="text-[11px] font-bold text-emerald-700 flex items-center gap-1">
                            <RotateCw className="w-3 h-3 text-emerald-600" />
                            Downstream Causal Effect Updated
                          </span>
                        ) : (
                          <span className="text-[11px] text-stone-400 flex items-center gap-1">
                            <ShieldCheck className="w-3 h-3 text-stone-400" />
                            Causally Invariant (Prior cause / non-descendant)
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Pearl formulation insight */}
          <div className="p-3.5 bg-stone-50 rounded-xl border border-stone-200/70 text-xs text-stone-600">
            <strong>Causal Grounding Verification:</strong> Notice that upstream ancestral features like <code>Age</code> remained strictly identical. Unlike black-box nearest-neighbor methods that perturb unrelated columns, the SCM preserves the applicant's unique latent noise vector &epsilon;, guaranteeing that only valid causal descendants were updated.
          </div>
        </div>
      )}
    </div>
  );
}
