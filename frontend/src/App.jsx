import React, { useState, useEffect } from 'react';
import LandingPage from './pages/LandingPage';
import DashboardOverview from './pages/DashboardOverview';
import DatasetPage from './pages/DatasetPage';
import CausalGraphPage from './pages/CausalGraphPage';
import GenerateDataPage from './pages/GenerateDataPage';
import SyntheticPreviewPage from './pages/SyntheticPreviewPage';
import CompareModelsPage from './pages/CompareModelsPage';
import CounterfactualPage from './pages/CounterfactualPage';
import ExplainabilityPage from './pages/ExplainabilityPage';
import TextGenerationPage from './pages/TextGenerationPage';
import MultimodalPage from './pages/MultimodalPage';
import SettingsPage from './pages/SettingsPage';
import Sidebar from './components/Sidebar';
import { ArrowLeft, Database, Sparkles } from 'lucide-react';

export default function App() {
  const [currentView, setCurrentView] = useState('landing'); // 'landing' | 'app'
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dataset, setDataset] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  // Load default dataset on start
  useEffect(() => {
    fetch('/api/datasets/load-default', { method: 'POST' })
      .then(res => res.json())
      .then(data => setDataset(data))
      .catch(console.error);
  }, []);

  const handleLaunchPlatform = (tab = 'dashboard') => {
    setActiveTab(tab);
    setCurrentView('app');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleBackToLanding = () => {
    setCurrentView('landing');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const triggerRefresh = () => {
    setRefreshKey(prev => prev + 1);
  };

  if (currentView === 'landing') {
    return (
      <LandingPage onLaunchPlatform={handleLaunchPlatform} />
    );
  }

  return (
    <div className="flex h-screen bg-[#fafbf9] text-stone-900 font-sans overflow-hidden">
      {/* Left Sidebar */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        onBackToLanding={handleBackToLanding} 
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Top App Bar */}
        <header className="h-16 bg-white border-b border-stone-200/80 px-6 flex items-center justify-between shrink-0 shadow-2xs">
          <div className="flex items-center gap-3">
            <button
              onClick={handleBackToLanding}
              className="text-stone-400 hover:text-stone-800 p-1.5 rounded-lg hover:bg-stone-100 transition"
              title="Return to Home Landing"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <div className="h-4 w-px bg-stone-200" />
            <div className="text-xs font-semibold text-stone-500">
              Workspace / <span className="text-stone-900 font-bold capitalize">{activeTab.replace('_', ' ')}</span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-stone-50 border border-stone-200 px-3 py-1 rounded-full text-xs">
              <Database className="w-3.5 h-3.5 text-forest-800" />
              <span className="font-semibold text-stone-800">{dataset?.name || 'employee_data.csv'}</span>
              <span className="text-[10px] text-stone-400">({dataset?.row_count || 300} rows)</span>
            </div>

            <button
              onClick={() => setActiveTab('generate')}
              className="bg-forest-900 hover:bg-forest-950 text-white px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 shadow-xs transition cursor-pointer"
            >
              <Sparkles className="w-3 h-3" />
              <span>Generate</span>
            </button>
          </div>
        </header>

        {/* Scrollable Page Body */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8 max-w-7xl w-full mx-auto">
          {activeTab === 'dashboard' && (
            <DashboardOverview 
              onNavigate={setActiveTab} 
              dataset={dataset} 
              onSelectDataset={setDataset} 
              refreshKey={refreshKey}
            />
          )}

          {activeTab === 'dataset' && (
            <DatasetPage 
              dataset={dataset} 
              onSelectDataset={setDataset} 
            />
          )}

          {activeTab === 'causal_graph' && (
            <CausalGraphPage 
              dataset={dataset} 
            />
          )}

          {activeTab === 'generate' && (
            <GenerateDataPage 
              dataset={dataset} 
              onGenerationComplete={triggerRefresh}
              onNavigate={setActiveTab}
            />
          )}

          {activeTab === 'preview' && (
            <SyntheticPreviewPage 
              dataset={dataset} 
            />
          )}

          {activeTab === 'compare' && (
            <CompareModelsPage 
              dataset={dataset} 
            />
          )}

          {activeTab === 'counterfactual' && (
            <CounterfactualPage 
              dataset={dataset} 
            />
          )}

          {activeTab === 'explainability' && (
            <ExplainabilityPage 
              dataset={dataset} 
            />
          )}

          {activeTab === 'text_generation' && (
            <TextGenerationPage />
          )}

          {activeTab === 'multimodal' && (
            <MultimodalPage />
          )}

          {activeTab === 'settings' && (
            <SettingsPage />
          )}
        </main>
      </div>
    </div>
  );
}
