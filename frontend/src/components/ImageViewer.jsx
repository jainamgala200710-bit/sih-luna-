import React, { useState } from 'react';
import { Upload } from 'lucide-react';

const FileDropzone = ({ label, file, setFile }) => {
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
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <h4 style={{ textAlign: 'center', color: 'var(--text-muted)' }}>{label}</h4>
      <div 
        className="image-canvas-container hover-lift" 
        onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}
        style={{ 
          borderColor: drag ? 'var(--accent-primary)' : 'var(--border-subtle)',
          boxShadow: drag ? 'var(--shadow-glow)' : 'none'
        }}
      >
        {file ? (
          <img src={URL.createObjectURL(file)} alt={label} className="image-layer" />
        ) : (
          <div style={{ 
            width: '100%', height: '100%', display: 'flex', flexDirection: 'column', 
            alignItems: 'center', justifyContent: 'center', color: 'var(--border-subtle)', gap: '16px',
            background: 'linear-gradient(45deg, var(--bg-base) 25%, transparent 25%, transparent 75%, var(--bg-base) 75%, var(--bg-base)), linear-gradient(45deg, var(--bg-base) 25%, transparent 25%, transparent 75%, var(--bg-base) 75%, var(--bg-base))',
            backgroundSize: '20px 20px', backgroundPosition: '0 0, 10px 10px'
          }}>
            <Upload size={32} />
            <p>Drag & Drop {label.split(' ')[0]} Image</p>
            <input type="file" onChange={(e) => setFile(e.target.files[0])} style={{ display: 'none' }} id={`file-${label}`} />
            <button className="btn" onClick={() => document.getElementById(`file-${label}`).click()}>
              Browse Files
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

const ImageViewer = ({ files, setFiles }) => {
  return (
    <div style={{ display: 'flex', gap: '24px', height: '100%' }}>
      <FileDropzone 
        label="Source Image (Unregistered)" 
        file={files.source} 
        setFile={(f) => setFiles(prev => ({...prev, source: f}))} 
      />
      <FileDropzone 
        label="Reference Target" 
        file={files.reference} 
        setFile={(f) => setFiles(prev => ({...prev, reference: f}))} 
      />
    </div>
  );
};

export default ImageViewer;
