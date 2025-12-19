import Link from "next/link";
import { Activity } from "lucide-react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Terms of Service",
  description: "PingDiff terms of service and usage guidelines.",
};

export default function TermsPage() {
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
        <h1 className="text-4xl font-bold mb-8">Terms of Service</h1>
        <p className="text-zinc-400 mb-8">Last updated: December 2024</p>

        <div className="prose prose-invert prose-zinc max-w-none space-y-8">
          <section>
            <h2 className="text-2xl font-semibold mb-4">Acceptance of Terms</h2>
            <p className="text-zinc-300 leading-relaxed">
              By using PingDiff, you agree to these terms. If you do not agree, please do not use our software or website.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Description of Service</h2>
            <p className="text-zinc-300 leading-relaxed">
              PingDiff is a free, open-source tool that tests your network connection to game servers.
              It provides ping, jitter, and packet loss measurements to help you choose the best server.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Use of Software</h2>
            <ul className="list-disc list-inside text-zinc-300 space-y-2">
              <li>PingDiff is provided free of charge for personal use</li>
              <li>You may not use PingDiff for any illegal purposes</li>
              <li>You may not attempt to disrupt or attack game servers</li>
              <li>You may not reverse engineer the software for malicious purposes</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Open Source License</h2>
            <p className="text-zinc-300 leading-relaxed">
              PingDiff is released under the MIT License. You are free to use, modify, and distribute
              the software in accordance with that license. See our{" "}
              <a href="https://github.com/bokiko/pingdiff/blob/main/LICENSE" className="text-blue-400 hover:underline">
                LICENSE file
              </a>{" "}
              for details.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Disclaimer</h2>
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <p className="text-zinc-300 leading-relaxed">
                PingDiff is provided &quot;as is&quot; without warranty of any kind. We do not guarantee:
              </p>
              <ul className="list-disc list-inside text-zinc-300 space-y-2 mt-4">
                <li>Accuracy of ping measurements</li>
                <li>Availability of the service</li>
                <li>Compatibility with all systems</li>
                <li>That using recommended servers will improve your gaming experience</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Limitation of Liability</h2>
            <p className="text-zinc-300 leading-relaxed">
              In no event shall PingDiff or its contributors be liable for any damages arising from
              the use of this software. Use at your own risk.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Third-Party Trademarks</h2>
            <p className="text-zinc-300 leading-relaxed">
              Game names mentioned (Overwatch 2, Valorant, Counter-Strike 2, etc.) are trademarks
              of their respective owners. PingDiff is not affiliated with or endorsed by any game publisher.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Changes to Terms</h2>
            <p className="text-zinc-300 leading-relaxed">
              We may update these terms from time to time. Continued use of PingDiff after changes
              constitutes acceptance of the new terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Contact</h2>
            <p className="text-zinc-300 leading-relaxed">
              For questions about these terms, please open an issue on our{" "}
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
