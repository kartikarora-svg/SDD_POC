/**
 * Stocks Module
 * Handles stock queries using Yahoo Finance RAG agent
 */

let currentStockData = null;

// Show stocks page
async function showStocksPage() {
    const stocksPage = document.getElementById('stocks-page');
    
    stocksPage.innerHTML = `
        <div class="stocks-container">
            <h2>Stock Intelligence</h2>
            <p class="subtitle">Ask questions about any stock using natural language</p>
            
            <div class="stock-query-card">
                <form id="stock-query-form" class="stock-query-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="stock-ticker">Stock Ticker</label>
                            <input 
                                type="text" 
                                id="stock-ticker" 
                                class="form-control" 
                                placeholder="e.g., AAPL, MSFT, GOOGL"
                                required
                            />
                        </div>
                        <div class="form-group" style="flex: 2;">
                            <label for="stock-question">Your Question</label>
                            <input 
                                type="text" 
                                id="stock-question" 
                                class="form-control" 
                                placeholder="What's the current price? How's the company performing?"
                                required
                            />
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">Ask</button>
                </form>
            </div>
            
            <div id="stock-result" class="stock-result hidden"></div>
            
            <div class="stock-history-section">
                <h3>Recent Queries</h3>
                <div id="stock-history" class="stock-history">
                    <div class="spinner"></div>
                </div>
            </div>
        </div>
    `;
    
    // Attach form handler
    document.getElementById('stock-query-form').addEventListener('submit', handleStockQuery);
    
    // Load history
    await loadStockHistory();
}

// Handle stock query
async function handleStockQuery(e) {
    e.preventDefault();
    
    const tickerInput = document.getElementById('stock-ticker');
    const questionInput = document.getElementById('stock-question');
    const ticker = tickerInput.value.trim().toUpperCase();
    const question = questionInput.value.trim();
    const resultDiv = document.getElementById('stock-result');
    
    if (!ticker || !question) return;
    
    // Show loading
    resultDiv.classList.remove('hidden');
    resultDiv.innerHTML = '<div class="spinner"></div><p>Analyzing stock data...</p>';
    
    try {
        // Query stock
        const response = await apiCall('/stocks/query', {
            method: 'POST',
            body: JSON.stringify({ ticker, question })
        });
        
        currentStockData = response.stock_data;
        
        // Display result
        renderStockResult(response);
        
        // Clear inputs
        questionInput.value = '';
        
        // Reload history
        await loadStockHistory();
        
    } catch (error) {
        resultDiv.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    }
}

// Render stock result
function renderStockResult(response) {
    const resultDiv = document.getElementById('stock-result');
    const stockData = response.stock_data;
    
    resultDiv.innerHTML = `
        <div class="stock-result-content">
            <div class="stock-header">
                <h3>${stockData.name} (${stockData.ticker})</h3>
                ${stockData.current_price ? `<span class="stock-price">$${stockData.current_price.toFixed(2)}</span>` : ''}
            </div>
            
            <div class="stock-metrics">
                ${stockData.market_cap_formatted ? `<div class="metric"><strong>Market Cap:</strong> ${stockData.market_cap_formatted}</div>` : ''}
                ${stockData.pe_ratio ? `<div class="metric"><strong>P/E Ratio:</strong> ${stockData.pe_ratio.toFixed(2)}</div>` : ''}
                ${stockData.dividend_yield ? `<div class="metric"><strong>Dividend:</strong> ${(stockData.dividend_yield * 100).toFixed(2)}%</div>` : ''}
                ${stockData.week_52_high && stockData.week_52_low ? `<div class="metric"><strong>52-Week Range:</strong> $${stockData.week_52_low.toFixed(2)} - $${stockData.week_52_high.toFixed(2)}</div>` : ''}
                ${stockData.sector ? `<div class="metric"><strong>Sector:</strong> ${stockData.sector}</div>` : ''}
                ${stockData.industry ? `<div class="metric"><strong>Industry:</strong> ${stockData.industry}</div>` : ''}
            </div>
            
            <div class="stock-qa">
                <div class="stock-question">
                    <strong>Q:</strong> ${response.question}
                </div>
                <div class="stock-answer">
                    <strong>A:</strong> ${response.answer}
                </div>
            </div>
        </div>
    `;
}

// Load stock history
async function loadStockHistory() {
    const historyDiv = document.getElementById('stock-history');
    
    try {
        const history = await apiCall('/stocks/history/queries?limit=10');
        
        if (history.length === 0) {
            historyDiv.innerHTML = '<p class="empty-state">No queries yet. Ask your first question above!</p>';
            return;
        }
        
        historyDiv.innerHTML = history.map(item => `
            <div class="stock-history-item">
                <div class="stock-history-header">
                    <span class="stock-ticker-badge">${item.ticker}</span>
                    <span class="stock-history-date">${new Date(item.created_at).toLocaleDateString()}</span>
                </div>
                <div class="stock-history-question">${item.question}</div>
                <div class="stock-history-answer">${truncateText(item.answer, 150)}</div>
                ${item.current_price ? `<div class="stock-history-price">Price: $${item.current_price.toFixed(2)}</div>` : ''}
            </div>
        `).join('');
        
    } catch (error) {
        historyDiv.innerHTML = `<p class="error-message">Error loading history: ${error.message}</p>`;
    }
}

// Truncate text
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Export functions
window.showStocksPage = showStocksPage;

