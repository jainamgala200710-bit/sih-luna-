import React from 'react';
import { Database, Zap, Map, CheckCircle, Navigation } from 'lucide-react';

const PipelineVisualizer = ({ currentStage, progress = 0 }) => {
  const stages = [
    { id: 'raw', icon: Database, label: 'Raw Ingestion' },
    { id: 'matched', icon: Map, label: 'Mathematical Extraction' },
    { id: 'verified', icon: CheckCircle, label: 'Geometric Verification' },
    { id: 'registered', icon: Navigation, label: 'Transform Modeling' },
    { id: 'generating_dossiers', icon: Zap, label: 'Telemetry Assembly' },
    { id: 'complete', icon: CheckCircle, label: 'Complete' }
  ];

  const currentIndex = stages.findIndex(s => s.id === currentStage);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', position: 'relative', marginTop: '10px' }}>
      {/* Vertical connection line (Background) */}
      <div style={{ 
        position: 'absolute', 
        left: '16px', 
        top: '16px', 
        bottom: '16px', 
        width: '2px', 
        background: 'var(--border-subtle)',
        zIndex: 0
      }}></div>
      
      {/* Vertical connection line (Fill) */}
      <div style={{ 
        position: 'absolute', 
        left: '16px', 
        top: '16px', 
        height: `calc(${progress}% - 32px)`, 
        width: '2px', 
        background: 'var(--accent-primary)',
        zIndex: 0,
        transition: 'height 0.5s ease',
        boxShadow: 'var(--shadow-glow)'
      }}></div>
      
      {stages.map((stage, index) => {
        const Icon = stage.icon;
        const isActive = index === currentIndex;
        const isPast = index < currentIndex || currentStage === 'complete';
        
        return (
          <div key={stage.id} style={{ display: 'flex', alignItems: 'center', gap: '16px', zIndex: 1 }}>
            <div style={{ 
              width: '34px', 
              height: '34px', 
              borderRadius: '50%', 
              background: isActive ? 'var(--accent-primary)' : isPast ? 'var(--bg-elevated)' : 'var(--bg-base)',
              border: `2px solid ${isPast || isActive ? 'var(--accent-primary)' : 'var(--border-subtle)'}`,
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              color: isActive ? '#fff' : isPast ? 'var(--accent-primary)' : 'var(--text-muted)',
              boxShadow: isActive ? 'var(--shadow-glow)' : 'none',
              transition: 'all 0.3s ease'
            }}>
              <Icon size={16} />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
               <span style={{ 
                 color: isActive || isPast ? 'var(--text-main)' : 'var(--text-muted)',
                 fontWeight: isActive ? 600 : 400,
                 fontSize: '0.9rem'
               }}>
                 {stage.label}
               </span>
               {isActive && currentStage !== 'complete' && (
                 <span style={{ fontSize: '0.75rem', color: 'var(--accent-primary)' }}>{progress}% Execution</span>
               )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default PipelineVisualizer;
