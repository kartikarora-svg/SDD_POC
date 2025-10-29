'use client';

import { useState, useEffect, FormEvent } from 'react';
import { apiCall, truncateText } from '@/lib/api';

interface StockData {
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
}

interface StockQueryResponse {
  ticker: string;
  question: string;
  answer: string;
  stock_data: StockData;
  queried_at: string;
}

interface HistoryItem {
  ticker: string;
  question: string;
  answer: string;
  current_price: number | null;
  created_at: string;
}

export default function StocksPage() {
  const [ticker, setTicker] = useState('');
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<StockQueryResponse | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await apiCall('/stocks/history/queries?limit=10');
      setHistory(data);
    } catch (err) {
      console.error('Error loading history:', err);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!ticker.trim() || !question.trim()) return;

    setLoading(true);
    setError('');

    try {
      const response = await apiCall('/stocks/query', {
        method: 'POST',
        body: JSON.stringify({
          ticker: ticker.toUpperCase(),
          question: question
        })
      });

      setResult(response);
      setQuestion('');
      await loadHistory();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="stocks-container" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <h2>Stock Intelligence</h2>
      <p className="subtitle" style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Ask questions about any stock using natural language
      </p>

      <div style={{ backgroundColor: 'var(--bg-primary)', padding: '2rem', borderRadius: '0.5rem', boxShadow: 'var(--shadow-md)', marginBottom: '2rem' }}>
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
            <div className="form-group" style={{ flex: '1', minWidth: '200px' }}>
              <label htmlFor="stock-ticker">Stock Ticker</label>
              <input
                type="text"
                id="stock-ticker"
                className="form-control"
                placeholder="e.g., AAPL, MSFT, GOOGL"
                value={ticker}
                onChange={(e) => setTicker(e.target.value)}
                required
              />
            </div>
            <div className="form-group" style={{ flex: '2', minWidth: '300px' }}>
              <label htmlFor="stock-question">Your Question</label>
              <input
                type="text"
                id="stock-question"
                className="form-control"
                placeholder="What's the current price? How's the company performing?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                required
              />
            </div>
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Analyzing...' : 'Ask'}
          </button>
        </form>
      </div>

      {result && (
        <div style={{ backgroundColor: 'var(--bg-primary)', padding: '2rem', borderRadius: '0.5rem', boxShadow: 'var(--shadow-md)', marginBottom: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', paddingBottom: '1rem', borderBottom: '2px solid var(--border-color)' }}>
            <h3>{result.stock_data.name} ({result.stock_data.ticker})</h3>
            {result.stock_data.current_price && (
              <span style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--success-color)' }}>
                ${result.stock_data.current_price.toFixed(2)}
              </span>
            )}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
            {result.stock_data.market_cap_formatted && (
              <div style={{ padding: '0.75rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '0.375rem' }}>
                <strong>Market Cap:</strong> {result.stock_data.market_cap_formatted}
              </div>
            )}
            {result.stock_data.pe_ratio && (
              <div style={{ padding: '0.75rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '0.375rem' }}>
                <strong>P/E Ratio:</strong> {result.stock_data.pe_ratio.toFixed(2)}
              </div>
            )}
            {result.stock_data.dividend_yield && (
              <div style={{ padding: '0.75rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '0.375rem' }}>
                <strong>Dividend:</strong> {(result.stock_data.dividend_yield * 100).toFixed(2)}%
              </div>
            )}
            {result.stock_data.week_52_high && result.stock_data.week_52_low && (
              <div style={{ padding: '0.75rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '0.375rem' }}>
                <strong>52-Week Range:</strong> ${result.stock_data.week_52_low.toFixed(2)} - ${result.stock_data.week_52_high.toFixed(2)}
              </div>
            )}
            {result.stock_data.sector && (
              <div style={{ padding: '0.75rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '0.375rem' }}>
                <strong>Sector:</strong> {result.stock_data.sector}
              </div>
            )}
            {result.stock_data.industry && (
              <div style={{ padding: '0.75rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '0.375rem' }}>
                <strong>Industry:</strong> {result.stock_data.industry}
              </div>
            )}
          </div>

          <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border-color)' }}>
            <div style={{ marginBottom: '1rem', lineHeight: '1.6', color: 'var(--text-primary)' }}>
              <strong>Q:</strong> {result.question}
            </div>
            <div style={{ padding: '1rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '0.375rem', borderLeft: '3px solid var(--primary-color)', lineHeight: '1.6' }}>
              <strong>A:</strong> {result.answer}
            </div>
          </div>
        </div>
      )}

      <div style={{ marginTop: '3rem' }}>
        <h3>Recent Queries</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
          {history.length === 0 ? (
            <p style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
              No queries yet. Ask your first question above!
            </p>
          ) : (
            history.map((item, index) => (
              <div
                key={index}
                style={{
                  padding: '1.5rem',
                  backgroundColor: 'var(--bg-primary)',
                  borderRadius: '0.5rem',
                  boxShadow: 'var(--shadow-md)',
                  borderLeft: '4px solid var(--success-color)'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <span style={{
                    padding: '0.25rem 0.75rem',
                    backgroundColor: 'var(--success-color)',
                    color: 'white',
                    borderRadius: '1rem',
                    fontSize: '0.75rem',
                    fontWeight: 600
                  }}>
                    {item.ticker}
                  </span>
                  <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    {new Date(item.created_at).toLocaleDateString()}
                  </span>
                </div>
                <div style={{ fontWeight: 600, marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
                  {item.question}
                </div>
                <div style={{ color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                  {truncateText(item.answer, 150)}
                </div>
                {item.current_price && (
                  <div style={{ fontSize: '0.875rem', color: 'var(--success-color)', fontWeight: 600 }}>
                    Price: ${item.current_price.toFixed(2)}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

