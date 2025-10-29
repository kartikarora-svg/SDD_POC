'use client';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <p>&copy; 2025 Finalytics. All rights reserved.</p>
      </div>
      <style jsx>{`
        .footer {
          background-color: var(--bg-primary);
          padding: 2rem 0;
          text-align: center;
          border-top: 1px solid var(--border-color);
          margin-top: auto;
        }
        
        .footer p {
          color: var(--text-secondary);
          margin: 0;
        }
      `}</style>
    </footer>
  );
}

