import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Sparkles, 
  Upload, 
  Send, 
  BarChart, 
  CheckCircle2, 
  Key, 
  Settings, 
  Layers, 
  RefreshCw,
  Hash,
  Sliders
} from 'lucide-react';

export default function TextGenerationPage() {
  const [inputText, setInputText] = useState('');
  const [categoryInput, setCategoryInput] = useState('');
  const [records, setRecords] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  
  // Generation state
  const [selectedModel, setSelectedModel] = useState('local_synthesizer');
  const [sampleCount, setSampleCount] = useState(4);
  const [biasCategory, setBiasCategory] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [generating, setGenerating] = useState(false);
  const [syntheticResults, setSyntheticResults] = useState([]);
  const [explainability, setExplainability] = useState(null);

  useEffect(() => {
    loadDefaultTextCorpus();
  }, []);

  const loadDefaultTextCorpus = async () => {
    try {
      const res = await fetch('/api/text/load-default', { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setRecords(data.records || []);
        setAnalysis(data.profile || null);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddCustomText = async () => {
    if (!inputText.trim()) return;
    const newRecord = {
      text: inputText.trim(),
      category: categoryInput.trim() || 'General'
    };
    const updated = [newRecord, ...records];
    setRecords(updated);
    setInputText('');
    setCategoryInput('');

    // Re-analyze
    try {
      const res = await fetch('/api/text/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ records: updated })
      });
      if (res.ok) {
        const p = await res.json();
        setAnalysis(p);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    setSyntheticResults([]);
    setExplainability(null);

    try {
      const res = await fetch('/api/text/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          records: records,
          model_name: selectedModel,
          sample_count: sampleCount,
          bias_category: biasCategory || undefined,
          api_key: apiKey || undefined
        })
      });

      if (res.ok) {
        const data = await res.json();
        setSyntheticResults(data.results || []);
        setExplainability(data.explainability || null);
      } else {
        const err = await res.json();
        alert('Generation failed: ' + (err.detail || 'Error'));
      }
    } catch (e) {
      alert('Error during text generation: ' + e.message);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-stone-950 tracking-tight">Text Synthetic Data Generation</h1>
          <p className="text-xs text-stone-500 mt-0.5">
            Style-conditioned text generation with corpus profiling, LLM API backends, and vocabulary Jaccard explainability.
          </p>
        </div>

        <button
          onClick={loadDefaultTextCorpus}
          className="border border-stone-200 text-stone-700 hover:bg-stone-50 px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Reload Sample Corpus</span>
        </button>
      </div>

      {/* 2-Column: Upload/Paste on Left, Corpus Analysis on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Upload / Paste Input */}
        <div className="lg:col-span-6 bg-white p-5 rounded-2xl border border-stone-200/90 shadow-2xs space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-stone-900">Reference Corpus Samples</h2>
            <span className="text-xs text-stone-600 font-medium bg-stone-100 px-2 py-0.5 rounded-full">
              {records.length} examples loaded
            </span>
          </div>

          <div className="space-y-3">
            <textarea
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              placeholder="Paste sample review, support ticket, or feedback text here..."
              rows={3}
              className="w-full bg-stone-50 border border-stone-200 rounded-xl p-3 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900"
            />
            <div className="flex gap-2">
              <input
                type="text"
                value={categoryInput}
                onChange={e => setCategoryInput(e.target.value)}
                placeholder="Category / Tag (e.g. Usability, Bug, Feature)"
                className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3 py-1.5 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900"
              />
              <button
                onClick={handleAddCustomText}
                disabled={!inputText.trim()}
                className="bg-forest-900 hover:bg-forest-950 disabled:opacity-40 text-white px-4 py-1.5 rounded-xl text-xs font-semibold shrink-0 transition"
              >
                Add Sample
              </button>
            </div>
          </div>

          {/* Sample Snippets Preview List */}
          <div className="max-h-48 overflow-y-auto space-y-2 pt-2 border-t border-stone-100">
            {records.slice(0, 5).map((r, i) => (
              <div key={i} className="p-2.5 bg-stone-50/70 rounded-xl border border-stone-200/60 text-xs">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-[10px] uppercase text-forest-800 bg-forest-50 px-2 py-0.5 rounded">
                    {r.category || 'Feedback'}
                  </span>
                  <span className="text-[10px] text-stone-400">Sample #{i + 1}</span>
                </div>
                <p className="text-stone-700 text-[11px] line-clamp-2 leading-relaxed">{r.text}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Corpus Profiling Summary */}
        <div className="lg:col-span-6 bg-white p-5 rounded-2xl border border-stone-200/90 shadow-2xs space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-stone-900">Corpus Statistical Profile</h2>
            <span className="text-xs text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full font-medium">
              Tone: {analysis?.detected_tone || 'Neutral'}
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <div className="bg-stone-50 p-3 rounded-xl border border-stone-200/60">
              <div className="text-[10px] text-stone-500 font-semibold uppercase">Avg Word Count</div>
              <div className="text-lg font-bold text-stone-900 mt-0.5">
                {analysis?.avg_word_count || 18} words
              </div>
            </div>
            <div className="bg-stone-50 p-3 rounded-xl border border-stone-200/60">
              <div className="text-[10px] text-stone-500 font-semibold uppercase">Vocabulary Size</div>
              <div className="text-lg font-bold text-stone-900 mt-0.5">
                {analysis?.vocab_size || 140} tokens
              </div>
            </div>
            <div className="bg-stone-50 p-3 rounded-xl border border-stone-200/60 col-span-2 sm:col-span-1">
              <div className="text-[10px] text-stone-500 font-semibold uppercase">Char Span</div>
              <div className="text-lg font-bold text-stone-900 mt-0.5">
                {analysis?.avg_char_count || 115} chars
              </div>
            </div>
          </div>

          {/* Top Keywords */}
          <div>
            <div className="text-xs font-semibold text-stone-700 mb-2">Dominant Vocabulary Keywords:</div>
            <div className="flex flex-wrap gap-1.5">
              {analysis?.top_keywords?.slice(0, 10).map((kw, i) => (
                <span key={i} className="text-[11px] bg-stone-100 border border-stone-200/60 text-stone-700 px-2 py-0.5 rounded-md">
                  {kw.word} <span className="text-stone-400 text-[10px]">({kw.count})</span>
                </span>
              )) || <span className="text-xs text-stone-400">Loading keywords...</span>}
            </div>
          </div>

          {/* Label Distribution */}
          <div>
            <div className="text-xs font-semibold text-stone-700 mb-2">Category Proportions:</div>
            <div className="space-y-1.5 text-[11px]">
              {analysis?.label_distribution && Object.entries(analysis.label_distribution).map(([cat, pct]) => (
                <div key={cat} className="flex items-center justify-between">
                  <span className="text-stone-600">{cat}</span>
                  <span className="font-semibold text-forest-900">{Math.round(pct * 100)}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>

      {/* Generator Configuration Bar */}
      <div className="bg-white p-5 rounded-2xl border border-stone-200/90 shadow-2xs space-y-4">
        <h2 className="text-sm font-bold text-stone-900">Configure Text Synthesis Backend</h2>

        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          {/* Model Backend */}
          <div>
            <label className="block text-xs font-semibold text-stone-700 mb-1">
              Synthesis Backend:
            </label>
            <select
              value={selectedModel}
              onChange={e => setSelectedModel(e.target.value)}
              className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3 py-2 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900"
            >
              <option value="local_synthesizer">Veritas Local Engine (Zero Key Needed)</option>
              <option value="groq_llama3">Groq (Llama 3.1 8B - Fast Free Tier)</option>
              <option value="gemini_flash">Google Gemini (1.5 Flash - Free Tier)</option>
            </select>
          </div>

          {/* Sample count */}
          <div>
            <label className="block text-xs font-semibold text-stone-700 mb-1">
              Generate Count:
            </label>
            <select
              value={sampleCount}
              onChange={e => setSampleCount(Number(e.target.value))}
              className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3 py-2 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900"
            >
              <option value={3}>3 synthetic texts</option>
              <option value={5}>5 synthetic texts</option>
              <option value={8}>8 synthetic texts</option>
            </select>
          </div>

          {/* Category bias */}
          <div>
            <label className="block text-xs font-semibold text-stone-700 mb-1">
              Optional Category Bias:
            </label>
            <input
              type="text"
              value={biasCategory}
              onChange={e => setBiasCategory(e.target.value)}
              placeholder="e.g. Usability, Performance"
              className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3 py-2 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900"
            />
          </div>

          {/* API key if cloud */}
          <div>
            <label className="block text-xs font-semibold text-stone-700 mb-1">
              {selectedModel === 'local_synthesizer' ? 'API Key:' : 'Provider API Key (Optional):'}
            </label>
            <input
              type="password"
              value={apiKey}
              disabled={selectedModel === 'local_synthesizer'}
              onChange={e => setApiKey(e.target.value)}
              placeholder={selectedModel === 'local_synthesizer' ? 'Not needed for Local Engine' : 'Enter Groq or Gemini key'}
              className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3 py-2 text-xs text-stone-800 focus:outline-none focus:ring-1 focus:ring-forest-900 disabled:opacity-50"
            />
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="bg-forest-900 hover:bg-forest-950 disabled:opacity-50 text-white px-6 py-2.5 rounded-xl font-semibold text-xs flex items-center gap-2 shadow-xs transition cursor-pointer"
          >
            {generating ? (
              <>
                <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Generating Synthetic Text...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Synthesize Text</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Synthetic Text Results & Explainability */}
      {syntheticResults.length > 0 && (
        <div className="space-y-6 animate-fade-in">
          
          {/* Text Explainability Scorecard */}
          {explainability && (
            <div className="bg-white p-5 rounded-2xl border border-emerald-300 shadow-sm space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-stone-100">
                <div>
                  <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-full">
                    Text Fidelity Scorecard
                  </span>
                  <h3 className="font-bold text-stone-900 text-base mt-1">
                    Distribution Alignment: {Math.round(explainability.overall_text_fidelity * 100)}%
                  </h3>
                </div>
                <div className="text-xs text-stone-500">
                  Real vs Synthetic Vocabulary & Length
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                <div className="bg-stone-50 p-3 rounded-xl border border-stone-200/60">
                  <div className="text-stone-500 font-semibold">Vocabulary Overlap (Jaccard)</div>
                  <div className="text-lg font-bold text-forest-900 mt-1">
                    {Math.round(explainability.vocabulary_jaccard_similarity * 100)}%
                  </div>
                  <div className="text-[10px] text-stone-400 mt-0.5">{explainability.shared_vocab_count} tokens shared</div>
                </div>

                <div className="bg-stone-50 p-3 rounded-xl border border-stone-200/60">
                  <div className="text-stone-500 font-semibold">Real vs Syn Avg Length</div>
                  <div className="text-lg font-bold text-forest-900 mt-1">
                    {explainability.real_avg_length} vs {explainability.synthetic_avg_length} words
                  </div>
                  <div className="text-[10px] text-stone-400 mt-0.5">{Math.round(explainability.length_alignment_score * 100)}% length similarity</div>
                </div>

                <div className="bg-stone-50 p-3 rounded-xl border border-stone-200/60 flex items-center">
                  <p className="text-[11px] text-stone-600 leading-snug">
                    {explainability.explanation}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Generated Text Items Cards */}
          <div className="bg-white p-6 rounded-2xl border border-stone-200/90 shadow-2xs space-y-4">
            <h3 className="font-bold text-stone-900 text-sm">Generated Synthetic Items:</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {syntheticResults.map((item, idx) => (
                <div key={idx} className="p-4 bg-stone-50/70 border border-stone-200/80 rounded-xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] uppercase font-bold text-forest-900 bg-forest-50 px-2 py-0.5 rounded border border-forest-100">
                      {item.category || 'Synthetic'}
                    </span>
                    <span className="text-[10px] text-stone-400">Generated #{idx + 1}</span>
                  </div>
                  <p className="text-xs text-stone-800 leading-relaxed font-normal">
                    "{item.text}"
                  </p>
                  <div className="text-[10px] text-stone-400 text-right">
                    {item.text.split(' ').length} words
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
