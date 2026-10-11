import React, { useState, useEffect } from 'react';
import { Database, Upload, FileText, CheckCircle2, AlertTriangle, Hash, Layers, ShieldAlert, RefreshCw } from 'lucide-react';

export default function DatasetPage({ dataset, onSelectDataset }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (dataset) {
      loadProfile(dataset.id);
    }
  }, [dataset]);

  const loadProfile = async (id) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/datasets/${id}`);
      if (res.ok) {
        const data = await res.json();
        setProfile(data.profile);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const res = await fetch('/api/datasets/upload', {
        method: 'POST',
        body: formData
      });
      if (res.ok) {
        const newDs = await res.json();
        onSelectDataset && onSelectDataset(newDs);
      }
    } catch (err) {
      alert('Upload failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-stone-950 tracking-tight">Dataset Profiling & Schema</h1>
          <p className="text-xs text-stone-500 mt-0.5">
            Statistical distribution profiling, data types, and sensitive attribute detection.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <label className="bg-forest-900 hover:bg-forest-950 text-white px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 shadow-xs cursor-pointer transition">
            <Upload className="w-3.5 h-3.5" />
            <span>Upload CSV Dataset</span>
            <input type="file" accept=".csv" onChange={handleFileUpload} className="hidden" />
          </label>
        </div>
      </div>

      {/* Dataset Summary Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-stone-200/90 shadow-2xs">
          <div className="text-xs text-stone-500 font-medium">Dataset Name</div>
          <div className="text-base font-bold text-stone-900 mt-1 truncate">
            {dataset?.name || 'employee_data.csv'}
          </div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-stone-200/90 shadow-2xs">
          <div className="text-xs text-stone-500 font-medium">Total Rows</div>
          <div className="text-2xl font-bold text-stone-900 mt-1">
            {profile?.row_count?.toLocaleString() || dataset?.row_count?.toLocaleString() || '300'}
          </div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-stone-200/90 shadow-2xs">
          <div className="text-xs text-stone-500 font-medium">Feature Columns</div>
          <div className="text-2xl font-bold text-stone-900 mt-1">
            {profile?.col_count || dataset?.col_count || '8'}
          </div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-stone-200/90 shadow-2xs">
          <div className="text-xs text-stone-500 font-medium">Memory Footprint</div>
          <div className="text-2xl font-bold text-stone-900 mt-1">
            {profile?.memory_mb ? `${profile.memory_mb} MB` : '< 1 MB'}
          </div>
        </div>
      </div>

      {/* Columns Profiling Table */}
      <div className="bg-white rounded-2xl border border-stone-200/90 shadow-2xs overflow-hidden">
        <div className="p-4 border-b border-stone-100 flex items-center justify-between">
          <h2 className="font-bold text-stone-900 text-sm">Feature Schema & Distributions</h2>
          <span className="text-xs text-stone-400">
            {profile?.columns?.length || 0} features inspected
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-stone-700">
            <thead className="bg-stone-50/80 text-stone-500 font-semibold uppercase tracking-wider text-[10px] border-b border-stone-200/70">
              <tr>
                <th className="py-3 px-4">Column Name</th>
                <th className="py-3 px-4">Type</th>
                <th className="py-3 px-4">Missing Values</th>
                <th className="py-3 px-4">Unique Cardinality</th>
                <th className="py-3 px-4">Summary Statistics</th>
                <th className="py-3 px-4">Fairness Audit</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-100">
              {profile?.columns?.map((col, idx) => (
                <tr key={idx} className="hover:bg-stone-50/60 transition">
                  <td className="py-3 px-4 font-semibold text-stone-900 flex items-center gap-2">
                    <Hash className="w-3.5 h-3.5 text-stone-400" />
                    <span>{col.name}</span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                      col.type === 'numeric'
                        ? 'bg-blue-50 text-blue-700 border border-blue-200/60'
                        : 'bg-amber-50 text-amber-700 border border-amber-200/60'
                    }`}>
                      {col.type}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-stone-600">
                    {col.null_count} ({col.null_pct}%)
                  </td>
                  <td className="py-3 px-4 text-stone-600">
                    {col.unique_count} distinct
                  </td>
                  <td className="py-3 px-4 text-stone-600">
                    {col.type === 'numeric' ? (
                      <span className="text-[11px]">
                        Mean: <strong>{col.mean}</strong> • Min: {col.min} • Max: {col.max}
                      </span>
                    ) : (
                      <span className="text-[11px] text-stone-500 truncate max-w-xs block">
                        Top: {Object.keys(col.top_categories || {}).join(', ')}
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4">
                    {col.is_sensitive ? (
                      <span className="inline-flex items-center gap-1 text-[11px] font-medium text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-full">
                        <ShieldAlert className="w-3 h-3 text-amber-600" />
                        Candidate Sensitive
                      </span>
                    ) : (
                      <span className="text-stone-400 text-[11px]">Standard</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
