'use client';

import { useState, useEffect, FormEvent, ChangeEvent } from 'react';
import { apiCall, formatFileSize } from '@/lib/api';
import { useRouter } from 'next/navigation';

interface Document {
  id: string;
  original_filename: string;
  file_size: number;
  page_count: number | null;
  status: string;
  error_message: string | null;
  created_at: string;
}

interface QueryHistoryItem {
  question: string;
  answer: string;
  created_at: string;
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
  const [qaHistory, setQaHistory] = useState<QueryHistoryItem[]>([]);
  const [question, setQuestion] = useState('');
  const [asking, setAsking] = useState(false);
  const router = useRouter();

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const docs = await apiCall('/documents/');
      setDocuments(docs);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setError('');
    }
  };

  const handleUpload = async (e: FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    // Check file size (50MB limit)
    const maxSize = 50 * 1024 * 1024; // 50MB
    if (selectedFile.size > maxSize) {
      setError('File size exceeds 50MB limit');
      return;
    }

    setUploading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const token = localStorage.getItem('access_token');
      
      // Connect directly to FastAPI backend (bypass Next.js proxy for large file uploads)
      // This avoids Next.js 10MB body size limit
      const response = await fetch('http://127.0.0.1:8000/api/documents/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Upload failed');
      }

      setSelectedFile(null);
      const fileInput = document.getElementById('document-file') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
      await loadDocuments();
    } catch (err: any) {
      setError(err.message || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const showDocumentQA = async (doc: Document) => {
    setSelectedDoc(doc);
    setQaHistory([]);
    
    try {
      const history = await apiCall(`/documents/${doc.id}/history`);
      setQaHistory(history.reverse());
    } catch (err: any) {
      console.error('Error loading history:', err);
    }
  };

  const handleAskQuestion = async (e: FormEvent) => {
    e.preventDefault();
    if (!question.trim() || !selectedDoc) return;

    setAsking(true);
    const currentQuestion = question;
    setQuestion('');

    // Optimistically add question to UI
    setQaHistory(prev => [...prev, {
      question: currentQuestion,
      answer: 'Thinking...',
      created_at: new Date().toISOString()
    }]);

    try {
      const response = await apiCall(`/documents/${selectedDoc.id}/query`, {
        method: 'POST',
        body: JSON.stringify({ question: currentQuestion })
      });

      // Update with real answer
      setQaHistory(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          question: currentQuestion,
          answer: response.answer,
          created_at: new Date().toISOString()
        };
        return updated;
      });
    } catch (err: any) {
      setQaHistory(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          question: currentQuestion,
          answer: `Error: ${err.message}`,
          created_at: new Date().toISOString()
        };
        return updated;
      });
    } finally {
      setAsking(false);
    }
  };

  const exportToPDF = async (documentId: string) => {
    try {
      const response = await apiCall('/exports/pdf', {
        method: 'POST',
        body: JSON.stringify({ document_id: documentId, format: 'pdf' })
      });

      // Download file
      const token = localStorage.getItem('access_token');
      const fileResponse = await fetch(response.download_url, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      const blob = await fileResponse.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analysis_${documentId}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    }
  };

  const exportToWord = async (documentId: string) => {
    try {
      const response = await apiCall('/exports/docx', {
        method: 'POST',
        body: JSON.stringify({ document_id: documentId, format: 'docx' })
      });

      const token = localStorage.getItem('access_token');
      const fileResponse = await fetch(response.download_url, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      const blob = await fileResponse.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analysis_${documentId}.docx`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    }
  };

  if (selectedDoc) {
    return (
      <div className="qa-container" style={{ maxWidth: '900px', margin: '0 auto' }}>
        <div className="qa-header" style={{ marginBottom: '2rem' }}>
          <button
            className="btn btn-link"
            onClick={() => setSelectedDoc(null)}
            style={{ marginBottom: '1rem' }}
          >
            ← Back to Documents
          </button>
          <h2>{selectedDoc.original_filename}</h2>
        </div>

        <div className="export-buttons" style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
          <button className="btn btn-secondary" onClick={() => exportToPDF(selectedDoc.id)}>
            Export to PDF
          </button>
          <button className="btn btn-secondary" onClick={() => exportToWord(selectedDoc.id)}>
            Export to Word
          </button>
        </div>

        <div className="qa-chat" style={{ backgroundColor: 'var(--bg-primary)', borderRadius: '0.5rem', boxShadow: 'var(--shadow-md)', marginBottom: '1rem' }}>
          <div className="qa-history" style={{ padding: '1.5rem', maxHeight: '500px', overflowY: 'auto' }}>
            {qaHistory.length === 0 ? (
              <p style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '3rem' }}>
                No questions yet. Ask your first question below!
              </p>
            ) : (
              qaHistory.map((item, index) => (
                <div key={index} className="qa-item" style={{ marginBottom: '1.5rem', paddingBottom: '1.5rem', borderBottom: '1px solid var(--border-color)' }}>
                  <div className="qa-question" style={{ marginBottom: '0.75rem', color: 'var(--text-primary)' }}>
                    <strong>Q:</strong> {item.question}
                  </div>
                  <div className="qa-answer" style={{ padding: '1rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '0.375rem', color: 'var(--text-primary)', lineHeight: '1.6' }}>
                    <strong>A:</strong> {item.answer}
                  </div>
                  <div className="qa-timestamp" style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    {new Date(item.created_at).toLocaleString()}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        <form onSubmit={handleAskQuestion} className="qa-form" style={{ display: 'flex', gap: '1rem' }}>
          <input
            type="text"
            className="form-control"
            placeholder="Ask a question about this document..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={asking}
            style={{ flex: 1 }}
          />
          <button type="submit" className="btn btn-primary" disabled={asking || !question.trim()}>
            {asking ? 'Asking...' : 'Ask'}
          </button>
        </form>
      </div>
    );
  }

  return (
    <div>
      <h2 style={{ marginBottom: '2rem' }}>Document Intelligence</h2>
      
      <div className="documents-container" style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
        <div className="upload-section" style={{ backgroundColor: 'var(--bg-primary)', padding: '2rem', borderRadius: '0.5rem', boxShadow: 'var(--shadow-md)' }}>
          <h3 style={{ marginBottom: '1.5rem' }}>Upload Document</h3>
          <form onSubmit={handleUpload}>
            <div className="form-group">
              <label
                htmlFor="document-file"
                style={{
                  display: 'block',
                  padding: '3rem',
                  border: '2px dashed var(--border-color)',
                  borderRadius: '0.5rem',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = 'var(--primary-color)';
                  e.currentTarget.style.backgroundColor = 'rgba(37, 99, 235, 0.05)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'var(--border-color)';
                  e.currentTarget.style.backgroundColor = 'transparent';
                }}
              >
                <span style={{ display: 'block', fontSize: '1.1rem', color: 'var(--text-primary)' }}>
                  {selectedFile ? selectedFile.name : 'Choose PDF or Image'}
                </span>
                <input
                  type="file"
                  id="document-file"
                  accept=".pdf,.png,.jpg,.jpeg,.tiff"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                />
              </label>
              <p style={{ marginTop: '0.5rem', fontSize: '0.875rem', color: 'var(--text-secondary)', textAlign: 'center' }}>
                Supported: PDF, PNG, JPG, TIFF (max 50MB)
              </p>
            </div>
            {error && <div className="error-message">{error}</div>}
            {uploading && (
              <div style={{ margin: '1rem 0' }}>
                <div style={{ width: '100%', height: '8px', backgroundColor: 'var(--bg-secondary)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', backgroundColor: 'var(--primary-color)', width: '50%', animation: 'progress 1.5s ease-in-out infinite' }} />
                </div>
                <p style={{ textAlign: 'center', color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
                  Uploading and processing...
                </p>
              </div>
            )}
            <button type="submit" className="btn btn-primary btn-block" disabled={!selectedFile || uploading}>
              {uploading ? 'Uploading...' : 'Upload & Analyze'}
            </button>
          </form>
        </div>

        <div className="documents-list-section" style={{ backgroundColor: 'var(--bg-primary)', padding: '2rem', borderRadius: '0.5rem', boxShadow: 'var(--shadow-md)' }}>
          <h3 style={{ marginBottom: '1.5rem' }}>Your Documents</h3>
          <div className="documents-list">
            {loading ? (
              <div className="spinner" />
            ) : documents.length === 0 ? (
              <p style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
                No documents yet. Upload your first document above!
              </p>
            ) : (
              documents.map(doc => (
                <div
                  key={doc.id}
                  className="document-card"
                  style={{
                    padding: '1.5rem',
                    border: '1px solid var(--border-color)',
                    borderRadius: '0.5rem',
                    marginBottom: '1rem',
                    transition: 'all 0.3s ease',
                    cursor: doc.status === 'completed' ? 'pointer' : 'default'
                  }}
                  onMouseEnter={(e) => {
                    if (doc.status === 'completed') {
                      e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                      e.currentTarget.style.borderColor = 'var(--primary-color)';
                    }
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.boxShadow = 'none';
                    e.currentTarget.style.borderColor = 'var(--border-color)';
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                    <h4 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--text-primary)' }}>
                      {doc.original_filename}
                    </h4>
                    <span
                      style={{
                        padding: '0.25rem 0.75rem',
                        borderRadius: '1rem',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        textTransform: 'uppercase',
                        backgroundColor: doc.status === 'completed' ? '#d1fae5' : doc.status === 'failed' ? '#fee2e2' : '#fef3c7',
                        color: doc.status === 'completed' ? 'var(--success-color)' : doc.status === 'failed' ? 'var(--danger-color)' : '#f59e0b'
                      }}
                    >
                      {doc.status}
                    </span>
                  </div>
                  <div style={{ display: 'flex', gap: '1rem', fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                    <span>{formatFileSize(doc.file_size)}</span>
                    {doc.page_count && <span>{doc.page_count} pages</span>}
                    <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                  </div>
                  {doc.status === 'completed' ? (
                    <button
                      className="btn btn-secondary"
                      onClick={() => showDocumentQA(doc)}
                      style={{ width: '100%' }}
                    >
                      Ask Questions
                    </button>
                  ) : doc.status === 'failed' ? (
                    <p className="error-message">{doc.error_message || 'Processing failed'}</p>
                  ) : (
                    <p style={{ color: '#f59e0b', fontStyle: 'italic', margin: 0 }}>
                      Processing... Check back in a moment
                    </p>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

