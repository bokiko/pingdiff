"use client";

import Link from "next/link";
import { useState } from "react";
import { Activity, Download, Shield, Settings, CheckCircle, Loader2, FolderOpen, Menu, X, AlertCircle } from "lucide-react";
import { useEffect } from "react";

interface ReleaseInfo {
  version: string;
  downloadUrl: string;
  size: string;
  date: string;
  isInstaller: boolean;
}

export default function DownloadPage() {
  const [release, setRelease] = useState<ReleaseInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [usingFallback, setUsingFallback] = useState(false);

  useEffect(() => {
    // Fetch latest release from GitHub API
    fetch("https://api.github.com/repos/bokiko/pingdiff/releases/latest")
      .then(res => {
        if (!res.ok) throw new Error("API error");
        return res.json();
      })
      .then(data => {
        const asset = data.assets?.find((a: { name: string }) => a.name.endsWith('.exe'));
        if (asset) {
          const isInstaller = asset.name.includes('Setup');
          setRelease({
            version: data.tag_name || "v1.7.0",
            downloadUrl: asset.browser_download_url,
            size: `${(asset.size / (1024 * 1024)).toFixed(1)}MB`,
            date: new Date(data.published_at).toLocaleDateString(),
            isInstaller
          });
        } else {
          throw new Error("No exe found");
        }
        setLoading(false);
      })
      .catch(() => {
        // Fallback - still provide download link
        setRelease({
          version: "v1.7.0",
          downloadUrl: "https://github.com/bokiko/pingdiff/releases/latest/download/PingDiff-Setup-1.7.0.exe",
          size: "~20MB",
          date: "",
          isInstaller: true
        });
        setUsingFallback(true);
        setLoading(false);
      });
  }, []);

  const getFileName = () => {
    if (!release) return "PingDiff";
    const version = release.version.replace('v', '');
    return release.isInstaller ? `PingDiff-Setup-${version}.exe` : `PingDiff-${release.version}.exe`;
  };

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
            <Link href="/community" className="text-zinc-400 hover:text-white transition focus-ring rounded-lg px-2 py-1">
              Community
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
              <Link href="/community" className="text-zinc-400 hover:text-white transition py-2" onClick={() => setMobileMenuOpen(false)}>
                Community
              </Link>
            </div>
          </div>
        )}
      </nav>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Download PingDiff</h1>
          <p className="text-zinc-400 text-lg">
            Get the desktop app to test your connection to game servers
          </p>
        </div>

        {/* Fallback Notice */}
        {usingFallback && (
          <div className="bg-yellow-900/20 border border-yellow-700/50 rounded-xl p-4 mb-6 flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-yellow-500 flex-shrink-0" />
            <p className="text-yellow-200 text-sm">
              Couldn&apos;t fetch latest version info. Showing fallback download link.
              Check <a href="https://github.com/bokiko/pingdiff/releases" target="_blank" rel="noopener noreferrer" className="underline hover:text-white">GitHub Releases</a> for the latest version.
            </p>
          </div>
        )}

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
                className={`inline-flex items-center gap-2 btn-primary px-8 py-4 rounded-xl font-semibold text-lg focus-ring ${loading ? 'opacity-50 pointer-events-none' : ''}`}
              >
                <Download className="w-5 h-5" />
                {loading ? "Loading..." : `Download ${getFileName()}`}
              </a>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6 card-hover">
            <div className="w-12 h-12 bg-green-500/20 rounded-xl flex items-center justify-center mb-4">
              <Shield className="w-6 h-6 text-green-500" />
            </div>
            <h3 className="font-semibold mb-2">Safe & Open Source</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">
              100% open source. No malware, no tracking, no ads. Check the code yourself on GitHub.
            </p>
          </div>

          <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6 card-hover">
            <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center mb-4">
              <Settings className="w-6 h-6 text-blue-500" />
            </div>
            <h3 className="font-semibold mb-2">Your Privacy, Your Choice</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Toggle result sharing on or off. Your settings are saved locally and persist across updates.
            </p>
          </div>

          <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6 card-hover">
            <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-4">
              <FolderOpen className="w-6 h-6 text-purple-500" />
            </div>
            <h3 className="font-semibold mb-2">Clean Install & Updates</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Proper Windows installer. Updates automatically clean up old versions while preserving your data.
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
              <span className="text-zinc-300">Admin rights for installation</span>
            </div>
          </div>
        </div>

        {/* Data Storage Info */}
        <div className="bg-blue-950/30 border border-blue-800/50 rounded-xl p-6 mb-12">
          <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
            <FolderOpen className="w-5 h-5 text-blue-400" />
            Where is my data stored?
          </h3>
          <div className="text-zinc-300 text-sm space-y-2">
            <p><span className="text-zinc-400">Program files:</span> <code className="bg-zinc-800 px-2 py-0.5 rounded">C:\Program Files\PingDiff</code></p>
            <p><span className="text-zinc-400">Settings & logs:</span> <code className="bg-zinc-800 px-2 py-0.5 rounded">%APPDATA%\PingDiff</code></p>
            <p className="text-zinc-500 mt-3">Your settings and logs are preserved when you update to a new version.</p>
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
              <p className="text-sm text-zinc-400">Download & run the installer</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
                2
              </div>
              <p className="text-sm text-zinc-400">Launch PingDiff from Start Menu</p>
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
            <span className="text-zinc-500 text-sm">© 2025</span>
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
