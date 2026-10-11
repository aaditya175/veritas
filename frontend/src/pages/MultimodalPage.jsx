import React, { useState, useEffect } from 'react';
import { Layers, Image as ImageIcon, Video, Code, CheckCircle2, ArrowRight, ShieldCheck, Cpu, GitFork } from 'lucide-react';

export default function MultimodalPage() {
  const [imageBlueprint, setImageBlueprint] = useState(null);
  const [videoBlueprint, setVideoBlueprint] = useState(null);

  useEffect(() => {
    fetch('/api/multimodal/image/blueprint')
      .then(res => res.json())
      .then(data => setImageBlueprint(data))
      .catch(console.error);

    fetch('/api/multimodal/video/blueprint')
      .then(res => res.json())
      .then(data => setVideoBlueprint(data))
      .catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-stone-950 tracking-tight">Multimodal Architectural Hub</h1>
          <p className="text-xs text-stone-500 mt-0.5">
            Architected for future multimodal expansion without refactoring core platform systems.
          </p>
        </div>
      </div>

      {/* Multimodal Architecture Banner */}
      <div className="bg-forest-900 text-white p-6 rounded-2xl shadow-md space-y-3">
        <div className="flex items-center gap-2">
          <span className="text-xs uppercase font-bold tracking-wider text-emerald-300 bg-emerald-950 px-2.5 py-0.5 rounded-full border border-emerald-800">
            System Design Architecture
          </span>
          <span className="text-xs text-emerald-200">Decoupled Plugin Architecture</span>
        </div>
        <h2 className="text-xl font-bold">Plug-and-Play Multimodal Expansion (Zero Refactoring)</h2>
        <p className="text-xs text-stone-300 max-w-3xl leading-relaxed">
          The Veritas backend enforces an abstract <code>BaseGenerator</code> and central <code>GeneratorRegistry</code>. Adding Image (CausalVAE) or Video (Causal Diffusion) generators requires only inheriting from the base interface and registering via <code>GeneratorRegistry.register(model)</code>. The API routing, SQLite experiment tracking, and UI navigation are already configured.
        </p>
      </div>

      {/* Two Future Scope Modality Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Module 1: Image Generation */}
        <div className="bg-white p-6 rounded-2xl border border-stone-200/90 shadow-2xs space-y-4 relative overflow-hidden flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <div className="w-10 h-10 rounded-xl bg-forest-50 text-forest-900 flex items-center justify-center">
                <ImageIcon className="w-5 h-5" />
              </div>
              <span className="text-[11px] font-bold text-stone-500 bg-stone-100 px-2.5 py-1 rounded-full border border-stone-200">
                Coming Soon • Phase 4
              </span>
            </div>

            <h3 className="font-bold text-stone-900 text-lg">Causal Image Synthesis (CausalVAE)</h3>
            <p className="text-xs text-stone-500 leading-relaxed mt-1">
              Disentangled representation learning with structural causal equations over interpretable latent factors (lighting, camera pose, object dimensions).
            </p>

            <div className="mt-4 p-3.5 bg-stone-50 rounded-xl border border-stone-200/60 text-xs space-y-2">
              <div className="font-semibold text-stone-800 text-[11px] uppercase tracking-wider">
                Planned Causal Latent Factors:
              </div>
              <div className="flex flex-wrap gap-1.5">
                {['Illumination Angle', 'Object Azimuth', 'Scale / Size', 'Background Texture'].map(f => (
                  <span key={f} className="text-[10px] bg-white border border-stone-200 px-2 py-0.5 rounded text-stone-700">
                    {f}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-stone-100 text-xs text-stone-500 flex items-center justify-between">
            <span>Interface: <code>BaseImageGenerator</code></span>
            <span className="font-semibold text-forest-900">CVPR Blueprint</span>
          </div>
        </div>

        {/* Module 2: Video Generation */}
        <div className="bg-white p-6 rounded-2xl border border-stone-200/90 shadow-2xs space-y-4 relative overflow-hidden flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <div className="w-10 h-10 rounded-xl bg-forest-50 text-forest-900 flex items-center justify-center">
                <Video className="w-5 h-5" />
              </div>
              <span className="text-[11px] font-bold text-stone-500 bg-stone-100 px-2.5 py-1 rounded-full border border-stone-200">
                Coming Soon • Phase 5
              </span>
            </div>

            <h3 className="font-bold text-stone-900 text-lg">Causal Video Diffusion (Temporal SCM)</h3>
            <p className="text-xs text-stone-500 leading-relaxed mt-1">
              Physics-grounded spatiotemporal diffusion modeling frame transition causality and trajectory velocity counterfactual interventions.
            </p>

            <div className="mt-4 p-3.5 bg-stone-50 rounded-xl border border-stone-200/60 text-xs space-y-2">
              <div className="font-semibold text-stone-800 text-[11px] uppercase tracking-wider">
                Planned Interventional Dynamics:
              </div>
              <div className="flex flex-wrap gap-1.5">
                {['Velocity / Acceleration', 'Collision Dynamics', 'Weather / Environment', 'Camera Trajectory'].map(f => (
                  <span key={f} className="text-[10px] bg-white border border-stone-200 px-2 py-0.5 rounded text-stone-700">
                    {f}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-stone-100 text-xs text-stone-500 flex items-center justify-between">
            <span>Interface: <code>BaseVideoGenerator</code></span>
            <span className="font-semibold text-forest-900">NeurIPS Blueprint</span>
          </div>
        </div>

      </div>

      {/* Code Contract Display */}
      <div className="bg-stone-900 text-stone-100 p-5 rounded-2xl shadow-sm text-xs font-mono space-y-3">
        <div className="flex items-center justify-between text-stone-400 pb-2 border-b border-stone-800 text-[11px]">
          <span>core/base_generator.py & core/registry.py (Code Architecture)</span>
          <span className="text-emerald-400">Live in Veritas</span>
        </div>
        <pre className="overflow-x-auto text-[11px] leading-relaxed text-emerald-200">
{`# Multimodal registration contract:
class BaseImageGenerator(BaseGenerator):
    modality = Modality.IMAGE
    def fit(self, data): ...
    def sample(self, n): ...
    def intervene_latent(self, image_id, latent_factor, target_val): ...

# Registering a new future module anywhere in the app:
GeneratorRegistry.register(CausalVAEImageGenerator())
# -> Instantly accessible at /api/generators?modality=image`}
        </pre>
      </div>
    </div>
  );
}
