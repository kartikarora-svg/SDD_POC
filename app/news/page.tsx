'use client';

import { useState, useEffect } from 'react';
import { apiCall, formatNewsDate, truncateText } from '@/lib/api';

interface NewsArticle {
  id: string;
  title: string;
  url: string;
  source: string;
  description: string | null;
  ai_summary: string | null;
  summary_generated: boolean;
  published_at: string | null;
  scraped_at: string;
}

export default function NewsPage() {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [sources, setSources] = useState<string[]>([]);
  const [selectedSource, setSelectedSource] = useState('');
  const [loading, setLoading] = useState(true);
  const [scraping, setScraping] = useState(false);
  const [summarizing, setSummarizing] = useState<string | null>(null);

  useEffect(() => {
    loadSources();
    loadNews();
  }, []);

  const loadSources = async () => {
    try {
      const response = await apiCall('/news/sources');
      setSources(response.sources);
    } catch (err) {
      console.error('Error loading sources:', err);
    }
  };

  const loadNews = async (source?: string) => {
    setLoading(true);
    try {
      const url = source ? `/news/?source=${source}` : '/news/';
      const data = await apiCall(url);
      setArticles(data);
    } catch (err: any) {
      console.error('Error loading news:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSourceFilter = (source: string) => {
    setSelectedSource(source);
    loadNews(source || undefined);
  };

  const scrapeNews = async () => {
    setScraping(true);
    try {
      await apiCall('/news/scrape', { method: 'POST' });
      
      // Wait 5 seconds then reload
      setTimeout(async () => {
        await loadNews(selectedSource || undefined);
        setScraping(false);
      }, 5000);
    } catch (err: any) {
      alert(`Error: ${err.message}`);
      setScraping(false);
    }
  };

  const summarizeArticle = async (articleId: string) => {
    setSummarizing(articleId);
    try {
      const response = await apiCall(`/news/${articleId}/summarize`, {
        method: 'POST'
      });

      // Update article with summary
      setArticles(prev => prev.map(article =>
        article.id === articleId
          ? { ...article, ai_summary: response.summary, summary_generated: true }
          : article
      ));
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setSummarizing(null);
    }
  };

  return (
    <div className="news-container" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <h2>Financial News Feed</h2>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <select
            className="form-control"
            value={selectedSource}
            onChange={(e) => handleSourceFilter(e.target.value)}
            style={{ minWidth: '150px' }}
          >
            <option value="">All Sources</option>
            {sources.map(source => (
              <option key={source} value={source}>{source}</option>
            ))}
          </select>
          <button className="btn btn-secondary" onClick={() => loadNews(selectedSource || undefined)}>
            Refresh
          </button>
          <button className="btn btn-primary" onClick={scrapeNews} disabled={scraping}>
            {scraping ? 'Scraping...' : 'Fetch Latest News'}
          </button>
        </div>
      </div>

      <div className="news-list">
        {loading ? (
          <div className="spinner" />
        ) : articles.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem', backgroundColor: 'var(--bg-primary)', borderRadius: '0.5rem', boxShadow: 'var(--shadow-md)' }}>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>No news articles yet!</p>
            <p style={{ color: 'var(--text-secondary)' }}>Click &quot;Fetch Latest News&quot; to scrape news from financial sources.</p>
          </div>
        ) : (
          articles.map(article => (
            <div
              key={article.id}
              className="news-card"
              style={{
                backgroundColor: 'var(--bg-primary)',
                padding: '1.5rem',
                borderRadius: '0.5rem',
                boxShadow: 'var(--shadow-md)',
                borderLeft: '4px solid var(--primary-color)',
                marginBottom: '1.5rem',
                transition: 'all 0.3s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.boxShadow = 'var(--shadow-lg)';
                e.currentTarget.style.transform = 'translateY(-2px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                e.currentTarget.style.transform = 'translateY(0)';
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <span style={{
                  display: 'inline-block',
                  padding: '0.25rem 0.75rem',
                  backgroundColor: 'var(--primary-color)',
                  color: 'white',
                  borderRadius: '1rem',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  textTransform: 'uppercase'
                }}>
                  {article.source}
                </span>
                <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                  {formatNewsDate(article.published_at)}
                </span>
              </div>

              <h3 style={{ margin: '0 0 1rem 0', fontSize: '1.25rem', lineHeight: '1.4' }}>
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    color: 'var(--text-primary)',
                    textDecoration: 'none',
                    transition: 'color 0.3s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.color = 'var(--primary-color)'}
                  onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-primary)'}
                >
                  {article.title}
                </a>
              </h3>

              {article.description && (
                <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '1rem' }}>
                  {truncateText(article.description, 200)}
                </p>
              )}

              {article.ai_summary ? (
                <div style={{
                  marginTop: '1rem',
                  padding: '1rem',
                  backgroundColor: 'var(--bg-secondary)',
                  borderRadius: '0.375rem',
                  borderLeft: '3px solid var(--success-color)'
                }}>
                  <h4 style={{
                    margin: '0 0 0.5rem 0',
                    fontSize: '0.875rem',
                    color: 'var(--success-color)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.5px'
                  }}>
                    AI Summary
                  </h4>
                  <p style={{ margin: 0, color: 'var(--text-primary)', lineHeight: '1.6' }}>
                    {article.ai_summary}
                  </p>
                </div>
              ) : (
                <button
                  className="btn btn-secondary"
                  style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                  onClick={() => summarizeArticle(article.id)}
                  disabled={summarizing === article.id}
                >
                  {summarizing === article.id ? 'Generating...' : 'Generate AI Summary'}
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

