/**
 * News Feed Module
 * Handles news display and AI summarization
 */

let currentArticles = [];

// Show news page
async function showNewsPage() {
    const newsPage = document.getElementById('news-page');
    
    newsPage.innerHTML = `
        <div class="news-container">
            <div class="news-header">
                <h2>Financial News Feed</h2>
                <div class="news-controls">
                    <select id="source-filter" class="form-control">
                        <option value="">All Sources</option>
                    </select>
                    <button class="btn btn-secondary" onclick="refreshNews()">
                        Refresh
                    </button>
                    <button class="btn btn-primary" onclick="scrapeNews()">
                        Fetch Latest News
                    </button>
                </div>
            </div>
            
            <div id="news-list" class="news-list">
                <div class="spinner"></div>
            </div>
        </div>
    `;
    
    // Load sources
    await loadNewsSources();
    
    // Load news
    await loadNews();
    
    // Attach filter handler
    document.getElementById('source-filter').addEventListener('change', handleSourceFilter);
}

// Load news sources
async function loadNewsSources() {
    try {
        const response = await apiCall('/news/sources');
        const sourceFilter = document.getElementById('source-filter');
        
        response.sources.forEach(source => {
            const option = document.createElement('option');
            option.value = source;
            option.textContent = source;
            sourceFilter.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading sources:', error);
    }
}

// Load news articles
async function loadNews(source = null) {
    const listDiv = document.getElementById('news-list');
    listDiv.innerHTML = '<div class="spinner"></div>';
    
    try {
        const url = source ? `/news/?source=${source}` : '/news/';
        const articles = await apiCall(url);
        currentArticles = articles;
        
        if (articles.length === 0) {
            listDiv.innerHTML = `
                <div class="empty-state">
                    <p>No news articles yet!</p>
                    <p>Click "Fetch Latest News" to scrape news from financial sources.</p>
                </div>
            `;
            return;
        }
        
        renderNewsArticles(articles);
        
    } catch (error) {
        listDiv.innerHTML = `<p class="error-message">Error loading news: ${error.message}</p>`;
    }
}

// Render news articles
function renderNewsArticles(articles) {
    const listDiv = document.getElementById('news-list');
    
    listDiv.innerHTML = articles.map(article => `
        <div class="news-card" data-article-id="${article.id}">
            <div class="news-card-header">
                <span class="news-source-badge">${article.source}</span>
                <span class="news-date">${formatNewsDate(article.published_at)}</span>
            </div>
            
            <h3 class="news-title">
                <a href="${article.url}" target="_blank" rel="noopener noreferrer">
                    ${article.title}
                </a>
            </h3>
            
            ${article.description ? `
                <p class="news-description">${truncateText(article.description, 200)}</p>
            ` : ''}
            
            ${article.ai_summary ? `
                <div class="news-summary">
                    <h4>AI Summary</h4>
                    <p>${article.ai_summary}</p>
                </div>
            ` : `
                <button 
                    class="btn btn-secondary btn-sm" 
                    onclick="summarizeArticle('${article.id}')"
                    id="summarize-btn-${article.id}"
                >
                    Generate AI Summary
                </button>
            `}
        </div>
    `).join('');
}

// Summarize article
async function summarizeArticle(articleId) {
    const btn = document.getElementById(`summarize-btn-${articleId}`);
    const originalText = btn.textContent;
    
    btn.textContent = 'Generating...';
    btn.disabled = true;
    
    try {
        const response = await apiCall(`/news/${articleId}/summarize`, {
            method: 'POST'
        });
        
        // Update the article card with summary
        const card = document.querySelector(`[data-article-id="${articleId}"]`);
        const summaryHtml = `
            <div class="news-summary">
                <h4>AI Summary</h4>
                <p>${response.summary}</p>
            </div>
        `;
        
        // Replace button with summary
        btn.parentElement.innerHTML = summaryHtml;
        
        // Update current articles array
        const article = currentArticles.find(a => a.id === articleId);
        if (article) {
            article.ai_summary = response.summary;
            article.summary_generated = true;
        }
        
    } catch (error) {
        btn.textContent = originalText;
        btn.disabled = false;
        alert(`Error generating summary: ${error.message}`);
    }
}

// Scrape news
async function scrapeNews() {
    const btn = event.target;
    const originalText = btn.textContent;
    
    btn.textContent = 'Scraping...';
    btn.disabled = true;
    
    try {
        await apiCall('/news/scrape', { method: 'POST' });
        
        showNotification('News scraping started! Refreshing in 5 seconds...', 'success');
        
        // Wait and reload
        setTimeout(async () => {
            await loadNews();
            btn.textContent = originalText;
            btn.disabled = false;
        }, 5000);
        
    } catch (error) {
        btn.textContent = originalText;
        btn.disabled = false;
        alert(`Error scraping news: ${error.message}`);
    }
}

// Refresh news
async function refreshNews() {
    const sourceFilter = document.getElementById('source-filter');
    const source = sourceFilter.value || null;
    await loadNews(source);
}

// Handle source filter
async function handleSourceFilter(e) {
    const source = e.target.value || null;
    await loadNews(source);
}

// Format news date
function formatNewsDate(dateStr) {
    if (!dateStr) return 'Recently';
    
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 60) {
        return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    } else if (diffDays < 7) {
        return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
    } else {
        return date.toLocaleDateString();
    }
}

// Truncate text
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Export functions
window.showNewsPage = showNewsPage;
window.summarizeArticle = summarizeArticle;
window.scrapeNews = scrapeNews;
window.refreshNews = refreshNews;

