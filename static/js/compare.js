/**
 * Stock Comparison Module
 * Compare two stocks side-by-side with AI analysis
 */

// Show compare page
async function showComparePage() {
    const comparePage = document.getElementById('compare-page');
    
    comparePage.innerHTML = `
        <div class="compare-container">
            <h2>Stock Comparison</h2>
            <p class="subtitle">Compare two stocks side-by-side with AI-powered analysis</p>
            
            <div class="comparison-form-card">
                <form id="comparison-form" class="comparison-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="ticker1">First Stock</label>
                            <input 
                                type="text" 
                                id="ticker1" 
                                class="form-control" 
                                placeholder="e.g., AAPL"
                                required
                            />
                        </div>
                        <div class="vs-divider">VS</div>
                        <div class="form-group">
                            <label for="ticker2">Second Stock</label>
                            <input 
                                type="text" 
                                id="ticker2" 
                                class="form-control" 
                                placeholder="e.g., MSFT"
                                required
                            />
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary btn-lg">Compare Stocks</button>
                </form>
            </div>
            
            <div id="comparison-result" class="comparison-result hidden"></div>
            
            <div class="comparison-history-section">
                <h3>Previous Comparisons</h3>
                <div id="comparison-history" class="comparison-history">
                    <div class="spinner"></div>
                </div>
            </div>
        </div>
    `;
    
    // Attach form handler
    document.getElementById('comparison-form').addEventListener('submit', handleComparison);
    
    // Load history
    await loadComparisonHistory();
}

// Handle comparison
async function handleComparison(e) {
    e.preventDefault();
    
    const ticker1Input = document.getElementById('ticker1');
    const ticker2Input = document.getElementById('ticker2');
    const ticker1 = ticker1Input.value.trim().toUpperCase();
    const ticker2 = ticker2Input.value.trim().toUpperCase();
    const resultDiv = document.getElementById('comparison-result');
    
    if (!ticker1 || !ticker2) return;
    
    if (ticker1 === ticker2) {
        alert('Please enter two different ticker symbols');
        return;
    }
    
    // Show loading
    resultDiv.classList.remove('hidden');
    resultDiv.innerHTML = '<div class="spinner"></div><p>Comparing stocks and generating AI analysis...</p>';
    
    try {
        // Compare stocks
        const response = await apiCall('/comparison/', {
            method: 'POST',
            body: JSON.stringify({ ticker1, ticker2 })
        });
        
        // Display result
        renderComparison(response);
        
        // Reload history
        await loadComparisonHistory();
        
    } catch (error) {
        resultDiv.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    }
}

