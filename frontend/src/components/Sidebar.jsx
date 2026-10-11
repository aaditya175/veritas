import React from 'react';
import { 
  Home, 
  Database, 
  GitFork, 
  Cpu, 
  Table, 
  BarChart3, 
  HelpCircle, 
  Sparkles, 
  Settings, 
  FileText, 
  Image as ImageIcon, 
  Video, 
  ArrowLeft,
  Lock,
  Layers
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, onBackToLanding }) {
  const mainNav = [
    { id: 'dashboard', label: 'Home', icon: Home },
    { id: 'dataset', label: 'Dataset', icon: Database },
    { id: 'causal_graph', label: 'Causal Graph', icon: GitFork },
    { id: 'generate', label: 'Generate Data', icon: Cpu },
    { id: 'preview', label: 'Synthetic Data Preview', icon: Table },
    { id: 'compare', label: 'Compare Models', icon: BarChart3 },
    { id: 'counterfactual', label: 'Counterfactual Explorer', icon: Sparkles },
    { id: 'explainability', label: 'Explainability', icon: HelpCircle },
    { id: 'text_generation', label: 'Text Generation', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const futureScopeNav = [
    { 
      id: 'image_gen', 
      label: 'Image Generation', 
      icon: ImageIcon, 
      tag: 'Coming soon',
      description: 'CausalVAE Latent Factor Intervention'
    },
    { 
      id: 'video_gen', 
      label: 'Video Generation', 
      icon: Video, 
      tag: 'Coming soon',
      description: 'Spatiotemporal Causal Diffusion'
    },
  ];

  return (
    <aside className="w-68 bg-[#ffffff] border-r border-stone-200/90 h-screen flex flex-col justify-between shrink-0 select-none shadow-2xs">
      <div>
        {/* Top Workspace Header */}
        <div className="p-5 border-b border-stone-100 flex items-center justify-between">
          <div 
            onClick={onBackToLanding}
            className="flex items-center gap-2.5 cursor-pointer group"
          >
            <div className="w-8 h-8 rounded-lg bg-forest-900 flex items-center justify-center text-white font-bold text-sm shadow-xs group-hover:bg-forest-950 transition">
              V
            </div>
            <div>
              <div className="font-bold text-stone-900 leading-tight flex items-center gap-1.5">
                Veritas
                <span className="text-[10px] font-semibold text-emerald-800 bg-emerald-100 px-1.5 py-0.2 rounded">v1.0</span>
              </div>
              <div className="text-[11px] text-stone-600 font-medium">Causal Synthetic AI</div>
            </div>
          </div>
        </div>

        {/* Navigation list */}
        <nav className="p-3 space-y-1">
          <div className="px-3 py-1.5 text-[11px] font-bold uppercase tracking-wider text-stone-600">
            Platform Modules
          </div>

          {mainNav.map(item => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition cursor-pointer text-left ${
                  isActive
                    ? 'bg-forest-900 text-white shadow-xs'
                    : 'text-stone-600 hover:text-stone-950 hover:bg-stone-100/70'
                }`}
              >
                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-stone-500'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}

          {/* Multimodal Future Scope Sections */}
          <div className="pt-4 px-3 py-1 text-[11px] font-bold uppercase tracking-wider text-stone-600 flex items-center justify-between">
            <span>Future Scope</span>
            <Layers className="w-3 h-3 text-stone-400" />
          </div>

          {futureScopeNav.map(item => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab('multimodal')}
                className="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs text-stone-400 hover:text-stone-700 hover:bg-stone-50 transition cursor-pointer text-left group"
                title={`${item.label} — ${item.description}`}
              >
                <div className="flex items-center gap-3">
                  <Icon className="w-4 h-4 text-stone-400 group-hover:text-forest-700 transition" />
                  <span className="font-medium text-stone-500 group-hover:text-stone-800">{item.label}</span>
                </div>
                <span className="text-[10px] bg-stone-100 text-stone-500 border border-stone-200/60 font-semibold px-2 py-0.5 rounded-full">
                  {item.tag}
                </span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Back to Landing Link */}
      <div className="p-4 border-t border-stone-100 bg-stone-50/50">
        <button
          onClick={onBackToLanding}
          className="w-full flex items-center justify-center gap-2 py-2 px-3 text-xs font-medium text-stone-600 hover:text-stone-900 hover:bg-stone-100 rounded-lg transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Exit to Landing Page</span>
        </button>
      </div>
    </aside>
  );
}
