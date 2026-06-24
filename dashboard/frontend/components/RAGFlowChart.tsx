'use client';

interface RAGFlowChartProps {
  active: boolean;
  maliciousInTopK?: number;
}

export default function RAGFlowChart({ active, maliciousInTopK = 3 }: RAGFlowChartProps) {
  const steps = [
    { id: 'question', label: 'User Question', x: 40, color: '#e2e8f0' },
    { id: 'retriever', label: 'Retriever', x: 180, color: '#00d4ff' },
    { id: 'contexts', label: 'Top-k Contexts', x: 340, color: '#fbbf24' },
    { id: 'llm', label: 'LLM', x: 500, color: '#10b981' },
    { id: 'answer', label: 'Answer', x: 640, color: '#ef4444' },
  ];

  return (
    <div className="glass-card p-4 h-full">
      <h3 className="text-sm font-semibold text-cyan-glow mb-3 uppercase tracking-wider">
        RAG Pipeline Flow
      </h3>
      <svg viewBox="0 0 720 200" className="w-full h-auto">
        <defs>
          <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#00d4ff" opacity="0.7" />
          </marker>
        </defs>

        {steps.slice(0, -1).map((step, i) => (
          <line
            key={`line-${i}`}
            x1={step.x + 50}
            y1={80}
            x2={steps[i + 1].x - 10}
            y2={80}
            stroke="#00d4ff"
            strokeWidth={active ? 2 : 1}
            strokeDasharray={active ? '8 4' : '4 4'}
            opacity={active ? 0.8 : 0.3}
            markerEnd="url(#arrowhead)"
            className={active ? 'animate-[flowDash_1.5s_linear_infinite]' : ''}
            style={active ? { strokeDashoffset: 0 } : undefined}
          />
        ))}

        {steps.map((step) => (
          <g key={step.id}>
            <rect
              x={step.x - 10}
              y={50}
              width={100}
              height={60}
              rx={8}
              fill="#151d35"
              stroke={step.color}
              strokeWidth={active && step.id === 'contexts' ? 2 : 1}
              opacity={active ? 1 : 0.6}
            />
            <text x={step.x + 40} y={85} textAnchor="middle" fill={step.color} fontSize={11} fontWeight={600}>
              {step.label}
            </text>
          </g>
        ))}

        {active && (
          <>
            <rect x={330} y={130} width="120" height="24" rx={4} fill="#ef4444" opacity={0.2} stroke="#ef4444" />
            <text x={390} y={146} textAnchor="middle" fill="#ef4444" fontSize={10}>
              {maliciousInTopK} malicious in top-k
            </text>
            <text x={40} y={170} fill="#64748b" fontSize={9}>
              P = S ⊕ I flows through retriever → poisons context → corrupts answer
            </text>
          </>
        )}

        {!active && (
          <text x={360} y={160} textAnchor="middle" fill="#64748b" fontSize={11}>
            Launch an attack to animate the pipeline
          </text>
        )}
      </svg>
    </div>
  );
}
