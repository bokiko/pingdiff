import Link from "next/link";
import { Activity } from "lucide-react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "PingDiff privacy policy - how we handle your data.",
};

export default function PrivacyPage() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="flex items-center gap-2">
            <Activity className="w-8 h-8 text-blue-500" />
            <span className="text-xl font-bold">PingDiff</span>
          </Link>
        </div>
      </nav>

      <main className="max-w-3xl mx-auto px-4 py-16">
        <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
        <p className="text-zinc-400 mb-8">Last updated: December 2024</p>

        <div className="prose prose-invert prose-zinc max-w-none space-y-8">
          <section>
            <h2 className="text-2xl font-semibold mb-4">Overview</h2>
            <p className="text-zinc-300 leading-relaxed">
              PingDiff is designed with privacy in mind. We collect minimal data to provide our service,
              and you have full control over what you share.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Data We Collect</h2>
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4">
              <div>
                <h3 className="font-semibold text-blue-400 mb-2">When sharing is enabled (opt-in):</h3>
                <ul className="list-disc list-inside text-zinc-300 space-y-2">
                  <li>Ping test results (latency, jitter, packet loss)</li>
                  <li>ISP name and general location (country/city)</li>
                  <li>Hashed IP address (cannot be reversed)</li>
                  <li>App version</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-green-400 mb-2">When sharing is disabled:</h3>
                <p className="text-zinc-300">No data is sent to our servers. Results are only stored locally on your device.</p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">How We Use Data</h2>
            <ul className="list-disc list-inside text-zinc-300 space-y-2">
              <li>Generate community statistics and recommendations</li>
              <li>Improve server recommendations for users with similar ISPs</li>
              <li>Display aggregate data on the public dashboard</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">What We Do NOT Collect</h2>
            <ul className="list-disc list-inside text-zinc-300 space-y-2">
              <li>Personal identification information</li>
              <li>Email addresses or account information</li>
              <li>Your actual IP address (only hashed)</li>
              <li>Any data from your games</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Your Control</h2>
            <p className="text-zinc-300 leading-relaxed">
              You can toggle data sharing on or off at any time in the desktop app settings.
              Your preference is stored locally and persists across updates.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Third-Party Services</h2>
            <ul className="list-disc list-inside text-zinc-300 space-y-2">
              <li><strong>ip-api.com</strong> - Used to detect your ISP and location (their privacy policy applies)</li>
              <li><strong>Supabase</strong> - Database hosting (their privacy policy applies)</li>
              <li><strong>Vercel</strong> - Website hosting (their privacy policy applies)</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Contact</h2>
            <p className="text-zinc-300 leading-relaxed">
              For privacy concerns, please open an issue on our{" "}
              <a href="https://github.com/bokiko/pingdiff" className="text-blue-400 hover:underline">
                GitHub repository
              </a>.
            </p>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-800 py-8 mt-16">
        <div className="max-w-6xl mx-auto px-4 text-center text-zinc-500 text-sm">
          <Link href="/" className="hover:text-white transition">
            ← Back to Home
          </Link>
        </div>
      </footer>
    </div>
  );
}
