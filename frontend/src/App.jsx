import React, { useState, useEffect } from 'react';
import { Layers, Image as ImageIcon, Crosshair, Settings, Play } from 'lucide-react';
import ImageViewer from './components/ImageViewer';
import MatchVisualizer from './components/MatchVisualizer';
import PipelineVisualizer from './components/PipelineVisualizer';
import ComparisonModes from './components/ComparisonModes';
import { apiService } from './services/apiService';

function App() {
  const [activeTab, setActiveTab] = useState('raw');
  const [sessionId, setSessionId] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [ws, setWs] = useState(null);

  const [pipelineState, setPipelineState] = useState({
    stage: 'raw',
    progress: 0,
    metrics: {
      rmse: '--',
      inliers: '--',
      model: '--',
      dossier_index: null
    }
  });

  const [files, setFiles] = useState({ source: null, reference: null });

  // Handle WebSocket Connection
  useEffect(() => {
    if (sessionId && isProcessing && !ws) {
      const socket = new WebSocket(apiService.getWebSocketUrl(sessionId));

      socket.onopen = () => {
        console.log("WebSocket connection opened");
      };

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("WS Data:", data);

        setPipelineState(prev => ({
          ...prev,
          stage: data.stage,
          progress: data.progress,
          metrics: data.metrics ? { ...prev.metrics, ...data.metrics } : prev.metrics
        }));

        if (data.stage === 'complete' || data.stage === 'error') {
          setIsProcessing(false);
          socket.close();
          setWs(null);

          if(data.stage === 'complete') {
             setActiveTab('matches'); // Auto-switch to results
          }
        }
      };

      socket.onclose = () => {
         console.log("WebSocket connection closed");
         setWs(null);
      };

      socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        setIsProcessing(false);
        setWs(null);
      };

      setWs(socket);

      // Cleanup
      return () => {
        socket.close();
      };
    }
  }, [sessionId, isProcessing]);

  const handleUploadAndRun = async () => {
    if (!files.source || !files.reference) {
      alert("Please upload both source and reference images.");
      return;
    }

    try {
      // 1. Upload Images
      const uploadRes = await apiService.uploadImages(files.source, files.reference);
      setSessionId(uploadRes.session_id);

      // 2. Trigger Pipeline
      setIsProcessing(true);
      setPipelineState(prev => ({ ...prev, stage: 'raw', progress: 0, metrics: { rmse: '--', inliers: '--', model: '--' }}));
      await apiService.triggerRegistration(uploadRes.session_id);

    } catch (err) {
      console.error(err);
      alert("Error starting pipeline: " + err.message);
      setIsProcessing(false);
    }
  };

  return (
    <div className="dashboard-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div>
          <h2 style={{ background: 'linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', fontSize: '1.5rem', marginBottom: '8px' }}>
            LunaAlign AI
          </h2>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <button
            className={`btn ${activeTab === 'raw' ? 'btn-primary' : ''}`}
            onClick={() => setActiveTab('raw')}
            style={{ justifyContent: 'flex-start' }}
          >
            <ImageIcon size={18} /> Raw Imagery
          </button>

          <button
            className={`btn ${activeTab === 'matches' ? 'btn-primary' : ''}`}
            onClick={() => setActiveTab('matches')}
            style={{ justifyContent: 'flex-start' }}
            disabled={!sessionId || isProcessing || pipelineState.stage !== 'complete'}
          >
            <Crosshair size={18} /> Diagnostics & Explanations
          </button>

          <button
            className={`btn ${activeTab === 'compare' ? 'btn-primary' : ''}`}
            onClick={() => setActiveTab('compare')}
            style={{ justifyContent: 'flex-start' }}
            disabled={!sessionId || isProcessing || pipelineState.stage !== 'complete'}
          >
            <Layers size={18} /> Registration Overlay
          </button>
        </nav>

        <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>

          <button
            className="btn btn-primary"
            style={{ justifyContent: 'center', padding: '12px', opacity: (isProcessing || !files.source || !files.reference) ? 0.5 : 1 }}
            onClick={handleUploadAndRun}
            disabled={isProcessing || !files.source || !files.reference}
          >
            <Play size={18} />
            {isProcessing ? `Processing... ${pipelineState.progress}%` : "Run Pipeline"}
          </button>

          <div className="glass-panel hover-lift">
            <div style={{ padding: '16px' }}>
              <h4 style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
                <Settings size={16} /> Pipeline Status
              </h4>
              <PipelineVisualizer currentStage={pipelineState.stage} progress={pipelineState.progress} />
            </div>
          </div>
        </div>
      </aside>

      {/* Main Display Area */}
      <main className="main-content">
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3>
            {activeTab === 'raw' && "Source & Reference Input"}
            {activeTab === 'matches' && "Explainable AI Match Diagnostics"}
            {activeTab === 'compare' && "Homographic Alignment Validation"}
          </h3>

          <div className="glass-panel" style={{ padding: '8px 16px', display: 'flex', gap: '16px' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              RMSE: <strong style={{ color: 'var(--accent-success)' }}>{pipelineState.metrics.rmse}px</strong>
            </span>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Inliers: <strong style={{ color: 'var(--text-main)' }}>{pipelineState.metrics.inliers}</strong>
            </span>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Model: <strong style={{ color: 'var(--accent-secondary)' }}>{String(pipelineState.metrics.model).toUpperCase()}</strong>
            </span>
          </div>
        </header>

        <section className="glass-panel" style={{ flex: 1, padding: '24px', display: 'flex', flexDirection: 'column', position: 'relative' }}>
          {activeTab === 'raw' && <ImageViewer files={files} setFiles={setFiles} />}
          {activeTab === 'matches' && <MatchVisualizer sessionId={sessionId} metrics={pipelineState.metrics} />}
          {activeTab === 'compare' && <ComparisonModes sessionId={sessionId} />}

          {/* Overlay loader when processing */}
          {isProcessing && (
             <div style={{
                position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
                background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)',
                display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                zIndex: 10, borderRadius: 'var(--radius-md)'
             }}>
                <div style={{ width: '40px', height: '40px', border: '3px solid var(--border-subtle)', borderTopColor: 'var(--accent-primary)', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div>
                <h3 style={{ marginTop: '16px', color: 'var(--accent-primary)' }}>{pipelineState.stage.toUpperCase()}</h3>
                <p style={{ color: 'var(--text-muted)' }}>Executing mathematical constraints...</p>
                <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
             </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;