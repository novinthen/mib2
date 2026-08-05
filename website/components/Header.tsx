'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';

export default function Header() {
  const [scrolled, setScrolled] = useState(false);

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

          <nav className="hidden lg:flex items-center space-x-1" aria-label="Main navigation">
            <NavLink href="/why">Why</NavLink>
            <NavLink href="/programmes">Programmes</NavLink>
            <NavLink href="/costing">Costing</NavLink>
            <NavLink href="/kpis">KPIs</NavLink>
            <NavLink href="/risks">Risks</NavLink>
            <NavLink href="/evidence">Evidence</NavLink>
          </nav>

          <button
            className="lg:hidden p-2 rounded-lg hover:bg-neutral-100 transition-colors"
            aria-label="Open menu"
          >
            <svg className="w-5 h-5 text-neutral-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
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
