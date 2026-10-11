import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Key, Save, Check, ShieldCheck, Database, RefreshCw } from 'lucide-react';

export default function SettingsPage() {
  const [groqKey, setGroqKey] = useState('');
  const [geminiKey, setGeminiKey] = useState('');
  const [settingsStatus, setSettingsStatus] = useState(null);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const res = await fetch('/api/settings');
      if (res.ok) {
        const data = await res.json();
        setSettingsStatus(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          groq_api_key: groqKey || undefined,
          gemini_api_key: geminiKey || undefined
        })
      });
      if (res.ok) {
        setSavedSuccess(true);
        loadSettings();
        setGroqKey('');
        setGeminiKey('');
        setTimeout(() => setSavedSuccess(false), 3000);
      }
    } catch (e) {
      alert('Error saving settings: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-stone-950 tracking-tight">Platform Configuration & API Keys</h1>
        <p className="text-xs text-stone-500 mt-0.5">
          Configure optional free LLM keys for text generation. All tabular models and local text generation run 100% offline.
        </p>
      </div>

      {/* Free Tier API Keys Box */}
      <div className="bg-white p-6 rounded-2xl border border-stone-200/90 shadow-2xs space-y-5">
        <div className="flex items-center justify-between pb-3 border-b border-stone-100">
          <div className="flex items-center gap-2">
            <Key className="w-4 h-4 text-forest-800" />
            <h2 className="font-bold text-stone-900 text-sm">Free Tier LLM Providers (Text Module)</h2>
          </div>
          <span className="text-xs text-stone-400">Keys stored locally in SQLite</span>
        </div>

        {/* Groq Key Input */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-stone-800">
              Groq Cloud API Key (Llama 3.1)
            </label>
            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
              settingsStatus?.has_groq_api_key 
                ? 'bg-emerald-100 text-emerald-800' 
                : 'bg-stone-100 text-stone-500'
            }`}>
              {settingsStatus?.has_groq_api_key ? `Active (${settingsStatus.groq_masked})` : 'Not configured'}
            </span>
          </div>
          <input
            type="password"
            value={groqKey}
            onChange={e => setGroqKey(e.target.value)}
            placeholder="gsk_..."
            className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3.5 py-2 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900"
          />
          <p className="text-[11px] text-stone-500">
            Obtain a free key at <a href="https://console.groq.com" target="_blank" rel="noreferrer" className="text-forest-800 underline">console.groq.com</a>. Fast inference on open models.
          </p>
        </div>

        {/* Gemini Key Input */}
        <div className="space-y-2 pt-2 border-t border-stone-100">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-stone-800">
              Google Gemini API Key (Gemini 1.5 Flash)
            </label>
            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
              settingsStatus?.has_gemini_api_key 
                ? 'bg-emerald-100 text-emerald-800' 
                : 'bg-stone-100 text-stone-500'
            }`}>
              {settingsStatus?.has_gemini_api_key ? `Active (${settingsStatus.gemini_masked})` : 'Not configured'}
            </span>
          </div>
          <input
            type="password"
            value={geminiKey}
            onChange={e => setGeminiKey(e.target.value)}
            placeholder="AIza..."
            className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3.5 py-2 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900"
          />
          <p className="text-[11px] text-stone-500">
            Obtain a free key at <a href="https://aistudio.google.com" target="_blank" rel="noreferrer" className="text-forest-800 underline">aistudio.google.com</a>. Generous free tier.
          </p>
        </div>

        <div className="flex justify-end pt-2">
          <button
            onClick={handleSave}
            disabled={loading}
            className="bg-forest-900 hover:bg-forest-950 text-white px-5 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 shadow-xs transition cursor-pointer"
          >
            {savedSuccess ? <Check className="w-3.5 h-3.5 text-emerald-300" /> : <Save className="w-3.5 h-3.5" />}
            <span>{savedSuccess ? 'Settings Saved!' : 'Save Credentials'}</span>
          </button>
        </div>
      </div>

      {/* Local Environment Integrity */}
      <div className="bg-white p-5 rounded-2xl border border-stone-200/90 shadow-2xs space-y-3">
        <h3 className="font-bold text-stone-900 text-sm flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-700" />
          Zero-Cost Open-Source Architecture
        </h3>
        <p className="text-xs text-stone-600 leading-relaxed">
          Veritas is designed to run entirely locally using free and open-source tools: SDV, PyTorch CPU, NOTEARS optimization, Scikit-Learn, SHAP, and SQLite. No paid accounts, subscription tiers, or external databases are required to run the full comparative study.
        </p>
      </div>
    </div>
  );
}
