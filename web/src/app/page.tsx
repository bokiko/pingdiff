"use client";

import Link from "next/link";
import { useState } from "react";
import { Activity, Download, Users, Zap, Globe, TrendingUp, Menu, X } from "lucide-react";

export default function Home() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen">
      {/* Skip to content - Accessibility */}
      <a href="#main-content" className="skip-to-content focus-ring">
        Skip to main content
      </a>

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
            aria-expanded={mobileMenuOpen}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>

          {/* Desktop menu */}
          <div className="hidden md:flex items-center gap-6">
            <Link href="/dashboard" className="text-zinc-400 hover:text-white transition focus-ring rounded-lg px-2 py-1">
              Dashboard
            </Link>
            <Link href="/community" className="text-zinc-400 hover:text-white transition focus-ring rounded-lg px-2 py-1">
              Community
            </Link>
            <Link
              href="/download"
              className="btn-primary px-5 py-2 rounded-lg font-medium focus-ring"
            >
              Download
            </Link>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-zinc-800 bg-zinc-950 fade-in">
            <div className="px-4 py-4 flex flex-col gap-4">
              <Link
                href="/dashboard"
                className="text-zinc-400 hover:text-white transition py-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                Dashboard
              </Link>
              <Link
                href="/community"
                className="text-zinc-400 hover:text-white transition py-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                Community
              </Link>
              <Link
                href="/download"
                className="btn-primary text-center py-3 rounded-lg font-medium"
                onClick={() => setMobileMenuOpen(false)}
              >
                Download
              </Link>
            </div>
          </div>
        )}
      </nav>

      <main id="main-content">
        {/* Hero Section */}
        <section className="max-w-6xl mx-auto px-4 py-16 md:py-24 text-center">
          <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-2 mb-6 fade-in">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            <span className="text-sm text-blue-400">Now supporting Overwatch 2, CoD, CS2 & Battlefield 6</span>
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mb-6 leading-tight fade-in-delay-1">
            Know Your Connection
            <br />
            <span className="gradient-text">Before You Queue</span>
          </h1>

          <p className="text-lg md:text-xl text-zinc-400 max-w-2xl mx-auto mb-10 leading-relaxed fade-in-delay-2">
            Test your ping, packet loss, and jitter to game servers without launching the game.
            Get personalized recommendations based on your ISP and location.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center fade-in-delay-3">
            <Link
              href="/download"
              className="inline-flex items-center justify-center gap-2 btn-primary px-8 py-4 rounded-xl font-semibold text-lg focus-ring"
            >
              <Download className="w-5 h-5" />
              Download for Windows
            </Link>
            <Link
              href="/dashboard"
              className="inline-flex items-center justify-center gap-2 btn-secondary px-8 py-4 rounded-xl font-semibold text-lg focus-ring"
            >
              View Dashboard
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 md:gap-8 max-w-2xl mx-auto mt-16 pt-8 border-t border-zinc-800">
            <div className="slide-up" style={{ animationDelay: "0.4s" }}>
              <div className="text-2xl md:text-3xl font-bold text-blue-500">10k+</div>
              <div className="text-zinc-500 text-xs md:text-sm">Tests Run</div>
            </div>
            <div className="slide-up" style={{ animationDelay: "0.5s" }}>
              <div className="text-2xl md:text-3xl font-bold text-green-500">50+</div>
              <div className="text-zinc-500 text-xs md:text-sm">ISPs Tracked</div>
            </div>
            <div className="slide-up" style={{ animationDelay: "0.6s" }}>
              <div className="text-2xl md:text-3xl font-bold text-purple-500">8</div>
              <div className="text-zinc-500 text-xs md:text-sm">Server Regions</div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="bg-zinc-900/50 py-16 md:py-24">
          <div className="max-w-6xl mx-auto px-4">
            <h2 className="text-2xl md:text-3xl font-bold text-center mb-4">Why PingDiff?</h2>
            <p className="text-zinc-400 text-center mb-12 max-w-2xl mx-auto">
              Stop guessing. Start knowing. Get real data about your connection before every game.
            </p>

            <div className="grid md:grid-cols-3 gap-6 md:gap-8">
              {/* Feature 1 */}
              <div className="bg-zinc-800/50 border border-zinc-700 rounded-xl p-6 card-hover">
                <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center mb-4">
                  <Zap className="w-6 h-6 text-blue-500" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Real Ping Tests</h3>
                <p className="text-zinc-400 leading-relaxed">
                  Test actual game server IPs with ICMP ping. Get real latency numbers, not estimates.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-zinc-800/50 border border-zinc-700 rounded-xl p-6 card-hover">
                <div className="w-12 h-12 bg-green-500/20 rounded-xl flex items-center justify-center mb-4">
                  <Globe className="w-6 h-6 text-green-500" />
                </div>
                <h3 className="text-xl font-semibold mb-2">ISP Intelligence</h3>
                <p className="text-zinc-400 leading-relaxed">
                  See how your ISP performs. Get recommendations based on what works for players like you.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-zinc-800/50 border border-zinc-700 rounded-xl p-6 card-hover">
                <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-4">
                  <Users className="w-6 h-6 text-purple-500" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Community Tips</h3>
                <p className="text-zinc-400 leading-relaxed">
                  Learn from other players. Share tips about the best servers for your region and ISP.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="py-16 md:py-24">
          <div className="max-w-6xl mx-auto px-4">
            <h2 className="text-2xl md:text-3xl font-bold text-center mb-4">How It Works</h2>
            <p className="text-zinc-400 text-center mb-12">
              Three simple steps to better gaming
            </p>

            <div className="grid md:grid-cols-3 gap-8 md:gap-12">
              <div className="text-center group">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center text-2xl font-bold mx-auto mb-4 shadow-lg shadow-blue-500/25 group-hover:scale-110 transition-transform">
                  1
                </div>
                <h3 className="text-xl font-semibold mb-2">Download</h3>
                <p className="text-zinc-400">
                  Get the lightweight app (under 20MB). Run the installer and launch from Start Menu.
                </p>
              </div>

              <div className="text-center group">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center text-2xl font-bold mx-auto mb-4 shadow-lg shadow-blue-500/25 group-hover:scale-110 transition-transform">
                  2
                </div>
                <h3 className="text-xl font-semibold mb-2">Test</h3>
                <p className="text-zinc-400">
                  Select your region and click test. Results in under 30 seconds.
                </p>
              </div>

              <div className="text-center group">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center text-2xl font-bold mx-auto mb-4 shadow-lg shadow-blue-500/25 group-hover:scale-110 transition-transform">
                  3
                </div>
                <h3 className="text-xl font-semibold mb-2">Know</h3>
                <p className="text-zinc-400">
                  See your results, track history, and get recommendations on the dashboard.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Supported Games */}
        <section className="bg-zinc-900/50 py-16 md:py-24">
          <div className="max-w-6xl mx-auto px-4 text-center">
            <h2 className="text-2xl md:text-3xl font-bold mb-4">Supported Games</h2>
            <p className="text-zinc-400 mb-12">
              Test your connection to your favorite games. More games coming soon.
            </p>

            <div className="flex justify-center gap-6 md:gap-8 flex-wrap">
              <div className="bg-zinc-800 border border-zinc-700 rounded-xl p-6 w-44 md:w-48 card-hover">
                <div className="w-16 h-16 bg-orange-500/20 rounded-xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-3xl">🎮</span>
                </div>
                <h3 className="font-semibold mb-2">Overwatch 2</h3>
                <span className="text-xs text-green-500 bg-green-500/20 px-3 py-1 rounded-full font-medium">
                  Active
                </span>
              </div>

              <div className="bg-zinc-800 border border-zinc-700 rounded-xl p-6 w-44 md:w-48 card-hover">
                <div className="w-16 h-16 bg-green-500/20 rounded-xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-3xl">🔫</span>
                </div>
                <h3 className="font-semibold mb-2">Call of Duty</h3>
                <span className="text-xs text-green-500 bg-green-500/20 px-3 py-1 rounded-full font-medium">
                  Active
                </span>
              </div>

              <div className="bg-zinc-800/50 border border-zinc-700/50 rounded-xl p-6 w-44 md:w-48 opacity-60">
                <div className="w-16 h-16 bg-red-500/20 rounded-xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-3xl">🎯</span>
                </div>
                <h3 className="font-semibold mb-2">Valorant</h3>
                <span className="text-xs text-zinc-500 bg-zinc-700 px-3 py-1 rounded-full">
                  Coming Soon
                </span>
              </div>

              <div className="bg-zinc-800 border border-zinc-700 rounded-xl p-6 w-44 md:w-48 card-hover">
                <div className="w-16 h-16 bg-yellow-500/20 rounded-xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-3xl">💥</span>
                </div>
                <h3 className="font-semibold mb-2">Counter-Strike 2</h3>
                <span className="text-xs text-green-500 bg-green-500/20 px-3 py-1 rounded-full font-medium">
                  Active
                </span>
              </div>

              <div className="bg-zinc-800 border border-zinc-700 rounded-xl p-6 w-44 md:w-48 card-hover">
                <div className="w-16 h-16 bg-emerald-500/20 rounded-xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-3xl">🎖️</span>
                </div>
                <h3 className="font-semibold mb-2">Battlefield 6</h3>
                <span className="text-xs text-green-500 bg-green-500/20 px-3 py-1 rounded-full font-medium">
                  Active
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 md:py-24">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <div className="w-20 h-20 bg-blue-500/20 rounded-2xl flex items-center justify-center mx-auto mb-6 float">
              <TrendingUp className="w-10 h-10 text-blue-500" />
            </div>
            <h2 className="text-2xl md:text-3xl font-bold mb-4">Ready to Improve Your Game?</h2>
            <p className="text-zinc-400 mb-8 max-w-xl mx-auto leading-relaxed">
              Join thousands of players who test their connection before every session.
              Know which server gives you the best ping.
            </p>
            <Link
              href="/download"
              className="inline-flex items-center gap-2 btn-primary px-8 py-4 rounded-xl font-semibold text-lg focus-ring"
            >
              <Download className="w-5 h-5" />
              Get PingDiff Free
            </Link>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-800 py-8">
        <div className="max-w-6xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-500" />
            <span className="font-semibold">PingDiff</span>
            <span className="text-zinc-500 text-sm">© 2025</span>
          </div>
          <div className="flex gap-6 text-zinc-400 text-sm">
            <Link href="/privacy" className="hover:text-white transition focus-ring rounded px-1">
              Privacy
            </Link>
            <Link href="/terms" className="hover:text-white transition focus-ring rounded px-1">
              Terms
            </Link>
            <a
              href="https://github.com/bokiko/pingdiff"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition focus-ring rounded px-1"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
