import React, { useState, useEffect, useRef } from 'react';
import { apiService } from '../services/apiService';
import { Layers, Sliders, Eye, RefreshCw, Grid, Maximize2 } from 'lucide-react';

const ComparisonModes = ({ sessionId }) => {
  const [mode, setMode] = useState('blend'); // blend, swipe, flicker
  const [sourceImage, setSourceImage] = useState(null);
  const [referenceImage, setReferenceImage] = useState(null);
  const [H, setH] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [swipePosition, setSwipePosition] = useState(50);
  const [blendAlpha, setBlendAlpha] = useState(0.5);
  const [flickerSpeed, setFlickerSpeed] = useState(500); // ms
  const [showSource, setShowSource] = useState(true);
  const [showGrid, setShowGrid] = useState(true);

  const canvasRef = useRef(null);
  const containerRef = useRef(null);

  const [resultsMeta, setResultsMeta] = useState(null);

  // Load images and homography matrix
  useEffect(() => {
    if (!sessionId) return;

    apiService.fetchResults(sessionId)
      .then(results => {
        setResultsMeta(results);
        if (results.H_matrix) {
          setH(results.H_matrix);
        }
      })
      .catch(err => {
        console.error('Failed to fetch results:', err);
      });

    const loadImage = (url) => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = (err) => reject(err);
        img.src = url;
      });
    };

    Promise.all([
      loadImage(apiService.getRawImageUrl(sessionId, 'source')),
      loadImage(apiService.getRawImageUrl(sessionId, 'reference'))
    ])
      .then(([srcImg, refImg]) => {
        setSourceImage(srcImg);
        setReferenceImage(refImg);
        setIsLoaded(true);
      })
      .catch(err => {
        console.error('Failed to load images:', err);
      });
  }, [sessionId]);

  // Flicker interval timer
  useEffect(() => {
    if (mode === 'flicker' && isLoaded) {
      const interval = setInterval(() => {
        setShowSource(prev => !prev);
      }, flickerSpeed);
      return () => clearInterval(interval);
    }
  }, [mode, isLoaded, flickerSpeed]);

  // Canvas rendering - Works even when H is null (fallback to Identity matrix for unwarped comparison)
  useEffect(() => {
    if (!isLoaded || !sourceImage || !referenceImage || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    canvas.width = sourceImage.width;
    canvas.height = sourceImage.height;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Fallback Identity matrix if H is null (e.g. OHRC vs TMC2 extreme scale differential)
    const effectiveH = H || [[1, 0, 0], [0, 1, 0], [0, 0, 1]];

    if (mode === 'blend') {
      drawBlendMode(ctx, sourceImage, referenceImage, effectiveH, blendAlpha);
    } else if (mode === 'swipe') {
      drawSwipeMode(ctx, sourceImage, referenceImage, effectiveH, swipePosition);
    } else if (mode === 'flicker') {
      drawFlickerMode(ctx, sourceImage, referenceImage, effectiveH, showSource);
    }

    if (showGrid) {
      drawTacticalGrid(ctx, canvas.width, canvas.height);
    }
  }, [isLoaded, sourceImage, referenceImage, H, mode, swipePosition, blendAlpha, showSource, showGrid]);

  const drawTacticalGrid = (ctx, w, h) => {
    ctx.save();
    ctx.strokeStyle = 'rgba(34, 211, 238, 0.15)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);

    const step = 64;
    for (let x = step; x < w; x += step) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }
    for (let y = step; y < h; y += step) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    // Center Crosshair
    ctx.strokeStyle = 'rgba(34, 211, 238, 0.4)';
    ctx.setLineDash([]);
    ctx.beginPath();
    ctx.moveTo(w / 2 - 20, h / 2);
    ctx.lineTo(w / 2 + 20, h / 2);
    ctx.moveTo(w / 2, h / 2 - 20);
    ctx.lineTo(w / 2, h / 2 + 20);
    ctx.stroke();

    ctx.restore();
  };

  const drawBlendMode = (ctx, sourceImg, referenceImg, H, alpha) => {
    ctx.globalAlpha = 1.0;
    ctx.drawImage(sourceImg, 0, 0);

    ctx.save();
    ctx.translate(-H[0][2], -H[1][2]);
    ctx.transform(H[0][0], H[1][0], H[0][1], H[1][1], 0, 0);
    ctx.globalAlpha = alpha;
    ctx.drawImage(referenceImg, 0, 0);
    ctx.restore();
  };

  const drawSwipeMode = (ctx, sourceImg, referenceImg, H, position) => {
    const splitX = (canvasRef.current.width * position) / 100;

    // Left side: Source
    ctx.save();
    ctx.beginPath();
    ctx.rect(0, 0, splitX, canvasRef.current.height);
    ctx.clip();
    ctx.drawImage(sourceImg, 0, 0);
    ctx.restore();

    // Right side: Warped Reference
    ctx.save();
    ctx.beginPath();
    ctx.rect(splitX, 0, canvasRef.current.width - splitX, canvasRef.current.height);
    ctx.clip();
    ctx.translate(-H[0][2], -H[1][2]);
    ctx.transform(H[0][0], H[1][0], H[0][1], H[1][1], 0, 0);
    ctx.drawImage(referenceImg, 0, 0);
    ctx.restore();

    // Dividing Laser Line
    ctx.save();
    ctx.strokeStyle = 'var(--primary-neon)';
    ctx.lineWidth = 2;
    ctx.shadowColor = 'var(--primary-neon)';
    ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.moveTo(splitX, 0);
    ctx.lineTo(splitX, canvasRef.current.height);
    ctx.stroke();
    ctx.restore();
  };

  const drawFlickerMode = (ctx, sourceImg, referenceImg, H, isSource) => {
    if (isSource) {
      ctx.drawImage(sourceImg, 0, 0);
    } else {
      ctx.save();
      ctx.translate(-H[0][2], -H[1][2]);
      ctx.transform(H[0][0], H[1][0], H[0][1], H[1][1], 0, 0);
      ctx.drawImage(referenceImg, 0, 0);
      ctx.restore();
    }
  };

  if (!sessionId) {
    return (
      <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-annotation)' }}>
        <Layers size={32} style={{ color: 'var(--primary-neon)', margin: '0 auto 1rem', opacity: 0.8 }} />
        <h4 style={{ color: 'var(--text-telemetry)' }}>REGISTRATION LAYER INACTIVE</h4>
        <p style={{ fontSize: '0.8125rem', marginTop: '0.5rem' }}>
          Execute the registration pipeline to compute the projective homography matrix.
        </p>
      </div>
    );
  }

  if (!isLoaded) {
    return (
      <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-annotation)' }}>
        <span className="ping-dot" style={{ color: 'var(--primary-neon)', width: '10px', height: '10px' }} />
        <p style={{ marginTop: '1rem', fontFamily: 'var(--font-telemetry)', fontSize: '0.8125rem' }}>
          WARPING ORBITAL LAYERS WITH HOMOGRAPHY MATRIX...
        </p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', height: '100%' }}>
      {/* Tactical Toolbar */}
      <div className="glass-panel" style={{ padding: '10px 14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {/* Mode Selectors */}
        <div style={{ display: 'flex', gap: '6px' }}>
          <button
            className={`btn ${mode === 'blend' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setMode('blend')}
            style={{ padding: '6px 14px', fontSize: '0.75rem' }}
          >
            <Layers size={14} /> Alpha Blend
          </button>
          <button
            className={`btn ${mode === 'swipe' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setMode('swipe')}
            style={{ padding: '6px 14px', fontSize: '0.75rem' }}
          >
            <Sliders size={14} /> Split Swipe
          </button>
          <button
            className={`btn ${mode === 'flicker' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setMode('flicker')}
            style={{ padding: '6px 14px', fontSize: '0.75rem' }}
          >
            <Eye size={14} /> Frequency Flicker
          </button>
        </div>

        {/* Dynamic Controls based on mode */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {mode === 'blend' && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontFamily: 'var(--font-telemetry)', fontSize: '0.6875rem', color: 'var(--text-annotation)' }}>
                OPACITY: {(blendAlpha * 100).toFixed(0)}%
              </span>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={blendAlpha}
                onChange={(e) => setBlendAlpha(parseFloat(e.target.value))}
                style={{ width: '100px' }}
              />
            </div>
          )}

          {mode === 'swipe' && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontFamily: 'var(--font-telemetry)', fontSize: '0.6875rem', color: 'var(--text-annotation)' }}>
                SPLIT: {swipePosition}%
              </span>
              <input
                type="range"
                min="0"
                max="100"
                value={swipePosition}
                onChange={(e) => setSwipePosition(parseInt(e.target.value))}
                style={{ width: '120px' }}
              />
            </div>
          )}

          {mode === 'flicker' && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontFamily: 'var(--font-telemetry)', fontSize: '0.6875rem', color: 'var(--text-annotation)' }}>
                FREQ:
              </span>
              {[
                { label: '1 Hz', ms: 1000 },
                { label: '2 Hz', ms: 500 },
                { label: '4 Hz', ms: 250 }
              ].map(f => (
                <button
                  key={f.label}
                  className={`btn ${flickerSpeed === f.ms ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ padding: '3px 8px', fontSize: '0.6875rem' }}
                  onClick={() => setFlickerSpeed(f.ms)}
                >
                  {f.label}
                </button>
              ))}
            </div>
          )}

          {/* Grid Reticle Toggle */}
          <button
            className={`btn ${showGrid ? 'btn-secondary' : ''}`}
            onClick={() => setShowGrid(!showGrid)}
            title="Toggle Tactical Reticle Grid"
            style={{
              padding: '6px 10px',
              fontSize: '0.75rem',
              color: showGrid ? 'var(--primary-neon)' : 'var(--text-muted)',
              borderColor: showGrid ? 'rgba(34, 211, 238, 0.4)' : 'var(--outline)'
            }}
          >
            <Grid size={14} />
          </button>
        </div>
      </div>

      {/* Main Validation Viewport */}
      <div
        ref={containerRef}
        className="image-canvas-container tactical-corner"
        style={{ flex: 1, minHeight: 0, position: 'relative' }}
      >
        <canvas
          ref={canvasRef}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            display: 'block'
          }}
        />

        {/* HUD Overlay Labels */}
        <div style={{
          position: 'absolute',
          top: '12px',
          left: '12px',
          display: 'flex',
          flexDirection: 'column',
          gap: '6px',
          pointerEvents: 'none',
          maxWidth: '85%'
        }}>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            {H ? (
              <span className="telemetry-chip telemetry-chip-cyan" style={{ fontSize: '0.625rem' }}>
                HOMOGRAPHY PROJECTED ({resultsMeta?.model || 'AFFINE'})
              </span>
            ) : (
              <span className="telemetry-chip telemetry-chip-warning" style={{ fontSize: '0.625rem' }}>
                ⚠️ PRE-REGISTRATION INSPECTION (INSUFFICIENT INLIERS &lt; 4)
              </span>
            )}

            {mode === 'flicker' && (
              <span className="telemetry-chip telemetry-chip-violet" style={{ fontSize: '0.625rem' }}>
                ACTIVE: {showSource ? 'SOURCE BINARY' : (H ? 'WARPED REFERENCE' : 'UNWARPED REFERENCE')}
              </span>
            )}
            {mode === 'swipe' && (
              <span className="telemetry-chip telemetry-chip-nominal" style={{ fontSize: '0.625rem' }}>
                LEFT: SOURCE | RIGHT: {H ? 'WARPED TARGET' : 'UNWARPED TARGET'}
              </span>
            )}
          </div>

          {!H && (
            <div style={{
              background: 'rgba(245, 158, 11, 0.15)',
              border: '1px solid rgba(245, 158, 11, 0.4)',
              borderRadius: 'var(--radius-sm)',
              padding: '6px 10px',
              color: 'var(--status-warning)',
              fontSize: '0.6875rem',
              fontFamily: 'var(--font-telemetry)'
            }}>
              DIAGNOSTIC AUTOPSY: 20x Scale differential & illumination gradient inverted local gradient histograms. Unwarped layers loaded for visual inspection.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ComparisonModes;