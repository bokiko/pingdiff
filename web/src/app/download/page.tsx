"use client";

import Link from "next/link";
import { Activity, Download, Shield, Cpu, HardDrive, CheckCircle, Loader2 } from "lucide-react";
import { useEffect, useState } from "react";

interface ReleaseInfo {
  version: string;
  downloadUrl: string;
  size: string;
  date: string;
}

export default function DownloadPage() {
  const [release, setRelease] = useState<ReleaseInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch latest release from GitHub API
    fetch("https://api.github.com/repos/bokiko/pingdiff/releases/latest")
      .then(res => res.json())
      .then(data => {
        const asset = data.assets?.find((a: { name: string }) => a.name.endsWith('.exe'));
        if (asset) {
          setRelease({
            version: data.tag_name || "v1.2.0",
            downloadUrl: asset.browser_download_url,
            size: `${(asset.size / (1024 * 1024)).toFixed(1)}MB`,
            date: new Date(data.published_at).toLocaleDateString()
          });
        }
        setLoading(false);
      })
      .catch(() => {
        // Fallback
        setRelease({
          version: "v1.2.0",
          downloadUrl: "https://github.com/bokiko/pingdiff/releases/latest/download/PingDiff-v1.2.0.exe",
          size: "~15MB",
          date: ""
        });
        setLoading(false);
      });
  }, []);

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
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Download PingDiff</h1>
          <p className="text-zinc-400 text-lg">
            Get the desktop app to test your connection to game servers
          </p>
        </div>

        {/* Download Card */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 mb-8">
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="w-24 h-24 bg-blue-600/20 rounded-2xl flex items-center justify-center">
              <Activity className="w-12 h-12 text-blue-500" />
            </div>

            <div className="flex-1 text-center md:text-left">
              <h2 className="text-2xl font-bold mb-2">PingDiff for Windows</h2>
              {loading ? (
                <div className="flex items-center gap-2 text-zinc-400 mb-4">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Loading version info...</span>
                </div>
              ) : (
                <p className="text-zinc-400 mb-4">
                  {release?.version} • {release?.size} • Windows 10/11
                  {release?.date && <span className="text-zinc-500"> • Released {release.date}</span>}
                </p>
              )}

              <a
                href={release?.downloadUrl || "#"}
                className={`inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-8 py-4 rounded-lg font-semibold text-lg transition ${loading ? 'opacity-50 pointer-events-none' : ''}`}
              >
                <Download className="w-5 h-5" />
                {loading ? "Loading..." : `Download PingDiff-${release?.version}.exe`}
              </a>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
            <Shield className="w-8 h-8 text-green-500 mb-4" />
            <h3 className="font-semibold mb-2">Safe & Open Source</h3>
            <p className="text-zinc-400 text-sm">
              100% open source. No malware, no tracking, no ads. Check the code yourself on GitHub.
            </p>
          </div>

          <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
            <Cpu className="w-8 h-8 text-blue-500 mb-4" />
            <h3 className="font-semibold mb-2">Lightweight</h3>
            <p className="text-zinc-400 text-sm">
              Under 20MB download. Minimal resource usage. No installation required - just run it.
            </p>
          </div>

          <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
            <HardDrive className="w-8 h-8 text-purple-500 mb-4" />
            <h3 className="font-semibold mb-2">Portable</h3>
            <p className="text-zinc-400 text-sm">
              No installation needed. Run from anywhere - USB, desktop, anywhere you want.
            </p>
          </div>
        </div>

        {/* System Requirements */}
        <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6 mb-12">
          <h3 className="text-xl font-semibold mb-4">System Requirements</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="text-zinc-300">Windows 10 or Windows 11</span>
            </div>
            <div className="flex items-center gap-3">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="text-zinc-300">Internet connection</span>
            </div>
            <div className="flex items-center gap-3">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="text-zinc-300">50MB free disk space</span>
            </div>
            <div className="flex items-center gap-3">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="text-zinc-300">Administrator not required</span>
            </div>
          </div>
        </div>

        {/* Other Platforms */}
        <div className="text-center">
          <h3 className="text-xl font-semibold mb-4">Other Platforms</h3>
          <p className="text-zinc-400 mb-6">
            Mac and Linux versions coming soon. Want to be notified?
          </p>
          <div className="flex justify-center gap-4">
            <span className="bg-zinc-800 text-zinc-500 px-4 py-2 rounded-lg">
              macOS - Coming Soon
            </span>
            <span className="bg-zinc-800 text-zinc-500 px-4 py-2 rounded-lg">
              Linux - Coming Soon
            </span>
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-16">
          <h3 className="text-xl font-semibold mb-6 text-center">How to Use</h3>
          <div className="grid md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
                1
              </div>
              <p className="text-sm text-zinc-400">Download PingDiff</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
                2
              </div>
              <p className="text-sm text-zinc-400">Double-click to run</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
                3
              </div>
              <p className="text-sm text-zinc-400">Select your region</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
                4
              </div>
              <p className="text-sm text-zinc-400">Click Test and see results</p>
            </div>
          </div>
        </div>

        {/* All Releases Link */}
        <div className="mt-12 text-center">
          <a
            href="https://github.com/bokiko/pingdiff/releases"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 hover:text-blue-300 transition"
          >
            View all releases on GitHub →
          </a>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-800 py-8 mt-16">
        <div className="max-w-6xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-500" />
            <span className="font-semibold">PingDiff</span>
          </div>
          <div className="flex gap-6 text-zinc-400 text-sm">
            <a
              href="https://github.com/bokiko/pingdiff"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition"
            >
              GitHub
            </a>
            <a
              href="https://github.com/bokiko/pingdiff/issues"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition"
            >
              Report Issue
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
