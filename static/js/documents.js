/**
 * Documents Module
 * Handles document upload, processing, and Q&A
 */

// Show documents page
async function showDocumentsPage() {
    const documentsPage = document.getElementById('documents-page');
    
    documentsPage.innerHTML = `
        <div class="documents-container">
            <div class="upload-section">
                <h2>Upload Document</h2>
                <form id="upload-form" class="upload-form">
                    <div class="form-group">
                        <label for="document-file" class="file-upload-label">
                            <span class="file-upload-text">Choose PDF or Image</span>
                            <input 
                                type="file" 
                                id="document-file" 
                                accept=".pdf,.png,.jpg,.jpeg,.tiff"
                                class="file-input"
                                required
                            />
                        </label>
                        <p class="file-hint">Supported: PDF, PNG, JPG, TIFF (max 50MB)</p>
                    </div>
                    <div id="upload-error" class="error-message hidden"></div>
                    <div id="upload-progress" class="hidden">
                        <div class="progress-bar">
                            <div class="progress-fill" id="progress-fill"></div>
                        </div>
                        <p class="progress-text">Uploading...</p>
                    </div>
                    <button type="submit" class="btn btn-primary" id="upload-btn">
                        Upload & Analyze
                    </button>
                </form>
            </div>
            
            <div class="documents-list-section">
                <h2>Your Documents</h2>
                <div id="documents-list" class="documents-list">
                    <div class="spinner"></div>
                </div>
            </div>
        </div>
    `;
    
    // Attach handlers
    document.getElementById('upload-form').addEventListener('submit', handleDocumentUpload);
    document.getElementById('document-file').addEventListener('change', handleFileSelect);
    
    // Load documents
    await loadDocuments();
}

// Handle file select
function handleFileSelect(e) {
    const file = e.target.files[0];
    const label = document.querySelector('.file-upload-text');
    
    if (file) {
        label.textContent = file.name;
    } else {
        label.textContent = 'Choose PDF or Image';
    }
}

// Handle document upload
async function handleDocumentUpload(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('document-file');
    const file = fileInput.files[0];
    const errorDiv = document.getElementById('upload-error');
    const progressDiv = document.getElementById('upload-progress');
    const uploadBtn = document.getElementById('upload-btn');
    
    if (!file) {
        errorDiv.textContent = 'Please select a file';
        errorDiv.classList.remove('hidden');
        return;
    }
    
    // Hide error, show progress
    errorDiv.classList.add('hidden');
    progressDiv.classList.remove('hidden');
    uploadBtn.disabled = true;
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        
        // Upload file
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/documents/upload', {
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
        
        const result = await response.json();
        
        // Reset form
        fileInput.value = '';
        document.querySelector('.file-upload-text').textContent = 'Choose PDF or Image';
        progressDiv.classList.add('hidden');
        uploadBtn.disabled = false;
        
        // Show success message
        showNotification('Document uploaded successfully! Processing...', 'success');
        
        // Reload documents list
        await loadDocuments();
        
    } catch (error) {
        errorDiv.textContent = error.message || 'Upload failed. Please try again.';
        errorDiv.classList.remove('hidden');
        progressDiv.classList.add('hidden');
        uploadBtn.disabled = false;
    }
}

// Load documents list
async function loadDocuments() {
    const listDiv = document.getElementById('documents-list');
    
    try {
        const documents = await apiCall('/documents/');
        
        if (documents.length === 0) {
            listDiv.innerHTML = '<p class="empty-state">No documents yet. Upload your first document above!</p>';
            return;
        }
        
        listDiv.innerHTML = documents.map(doc => `
            <div class="document-card" data-doc-id="${doc.id}">
                <div class="document-header">
                    <h3 class="document-title">${doc.original_filename}</h3>
                    <span class="document-status status-${doc.status}">${doc.status}</span>
                </div>
                <div class="document-meta">
                    <span>${formatFileSize(doc.file_size)}</span>
                    <span>${doc.page_count ? `${doc.page_count} pages` : ''}</span>
                    <span>${new Date(doc.created_at).toLocaleDateString()}</span>
                </div>
                ${doc.status === 'completed' ? `
                    <button class="btn btn-secondary btn-sm" onclick="showDocumentQA('${doc.id}', '${doc.original_filename}')">
                        Ask Questions
                    </button>
                ` : doc.status === 'failed' ? `
                    <p class="error-message">${doc.error_message || 'Processing failed'}</p>
                ` : `
                    <p class="processing-message">Processing... Check back in a moment</p>
                `}
            </div>
        `).join('');
        
    } catch (error) {
        listDiv.innerHTML = `<p class="error-message">Error loading documents: ${error.message}</p>`;
    }
}

// Show document Q&A interface
async function showDocumentQA(documentId, filename) {
    const documentsPage = document.getElementById('documents-page');
    
    documentsPage.innerHTML = `
        <div class="qa-container">
            <div class="qa-header">
                <button class="btn btn-link" onclick="showDocumentsPage()">← Back to Documents</button>
                <h2>${filename}</h2>
            </div>
            
            <div class="qa-chat">
                <div id="qa-history" class="qa-history">
                    <div class="spinner"></div>
                </div>
            </div>
            
            <div class="export-buttons">
                <button class="btn btn-secondary btn-sm" onclick="exportToPDF('${documentId}')">
                    Export to PDF
                </button>
                <button class="btn btn-secondary btn-sm" onclick="exportToWord('${documentId}')">
                    Export to Word
                </button>
                <button class="btn btn-secondary btn-sm" onclick="emailExport('${documentId}')">
                    Email Report
                </button>
            </div>
            
            <form id="qa-form" class="qa-form">
                <input 
                    type="text" 
                    id="qa-question" 
                    class="form-control" 
                    placeholder="Ask a question about this document..."
                    required
                />
                <button type="submit" class="btn btn-primary">Ask</button>
            </form>
        </div>
    `;
    
    // Load history
    await loadQAHistory(documentId);
    
    // Attach handler
    document.getElementById('qa-form').addEventListener('submit', (e) => handleQASubmit(e, documentId));
}

