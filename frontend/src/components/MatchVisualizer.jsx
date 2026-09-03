import React, { useState, useEffect } from 'react';
import { apiService } from '../services/apiService';
import { Eye, Download, Info } from 'lucide-react';

const MatchVisualizer = ({ sessionId, metrics }) => {
  const [dossier, setDossier] = useState(null);
  const [dossierError, setDossierError] = useState(null);

  useEffect(() => {
    // Only attempt to load dossier if we have a valid session ID, dossier index is defined and non-negative
    if (sessionId && metrics.dossier_index !== null && metrics.dossier_index !== undefined && metrics.dossier_index >= 0) {
      apiService.fetchResults(sessionId)
        .then(() => {
          // Convert WebSocket URL to HTTP URL for the dossier endpoint
          // WS: ws://localhost:8000/api/v1/registration/ws/progress/{sessionId}
          // HTTP: http://localhost:8000/api/v1/results/{sessionId}/dossier/{idx}
          const wsUrl = apiService.getWebSocketUrl(sessionId);
          const httpUrl = wsUrl.replace('ws://', 'http://')
                               .replace('/api/v1/registration/ws/progress/', '/api/v1/results/');
          return fetch(`${httpUrl}/dossier/${metrics.dossier_index}`);
        })
        .then(res => {
          if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
          }
          return res.json();
        })
        .then(data => {
          setDossier(data);
          setDossierError(null);
        })
        .catch(err => {
          console.error("Error loading dossier", err);
          setDossier(null);
          setDossierError(`Failed to load dossier: ${err.message}`);
        });
    } else if (sessionId && (metrics.dossier_index === null || metrics.dossier_index === undefined)) {
      // If dossier index is null or undefined, we don't attempt to load but clear any previous data/error
      setDossier(null);
      setDossierError(null);
    }
    // If dossier index is negative, we also clear data and error (no dossier to load)
    else if (sessionId && metrics.dossier_index < 0) {
      setDossier(null);
      setDossierError(null);
    }
  }, [sessionId, metrics]);

  if (!sessionId) {
    return <div style={{ color: 'var(--text-muted)' }}>Run the pipeline to generate Explainability Dossiers.</div>;
  }

  if (dossierError) {
    return <div style={{ color: 'var(--text-error)' }}>Error loading dossier: {dossierError}</div>;
  }

  // Determine if we should show loading state
  const isLoading = sessionId && metrics.dossier_index >= 0 && !dossier && !dossierError;

  if (isLoading) {
     return <div style={{ color: 'var(--text-muted)' }}>Loading Dossier for match {metrics.dossier_index}...</div>;
  }

  // If dossier index is invalid (null, undefined, or negative), show unavailability message
  if (sessionId && (metrics.dossier_index === null || metrics.dossier_index === undefined || metrics.dossier_index < 0)) {
     return <div style={{ color: 'var(--text-muted)' }}>No dossier available (no inlier matches found or index invalid).</div>;
  }

  // Fallback: if we have no dossier and not loading, show generic message
  if (!dossier) {
     return <div style={{ color: 'var(--text-muted)' }}>No dossier data available.</div>;
  }

  // Defensive checks for dossier structure
  const matchInfo = dossier && dossier['Match Information'] ? dossier['Match Information'] : {};
  const hasMatchInfo = matchInfo && Object.keys(matchInfo).length > 0;

  // Format values with appropriate units
  const formatValue = (key, value) => {
    if (typeof value === 'number') {
      if (key.includes('Coordinate') || key.includes('Distance') || key.includes('Scale')) {
        return `${value.toFixed(3)} px`;
      } else if (key.includes(' Angle') || key === 'Angle Difference') {
        return `${value.toFixed(1)}°`;
      } else if (key === 'Descriptor Distance') {
        return `${value.toFixed(3)}`;
      } else if (key.includes('Ratio')) {
        return `${value.toFixed(3)}`;
      } else {
        return value.toString();
      }
    }
    return typeof value === 'string' ? value : JSON.stringify(value);
  };

  // Export report functionality
  const exportReport = () => {
    if (!dossier) {
      alert('No dossier data available to export');
      return;
    }

    // Convert dossier to JSON string
    const dataStr = JSON.stringify(dossier, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });

    // Create a download link
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `lunalign_dossier_${sessionId}_match_${metrics.dossier_index}.json`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', height: '100%', overflowY: 'auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <h4 style={{ color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Info size={18} color="var(--accent-primary)" /> Match Diagnostics: Inlier #{metrics.dossier_index}
        </h4>
        <button className="btn btn-primary" style={{ padding: '6px 12px', fontSize: '0.8rem' }} onClick={exportReport}>
          <Download size={14} /> Export Report
        </button>
      </div>

      {/* Evaluation Metrics Panel */}
      <div className="glass-panel" style={{ padding: '16px' }}>
        <h5 style={{ marginBottom: '12px', color: 'var(--text-muted)' }}>Evaluation Metrics</h5>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-muted)' }}>RMSE</span>
            <strong style={{ color: 'var(--text-main)' }}>{metrics.rmse !== '--' ? `${metrics.rmse} px` : '--'}</strong>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-muted)' }}>Inlier Match Count</span>
            <strong style={{ color: 'var(--text-main)' }}>{metrics.inliers}</strong>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-muted)' }}>Inlier Ratio</span>
            <strong style={{ color: 'var(--text-main)' }}>
              {metrics.total_matches > 0 ? `${(metrics.inliers / metrics.total_matches * 100).toFixed(1)}%` : '0%'}
            </strong>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>

        {/* Metric Table */}
        <div className="glass-panel" style={{ padding: '16px' }}>
           <h5 style={{ marginBottom: '12px', color: 'var(--text-muted)' }}>Match Information Panel</h5>
           {hasMatchInfo ? (
             <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.9rem' }}>
                {Object.entries(matchInfo).map(([k, v]) => (
                   <div key={k} style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '4px' }}>
                      <span style={{ color: 'var(--text-muted)' }}>{k}</span>
                      <strong style={{ color: 'var(--text-main)' }}>{formatValue(k, v)}</strong>
                   </div>
                ))}
             </div>
           ) : (
             <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px' }}>
               No match information available
             </div>
           )}
        </div>

        {/* Feature Patch Viewer */}
        <div className="glass-panel" style={{ padding: '16px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
           <h5 style={{ marginBottom: '12px', color: 'var(--text-muted)' }}>Feature Similarity Structure</h5>
           <img
              src={apiService.getImageUrl(sessionId, 'patch', metrics.dossier_index)}
              alt="Feature Patch"
              onError={(e) => {
                console.error(`Failed to load patch image for session ${sessionId} and index ${metrics.dossier_index}`, e);
                // Keep broken image - browser will show broken image icon
              }}
              style={{ width: '100%', maxWidth: '300px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}
           />
           <p style={{ marginTop: '12px', fontSize: '0.8rem', color: 'var(--text-muted)', textAlign: 'center' }}>
             Side-by-side local pixel neighborhoods extracted at the exact sub-pixel coordinate.
           </p>
        </div>

      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '8px' }}>
         {/* Source Uncertainty */}
         <div className="glass-panel hover-lift" style={{ padding: '16px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
           <h5 style={{ marginBottom: '12px', color: 'var(--text-muted)' }}>Source Scale Uncertainty</h5>
           <img
              src={apiService.getImageUrl(sessionId, 'src_uncertainty', metrics.dossier_index)}
              alt="Source Uncertainty"
              onError={(e) => {
                console.error(`Failed to load source uncertainty image for session ${sessionId} and index ${metrics.dossier_index}`, e);
              }}
              style={{ width: '100%', maxWidth: '250px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}
           />
         </div>

         {/* Reference Uncertainty */}
         <div className="glass-panel hover-lift" style={{ padding: '16px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
           <h5 style={{ marginBottom: '12px', color: 'var(--text-muted)' }}>Reference Scale Uncertainty</h5>
           <img
              src={apiService.getImageUrl(sessionId, 'ref_uncertainty', metrics.dossier_index)}
              alt="Ref Uncertainty"
              onError={(e) => {
                console.error(`Failed to load reference uncertainty image for session ${sessionId} and index ${metrics.dossier_index}`, e);
              }}
              style={{ width: '100%', maxWidth: '250px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}
           />
         </div>
      </div>
    </div>
  );
};

export default MatchVisualizer;