import React, { useState, useMemo } from 'react';
import { ArrowRight, Plus, Trash2, RotateCw, CheckCircle2, AlertCircle, Info, Sparkles } from 'lucide-react';

export default function CausalGraphCanvas({
  nodes = [],
  edges = [],
  onUpdateGraph,
  readOnly = false,
  highlightedEdges = []
}) {
  const [selectedSource, setSelectedSource] = useState('');
  const [selectedTarget, setSelectedTarget] = useState('');
  const [activeNode, setActiveNode] = useState(null);

  // Auto-layout nodes in a clean DAG hierarchy
  const layout = useMemo(() => {
    const nodeMap = {};
    const inDegree = {};
    nodes.forEach(n => {
      inDegree[n.id] = 0;
    });
    edges.forEach(e => {
      if (inDegree[e.target] !== undefined) {
        inDegree[e.target] += 1;
      }
    });

    // Assign levels: root nodes (inDegree 0) at level 0, then children at level 1, 2...
    const levels = {};
    const queue = nodes.filter(n => inDegree[n.id] === 0).map(n => n.id);
    queue.forEach(id => { levels[id] = 0; });

    let safety = 0;
    let currentQueue = [...queue];
    while (currentQueue.length > 0 && safety < 10) {
      safety++;
      const nextQueue = [];
      currentQueue.forEach(u => {
        edges.filter(e => e.source === u).forEach(e => {
          const v = e.target;
          levels[v] = Math.max(levels[v] || 0, (levels[u] || 0) + 1);
          if (!nextQueue.includes(v)) nextQueue.push(v);
        });
      });
      currentQueue = nextQueue;
    }

    // Assign fallback level for any remaining
    nodes.forEach(n => {
      if (levels[n.id] === undefined) levels[n.id] = 1;
    });

    // Group nodes by level
    const levelGroups = {};
    nodes.forEach(n => {
      const lvl = levels[n.id];
      if (!levelGroups[lvl]) levelGroups[lvl] = [];
      levelGroups[lvl].push(n.id);
    });

    const maxLevel = Math.max(0, ...Object.keys(levelGroups).map(Number));
    const width = 640;
    const height = 340;
    const paddingX = 80;
    const paddingY = 50;

    const positions = {};
    Object.keys(levelGroups).forEach(lvlStr => {
      const lvl = Number(lvlStr);
      const group = levelGroups[lvl];
      const x = maxLevel === 0 ? width / 2 : paddingX + (lvl / maxLevel) * (width - 2 * paddingX);
      group.forEach((id, idx) => {
        const y = group.length === 1 
          ? height / 2 
          : paddingY + (idx / (group.length - 1)) * (height - 2 * paddingY);
        positions[id] = { x, y };
      });
    });

    return positions;
  }, [nodes, edges]);

  const handleAddEdge = () => {
    if (!selectedSource || !selectedTarget || selectedSource === selectedTarget) return;
    const exists = edges.some(e => e.source === selectedSource && e.target === selectedTarget);
    if (exists) return;

    const newEdges = [...edges, { source: selectedSource, target: selectedTarget, weight: 0.5 }];
    onUpdateGraph && onUpdateGraph({ nodes, edges: newEdges });
    setSelectedSource('');
    setSelectedTarget('');
  };

  const handleDeleteEdge = (src, tgt) => {
    const newEdges = edges.filter(e => !(e.source === src && e.target === tgt));
    onUpdateGraph && onUpdateGraph({ nodes, edges: newEdges });
  };

  const handleReverseEdge = (src, tgt) => {
    const newEdges = edges.map(e => {
      if (e.source === src && e.target === tgt) {
        return { source: tgt, target: src, weight: e.weight };
      }
      return e;
    });
    onUpdateGraph && onUpdateGraph({ nodes, edges: newEdges });
  };

  return (
    <div className="bg-white rounded-2xl border border-stone-200/90 shadow-sm overflow-hidden flex flex-col">
      {/* Header bar */}
      <div className="px-5 py-3.5 border-b border-stone-100 flex items-center justify-between bg-stone-50/50">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
          <h3 className="text-sm font-semibold text-stone-800">
            Causal Directed Acyclic Graph (DAG)
          </h3>
          <span className="text-xs text-stone-500 bg-stone-100 px-2 py-0.5 rounded-full">
            {nodes.length} nodes • {edges.length} edges
          </span>
        </div>
        {!readOnly && (
          <span className="text-xs text-emerald-700 bg-emerald-50 border border-emerald-200/60 px-2.5 py-1 rounded-full font-medium flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" /> Human-in-the-Loop Editable
          </span>
        )}
      </div>

      {/* SVG Canvas */}
      <div className="relative p-2 bg-[#fcfdfa] overflow-x-auto min-h-[340px] flex items-center justify-center">
        <svg viewBox="0 0 640 340" className="w-full h-[340px] max-w-[640px]">
          <defs>
            <marker
              id="arrowhead"
              markerWidth="8"
              markerHeight="6"
              refX="18"
              refY="3"
              orient="auto"
            >
              <polygon points="0 0, 8 3, 0 6" fill="#0d4734" />
            </marker>
            <marker
              id="arrowhead-highlight"
              markerWidth="8"
              markerHeight="6"
              refX="18"
              refY="3"
              orient="auto"
            >
              <polygon points="0 0, 8 3, 0 6" fill="#059669" />
            </marker>
          </defs>

          {/* Render directed edges */}
          {edges.map((e, idx) => {
            const srcPos = layout[e.source];
            const tgtPos = layout[e.target];
            if (!srcPos || !tgtPos) return null;

            const isHighlighted = highlightedEdges.some(
              he => (he.source === e.source && he.target === e.target) ||
                    (he.source === e.source || he.target === e.target)
            );

            return (
              <g key={`${e.source}-${e.target}-${idx}`} className="group cursor-pointer">
                <line
                  x1={srcPos.x}
                  y1={srcPos.y}
                  x2={tgtPos.x}
                  y2={tgtPos.y}
                  stroke={isHighlighted ? '#059669' : '#0d4734'}
                  strokeWidth={isHighlighted ? '2.5' : '1.8'}
                  strokeDasharray={isHighlighted ? '4 2' : 'none'}
                  strokeOpacity={isHighlighted ? '1' : '0.65'}
                  markerEnd={isHighlighted ? 'url(#arrowhead-highlight)' : 'url(#arrowhead)'}
                  className="transition-all duration-300 group-hover:stroke-emerald-600 group-hover:stroke-width-2"
                />
              </g>
            );
          })}

          {/* Render nodes */}
          {nodes.map(n => {
            const pos = layout[n.id] || { x: 100, y: 100 };
            const isSelected = activeNode === n.id;
            const hasEdges = edges.some(e => e.source === n.id || e.target === n.id);

            return (
              <g
                key={n.id}
                transform={`translate(${pos.x}, ${pos.y})`}
                onClick={() => setActiveNode(isSelected ? null : n.id)}
                className="cursor-pointer transition-transform duration-200 hover:scale-105"
              >
                <rect
                  x="-54"
                  y="-16"
                  width="108"
                  height="32"
                  rx="8"
                  className={`${
                    isSelected
                      ? 'fill-forest-900 stroke-forest-700'
                      : 'fill-white stroke-stone-200 hover:stroke-forest-600'
                  } stroke-1 shadow-sm transition-colors`}
                  filter="drop-shadow(0 1px 2px rgba(0,0,0,0.05))"
                />
                <text
                  x="0"
                  y="4"
                  textAnchor="middle"
                  className={`text-[11px] font-medium select-none pointer-events-none ${
                    isSelected ? 'fill-white font-semibold' : 'fill-stone-800'
                  }`}
                >
                  {n.id.length > 13 ? `${n.id.slice(0, 11)}..` : n.id}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Editor Controls for Human-in-the-loop */}
      {!readOnly && (
        <div className="p-4 bg-stone-50/80 border-t border-stone-200 text-xs">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-stone-700">Add Edge:</span>
              <select
                value={selectedSource}
                onChange={e => setSelectedSource(e.target.value)}
                className="bg-white border border-stone-300 rounded-lg px-2.5 py-1.5 text-stone-700 focus:outline-none focus:ring-1 focus:ring-forest-600"
              >
                <option value="">Source (Cause)</option>
                {nodes.map(n => (
                  <option key={n.id} value={n.id}>{n.id}</option>
                ))}
              </select>
              <ArrowRight className="w-3.5 h-3.5 text-stone-400" />
              <select
                value={selectedTarget}
                onChange={e => setSelectedTarget(e.target.value)}
                className="bg-white border border-stone-300 rounded-lg px-2.5 py-1.5 text-stone-700 focus:outline-none focus:ring-1 focus:ring-forest-600"
              >
                <option value="">Target (Effect)</option>
                {nodes.filter(n => n.id !== selectedSource).map(n => (
                  <option key={n.id} value={n.id}>{n.id}</option>
                ))}
              </select>
              <button
                onClick={handleAddEdge}
                disabled={!selectedSource || !selectedTarget}
                className="bg-forest-900 hover:bg-forest-950 disabled:opacity-40 text-white px-3 py-1.5 rounded-lg font-medium flex items-center gap-1 transition"
              >
                <Plus className="w-3.5 h-3.5" /> Add
              </button>
            </div>

            <div className="text-stone-500 italic flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5 text-stone-400" />
              Click any edge in the list below to reverse or prune.
            </div>
          </div>

          {/* Current Edges list badge strip */}
          <div className="mt-3 flex flex-wrap gap-2 max-h-24 overflow-y-auto pt-1">
            {edges.map((e, idx) => (
              <div
                key={`${e.source}-${e.target}-${idx}`}
                className="bg-white border border-stone-200 px-2 py-1 rounded-md text-stone-700 flex items-center gap-2 text-[11px] shadow-2xs hover:border-forest-300"
              >
                <span className="font-medium text-stone-900">{e.source}</span>
                <span className="text-forest-700 font-bold">→</span>
                <span className="font-medium text-stone-900">{e.target}</span>
                <button
                  onClick={() => handleReverseEdge(e.source, e.target)}
                  title="Reverse direction"
                  className="text-stone-400 hover:text-emerald-700 transition"
                >
                  <RotateCw className="w-3 h-3" />
                </button>
                <button
                  onClick={() => handleDeleteEdge(e.source, e.target)}
                  title="Remove edge"
                  className="text-stone-400 hover:text-rose-600 transition"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