// Load Q&A history
async function loadQAHistory(documentId) {
    const historyDiv = document.getElementById('qa-history');
    
    try {
        const history = await apiCall(`/documents/${documentId}/history`);
        
        if (history.length === 0) {
            historyDiv.innerHTML = '<p class="empty-state">No questions yet. Ask your first question below!</p>';
            return;
        }
        
        historyDiv.innerHTML = history.reverse().map(item => `
            <div class="qa-item">
                <div class="qa-question">
                    <strong>Q:</strong> ${item.question}
                </div>
                <div class="qa-answer">
                    <strong>A:</strong> ${item.answer}
                </div>
                <div class="qa-timestamp">${new Date(item.created_at).toLocaleString()}</div>
            </div>
        `).join('');
        
        // Scroll to bottom
        historyDiv.scrollTop = historyDiv.scrollHeight;
        
    } catch (error) {
        historyDiv.innerHTML = `<p class="error-message">Error loading history: ${error.message}</p>`;
    }
}

// Handle Q&A submit
async function handleQASubmit(e, documentId) {
    e.preventDefault();
    
    const questionInput = document.getElementById('qa-question');
    const question = questionInput.value.trim();
    const historyDiv = document.getElementById('qa-history');
    
    if (!question) return;
    
    // Add question to UI immediately
    const qaItem = document.createElement('div');
    qaItem.className = 'qa-item';
    qaItem.innerHTML = `
        <div class="qa-question">
            <strong>Q:</strong> ${question}
        </div>
        <div class="qa-answer">
            <strong>A:</strong> <span class="spinner-small"></span> Thinking...
        </div>
    `;
    historyDiv.appendChild(qaItem);
    historyDiv.scrollTop = historyDiv.scrollHeight;
    
    // Clear input
    questionInput.value = '';
    questionInput.disabled = true;
    
    try {
        // Send question
        const response = await apiCall(`/documents/${documentId}/query`, {
            method: 'POST',
            body: JSON.stringify({ question })
        });
        
        // Update answer
        qaItem.innerHTML = `
            <div class="qa-question">
                <strong>Q:</strong> ${question}
            </div>
            <div class="qa-answer">
                <strong>A:</strong> ${response.answer}
            </div>
            <div class="qa-timestamp">${new Date().toLocaleString()}</div>
        `;
        
        historyDiv.scrollTop = historyDiv.scrollHeight;
        
    } catch (error) {
        qaItem.innerHTML = `
            <div class="qa-question">
                <strong>Q:</strong> ${question}
            </div>
            <div class="qa-answer error-message">
                Error: ${error.message}
            </div>
        `;
    } finally {
        questionInput.disabled = false;
        questionInput.focus();
    }
}

// Utility: Format file size
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Utility: Show notification
function showNotification(message, type = 'info') {
    // Simple alert for now (can be enhanced with toast notifications)
    alert(message);
}

// Export to PDF
async function exportToPDF(documentId) {
    try {
        showNotification('Generating PDF...', 'info');
        
        const response = await apiCall('/exports/pdf', {
            method: 'POST',
            body: JSON.stringify({ document_id: documentId, format: 'pdf' })
        });
        
        // Download the file with authentication
        await downloadFile(response.download_url, `document_analysis_${documentId}.pdf`);
        showNotification('PDF generated successfully!', 'success');
        
    } catch (error) {
        alert(`Error generating PDF: ${error.message}`);
    }
}

// Export to Word
async function exportToWord(documentId) {
    try {
        showNotification('Generating Word document...', 'info');
        
        const response = await apiCall('/exports/docx', {
            method: 'POST',
            body: JSON.stringify({ document_id: documentId, format: 'docx' })
        });
        
        // Download the file with authentication
        await downloadFile(response.download_url, `document_analysis_${documentId}.docx`);
        showNotification('Word document generated successfully!', 'success');
        
    } catch (error) {
        alert(`Error generating Word document: ${error.message}`);
    }
}

// Helper function to download files with authentication
async function downloadFile(url, filename) {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    if (!response.ok) {
        throw new Error('Download failed');
    }
    
    // Create blob from response
    const blob = await response.blob();
    
    // Create temporary download link
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = filename || 'download';
    document.body.appendChild(a);
    a.click();
    
    // Cleanup
    window.URL.revokeObjectURL(downloadUrl);
    document.body.removeChild(a);
}

// Email export
async function emailExport(documentId) {
    const email = prompt('Enter recipient email address:');
    
    if (!email) return;
    
    const format = confirm('Send as PDF? (Cancel for Word)') ? 'pdf' : 'docx';
    
    try {
        showNotification('Sending email...', 'info');
        
        await apiCall('/exports/email', {
            method: 'POST',
            body: JSON.stringify({
                document_id: documentId,
                recipient_email: email,
                format: format
            })
        });
        
        showNotification(`Email will be sent to ${email}`, 'success');
        
    } catch (error) {
        alert(`Error sending email: ${error.message}`);
    }
}

// Export functions
window.showDocumentsPage = showDocumentsPage;
window.showDocumentQA = showDocumentQA;
window.exportToPDF = exportToPDF;
window.exportToWord = exportToWord;
window.emailExport = emailExport;

