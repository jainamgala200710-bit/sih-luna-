import React, { useState, useEffect, useRef } from 'react';
import { apiService } from '../services/apiService';

const ComparisonModes = ({ sessionId }) => {
  const [mode, setMode] = useState('blend'); // blend, swipe, flicker
  const [sourceImage, setSourceImage] = useState(null);
  const [referenceImage, setReferenceImage] = useState(null);
  const [H, setH] = useState(null); // Homography matrix
  const [isLoaded, setIsLoaded] = useState(false);
  const [swipePosition, setSwipePosition] = useState(50); // 0-100% for swipe mode
  const [flickerInterval, setFlickerInterval] = useState(null);
  const [showSource, setShowSource] = useState(true); // For flicker mode

  const canvasRef = useRef(null);

  // Load images and homography data when sessionId changes
  useEffect(() => {
    if (!sessionId) return;

    // Fetch results to get homography matrix
    apiService.fetchResults(sessionId)
      .then(results => {
        if (results.H_matrix) {
          setH(results.H_matrix);
        }
      })
      .catch(err => {
        console.error('Failed to fetch results:', err);
      });

    // Load source and reference images using the API
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

    // Cleanup flicker interval on unmount or sessionId change
    return () => {
      if (flickerInterval) {
        clearInterval(flickerInterval);
      }
    };
  }, [sessionId]);

  // Start/stop flicker interval based on mode
  useEffect(() => {
    if (mode === 'flicker' && isLoaded) {
      const interval = setInterval(() => {
        setShowSource(!showSource);
      }, 500); // Flicker every 500ms
      setFlickerInterval(interval);
    } else {
      if (flickerInterval) {
        clearInterval(flickerInterval);
        setFlickerInterval(null);
      }
    }

    return () => {
      if (flickerInterval) {
        clearInterval(flickerInterval);
      }
    };
  }, [mode, isLoaded, flickerInterval]);

  // Apply homography transformation and draw to canvas
  useEffect(() => {
    if (!isLoaded || !sourceImage || !referenceImage || !H || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    // Set canvas size to match images (assuming same size)
    canvas.width = sourceImage.width;
    canvas.height = sourceImage.height;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Depending on mode, draw differently
    if (mode === 'blend') {
      drawBlendMode(ctx, sourceImage, referenceImage, H);
    } else if (mode === 'swipe') {
      drawSwipeMode(ctx, sourceImage, referenceImage, H, swipePosition);
    } else if (mode === 'flicker') {
      drawFlickerMode(ctx, sourceImage, referenceImage, H, showSource);
    }
  }, [isLoaded, sourceImage, referenceImage, H, mode, swipePosition, showSource]);

  // Draw blend mode: alpha blend source and warped reference
  const drawBlendMode = (ctx, sourceImg, referenceImg, H) => {
    // Draw source image
    ctx.globalAlpha = 1.0;
    ctx.drawImage(sourceImg, 0, 0);

    // Save context for transformation
    ctx.save();

    // Apply homography with translation compensation to keep images aligned and visible
    ctx.translate(-H[0][2], -H[1][2]);
    ctx.transform(
      H[0][0], H[1][0],
      H[0][1], H[1][1],
      0, 0
    );

    // Draw reference image with transformation and alpha blend
    ctx.globalAlpha = 0.5;
    ctx.drawImage(referenceImg, 0, 0);
    ctx.restore();
  };

  // Draw swipe mode: split screen with slider
  const drawSwipeMode = (ctx, sourceImg, referenceImg, H, position) => {
    // Draw source image on left side
    ctx.save();
    ctx.beginPath();
    ctx.rect(0, 0, canvas.width * position / 100, canvas.height);
    ctx.clip();
    ctx.drawImage(sourceImg, 0, 0);
    ctx.restore();

    // Draw warped reference image on right side
    ctx.save();
    ctx.beginPath();
    ctx.rect(canvas.width * position / 100, 0, canvas.width * (100 - position) / 100, canvas.height);
    ctx.clip();

    // Apply homography transformation with compensation
    ctx.translate(-H[0][2], -H[1][2]);
    ctx.transform(
      H[0][0], H[1][0],
      H[0][1], H[1][1],
      0, 0
    );
    ctx.drawImage(referenceImg, 0, 0);
    ctx.restore();

    // Draw slider handle
    ctx.fillStyle = 'var(--accent-primary)';
    ctx.fillRect(
      canvas.width * position / 100 - 2,
      0,
      4,
      canvas.height
    );
  };

  // Draw flicker mode: alternate between source and warped reference
  const drawFlickerMode = (ctx, sourceImg, referenceImg, H, showSource) => {
    if (showSource) {
      ctx.drawImage(sourceImg, 0, 0);
    } else {
      ctx.save();
      // Apply homography transformation with compensation
      ctx.translate(-H[0][2], -H[1][2]);
      ctx.transform(
        H[0][0], H[1][0],
        H[0][1], H[1][1],
        0, 0
      );
      ctx.drawImage(referenceImg, 0, 0);
      ctx.restore();
    }
  };

  if (!sessionId) {
    return (
      <div className="image-canvas-container hover-lift" style={{
        height: '600px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--border-focus)',
        background: 'var(--bg-elevated)',
        border: '1px dashed var(--accent-secondary)'
      }}>
        <p>No session selected</p>
      </div>
    );
  }

  if (!isLoaded) {
    return (
      <div className="image-canvas-container hover-lift" style={{
        height: '600px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--border-focus)',
        background: 'var(--bg-elevated)',
        border: '1px dashed var(--accent-secondary)'
      }}>
        <p>Loading registration results...</p>
        <div style={{
          width: '40px',
          height: '40px',
          border: '3px solid var(--border-subtle)',
          borderTopColor: 'var(--accent-primary)',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
          marginTop: '16px'
        }}></div>
        <style>{`
          @keyframes spin {
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', height: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h4 style={{ color: 'var(--text-main)' }}>Registration Validation Layer</h4>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            className={`btn ${mode === 'blend' ? 'btn-primary' : ''}`}
            onClick={() => setMode('blend')}
            style={{ padding: '6px 12px', fontSize: '0.8rem' }}
          >
            Alpha Blend
          </button>
          <button
            className={`btn ${mode === 'swipe' ? 'btn-primary' : ''}`}
            onClick={() => setMode('swipe')}
            style={{ padding: '6px 12px', fontSize: '0.8rem' }}
          >
            Slider Swipe
          </button>
          <button
            className={`btn ${mode === 'flicker' ? 'btn-primary' : ''}`}
            onClick={() => setMode('flicker')}
            style={{ padding: '6px 12px', fontSize: '0.8rem' }}
          >
            Flicker
          </button>
        </div>
      </div>

      <div className="image-canvas-container hover-lift" style={{
        height: '600px',
        position: 'relative'
      }}>
        <canvas
          ref={canvasRef}
          width="800"
          height="600"
          style={{
            width: '100%',
            height: '100%',
            display: 'block'
          }}
        />

        {/* Swipe mode slider */}
        {mode === 'swipe' && (
          <div style={{
            position: 'absolute',
            bottom: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: '80%',
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}>
            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Swipe Position</span>
            <input
              type="range"
              min="0"
              max="100"
              value={swipePosition}
              onChange={(e) => setSwipePosition(parseInt(e.target.value))}
              style={{ flex: 1 }}
            />
            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>{swipePosition}%</span>
          </div>
        )}

        {/* Flicker mode info */}
        {mode === 'flicker' && (
          <div style={{
            position: 'absolute',
            top: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'rgba(0,0,0,0.6)',
            color: 'white',
            padding: '8px 16px',
            borderRadius: '4px',
            fontSize: '0.9rem'
          }}>
            Flicker mode: alternating images every 500ms
          </div>
        )}
      </div>
    </div>
  );
};

export default ComparisonModes;