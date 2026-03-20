"use client";

import { MessageSquare, ThumbsUp, Users, Construction } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";

export default function CommunityPage() {
  return (
    <div className="min-h-screen">
      <a href="#main-content" className="skip-to-content focus-ring">
        Skip to main content
      </a>
      <Navbar />

      <main id="main-content" className="max-w-6xl mx-auto px-4 py-16">
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

      <Footer />
    </div>
  );
}
