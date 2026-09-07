import React from 'react';
import { Database, Zap, Cpu, CheckCircle2, Navigation, Radio } from 'lucide-react';

const PipelineVisualizer = ({ currentStage, progress = 0 }) => {
  const stages = [
    { id: 'raw', code: 'STG-01', label: 'Payload Ingestion', icon: Database, desc: 'PDS/IMG Binary Normalization' },
    { id: 'matched', code: 'STG-02', label: 'Feature Extraction', icon: Cpu, desc: 'Illumination-Invariant Descriptors' },
    { id: 'verified', code: 'STG-03', label: 'Sub-Pixel Refinement', icon: Zap, desc: 'Spatial ANNS & Gradient Optimization' },
    { id: 'registered', code: 'STG-04', label: 'Geometric Model', icon: Navigation, desc: 'Homography Matrix & RANSAC Inliers' },
    { id: 'generating_dossiers', code: 'STG-05', label: 'Telemetry Assembly', icon: Radio, desc: 'Explainability & Uncertainty Fields' },
    { id: 'complete', code: 'STG-06', label: 'Registration Locked', icon: CheckCircle2, desc: 'Sub-Pixel Convergence Verified' }
  ];

  const stageOrder = ['raw', 'matched', 'verified', 'registered', 'generating_dossiers', 'complete'];
  const currentIndex = stageOrder.indexOf(currentStage);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', position: 'relative' }}>
      {/* Global Progress Track Bar */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontFamily: 'var(--font-telemetry)', fontSize: '0.6875rem', color: 'var(--text-annotation)' }}>
            PIPELINE CONVERGENCE
          </span>
          <span style={{ fontFamily: 'var(--font-telemetry)', fontSize: '0.75rem', fontWeight: 600, color: 'var(--primary-neon)' }}>
            {progress}%
          </span>
        </div>
        
        <div style={{
          width: '100%',
          height: '6px',
          background: 'rgba(8, 13, 26, 0.8)',
          borderRadius: '3px',
          overflow: 'hidden',
          border: '1px solid var(--outline)'
        }}>
          <div style={{
            width: `${Math.max(progress, currentStage === 'complete' ? 100 : 0)}%`,
            height: '100%',
            background: 'linear-gradient(90deg, var(--primary-container), var(--secondary-neon))',
            boxShadow: '0 0 10px rgba(34, 211, 238, 0.5)',
            transition: 'width 0.4s cubic-bezier(0.16, 1, 0.3, 1)'
          }} />
        </div>
      </div>

      {/* Stage Nodes Sequence */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', position: 'relative', marginTop: '4px' }}>
        {/* Background connector line */}
        <div style={{
          position: 'absolute',
          left: '15px',
          top: '12px',
          bottom: '12px',
          width: '2px',
          background: 'rgba(30, 41, 59, 0.8)',
          zIndex: 0
        }} />

        {stages.map((stage, index) => {
          const Icon = stage.icon;
          const isDone = currentStage === 'complete' || (currentIndex > index);
          const isCurrent = currentStage === stage.id && currentStage !== 'complete';
          const isPending = !isDone && !isCurrent;

          return (
            <div
              key={stage.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                zIndex: 1,
                padding: '6px 8px',
                borderRadius: 'var(--radius-sm)',
                background: isCurrent ? 'rgba(34, 211, 238, 0.06)' : 'transparent',
                border: isCurrent ? '1px solid rgba(34, 211, 238, 0.25)' : '1px solid transparent',
                transition: 'all 0.25s ease'
              }}
            >
              {/* Node Icon Circle */}
              <div style={{
                width: '30px',
                height: '30px',
                minWidth: '30px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: isCurrent 
                  ? 'var(--primary-container)' 
                  : isDone 
                  ? 'rgba(34, 197, 94, 0.15)' 
                  : 'rgba(14, 19, 32, 0.9)',
                border: `1px solid ${
                  isCurrent 
                    ? 'var(--primary-neon)' 
                    : isDone 
                    ? 'var(--status-nominal)' 
                    : 'var(--outline)'
                }`,
                color: isCurrent 
                  ? 'var(--bg-void)' 
                  : isDone 
                  ? 'var(--status-nominal)' 
                  : 'var(--text-muted)',
                boxShadow: isCurrent 
                  ? 'var(--glow-btn)' 
                  : isDone 
                  ? '0 0 8px rgba(34, 197, 94, 0.3)' 
                  : 'none',
                position: 'relative'
              }}>
                <Icon size={14} />
                {isCurrent && (
                  <span
                    className="ping-dot"
                    style={{
                      position: 'absolute',
                      top: '-2px',
                      right: '-2px',
                      color: 'var(--primary-neon)'
                    }}
                  />
                )}
              </div>

              {/* Stage Info */}
              <div style={{ display: 'flex', flexDirection: 'column', minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span style={{
                    fontFamily: 'var(--font-telemetry)',
                    fontSize: '0.625rem',
                    color: isCurrent ? 'var(--primary-neon)' : 'var(--text-annotation)',
                    fontWeight: 600
                  }}>
                    {stage.code}
                  </span>
                  <span style={{
                    fontFamily: 'var(--font-display)',
                    fontSize: '0.8125rem',
                    fontWeight: isCurrent || isDone ? 600 : 400,
                    color: isCurrent 
                      ? 'var(--text-telemetry)' 
                      : isDone 
                      ? 'var(--text-main)' 
                      : 'var(--text-muted)',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis'
                  }}>
                    {stage.label}
                  </span>
                </div>
                <span style={{
                  fontFamily: 'var(--font-body)',
                  fontSize: '0.6875rem',
                  color: isCurrent ? 'var(--primary)' : 'var(--text-muted)',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}>
                  {stage.desc}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default PipelineVisualizer;
