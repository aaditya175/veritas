import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-[#fafbf9] flex items-center justify-center p-6 text-stone-900">
          <div className="bg-white p-8 rounded-2xl border border-rose-200 shadow-lg max-w-lg w-full text-center space-y-4">
            <div className="w-12 h-12 bg-rose-50 text-rose-600 rounded-xl mx-auto flex items-center justify-center">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-bold text-stone-950">Something went wrong</h2>
            <p className="text-xs text-stone-600 leading-relaxed font-mono bg-stone-50 p-3 rounded-lg border border-stone-200 break-words text-left">
              {this.state.error?.message || "An unexpected error occurred."}
            </p>
            <button
              onClick={() => {
                this.setState({ hasError: false, error: null });
                window.location.reload();
              }}
              className="bg-forest-900 hover:bg-forest-950 text-white px-5 py-2.5 rounded-xl text-xs font-semibold inline-flex items-center gap-2 transition"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Reload Application</span>
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
