import React, { useState } from 'react';
import { 
  ArrowRight, 
  Play, 
  Database, 
  GitFork, 
  FileText, 
  ShieldCheck, 
  Sparkles, 
  BarChart3, 
  Check, 
  Cpu, 
  Layers,
  ArrowUpRight,
  ChevronRight,
  Sliders,
  Eye,
  Activity
} from 'lucide-react';
import Navbar from '../components/Navbar';

export default function LandingPage({ onLaunchPlatform }) {
  const [isVideoModalOpen, setIsVideoModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#fafbf9] text-stone-900 flex flex-col font-sans">
      {/* Top Navigation Bar */}
      <Navbar 
        activePage="landing" 
        setActivePage={() => {}} 
        onOpenApp={onLaunchPlatform} 
      />

      {/* ========================================================
          HERO SECTION — EXACT MATCH TO REFERENCE SCREENSHOT
         ======================================================== */}
      <section className="relative pt-12 pb-20 md:pt-16 md:pb-28 overflow-hidden">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
            
            {/* Left Hero Content */}
            <div className="lg:col-span-6 z-10">
              
              {/* Rounded pill-shaped badge */}
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-stone-200/90 bg-stone-100/60 text-stone-600 text-xs font-semibold tracking-wider uppercase mb-7 shadow-2xs">
                <span className="w-2 h-2 rounded-full bg-forest-900 inline-block animate-pulse" />
                <span>SYNTHETIC DATA • CAUSAL AI • EXPLAINABLE AI</span>
              </div>

              {/* Bold large headline */}
              <h1 className="text-5xl sm:text-6xl lg:text-[4rem] font-extrabold tracking-tight text-stone-950 leading-[1.08] mb-6">
                Generate <br />
                <span className="text-[#0d4734]">Synthetic Data</span> <br />
                That Makes Sense
              </h1>

              {/* Descriptive paragraph */}
              <p className="text-stone-600 text-lg md:text-xl leading-relaxed mb-9 max-w-xl">
                Veritas combines deep generative models with causal structure and explainable AI — so you can create realistic data, explore what-if scenarios, and understand why it looks the way it does.
              </p>

              {/* Side-by-side Call to Action buttons */}
              <div className="flex flex-wrap items-center gap-4 mb-14">
                <button
                  onClick={() => onLaunchPlatform('dashboard')}
                  className="bg-[#0d4734] hover:bg-[#073325] text-white px-7 py-3.5 rounded-xl font-semibold text-base flex items-center gap-2.5 shadow-sm transition hover:shadow-md cursor-pointer group"
                >
                  <span>Try Veritas</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                </button>

                <button
                  onClick={() => setIsVideoModalOpen(true)}
                  className="border border-stone-300 hover:border-stone-400 bg-white text-stone-800 px-6 py-3.5 rounded-xl font-semibold text-base flex items-center gap-2.5 shadow-2xs transition hover:bg-stone-50/80 cursor-pointer"
                >
                  <div className="w-5 h-5 rounded-full bg-stone-900 text-white flex items-center justify-center shrink-0">
                    <Play className="w-2.5 h-2.5 fill-current ml-0.5" />
                  </div>
                  <span>Watch Demo</span>
                </button>
              </div>

              {/* Feature Icons Row beneath hero — matching reference layout */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 pt-6 border-t border-stone-200/80">
                
                {/* 1. Multiple Generative Models */}
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl bg-forest-50 border border-forest-100 flex items-center justify-center text-forest-900 shrink-0">
                    <Database className="w-4 h-4" />
                  </div>
                  <div className="text-xs font-semibold text-stone-700 leading-snug">
                    Multiple<br />Generative Models
                  </div>
                </div>

                {/* 2. Causal Reasoning */}
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl bg-forest-50 border border-forest-100 flex items-center justify-center text-forest-900 shrink-0">
                    <GitFork className="w-4 h-4" />
                  </div>
                  <div className="text-xs font-semibold text-stone-700 leading-snug">
                    Causal<br />Reasoning
                  </div>
                </div>

                {/* 3. Explainable Results */}
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl bg-forest-50 border border-forest-100 flex items-center justify-center text-forest-900 shrink-0">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div className="text-xs font-semibold text-stone-700 leading-snug">
                    Explainable<br />Results
                  </div>
                </div>

                {/* 4. Privacy & Fairness Evaluation */}
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl bg-forest-50 border border-forest-100 flex items-center justify-center text-forest-900 shrink-0">
                    <ShieldCheck className="w-4 h-4" />
                  </div>
                  <div className="text-xs font-semibold text-stone-700 leading-snug">
                    Privacy &<br />Fairness Evaluation
                  </div>
                </div>

              </div>

            </div>

            {/* Right Hero Visual — matching the laptop scene in reference */}
            <div className="lg:col-span-6 relative flex justify-center lg:justify-end">
              <div className="relative w-full max-w-xl group">
                {/* Reference mockup visual container */}
                <div className="rounded-2xl overflow-hidden shadow-2xl border border-stone-200/80 bg-white">
                  <img 
                    src="/hero_laptop.jpg" 
                    alt="Veritas Causal Synthetic Data Platform Workspace" 
                    className="w-full h-auto object-cover transition-transform duration-700 group-hover:scale-[1.01]"
                  />
                </div>

                {/* Interactive floating launch pill */}
                <div 
                  onClick={() => onLaunchPlatform('dashboard')}
                  className="absolute -bottom-5 right-6 bg-white/95 backdrop-blur-md border border-stone-200 px-4 py-2.5 rounded-xl shadow-lg flex items-center gap-3 cursor-pointer hover:border-forest-600 transition"
                >
                  <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping" />
                  <div className="text-xs">
                    <span className="font-bold text-stone-900">Live Workspace Ready:</span>{' '}
                    <span className="text-forest-800 font-medium">employee_data.csv loaded</span>
                  </div>
                  <ArrowUpRight className="w-3.5 h-3.5 text-stone-400" />
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* ========================================================
          PLATFORM PILLARS & RESEARCH FOUNDATIONS
         ======================================================== */}
      <section id="features-section" className="py-20 bg-white border-y border-stone-200/70">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-xs font-bold uppercase tracking-widest text-forest-900 bg-forest-50 px-3.5 py-1.5 rounded-full border border-forest-100">
              Beyond Black-Box Generation
            </span>
            <h2 className="text-3xl md:text-4xl font-extrabold text-stone-950 mt-4 mb-4">
              Why Synthetic Data Needs Causal Reasoning
            </h2>
            <p className="text-stone-600 text-base md:text-lg">
              Standard deep generators model correlation, not causation. When you tweak a feature for what-if scenarios, correlation alone fails. Veritas embeds causal structure and explainability directly into synthesis.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="p-8 rounded-2xl bg-stone-50/70 border border-stone-200/80 hover:border-forest-300 transition hover:shadow-md flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-xl bg-forest-900 text-white flex items-center justify-center mb-6 shadow-xs">
                  <GitFork className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold text-stone-950 mb-3">
                  Human-in-the-Loop DAGs
                </h3>
                <p className="text-stone-600 text-sm leading-relaxed mb-4">
                  Runs continuous NOTEARS structure discovery to propose a causal Directed Acyclic Graph (DAG), then empowers domain experts to inspect, reverse, or add edges directly before training.
                </p>
              </div>
              <div className="text-xs font-semibold text-forest-900 flex items-center gap-1.5 pt-4 border-t border-stone-200">
                <span>NOTEARS continuous formulation</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </div>
            </div>

            {/* Feature 2 */}
            <div className="p-8 rounded-2xl bg-stone-50/70 border border-stone-200/80 hover:border-forest-300 transition hover:shadow-md flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-xl bg-forest-900 text-white flex items-center justify-center mb-6 shadow-xs">
                  <Sparkles className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold text-stone-950 mb-3">
                  Pearl's 3-Step Counterfactuals
                </h3>
                <p className="text-stone-600 text-sm leading-relaxed mb-4">
                  Select any row, perform an intervention (e.g. "What if this applicant held a Master's degree?"), and recompute downstream effects through structural equations using Abduction, Action, and Prediction.
                </p>
              </div>
              <div className="text-xs font-semibold text-forest-900 flex items-center gap-1.5 pt-4 border-t border-stone-200">
                <span>Exact latent noise abduction</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </div>
            </div>

            {/* Feature 3 */}
            <div className="p-8 rounded-2xl bg-stone-50/70 border border-stone-200/80 hover:border-forest-300 transition hover:shadow-md flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-xl bg-forest-900 text-white flex items-center justify-center mb-6 shadow-xs">
                  <BarChart3 className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold text-stone-950 mb-3">
                  SHAP Explainability Scorecard
                </h3>
                <p className="text-stone-600 text-sm leading-relaxed mb-4">
                  Train a Real vs Synthetic discriminator (C2ST) with SHAP feature attributions. Immediately diagnose which specific columns trigger distributional divergence between backends.
                </p>
              </div>
              <div className="text-xs font-semibold text-forest-900 flex items-center gap-1.5 pt-4 border-t border-stone-200">
                <span>Game-theoretic Shapley values</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================
          GENERATOR ZOO & MULTIMODAL ARCHITECTURE
         ======================================================== */}
      <section className="py-20 bg-[#fafbf9]">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-12">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full">
                Unified Plugin Registry
              </span>
              <h2 className="text-3xl font-extrabold text-stone-950 mt-3">
                The Veritas Generator Zoo
              </h2>
            </div>
            <p className="text-stone-500 text-sm max-w-md mt-2 md:mt-0">
              Pluggable model backends behind a unified interface: fit, sample, and intervene without modifying application logic.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            {/* Tabular Causal */}
            <div className="bg-white p-6 rounded-2xl border border-emerald-300/80 shadow-xs relative overflow-hidden">
              <div className="absolute top-0 right-0 bg-forest-900 text-white text-[10px] font-bold uppercase tracking-wider px-3 py-1 rounded-bl-xl">
                Core Contribution
              </div>
              <div className="text-xs font-bold text-forest-800 uppercase tracking-wider mb-2">Tabular SCM</div>
              <h4 className="text-lg font-bold text-stone-950 mb-2">Causal SCM Generator</h4>
              <p className="text-xs text-stone-600 mb-4 leading-relaxed">
                NOTEARS DAG discovery + per-node structural equations with ancestral topological sampling and counterfactuals.
              </p>
              <div className="flex items-center justify-between text-xs pt-3 border-t border-stone-100 font-medium">
                <span className="text-stone-500">Counterfactuals:</span>
                <span className="text-emerald-700 font-semibold">Native Support</span>
              </div>
            </div>

            {/* CTGAN Baseline */}
            <div className="bg-white p-6 rounded-2xl border border-stone-200 shadow-xs">
              <div className="text-xs font-bold text-stone-500 uppercase tracking-wider mb-2">GAN Baseline</div>
              <h4 className="text-lg font-bold text-stone-950 mb-2">CTGAN Synthesizer</h4>
              <p className="text-xs text-stone-600 mb-4 leading-relaxed">
                Conditional Generative Adversarial Network with mode-specific normalization for mixed continuous & discrete data.
              </p>
              <div className="flex items-center justify-between text-xs pt-3 border-t border-stone-100 font-medium">
                <span className="text-stone-500">Framework:</span>
                <span className="text-stone-700">PyTorch / SDV</span>
              </div>
            </div>

            {/* TVAE Baseline */}
            <div className="bg-white p-6 rounded-2xl border border-stone-200 shadow-xs">
              <div className="text-xs font-bold text-stone-500 uppercase tracking-wider mb-2">VAE Baseline</div>
              <h4 className="text-lg font-bold text-stone-950 mb-2">TVAE Synthesizer</h4>
              <p className="text-xs text-stone-600 mb-4 leading-relaxed">
                Variational Autoencoder optimizing Evidence Lower Bound (ELBO) over continuous distributions and embeddings.
              </p>
              <div className="flex items-center justify-between text-xs pt-3 border-t border-stone-100 font-medium">
                <span className="text-stone-500">Framework:</span>
                <span className="text-stone-700">PyTorch / SDV</span>
              </div>
            </div>

            {/* Gaussian Copula */}
            <div className="bg-white p-6 rounded-2xl border border-stone-200 shadow-xs">
              <div className="text-xs font-bold text-stone-500 uppercase tracking-wider mb-2">Statistical</div>
              <h4 className="text-lg font-bold text-stone-950 mb-2">Gaussian Copula</h4>
              <p className="text-xs text-stone-600 mb-4 leading-relaxed">
                Parametric copula modeling joint CDF with marginal distributions (Gaussian, Student-T, Beta, Uniform).
              </p>
              <div className="flex items-center justify-between text-xs pt-3 border-t border-stone-100 font-medium">
                <span className="text-stone-500">Latency:</span>
                <span className="text-stone-700">&lt; 1.0 sec</span>
              </div>
            </div>

          </div>

          {/* Text & Multimodal Roadmap Bar */}
          <div className="mt-8 p-6 rounded-2xl bg-stone-900 text-white flex flex-col md:flex-row items-center justify-between gap-6 shadow-md">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs uppercase font-bold tracking-wider text-emerald-400 bg-emerald-950/80 px-2 py-0.5 rounded">
                  Active
                </span>
                <h4 className="font-bold text-lg">Text Generation Module</h4>
                <span className="text-xs text-stone-400">• Style-conditioned synthesis via Groq & Gemini</span>
              </div>
              <p className="text-xs text-stone-300 max-w-2xl">
                Upload customer reviews, tickets, or feedback. Analyzes vocabulary overlap, tone, and sentence length distributions with automated prompt crafting.
              </p>
            </div>
            <button
              onClick={() => onLaunchPlatform('text_generation')}
              className="bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2.5 rounded-xl text-xs font-bold tracking-wide transition shrink-0 cursor-pointer"
            >
              Explore Text Engine
            </button>
          </div>

          {/* Future Multimodal Teaser Bar */}
          <div className="mt-4 p-5 rounded-2xl bg-white border border-stone-200 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-stone-600">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-stone-100 rounded-lg text-stone-600">
                <Layers className="w-4 h-4" />
              </div>
              <div>
                <span className="font-bold text-stone-900">Multimodal Architecture Extension Point:</span>{' '}
                Image (CausalVAE) and Video (Causal Diffusion) generator interfaces are already declared in the registry.
              </div>
            </div>
            <button
              onClick={() => onLaunchPlatform('multimodal')}
              className="font-semibold text-forest-800 hover:text-forest-950 flex items-center gap-1 shrink-0"
            >
              <span>View Architectural Blueprint</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

        </div>
      </section>

      {/* ========================================================
          FOOTER CALL TO ACTION
         ======================================================== */}
      <footer className="mt-auto py-12 bg-white border-t border-stone-200">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded-lg bg-forest-900 text-white flex items-center justify-center font-bold text-sm">
              V
            </div>
            <div>
              <div className="font-bold text-stone-900 text-sm">Veritas Platform</div>
              <div className="text-xs text-stone-500">Causally-Grounded, Explainable Synthetic Data</div>
            </div>
          </div>

          <div className="text-xs text-stone-500">
            Engineered for BE Major Project • Causal Inference & Deep Generative Models
          </div>

          <div>
            <button
              onClick={() => onLaunchPlatform('dashboard')}
              className="bg-forest-900 hover:bg-forest-950 text-white text-xs font-semibold px-4 py-2 rounded-lg transition"
            >
              Launch Dashboard
            </button>
          </div>
        </div>
      </footer>

      {/* Video Demo Modal */}
      {isVideoModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full p-6 shadow-2xl border border-stone-200">
            <div className="flex items-center justify-between pb-4 border-b border-stone-100">
              <h3 className="font-bold text-stone-900 text-lg flex items-center gap-2">
                <Play className="w-4 h-4 text-forest-800" />
                Veritas Walkthrough Overview
              </h3>
              <button 
                onClick={() => setIsVideoModalOpen(false)}
                className="text-stone-400 hover:text-stone-700 text-xl font-bold leading-none"
              >
                ×
              </button>
            </div>
            <div className="py-6 space-y-4 text-sm text-stone-600">
              <div className="p-4 bg-stone-50 rounded-xl border border-stone-200/60">
                <h4 className="font-bold text-stone-900 mb-1">1. Tabular Causal SCM Pipeline</h4>
                <p className="text-xs">Upload CSV dataset → Profile column distributions → Review & edit the NOTEARS causal graph → Ancestral sampling → Counterfactual queries.</p>
              </div>
              <div className="p-4 bg-stone-50 rounded-xl border border-stone-200/60">
                <h4 className="font-bold text-stone-900 mb-1">2. Multi-Model Benchmark Zoo</h4>
                <p className="text-xs">Compare Causal SCM against CTGAN, TVAE, and Gaussian Copula across Fidelity, Utility (TSTR), Privacy (DCR), and Fairness.</p>
              </div>
              <div className="p-4 bg-stone-50 rounded-xl border border-stone-200/60">
                <h4 className="font-bold text-stone-900 mb-1">3. Text Synthesis & XAI Diagnostics</h4>
                <p className="text-xs">Profile text corpus → Synthesize via Groq Llama 3 or Gemini → Examine vocabulary Jaccard similarity and SHAP feature importance.</p>
              </div>
            </div>
            <div className="flex justify-end gap-3 pt-3 border-t border-stone-100">
              <button
                onClick={() => { setIsVideoModalOpen(false); onLaunchPlatform('dashboard'); }}
                className="bg-forest-900 text-white px-5 py-2 rounded-xl text-xs font-semibold hover:bg-forest-950 transition"
              >
                Proceed to Live Workspace
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
