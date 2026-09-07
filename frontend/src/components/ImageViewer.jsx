import React, { useState } from 'react';
import { Upload, FileCheck, Sparkles, AlertTriangle, RefreshCw, Crosshair, Database } from 'lucide-react';

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
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '8px', height: '100%' }}>
      {/* Zone Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0 4px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="telemetry-chip telemetry-chip-cyan" style={{ fontSize: '0.625rem' }}>
            {sensorTag}
          </span>
          <h4 style={{ fontSize: '0.875rem', color: 'var(--text-telemetry)' }}>{label}</h4>
        </div>
        {file && (
          <span className="telemetry-chip telemetry-chip-nominal" style={{ fontSize: '0.625rem' }}>
            <span className="ping-dot" /> {(file.size / 1024).toFixed(1)} KB
          </span>
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
            {/* HUD Corner Reticle Annotations */}
            <div style={{
              position: 'absolute',
              top: '12px',
              left: '12px',
              background: 'rgba(8, 13, 26, 0.85)',
              border: '1px solid var(--outline)',
              borderRadius: 'var(--radius-sm)',
              padding: '4px 8px',
              fontFamily: 'var(--font-telemetry)',
              fontSize: '0.6875rem',
              color: 'var(--primary-neon)',
              pointerEvents: 'none'
            }}>
              PAYLOAD: {file.name.substring(0, 20)}
            </div>

            <div style={{
              position: 'absolute',
              bottom: '12px',
              right: '12px',
              display: 'flex',
              gap: '6px'
            }}>
              <button
                className="btn btn-secondary"
                style={{ padding: '4px 10px', fontSize: '0.75rem', background: 'rgba(8, 13, 26, 0.85)' }}
                onClick={() => setFile(null)}
              >
                <RefreshCw size={12} /> Replace
              </button>
            </div>
          </>
        ) : (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '14px',
            padding: '24px',
            textAlign: 'center',
            zIndex: 1
          }}>
            <div style={{
              width: '54px',
              height: '54px',
              borderRadius: '50%',
              background: 'rgba(34, 211, 238, 0.08)',
              border: '1px solid rgba(34, 211, 238, 0.25)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--primary-neon)',
              boxShadow: '0 0 16px rgba(34, 211, 238, 0.1)'
            }}>
              <Upload size={24} />
            </div>

            <div>
              <p style={{ fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '0.9375rem', color: 'var(--text-telemetry)' }}>
                Drag & drop {label.toLowerCase()}
              </p>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-annotation)', marginTop: '4px' }}>
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
              style={{ fontSize: '0.8125rem', padding: '6px 14px' }}
              onClick={() => document.getElementById(`file-input-${role}`).click()}
            >
              Browse Files
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

const ImageViewer = ({ files, setFiles }) => {
  const [loadingPreset, setLoadingPreset] = useState(false);

  // Helper to load bundled demo pairs as File objects
  const loadPresetPair = async (presetType) => {
    try {
      setLoadingPreset(true);
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

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', height: '100%' }}>
      {/* Mission Proxy Pair Selector (from Required.md) */}
      <div className="glass-panel" style={{ padding: '10px 14px', display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Database size={15} color="var(--primary-neon)" />
          <span style={{ fontFamily: 'var(--font-telemetry)', fontSize: '0.75rem', color: 'var(--text-annotation)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
            Mission Pairs (Required.md):
          </span>
        </div>

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          <button
            className="btn btn-secondary"
            style={{ padding: '4px 10px', fontSize: '0.6875rem' }}
            onClick={() => loadPresetPair('tmc2_tmc2')}
            disabled={loadingPreset}
            title="TMC2 vs TMC2: Same sensor, temporal pass, minor noise (Status: SUCCESS, Inliers: 22, Affine)"
          >
            <Sparkles size={12} color="var(--status-nominal)" />
            TMC2 vs TMC2
          </button>

          <button
            className="btn btn-secondary"
            style={{ padding: '4px 10px', fontSize: '0.6875rem' }}
            onClick={() => loadPresetPair('ohrc_ohrc')}
            disabled={loadingPreset}
            title="OHRC vs OHRC: High-res sensor with 15° structural rotation (Status: SUCCESS, Inliers: 5, Partial Affine)"
          >
            <Sparkles size={12} color="var(--primary-neon)" />
            OHRC vs OHRC
          </button>

          <button
            className="btn btn-secondary"
            style={{ padding: '4px 10px', fontSize: '0.6875rem' }}
            onClick={() => loadPresetPair('ohrc_tmc2')}
            disabled={loadingPreset}
            title="OHRC vs TMC2: Extreme 20x scale differential (0.25m/px vs 5m/px), noise & sun gradient"
          >
            <AlertTriangle size={12} color="var(--status-warning)" />
            OHRC vs TMC2 (Extreme)
          </button>

          <button
            className="btn btn-violet"
            style={{ padding: '4px 10px', fontSize: '0.6875rem' }}
            onClick={() => loadPresetPair('stereo_dem')}
            disabled={loadingPreset}
            title="Stereo Lunar Crater Pair: Parallax baseline for OpenCV StereoSGBM 3D DEM generation"
          >
            <Sparkles size={12} color="var(--secondary-neon)" />
            Stereo Pair (3D DEM)
          </button>
        </div>
      </div>

      {/* Dual Split Viewports */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', flex: 1, minHeight: 0 }}>
        <FileDropzone
          label="Source Lunar Image"
          sensorTag="CHANDRAYAAN-2 / TMC-2"
          file={files.source}
          setFile={(f) => setFiles(prev => ({ ...prev, source: f }))}
          role="source"
        />
        <FileDropzone
          label="Reference Target Map"
          sensorTag="LROC-NAC / ORBITAL"
          file={files.reference}
          setFile={(f) => setFiles(prev => ({ ...prev, reference: f }))}
          role="reference"
        />
      </div>
    </div>
  );
};

export default ImageViewer;
