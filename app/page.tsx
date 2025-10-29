'use client';

import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();

  const navigateToFeature = (featureName: string) => {
    router.push(`/${featureName}`);
  };

  return (
    <div className="hero">
      <h1>Welcome to Finalytics</h1>
      <p className="subtitle">AI-Powered Financial Analytics Platform</p>
      <div className="features">
        <div
          className="feature-card clickable"
          onClick={() => navigateToFeature('documents')}
        >
          <h3>📄 Document Intelligence</h3>
          <p>Upload financial documents and ask questions powered by AI</p>
          <span className="card-arrow">→</span>
        </div>
        <div
          className="feature-card clickable"
          onClick={() => navigateToFeature('news')}
        >
          <h3>📰 Market News</h3>
          <p>Real-time financial news with AI-generated summaries</p>
          <span className="card-arrow">→</span>
        </div>
        <div
          className="feature-card clickable"
          onClick={() => navigateToFeature('stocks')}
        >
          <h3>📈 Stock Research</h3>
          <p>Natural language queries for real-time stock data</p>
          <span className="card-arrow">→</span>
        </div>
        <div
          className="feature-card clickable"
          onClick={() => navigateToFeature('compare')}
        >
          <h3>⚖️ Stock Comparison</h3>
          <p>Side-by-side analysis of any two stocks</p>
          <span className="card-arrow">→</span>
        </div>
      </div>
    </div>
  );
}

