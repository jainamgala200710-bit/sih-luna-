const API_BASE = 'http://localhost:8000/api/v1';

export const apiService = {
  async uploadImages(sourceFile, referenceFile) {
    const formData = new FormData();
    formData.append('source', sourceFile);
    formData.append('reference', referenceFile);

    const response = await fetch(`${API_BASE}/upload/`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload images');
    }
    return await response.json();
  },

  async triggerRegistration(sessionId) {
    const response = await fetch(`${API_BASE}/registration/${sessionId}`, {
      method: 'POST'
    });

    if (!response.ok) {
      throw new Error('Failed to trigger pipeline');
    }
    return await response.json();
  },

  async fetchResults(sessionId) {
    const response = await fetch(`${API_BASE}/results/${sessionId}/summary`);

    if (!response.ok) {
      throw new Error('Failed to fetch results');
    }
    return await response.json();
  },

  getWebSocketUrl(sessionId) {
    return `ws://localhost:8000/api/v1/registration/ws/progress/${sessionId}`;
  },

  getImageUrl(sessionId, type, idx) {
      return `${API_BASE}/results/${sessionId}/dossier/${idx}/image/${type}`;
  },

  getRawImageUrl(sessionId, type) {
      return `${API_BASE}/results/${sessionId}/image/${type}`;
  }
};