import React from 'react';
import { ArrowRight, Sparkles, Database, Layers } from 'lucide-react';

export default function Navbar({ activePage, setActivePage, onOpenApp }) {
  return (
    <header className="sticky top-0 z-40 w-full bg-[#fafbf9]/90 backdrop-blur-md border-b border-stone-200/70 transition-all">
      <div className="max-w-7xl mx-auto px-6 h-18 flex items-center justify-between">
        {/* Brand Logo */}
        <div 
          onClick={() => setActivePage('landing')}
          className="flex items-center gap-2.5 cursor-pointer group"
        >
          <div className="w-8 h-8 rounded-lg bg-forest-900 flex items-center justify-center text-white font-bold text-lg tracking-tight shadow-xs group-hover:bg-forest-950 transition">
            V
          </div>
          <span className="text-2xl font-bold tracking-tight text-gray-900">
            Veritas
          </span>
        </div>

        {/* Center Nav Links - Matching Reference Exactly */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-stone-600">
          <button
            onClick={() => setActivePage('landing')}
            className={`transition-colors relative py-1 ${
              activePage === 'landing' 
                ? 'text-gray-950 font-semibold after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-forest-900' 
                : 'hover:text-forest-900'
            }`}
          >
            Home
          </button>
          <button
            onClick={() => {
              if (activePage === 'landing') {
                const el = document.getElementById('features-section');
                if (el) el.scrollIntoView({ behavior: 'smooth' });
                else onOpenApp('dashboard');
              } else {
                onOpenApp('dashboard');
              }
            }}
            className="hover:text-forest-900 transition-colors"
          >
            Features
          </button>
          <button
            onClick={() => onOpenApp('compare')}
            className="hover:text-forest-900 transition-colors"
          >
            Models
          </button>
          <button
            onClick={() => onOpenApp('compare')}
            className="hover:text-forest-900 transition-colors"
          >
            Evaluation
          </button>
          <button
            onClick={() => onOpenApp('multimodal')}
            className="hover:text-forest-900 transition-colors flex items-center gap-1.5"
          >
            Documentation
            <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800">
              Multimodal
            </span>
          </button>
        </nav>

        {/* Right CTA Button - Matching Reference Exactly */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => onOpenApp('dashboard')}
            className="bg-forest-900 hover:bg-forest-950 text-white px-5 py-2.5 rounded-xl text-sm font-semibold flex items-center gap-2 shadow-sm transition hover:shadow-md cursor-pointer"
          >
            <span>Get Started</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
