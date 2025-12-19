"use client";

import Link from "next/link";
import { Activity, Download, Users, Zap, Globe, TrendingUp } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="flex items-center gap-2">
            <Activity className="w-8 h-8 text-blue-500" />
            <span className="text-xl font-bold">PingDiff</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link href="/dashboard" className="text-zinc-400 hover:text-white transition">
              Dashboard
            </Link>
            <Link href="/community" className="text-zinc-400 hover:text-white transition">
              Community
            </Link>
            <Link
              href="/download"
              className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg font-medium transition"
            >
              Download
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-4 py-20 text-center">
        <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-2 mb-6">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          <span className="text-sm text-blue-400">Now supporting Overwatch 2</span>
        </div>

        <h1 className="text-5xl md:text-6xl font-bold mb-6">
          Know Your Connection
          <br />
          <span className="text-blue-500">Before You Queue</span>
        </h1>

        <p className="text-xl text-zinc-400 max-w-2xl mx-auto mb-8">
          Test your ping, packet loss, and jitter to game servers without launching the game.
          Get personalized recommendations based on your ISP and location.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/download"
            className="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 px-8 py-4 rounded-lg font-semibold text-lg transition pulse-glow"
          >
            <Download className="w-5 h-5" />
            Download for Windows
          </Link>
          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center gap-2 bg-zinc-800 hover:bg-zinc-700 px-8 py-4 rounded-lg font-semibold text-lg transition"
          >
            View Dashboard
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto mt-16 pt-8 border-t border-zinc-800">
          <div>
            <div className="text-3xl font-bold text-blue-500">10k+</div>
            <div className="text-zinc-500 text-sm">Tests Run</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-green-500">50+</div>
            <div className="text-zinc-500 text-sm">ISPs Tracked</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-purple-500">8</div>
            <div className="text-zinc-500 text-sm">Server Regions</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-zinc-900/50 py-20">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-4">Why PingDiff?</h2>
          <p className="text-zinc-400 text-center mb-12 max-w-2xl mx-auto">
            Stop guessing. Start knowing. Get real data about your connection before every game.
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-zinc-800/50 border border-zinc-700 rounded-xl p-6">
              <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-blue-500" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Real Ping Tests</h3>
              <p className="text-zinc-400">
                Test actual game server IPs with ICMP ping. Get real latency numbers, not estimates.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-zinc-800/50 border border-zinc-700 rounded-xl p-6">
              <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center mb-4">
                <Globe className="w-6 h-6 text-green-500" />
              </div>
              <h3 className="text-xl font-semibold mb-2">ISP Intelligence</h3>
              <p className="text-zinc-400">
                See how your ISP performs. Get recommendations based on what works for players like you.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-zinc-800/50 border border-zinc-700 rounded-xl p-6">
              <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4">
                <Users className="w-6 h-6 text-purple-500" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Community Tips</h3>
              <p className="text-zinc-400">
                Learn from other players. Share tips about the best servers for your region and ISP.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-4">How It Works</h2>
          <p className="text-zinc-400 text-center mb-12">
            Three simple steps to better gaming
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold mb-2">Download</h3>
              <p className="text-zinc-400">
                Get the lightweight app (under 20MB). No installation required - just run it.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold mb-2">Test</h3>
              <p className="text-zinc-400">
                Select your region and click test. Results in under 30 seconds.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
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
      <section className="bg-zinc-900/50 py-20">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Supported Games</h2>
          <p className="text-zinc-400 mb-12">
            Starting with Overwatch 2. More games coming soon.
          </p>

          <div className="flex justify-center gap-8 flex-wrap">
            <div className="bg-zinc-800 border border-zinc-700 rounded-xl p-6 w-48">
              <div className="w-16 h-16 bg-orange-500/20 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <span className="text-3xl">🎮</span>
              </div>
              <h3 className="font-semibold">Overwatch 2</h3>
              <span className="text-xs text-green-500 bg-green-500/20 px-2 py-1 rounded-full">
                Active
              </span>
            </div>

            <div className="bg-zinc-800/50 border border-zinc-700/50 rounded-xl p-6 w-48 opacity-50">
              <div className="w-16 h-16 bg-red-500/20 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <span className="text-3xl">🎯</span>
              </div>
              <h3 className="font-semibold">Valorant</h3>
              <span className="text-xs text-zinc-500 bg-zinc-700 px-2 py-1 rounded-full">
                Coming Soon
              </span>
            </div>

            <div className="bg-zinc-800/50 border border-zinc-700/50 rounded-xl p-6 w-48 opacity-50">
              <div className="w-16 h-16 bg-yellow-500/20 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <span className="text-3xl">💥</span>
              </div>
              <h3 className="font-semibold">Counter-Strike 2</h3>
              <span className="text-xs text-zinc-500 bg-zinc-700 px-2 py-1 rounded-full">
                Coming Soon
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <TrendingUp className="w-16 h-16 text-blue-500 mx-auto mb-6" />
          <h2 className="text-3xl font-bold mb-4">Ready to Improve Your Game?</h2>
          <p className="text-zinc-400 mb-8 max-w-xl mx-auto">
            Join thousands of players who test their connection before every session.
            Know which server gives you the best ping.
          </p>
          <Link
            href="/download"
            className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-8 py-4 rounded-lg font-semibold text-lg transition"
          >
            <Download className="w-5 h-5" />
            Get PingDiff Free
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-zinc-800 py-8">
        <div className="max-w-6xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-500" />
            <span className="font-semibold">PingDiff</span>
            <span className="text-zinc-500 text-sm">© 2024</span>
          </div>
          <div className="flex gap-6 text-zinc-400 text-sm">
            <Link href="/privacy" className="hover:text-white transition">
              Privacy
            </Link>
            <Link href="/terms" className="hover:text-white transition">
              Terms
            </Link>
            <a
              href="https://github.com/bokiko/pingdiff"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
