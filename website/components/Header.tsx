'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import AuthButton from './AuthButton';

const NAV_ITEMS = [
  { href: '/why', label: 'Why' },
  { href: '/programmes', label: 'Programmes' },
  { href: '/costing', label: 'Costing' },
  { href: '/kpis', label: 'KPIs' },
  { href: '/risks', label: 'Risks' },
  { href: '/evidence', label: 'Evidence' },
  { href: '/ideas', label: 'Ideas' },
  { href: '/participate', label: 'Participate' },
];

export default function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`sticky top-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-white/80 backdrop-blur-xl border-b border-neutral-200/50 shadow-soft'
          : 'bg-white/50 backdrop-blur-md border-b border-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="w-10 h-10 bg-gradient-primary rounded-xl flex items-center justify-center font-bold text-white shadow-glow group-hover:scale-105 transition-transform">
              MIB
            </div>
            <div>
              <div className="font-semibold text-base leading-tight text-neutral-900">
                Malaysian Indian Blueprint 2.0
              </div>
              <div className="text-xs text-neutral-500">Progression Blueprint 2026–2031</div>
            </div>
          </Link>

          <div className="hidden lg:flex items-center gap-2">
            <nav className="flex items-center space-x-1" aria-label="Main navigation">
              {NAV_ITEMS.map((item) => (
                <NavLink key={item.href} href={item.href}>
                  {item.label}
                </NavLink>
              ))}
            </nav>
            <AuthButton />
          </div>

          <button
            className="lg:hidden p-2 rounded-lg hover:bg-neutral-100 transition-colors"
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={menuOpen}
            aria-controls="mobile-menu"
            onClick={() => setMenuOpen((open) => !open)}
          >
            <svg className="w-6 h-6 text-neutral-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {menuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <nav
          id="mobile-menu"
          className="lg:hidden border-t border-neutral-200/70 bg-white/95 backdrop-blur-xl"
          aria-label="Mobile navigation"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 space-y-1">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname === item.href || pathname?.startsWith(item.href + '/');
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMenuOpen(false)}
                  className={`block px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-primary-50 text-primary-600'
                      : 'text-neutral-700 hover:bg-neutral-50'
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
            <div className="px-4 pt-3 mt-2 border-t border-neutral-200/70">
              <AuthButton />
            </div>
          </div>
        </nav>
      )}
    </header>
  );
}

function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  const pathname = usePathname();
  const isActive = pathname === href || pathname?.startsWith(href + '/');

  return (
    <Link
      href={href}
      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
        isActive
          ? 'bg-primary-50 text-primary-600'
          : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
      }`}
    >
      {children}
    </Link>
  );
}
