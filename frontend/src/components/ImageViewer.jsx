import React, { useState } from 'react';
import { Upload, FileCheck, Sparkles, AlertTriangle, RefreshCw, Crosshair, Database, Trash2, CheckCircle2 } from 'lucide-react';

const FileDropzone = ({ label, sensorTag, file, setFile, role }) => {
  const [drag, setDrag] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') setDrag(true);
    else if (e.type === 'dragleave') setDrag(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDrag(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '8px', height: '100%', minWidth: 0 }}>
      {/* Zone Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '2px 6px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="telemetry-chip telemetry-chip-cyan" style={{ fontSize: '0.6875rem' }}>
            {sensorTag}
          </span>
          <h4 style={{ fontSize: '0.9375rem', color: 'var(--text-telemetry)' }}>{label}</h4>
        </div>
        {file ? (
          <span className="telemetry-chip telemetry-chip-nominal" style={{ fontSize: '0.6875rem' }}>
            <span className="ping-dot" /> {(file.size / 1024).toFixed(1)} KB
          </span>
        ) : (
          <span style={{ fontSize: '0.6875rem', color: 'var(--text-muted)' }}>Awaiting Binary</span>
        )}
      </div>

      {/* Main Tactical Container */}
      <div
        className={`image-canvas-container tactical-corner ${!file ? 'radar-grid' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        style={{
          flex: 1,
          minHeight: '380px',
          borderColor: drag ? 'var(--primary-neon)' : 'var(--outline)',
          boxShadow: drag ? 'var(--glow-cyan)' : 'var(--shadow-hud)',
          transition: 'all 0.25s ease',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative'
        }}
      >
        {file ? (
          <>
            <img
              src={URL.createObjectURL(file)}
              alt={label}
              className="image-layer"
            />
            {/* HUD Reticle Annotations */}
            <div style={{
              position: 'absolute',
              top: '12px',
              left: '12px',
              background: 'rgba(8, 13, 26, 0.88)',
              border: '1px solid var(--outline)',
              borderRadius: 'var(--radius-sm)',
              padding: '6px 10px',
              fontFamily: 'var(--font-telemetry)',
              fontSize: '0.75rem',
              color: 'var(--primary-neon)',
              pointerEvents: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}>
              <FileCheck size={13} />
              <span>PAYLOAD: {file.name.substring(0, 24)}</span>
            </div>

            <div style={{
              position: 'absolute',
              bottom: '14px',
              right: '14px',
              display: 'flex',
              gap: '8px'
            }}>
              <button
                className="btn btn-secondary"
                style={{ padding: '6px 12px', fontSize: '0.75rem', background: 'rgba(8, 13, 26, 0.88)' }}
                onClick={() => setFile(null)}
              >
                <RefreshCw size={13} /> Replace Image
              </button>
            </div>
          </>
        ) : (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '16px',
            padding: '32px',
            textAlign: 'center',
            zIndex: 1
          }}>
            <div style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              background: 'rgba(34, 211, 238, 0.08)',
              border: '1px solid rgba(34, 211, 238, 0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--primary-neon)',
              boxShadow: '0 0 20px rgba(34, 211, 238, 0.15)'
            }}>
              <Upload size={28} />
            </div>

            <div>
              <p style={{ fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '1rem', color: 'var(--text-telemetry)' }}>
                Drag & drop {label.toLowerCase()}
              </p>
              <p style={{ fontSize: '0.8125rem', color: 'var(--text-annotation)', marginTop: '4px' }}>
                Supports PNG, TIFF, JPG, or Planetary IMG binaries
              </p>
            </div>

            <input
              type="file"
              accept="image/*,.png,.jpg,.jpeg,.tif,.tiff"
              onChange={(e) => setFile(e.target.files[0])}
              style={{ display: 'none' }}
              id={`file-input-${role}`}
            />

            <button
              className="btn btn-secondary"
              style={{ fontSize: '0.875rem', padding: '8px 18px' }}
              onClick={() => document.getElementById(`file-input-${role}`).click()}
            >
              Browse Local Disk
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

const ImageViewer = ({ files, setFiles }) => {
  const [loadingPreset, setLoadingPreset] = useState(false);
  const [activePreset, setActivePreset] = useState(null);

  // Helper to load bundled demo pairs as File objects
  const loadPresetPair = async (presetType) => {
    try {
      setLoadingPreset(true);
      setActivePreset(presetType);
      const srcUrl = `/demo_pairs/${presetType}/source.png`;
      const refUrl = `/demo_pairs/${presetType}/reference.png`;

      const [srcBlob, refBlob] = await Promise.all([
        fetch(srcUrl).then(r => {
          if (!r.ok) throw new Error('Preset source not found');
          return r.blob();
        }),
        fetch(refUrl).then(r => {
          if (!r.ok) throw new Error('Preset ref not found');
          return r.blob();
        })
      ]);

      const sourceFile = new File([srcBlob], `${presetType}_source.png`, { type: 'image/png' });
      const referenceFile = new File([refBlob], `${presetType}_reference.png`, { type: 'image/png' });

      setFiles({
        source: sourceFile,
        reference: referenceFile
      });
    } catch (e) {
      console.error('Failed to load preset:', e);
      alert('Could not load preset pair: ' + e.message);
    } finally {
      setLoadingPreset(false);
    }
  };

  const clearFiles = () => {
    setFiles({ source: null, reference: null });
    setActivePreset(null);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', height: '100%' }}>
      {/* Spacious Mission Proxy Pair Selector Command Bar */}
      <div className="glass-panel" style={{ padding: '12px 18px', display: 'flex', flexWrap: 'wrap', gap: '10px', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '28px',
            height: '28px',
            borderRadius: '6px',
            background: 'rgba(34, 211, 238, 0.12)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--primary-neon)'
          }}>
            <Database size={15} />
          </div>
          <div>
            <span style={{ fontFamily: 'var(--font-telemetry)', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-telemetry)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              Mission Benchmark Presets:
            </span>
            <p style={{ fontSize: '0.6875rem', color: 'var(--text-muted)' }}>
              1-Click ingest verified sensor pairs from Required.md
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
          <button
            className={`btn ${activePreset === 'tmc2_tmc2' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ padding: '6px 12px', fontSize: '0.75rem' }}
            onClick={() => loadPresetPair('tmc2_tmc2')}
            disabled={loadingPreset}
            title="TMC2 vs TMC2: Same sensor, temporal pass, minor noise (Status: SUCCESS, Inliers: 22, Affine)"
          >
            <Sparkles size={13} color={activePreset === 'tmc2_tmc2' ? '#080d1a' : 'var(--status-nominal)'} />
            <span>TMC2 vs TMC2</span>
            <span style={{ opacity: 0.8, fontSize: '0.625rem' }}>[Affine]</span>
          </button>

          <button
            className={`btn ${activePreset === 'ohrc_ohrc' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ padding: '6px 12px', fontSize: '0.75rem' }}
            onClick={() => loadPresetPair('ohrc_ohrc')}
            disabled={loadingPreset}
            title="OHRC vs OHRC: High-res sensor with 15° structural rotation (Status: SUCCESS, Inliers: 5, Partial Affine)"
          >
            <Sparkles size={13} color={activePreset === 'ohrc_ohrc' ? '#080d1a' : 'var(--primary-neon)'} />
            <span>OHRC vs OHRC</span>
            <span style={{ opacity: 0.8, fontSize: '0.625rem' }}>[Rot 15°]</span>
          </button>

          <button
            className={`btn ${activePreset === 'ohrc_tmc2' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ padding: '6px 12px', fontSize: '0.75rem' }}
            onClick={() => loadPresetPair('ohrc_tmc2')}
            disabled={loadingPreset}
            title="OHRC vs TMC2: Extreme 20x scale differential (0.25m/px vs 5m/px), noise & sun gradient"
          >
            <AlertTriangle size={13} color={activePreset === 'ohrc_tmc2' ? '#080d1a' : 'var(--status-warning)'} />
            <span>OHRC vs TMC2</span>
            <span style={{ opacity: 0.8, fontSize: '0.625rem' }}>[20x Scale]</span>
          </button>

          <button
            className={`btn ${activePreset === 'stereo_dem' ? 'btn-primary' : 'btn-violet'}`}
            style={{ padding: '6px 14px', fontSize: '0.75rem' }}
            onClick={() => loadPresetPair('stereo_dem')}
            disabled={loadingPreset}
            title="Stereo Lunar Crater Pair: Parallax baseline for OpenCV StereoSGBM 3D DEM generation"
          >
            <Sparkles size={13} color={activePreset === 'stereo_dem' ? '#080d1a' : 'var(--secondary-neon)'} />
            <span>Stereo Pair (3D DEM)</span>
          </button>

          {(files.source || files.reference) && (
            <button
              className="btn btn-secondary"
              onClick={clearFiles}
              style={{ padding: '6px 10px', fontSize: '0.75rem', color: 'var(--text-muted)' }}
              title="Clear Loaded Images"
            >
              <Trash2 size={13} />
            </button>
          )}
        </div>
      </div>

      {/* Dual Split Viewports with Generous Breathing Room */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', flex: 1, minHeight: 0 }}>
        <FileDropzone
          label="Source Lunar Image"
          sensorTag="CHANDRAYAAN-2 / TMC-2"
          file={files.source}
          setFile={(f) => {
            setFiles(prev => ({ ...prev, source: f }));
            setActivePreset(null);
          }}
          role="source"
        />
        <FileDropzone
          label="Reference Target Map"
          sensorTag="LROC-NAC / ORBITAL"
          file={files.reference}
          setFile={(f) => {
            setFiles(prev => ({ ...prev, reference: f }));
            setActivePreset(null);
          }}
          role="reference"
        />
      </div>
    </div>
  );
};

export default ImageViewer;
