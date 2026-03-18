"use client";

import Link from "next/link";
import { useState } from "react";
import { Activity, Menu, X } from "lucide-react";
import { usePathname } from "next/navigation";

interface NavLink {
  href: string;
  label: string;
}

const NAV_LINKS: NavLink[] = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/community", label: "Community" },
  { href: "/download", label: "Download" },
];

export function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  const isActive = (href: string) => pathname === href;
  const isDownload = (href: string) => href === "/download";

  return (
    <nav className="border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="flex items-center gap-2 focus-ring rounded-lg">
          <Activity className="w-7 h-7 md:w-8 md:h-8 text-blue-500" />
          <span className="text-lg md:text-xl font-bold">PingDiff</span>
        </Link>

        {/* Mobile menu button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 text-zinc-400 hover:text-white transition focus-ring rounded-lg"
          aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
          aria-expanded={mobileMenuOpen}
          aria-controls="mobile-menu"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>

        {/* Desktop menu */}
        <div className="hidden md:flex items-center gap-6">
          {NAV_LINKS.map(({ href, label }) =>
            isDownload(href) ? (
              <Link
                key={href}
                href={href}
                className="btn-primary px-5 py-2 rounded-lg font-medium focus-ring"
              >
                {label}
              </Link>
            ) : (
              <Link
                key={href}
                href={href}
                className={`transition focus-ring rounded-lg px-2 py-1 ${
                  isActive(href) ? "text-white font-medium" : "text-zinc-400 hover:text-white"
                }`}
              >
                {label}
              </Link>
            )
          )}
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div
          id="mobile-menu"
          className="md:hidden border-t border-zinc-800 bg-zinc-950 fade-in"
        >
          <div className="px-4 py-4 flex flex-col gap-4">
            {NAV_LINKS.map(({ href, label }) =>
              isDownload(href) ? (
                <Link
                  key={href}
                  href={href}
                  className="btn-primary text-center py-3 rounded-lg font-medium"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {label}
                </Link>
              ) : (
                <Link
                  key={href}
                  href={href}
                  className={`transition py-2 ${
                    isActive(href) ? "text-white font-medium" : "text-zinc-400 hover:text-white"
                  }`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {label}
                </Link>
              )
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
