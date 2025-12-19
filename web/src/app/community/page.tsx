"use client";

import Link from "next/link";
import { useState } from "react";
import { Activity, MessageSquare, ThumbsUp, Users, Menu, X, Construction } from "lucide-react";

export default function CommunityPage() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen">
      {/* Navigation */}
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
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>

          {/* Desktop menu */}
          <div className="hidden md:flex items-center gap-6">
            <Link href="/dashboard" className="text-zinc-400 hover:text-white transition focus-ring rounded-lg px-2 py-1">
              Dashboard
            </Link>
            <Link href="/community" className="text-white font-medium focus-ring rounded-lg px-2 py-1">
              Community
            </Link>
            <Link href="/download" className="btn-primary px-5 py-2 rounded-lg font-medium focus-ring">
              Download
            </Link>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-zinc-800 bg-zinc-950 fade-in">
            <div className="px-4 py-4 flex flex-col gap-4">
              <Link href="/dashboard" className="text-zinc-400 hover:text-white transition py-2" onClick={() => setMobileMenuOpen(false)}>
                Dashboard
              </Link>
              <Link href="/community" className="text-white font-medium py-2" onClick={() => setMobileMenuOpen(false)}>
                Community
              </Link>
              <Link href="/download" className="btn-primary text-center py-3 rounded-lg font-medium" onClick={() => setMobileMenuOpen(false)}>
                Download
              </Link>
            </div>
          </div>
        )}
      </nav>

      <main className="max-w-6xl mx-auto px-4 py-16">
        {/* Coming Soon Banner */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-yellow-500/20 rounded-2xl mb-6">
            <Construction className="w-10 h-10 text-yellow-500" />
          </div>
          <h1 className="text-4xl font-bold mb-4">Community Hub</h1>
          <p className="text-zinc-400 text-lg max-w-xl mx-auto">
            Share tips, compare results, and help other players find the best servers.
          </p>
          <div className="mt-6 inline-flex items-center gap-2 bg-yellow-500/10 border border-yellow-500/20 rounded-full px-4 py-2">
            <span className="text-yellow-400 text-sm font-medium">Coming Soon</span>
          </div>
        </div>

        {/* Preview Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-16">
          <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6 opacity-60">
            <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center mb-4">
              <MessageSquare className="w-6 h-6 text-blue-500" />
            </div>
            <h3 className="text-xl font-semibold mb-2">ISP Tips</h3>
            <p className="text-zinc-400">
              Share and discover tips for optimizing your connection based on your ISP and region.
            </p>
          </div>

          <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6 opacity-60">
            <div className="w-12 h-12 bg-green-500/20 rounded-xl flex items-center justify-center mb-4">
              <ThumbsUp className="w-6 h-6 text-green-500" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Upvote System</h3>
            <p className="text-zinc-400">
              Vote on the most helpful tips to surface the best advice for each region.
            </p>
          </div>

          <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6 opacity-60">
            <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-4">
              <Users className="w-6 h-6 text-purple-500" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Leaderboards</h3>
            <p className="text-zinc-400">
              See the best ping results by region, ISP, and server location.
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center bg-zinc-900/50 border border-zinc-800 rounded-2xl p-8">
          <h2 className="text-2xl font-bold mb-4">Want to be notified when Community launches?</h2>
          <p className="text-zinc-400 mb-6">
            Star our GitHub repo to get updates on new features.
          </p>
          <a
            href="https://github.com/bokiko/pingdiff"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 btn-primary px-6 py-3 rounded-xl font-medium"
          >
            Star on GitHub
          </a>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-800 py-8 mt-16">
        <div className="max-w-6xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-500" />
            <span className="font-semibold">PingDiff</span>
            <span className="text-zinc-500 text-sm">© 2025</span>
          </div>
          <div className="flex gap-6 text-zinc-400 text-sm">
            <Link href="/privacy" className="hover:text-white transition">Privacy</Link>
            <Link href="/terms" className="hover:text-white transition">Terms</Link>
            <a href="https://github.com/bokiko/pingdiff" target="_blank" rel="noopener noreferrer" className="hover:text-white transition">
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
