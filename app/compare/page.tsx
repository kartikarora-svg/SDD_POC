'use client';

import { useState, useEffect, FormEvent } from 'react';
import { apiCall, truncateText } from '@/lib/api';

interface StockComparisonData {
  ticker: string;
  name: string;
  current_price: number | null;
  market_cap_formatted: string;
  pe_ratio: number | null;
  dividend_yield: number | null;
  week_52_high: number | null;
  week_52_low: number | null;
  sector: string | null;
  industry: string | null;
  beta: number | null;
  profit_margins: number | null;
  earnings_growth: number | null;
}

interface ComparisonResponse {
  comparison_id: string;
  stock1: StockComparisonData;
  stock2: StockComparisonData;
  ai_summary: string;
  created_at: string;
}

interface HistoryItem {
  id: string;
  ticker1: string;
  ticker2: string;
  created_at: string;
  ai_summary: string;
}

export default function ComparePage() {
  const [ticker1, setTicker1] = useState('');
  const [ticker2, setTicker2] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ComparisonResponse | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await apiCall('/comparison/history?limit=5');
      setHistory(data);
    } catch (err) {
      console.error('Error loading history:', err);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!ticker1.trim() || !ticker2.trim()) return;

    if (ticker1.toUpperCase() === ticker2.toUpperCase()) {
      setError('Please enter two different ticker symbols');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await apiCall('/comparison/', {
        method: 'POST',
        body: JSON.stringify({
          ticker1: ticker1.toUpperCase(),
          ticker2: ticker2.toUpperCase()
        })
      });

      setResult(response);
      await loadHistory();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadComparison = async (comparisonId: string) => {
    setLoading(true);
    try {
      const data = await apiCall(`/comparison/${comparisonId}`);
      setResult(data);
      
      // Scroll to result
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderStockColumn = (stock: StockComparisonData) => (
    <div style={{ padding: '1.5rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '0.5rem' }}>
      <div style={{ marginBottom: '1.5rem', paddingBottom: '1rem', borderBottom: '2px solid var(--border-color)' }}>
        <h4 style={{ margin: '0 0 0.5rem 0', color: 'var(--text-primary)' }}>{stock.name}</h4>
        <span style={{
          display: 'inline-block',
          padding: '0.25rem 0.75rem',
          backgroundColor: 'var(--primary-color)',
          color: 'white',
          borderRadius: '1rem',
          fontSize: '0.875rem',
          fontWeight: 600
        }}>
          {stock.ticker}
        </span>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {stock.current_price && (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', backgroundColor: 'var(--bg-primary)', borderRadius: '0.25rem' }}>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Price:</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>${stock.current_price.toFixed(2)}</span>
          </div>
        )}
        {stock.market_cap_formatted && (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', backgroundColor: 'var(--bg-primary)', borderRadius: '0.25rem' }}>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Market Cap:</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{stock.market_cap_formatted}</span>
          </div>
        )}
        {stock.pe_ratio && (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', backgroundColor: 'var(--bg-primary)', borderRadius: '0.25rem' }}>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>P/E Ratio:</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{stock.pe_ratio.toFixed(2)}</span>
          </div>
        )}
        {stock.dividend_yield && (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', backgroundColor: 'var(--bg-primary)', borderRadius: '0.25rem' }}>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Dividend:</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{(stock.dividend_yield * 100).toFixed(2)}%</span>
          </div>
        )}
        {stock.sector && (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', backgroundColor: 'var(--bg-primary)', borderRadius: '0.25rem' }}>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Sector:</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{stock.sector}</span>
          </div>
        )}
        {stock.industry && (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', backgroundColor: 'var(--bg-primary)', borderRadius: '0.25rem' }}>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Industry:</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{stock.industry}</span>
          </div>
        )}
        {stock.beta && (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', backgroundColor: 'var(--bg-primary)', borderRadius: '0.25rem' }}>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Beta:</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{stock.beta.toFixed(2)}</span>
          </div>
        )}
        {stock.profit_margins && (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', backgroundColor: 'var(--bg-primary)', borderRadius: '0.25rem' }}>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Profit Margin:</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{(stock.profit_margins * 100).toFixed(2)}%</span>
          </div>
        )}
        {stock.earnings_growth && (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', backgroundColor: 'var(--bg-primary)', borderRadius: '0.25rem' }}>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Earnings Growth:</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{(stock.earnings_growth * 100).toFixed(2)}%</span>
          </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="compare-container" style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <h2>Stock Comparison</h2>
      <p className="subtitle" style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Compare two stocks side-by-side with AI-powered analysis
      </p>

      <div style={{ backgroundColor: 'var(--bg-primary)', padding: '2rem', borderRadius: '0.5rem', boxShadow: 'var(--shadow-md)', marginBottom: '2rem' }}>
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', gap: '2rem', alignItems: 'flex-end', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
            <div className="form-group" style={{ flex: 1, minWidth: '200px' }}>
              <label htmlFor="ticker1">First Stock</label>
              <input
                type="text"
                id="ticker1"
                className="form-control"
                placeholder="e.g., AAPL"
                value={ticker1}
                onChange={(e) => setTicker1(e.target.value)}
                required
              />
            </div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary-color)', paddingBottom: '0.5rem' }}>
              VS
            </div>
            <div className="form-group" style={{ flex: 1, minWidth: '200px' }}>
              <label htmlFor="ticker2">Second Stock</label>
              <input
                type="text"
                id="ticker2"
                className="form-control"
                placeholder="e.g., MSFT"
                value={ticker2}
                onChange={(e) => setTicker2(e.target.value)}
                required
              />
            </div>
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="btn btn-primary" style={{ padding: '1rem 2rem', fontSize: '1.1rem' }} disabled={loading}>
            {loading ? 'Comparing...' : 'Compare Stocks'}
          </button>
        </form>
      </div>

      {result && (
        <div style={{ backgroundColor: 'var(--bg-primary)', padding: '2rem', borderRadius: '0.5rem', boxShadow: 'var(--shadow-md)', marginBottom: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', paddingBottom: '1rem', borderBottom: '2px solid var(--border-color)' }}>
            <h3>Comparison Results</h3>
            <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              {new Date(result.created_at).toLocaleDateString()}
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: '2rem', marginBottom: '2rem' }}>
            {renderStockColumn(result.stock1)}
            
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <div style={{
                width: '60px',
                height: '60px',
                borderRadius: '50%',
                backgroundColor: 'var(--primary-color)',
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.5rem',
                fontWeight: 'bold',
                boxShadow: 'var(--shadow-lg)'
              }}>
                VS
              </div>
            </div>

            {renderStockColumn(result.stock2)}
          </div>

          <div style={{
            marginTop: '2rem',
            padding: '2rem',
            backgroundColor: 'var(--bg-secondary)',
            borderRadius: '0.5rem',
            borderLeft: '4px solid var(--success-color)'
          }}>
            <h4 style={{ margin: '0 0 1rem 0', color: 'var(--success-color)' }}>AI Analysis</h4>
            <div style={{ lineHeight: '1.8', color: 'var(--text-primary)' }}>
              {result.ai_summary.split('\n\n').map((paragraph, index) => (
                <p key={index} style={{ marginBottom: '1rem' }}>{paragraph}</p>
              ))}
            </div>
          </div>
        </div>
      )}

      <div style={{ marginTop: '3rem' }}>
        <h3>Previous Comparisons</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
          {history.length === 0 ? (
            <p style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)', gridColumn: '1 / -1' }}>
              No comparisons yet. Compare your first pair of stocks above!
            </p>
          ) : (
            history.map(item => (
              <div
                key={item.id}
                onClick={() => loadComparison(item.id)}
                style={{
                  padding: '1.5rem',
                  backgroundColor: 'var(--bg-primary)',
                  borderRadius: '0.5rem',
                  boxShadow: 'var(--shadow-md)',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  borderLeft: '4px solid var(--primary-color)'
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
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{
                      padding: '0.2rem 0.5rem',
                      backgroundColor: 'var(--primary-color)',
                      color: 'white',
                      borderRadius: '0.75rem',
                      fontSize: '0.75rem',
                      fontWeight: 600
                    }}>
                      {item.ticker1}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>vs</span>
                    <span style={{
                      padding: '0.2rem 0.5rem',
                      backgroundColor: 'var(--primary-color)',
                      color: 'white',
                      borderRadius: '0.75rem',
                      fontSize: '0.75rem',
                      fontWeight: 600
                    }}>
                      {item.ticker2}
                    </span>
                  </div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    {new Date(item.created_at).toLocaleDateString()}
                  </span>
                </div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: '1.4', margin: 0 }}>
                  {truncateText(item.ai_summary, 120)}
                </p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