// Render comparison
function renderComparison(comparison) {
    const resultDiv = document.getElementById('comparison-result');
    const stock1 = comparison.stock1;
    const stock2 = comparison.stock2;
    
    resultDiv.innerHTML = `
        <div class="comparison-content">
            <div class="comparison-header">
                <h3>Comparison Results</h3>
                <span class="comparison-date">${new Date(comparison.created_at).toLocaleDateString()}</span>
            </div>
            
            <div class="comparison-grid">
                <div class="stock-column">
                    <div class="stock-column-header">
                        <h4>${stock1.name}</h4>
                        <span class="ticker-badge">${stock1.ticker}</span>
                    </div>
                    <div class="stock-metrics-list">
                        ${stock1.current_price ? `<div class="metric-item"><span class="metric-label">Price:</span> <span class="metric-value">$${stock1.current_price.toFixed(2)}</span></div>` : ''}
                        ${stock1.market_cap_formatted ? `<div class="metric-item"><span class="metric-label">Market Cap:</span> <span class="metric-value">${stock1.market_cap_formatted}</span></div>` : ''}
                        ${stock1.pe_ratio ? `<div class="metric-item"><span class="metric-label">P/E Ratio:</span> <span class="metric-value">${stock1.pe_ratio.toFixed(2)}</span></div>` : ''}
                        ${stock1.dividend_yield ? `<div class="metric-item"><span class="metric-label">Dividend:</span> <span class="metric-value">${(stock1.dividend_yield * 100).toFixed(2)}%</span></div>` : ''}
                        ${stock1.sector ? `<div class="metric-item"><span class="metric-label">Sector:</span> <span class="metric-value">${stock1.sector}</span></div>` : ''}
                        ${stock1.industry ? `<div class="metric-item"><span class="metric-label">Industry:</span> <span class="metric-value">${stock1.industry}</span></div>` : ''}
                        ${stock1.beta ? `<div class="metric-item"><span class="metric-label">Beta:</span> <span class="metric-value">${stock1.beta.toFixed(2)}</span></div>` : ''}
                        ${stock1.profit_margins ? `<div class="metric-item"><span class="metric-label">Profit Margin:</span> <span class="metric-value">${(stock1.profit_margins * 100).toFixed(2)}%</span></div>` : ''}
                        ${stock1.earnings_growth ? `<div class="metric-item"><span class="metric-label">Earnings Growth:</span> <span class="metric-value">${(stock1.earnings_growth * 100).toFixed(2)}%</span></div>` : ''}
                    </div>
                </div>
                
                <div class="vs-column">
                    <div class="vs-circle">VS</div>
                </div>
                
                <div class="stock-column">
                    <div class="stock-column-header">
                        <h4>${stock2.name}</h4>
                        <span class="ticker-badge">${stock2.ticker}</span>
                    </div>
                    <div class="stock-metrics-list">
                        ${stock2.current_price ? `<div class="metric-item"><span class="metric-label">Price:</span> <span class="metric-value">$${stock2.current_price.toFixed(2)}</span></div>` : ''}
                        ${stock2.market_cap_formatted ? `<div class="metric-item"><span class="metric-label">Market Cap:</span> <span class="metric-value">${stock2.market_cap_formatted}</span></div>` : ''}
                        ${stock2.pe_ratio ? `<div class="metric-item"><span class="metric-label">P/E Ratio:</span> <span class="metric-value">${stock2.pe_ratio.toFixed(2)}</span></div>` : ''}
                        ${stock2.dividend_yield ? `<div class="metric-item"><span class="metric-label">Dividend:</span> <span class="metric-value">${(stock2.dividend_yield * 100).toFixed(2)}%</span></div>` : ''}
                        ${stock2.sector ? `<div class="metric-item"><span class="metric-label">Sector:</span> <span class="metric-value">${stock2.sector}</span></div>` : ''}
                        ${stock2.industry ? `<div class="metric-item"><span class="metric-label">Industry:</span> <span class="metric-value">${stock2.industry}</span></div>` : ''}
                        ${stock2.beta ? `<div class="metric-item"><span class="metric-label">Beta:</span> <span class="metric-value">${stock2.beta.toFixed(2)}</span></div>` : ''}
                        ${stock2.profit_margins ? `<div class="metric-item"><span class="metric-label">Profit Margin:</span> <span class="metric-value">${(stock2.profit_margins * 100).toFixed(2)}%</span></div>` : ''}
                        ${stock2.earnings_growth ? `<div class="metric-item"><span class="metric-label">Earnings Growth:</span> <span class="metric-value">${(stock2.earnings_growth * 100).toFixed(2)}%</span></div>` : ''}
                    </div>
                </div>
            </div>
            
            <div class="ai-analysis">
                <h4>AI Analysis</h4>
                <div class="analysis-content">
                    ${formatAnalysisText(comparison.ai_summary)}
                </div>
            </div>
        </div>
    `;
}

// Format analysis text into paragraphs
function formatAnalysisText(text) {
    return text.split('\n\n').map(para => `<p>${para}</p>`).join('');
}

// Load comparison history
async function loadComparisonHistory() {
    const historyDiv = document.getElementById('comparison-history');
    
    try {
        const history = await apiCall('/comparison/history?limit=5');
        
        if (history.length === 0) {
            historyDiv.innerHTML = '<p class="empty-state">No comparisons yet. Compare your first pair of stocks above!</p>';
            return;
        }
        
        historyDiv.innerHTML = history.map(item => `
            <div class="history-card" onclick="loadComparison('${item.id}')">
                <div class="history-header">
                    <div class="ticker-pair">
                        <span class="ticker-badge-small">${item.ticker1}</span>
                        <span class="vs-small">vs</span>
                        <span class="ticker-badge-small">${item.ticker2}</span>
                    </div>
                    <span class="history-date">${new Date(item.created_at).toLocaleDateString()}</span>
                </div>
                <p class="history-summary">${truncateText(item.ai_summary, 120)}</p>
            </div>
        `).join('');
        
    } catch (error) {
        historyDiv.innerHTML = `<p class="error-message">Error loading history: ${error.message}</p>`;
    }
}

// Load specific comparison
async function loadComparison(comparisonId) {
    const resultDiv = document.getElementById('comparison-result');
    
    resultDiv.classList.remove('hidden');
    resultDiv.innerHTML = '<div class="spinner"></div><p>Loading comparison...</p>';
    
    try {
        const comparison = await apiCall(`/comparison/${comparisonId}`);
        renderComparison(comparison);
        
        // Scroll to result
        resultDiv.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        resultDiv.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    }
}

// Truncate text
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Export functions
window.showComparePage = showComparePage;
window.loadComparison = loadComparison;

