'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/hooks/useAuth';

export default function Navigation() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const isActive = (path: string) => pathname === path || pathname?.startsWith(path + '/');

  return (
    <nav className="navbar">
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem' }}>
        <div className="nav-brand">
          <h1 style={{ color: 'var(--primary-color)', fontSize: '1.5rem', fontWeight: '700' }}>
            <Link href="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              Finalytics
            </Link>
          </h1>
        </div>
        <ul style={{ display: 'flex', listStyle: 'none', gap: '2rem', margin: 0, padding: 0 }}>
          <li>
            <Link
              href="/"
              className={`nav-link ${isActive('/') && pathname === '/' ? 'active' : ''}`}
              style={{
                textDecoration: 'none',
                color: isActive('/') && pathname === '/' ? 'var(--primary-color)' : 'var(--text-secondary)',
                fontWeight: '500',
                transition: 'color 0.2s'
              }}
            >
              Home
            </Link>
          </li>
          <li>
            <Link
              href="/documents"
              className={`nav-link ${isActive('/documents') ? 'active' : ''}`}
              style={{
                textDecoration: 'none',
                color: isActive('/documents') ? 'var(--primary-color)' : 'var(--text-secondary)',
                fontWeight: '500',
                transition: 'color 0.2s'
              }}
            >
              Documents
            </Link>
          </li>
          <li>
            <Link
              href="/news"
              className={`nav-link ${isActive('/news') ? 'active' : ''}`}
              style={{
                textDecoration: 'none',
                color: isActive('/news') ? 'var(--primary-color)' : 'var(--text-secondary)',
                fontWeight: '500',
                transition: 'color 0.2s'
              }}
            >
              News
            </Link>
          </li>
          <li>
            <Link
              href="/stocks"
              className={`nav-link ${isActive('/stocks') ? 'active' : ''}`}
              style={{
                textDecoration: 'none',
                color: isActive('/stocks') ? 'var(--primary-color)' : 'var(--text-secondary)',
                fontWeight: '500',
                transition: 'color 0.2s'
              }}
            >
              Stocks
            </Link>
          </li>
          <li>
            <Link
              href="/compare"
              className={`nav-link ${isActive('/compare') ? 'active' : ''}`}
              style={{
                textDecoration: 'none',
                color: isActive('/compare') ? 'var(--primary-color)' : 'var(--text-secondary)',
                fontWeight: '500',
                transition: 'color 0.2s'
              }}
            >
              Compare
            </Link>
          </li>
          {user ? (
            <>
              <li style={{ color: 'var(--text-secondary)' }}>
                Welcome, {user.email}
              </li>
              <li>
                <button
                  onClick={logout}
                  style={{
                    textDecoration: 'none',
                    color: 'var(--text-secondary)',
                    fontWeight: '500',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    font: 'inherit'
                  }}
                >
                  Logout
                </button>
              </li>
            </>
          ) : (
            <li>
              <Link
                href="/login"
                className={`nav-link ${isActive('/login') ? 'active' : ''}`}
                style={{
                  textDecoration: 'none',
                  color: isActive('/login') ? 'var(--primary-color)' : 'var(--text-secondary)',
                  fontWeight: '500',
                  transition: 'color 0.2s'
                }}
              >
                Login
              </Link>
            </li>
          )}
        </ul>
      </div>
      <style jsx>{`
        .navbar {
          background-color: var(--bg-primary);
          box-shadow: var(--shadow-md);
          position: sticky;
          top: 0;
          z-index: 100;
        }
        
        .nav-link:hover {
          color: var(--primary-color) !important;
        }
      `}</style>
    </nav>
  );
}

