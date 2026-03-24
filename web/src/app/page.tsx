"use client";

import Link from "next/link";
import { Download, Zap, Globe, TrendingUp, Shield, Code, Lock, Github } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Skip to content - Accessibility */}
      <a href="#main-content" className="skip-to-content focus-ring">
        Skip to main content
      </a>

      <Navbar />

      <main id="main-content">
        {/* Hero Section */}
        <section className="max-w-6xl mx-auto px-4 py-16 md:py-24 relative">
          {/* Background glow */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[#00F0FF]/5 rounded-full blur-[120px] pointer-events-none" />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            {/* Text Content */}
            <div className="space-y-8 z-10 text-center lg:text-left">
              {/* Open Source Trust Badge */}
              <div className="inline-flex items-center gap-3 bg-zinc-800/80 border border-zinc-700 rounded-full px-5 py-2.5 fade-in">
                <div className="flex items-center gap-2">
                  <Shield className="w-4 h-4 text-green-500" />
                  <span className="text-sm font-medium text-green-400">100% Open Source</span>
                </div>
                <span className="text-zinc-600">|</span>
                <div className="flex items-center gap-3">
                  <a
                    href="https://github.com/bokiko/pingdiff"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1.5 text-sm text-zinc-400 hover:text-white transition"
                  >
                    <Github className="w-4 h-4" />
                    GitHub
                  </a>
                </div>
              </div>

              <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight leading-tight fade-in-delay-1">
                <span className="bg-gradient-to-r from-white to-zinc-400 bg-clip-text text-transparent">
                  KNOW YOUR
                </span>
                <br />
                <span className="gradient-text">CONNECTION</span>
              </h1>

              <p className="text-lg text-zinc-400 max-w-lg leading-relaxed fade-in-delay-2">
                PingDiff ensures you always know your true connection quality.
                Test, compare, and optimize your network for competitive gaming.
              </p>

              <div className="pt-2 fade-in-delay-3">
                <Link
                  href="/download"
                  className="inline-flex items-center justify-center gap-2 btn-primary px-8 py-4 rounded-md text-lg uppercase tracking-wider focus-ring"
                >
                  <Download className="w-5 h-5" />
                  Get PingDiff Free
                </Link>
              </div>
            </div>

            {/* Ping Display Visual */}
            <div className="relative z-10 flex justify-center lg:justify-end fade-in-delay-2">
              <div className="relative w-full max-w-md aspect-video rounded-xl ping-display flex items-center justify-center">
                <div className="corner-decoration corner-tl" />
                <div className="corner-decoration corner-br" />
                <div className="text-center z-10">
                  <span className="text-4xl md:text-5xl font-bold font-mono text-[#00F0FF] drop-shadow-[0_0_15px_rgba(0,240,255,0.8)]">
                    PING: 18ms
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 md:gap-8 max-w-2xl mx-auto mt-16 pt-8 border-t border-white/10">
            <div className="slide-up text-center" style={{ animationDelay: "0.4s" }}>
              <div className="text-2xl md:text-3xl font-bold text-[#00F0FF]">10k+</div>
              <div className="text-zinc-500 text-xs md:text-sm">Tests Run</div>
            </div>
            <div className="slide-up text-center" style={{ animationDelay: "0.5s" }}>
              <div className="text-2xl md:text-3xl font-bold text-[#00F0FF]">50+</div>
              <div className="text-zinc-500 text-xs md:text-sm">ISPs Tracked</div>
            </div>
            <div className="slide-up text-center" style={{ animationDelay: "0.6s" }}>
              <div className="text-2xl md:text-3xl font-bold text-[#00F0FF]">8</div>
              <div className="text-zinc-500 text-xs md:text-sm">Server Regions</div>
            </div>
          </div>
        </section>

        {/* Features Section - Neon Cards */}
        <section className="max-w-6xl mx-auto px-4 py-16 md:py-24" aria-labelledby="features-heading">
          <div className="grid md:grid-cols-3 gap-6 md:gap-8">
            {/* Feature 1 */}
            <div className="neon-card rounded-xl p-8 flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-full border border-[#00F0FF]/30 flex items-center justify-center mb-6 text-[#00F0FF]">
                <Zap className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Real Ping Tests</h3>
              <p className="text-sm text-zinc-400 leading-relaxed">
                Execute accurate ICMP and TCP ping tests directly to game servers to see your true latency.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="neon-card rounded-xl p-8 flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-full border border-[#00F0FF]/30 flex items-center justify-center mb-6 text-[#00F0FF]">
                <Globe className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">ISP Intelligence</h3>
              <p className="text-sm text-zinc-400 leading-relaxed">
                Analyze routing paths and identify potential bottlenecks caused by your Internet Service Provider.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="neon-card rounded-xl p-8 flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-full border border-[#00F0FF]/30 flex items-center justify-center mb-6 text-[#00F0FF]">
                <TrendingUp className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Multi-Region Compare</h3>
              <p className="text-sm text-zinc-400 leading-relaxed">
                Simultaneously check your connection quality across multiple regional data centers.
              </p>
            </div>
          </div>
        </section>

        {/* Why PingDiff Section */}
        <section className="py-16 md:py-24" aria-labelledby="why-heading">
          <div className="max-w-6xl mx-auto px-4">
            <h2 id="why-heading" className="text-3xl font-bold text-center mb-4 tracking-wider uppercase">
              Why PingDiff?
            </h2>
            <p className="text-zinc-400 text-center mb-12 max-w-2xl mx-auto">
              Stop guessing. Start knowing. Get real data about your connection before every game.
            </p>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="glass p-6 rounded-lg border border-white/10 hover:border-[#00F0FF]/50 transition-colors group">
                <div className="flex flex-col items-center text-center space-y-4">
                  <div className="text-[#00F0FF] group-hover:scale-110 transition-transform">
                    <Zap className="w-10 h-10" />
                  </div>
                  <h4 className="text-lg font-semibold text-white">Real Ping Tests</h4>
                  <p className="text-sm text-zinc-400">Stop relying on misleading in-game meters. Get raw network data.</p>
                </div>
              </div>

              <div className="glass p-6 rounded-lg border border-white/10 hover:border-[#00F0FF]/50 transition-colors group">
                <div className="flex flex-col items-center text-center space-y-4">
                  <div className="text-[#00F0FF] group-hover:scale-110 transition-transform">
                    <Globe className="w-10 h-10" />
                  </div>
                  <h4 className="text-lg font-semibold text-white">ISP Intelligence</h4>
                  <p className="text-sm text-zinc-400">Know exactly when your provider is routing you inefficiently.</p>
                </div>
              </div>

              <div className="glass p-6 rounded-lg border border-white/10 hover:border-[#00F0FF]/50 transition-colors group">
                <div className="flex flex-col items-center text-center space-y-4">
                  <div className="text-[#00F0FF] group-hover:scale-110 transition-transform">
                    <TrendingUp className="w-10 h-10" />
                  </div>
                  <h4 className="text-lg font-semibold text-white">Multi-Region Compare</h4>
                  <p className="text-sm text-zinc-400">Find the optimal server location before you queue up.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Open Source Trust Section */}
        <section className="py-16 md:py-24">
          <div className="max-w-6xl mx-auto px-4">
            <div className="neon-card rounded-2xl p-8 md:p-12">
              <div className="flex flex-col md:flex-row items-center gap-8">
                <div className="flex-shrink-0">
                  <div className="w-20 h-20 bg-green-500/20 rounded-2xl flex items-center justify-center">
                    <Code className="w-10 h-10 text-green-500" />
                  </div>
                </div>
                <div className="text-center md:text-left flex-1">
                  <h2 className="text-2xl md:text-3xl font-bold mb-3">Built in the Open</h2>
                  <p className="text-zinc-400 mb-4 max-w-2xl leading-relaxed">
                    PingDiff is 100% open source. Every line of code is public on GitHub.
                    No hidden trackers, no data harvesting, no premium tiers.
                    Built by gamers who were tired of sketchy &quot;ping tools&quot; that sell your data.
                  </p>
                  <div className="flex flex-wrap gap-4 justify-center md:justify-start">
                    <div className="flex items-center gap-2 text-sm">
                      <Shield className="w-4 h-4 text-green-500" />
                      <span className="text-zinc-300">No Tracking</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <Lock className="w-4 h-4 text-[#00F0FF]" />
                      <span className="text-zinc-300">Privacy First</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <Code className="w-4 h-4 text-purple-500" />
                      <span className="text-zinc-300">MIT License</span>
                    </div>
                  </div>
                </div>
                <div className="flex-shrink-0 flex flex-col sm:flex-row gap-3">
                  <a
                    href="https://github.com/bokiko/pingdiff"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 bg-zinc-700 hover:bg-zinc-600 text-white px-6 py-3 rounded-xl font-semibold transition"
                  >
                    <Github className="w-5 h-5" />
                    GitHub
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="py-16 md:py-24" aria-labelledby="how-it-works-heading">
          <div className="max-w-5xl mx-auto px-4">
            <h2 id="how-it-works-heading" className="text-3xl font-bold text-center mb-4 tracking-wider uppercase">
              How It Works
            </h2>
            <p className="text-zinc-400 text-center mb-12">
              Three simple steps to better gaming
            </p>

            <div className="flex flex-col md:flex-row items-center justify-between gap-4 relative">
              {/* Connecting line (desktop) */}
              <div className="hidden md:block absolute top-1/2 left-[10%] right-[10%] h-[1px] bg-white/10 -translate-y-1/2 -z-10" />

              {/* Step 1 */}
              <div className="glass w-full md:w-1/3 p-6 rounded-xl border border-white/5 relative">
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-[#00F0FF] text-[#0B0F19] font-bold flex items-center justify-center text-sm shadow-[0_0_20px_rgba(0,240,255,0.4)]">
                  1
                </div>
                <div className="text-center mt-4">
                  <h4 className="text-lg font-semibold text-white mb-2">Download</h4>
                  <p className="text-sm text-zinc-400">Get the lightweight app. Run the installer and launch from Start Menu.</p>
                </div>
              </div>

              {/* Arrow (mobile) */}
              <div className="md:hidden text-[#00F0FF] py-2">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 14l-7 7m0 0l-7-7m7 7V3" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" /></svg>
              </div>
              {/* Arrow (desktop) */}
              <div className="hidden md:block text-[#00F0FF] bg-[#0B0F19] px-2 z-10">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M14 5l7 7m0 0l-7 7m7-7H3" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" /></svg>
              </div>

              {/* Step 2 */}
              <div className="glass w-full md:w-1/3 p-6 rounded-xl border border-white/5 relative">
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-[#00F0FF] text-[#0B0F19] font-bold flex items-center justify-center text-sm shadow-[0_0_20px_rgba(0,240,255,0.4)]">
                  2
                </div>
                <div className="text-center mt-4">
                  <h4 className="text-lg font-semibold text-white mb-2">Test</h4>
                  <p className="text-sm text-zinc-400">Select multiple regions to compare. PingDiff runs diagnostics to server endpoints.</p>
                </div>
              </div>

              {/* Arrow (mobile) */}
              <div className="md:hidden text-[#00F0FF] py-2">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 14l-7 7m0 0l-7-7m7 7V3" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" /></svg>
              </div>
              {/* Arrow (desktop) */}
              <div className="hidden md:block text-[#00F0FF] bg-[#0B0F19] px-2 z-10">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M14 5l7 7m0 0l-7 7m7-7H3" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" /></svg>
              </div>

              {/* Step 3 */}
              <div className="glass w-full md:w-1/3 p-6 rounded-xl border border-white/5 relative">
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-[#00F0FF] text-[#0B0F19] font-bold flex items-center justify-center text-sm shadow-[0_0_20px_rgba(0,240,255,0.4)]">
                  3
                </div>
                <div className="text-center mt-4">
                  <h4 className="text-lg font-semibold text-white mb-2">Know</h4>
                  <p className="text-sm text-zinc-400">Review results ranked by ping. Find your best server across all regions.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Supported Games */}
        <section className="py-16 md:py-24" aria-labelledby="supported-games-heading">
          <div className="max-w-5xl mx-auto px-4 text-center">
            <div className="inline-flex items-center gap-2 bg-[#00F0FF]/10 border border-[#00F0FF]/20 rounded-full px-4 py-2 mb-4" aria-hidden="true">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
              <span className="text-sm text-[#00F0FF]">9 games &bull; 141 servers worldwide</span>
            </div>
            <h2 id="supported-games-heading" className="text-3xl font-bold mb-4 tracking-wider uppercase">Supported Games</h2>
            <p className="text-zinc-400 mb-12">
              Test your connection to your favorite games. More coming soon.
            </p>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 lg:gap-6">
              {[
                { name: "Valorant", abbr: "VAL", color: "text-red-500" },
                { name: "Overwatch 2", abbr: "OW2", color: "text-orange-500" },
                { name: "Apex Legends", abbr: "APX", color: "text-red-400" },
                { name: "CS 2", abbr: "CS2", color: "text-amber-500" },
                { name: "League of Legends", abbr: "LOL", color: "text-amber-400" },
                { name: "Fortnite", abbr: "FN", color: "text-purple-500" },
              ].map((game) => (
                <div
                  key={game.name}
                  className="glass rounded-xl p-6 flex flex-col items-center justify-center border border-white/5 hover:border-white/20 transition-all hover:-translate-y-1 aspect-video group cursor-default"
                >
                  <div className="w-16 h-16 bg-zinc-800/50 rounded-xl mx-auto mb-4 flex items-center justify-center">
                    <span className={`text-2xl font-bold ${game.color}`}>{game.abbr}</span>
                  </div>
                  <h3 className="text-lg font-bold text-white uppercase tracking-wider mb-2">{game.name}</h3>
                  <span className="text-xs text-green-500 bg-green-500/20 px-3 py-1 rounded-full font-medium">
                    Active
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 md:py-24">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <div className="w-20 h-20 bg-[#00F0FF]/20 rounded-2xl flex items-center justify-center mx-auto mb-6 float">
              <TrendingUp className="w-10 h-10 text-[#00F0FF]" />
            </div>
            <h2 className="text-2xl md:text-3xl font-bold mb-4">Ready to Improve Your Game?</h2>
            <p className="text-zinc-400 mb-8 max-w-xl mx-auto leading-relaxed">
              Join thousands of players who test their connection before every session.
              Know which server gives you the best ping.
            </p>
            <Link
              href="/download"
              className="inline-flex items-center gap-2 btn-primary px-8 py-4 rounded-md font-semibold text-lg uppercase tracking-wider focus-ring"
            >
              <Download className="w-5 h-5" />
              Get PingDiff Free
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
