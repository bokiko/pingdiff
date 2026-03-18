import type { NextConfig } from "next";

// Content Security Policy — tightened to allow only what PingDiff actually loads.
// Recharts renders SVG inline; no external scripts are needed.
const csp = [
  "default-src 'self'",
  // Next.js uses inline styles and style-src 'unsafe-inline' is currently required for Recharts tooltips
  "style-src 'self' 'unsafe-inline'",
  // Scripts: only same-origin chunks produced by Next.js
  "script-src 'self' 'unsafe-eval'",
  // Fonts served from the same origin
  "font-src 'self'",
  // Images: self + data URIs (used by Recharts)
  "img-src 'self' data:",
  // API calls only go back to the same origin (Supabase calls are server-side)
  "connect-src 'self'",
  // Prevent embedding in frames
  "frame-ancestors 'none'",
  // Disallow plugins (Flash, etc.)
  "object-src 'none'",
  // Upgrade all mixed HTTP requests
  "upgrade-insecure-requests",
].join("; ");

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          {
            key: "Content-Security-Policy",
            value: csp,
          },
          {
            // HSTS: 1 year, include subdomains, allow preload
            key: "Strict-Transport-Security",
            value: "max-age=31536000; includeSubDomains; preload",
          },
          {
            key: "X-DNS-Prefetch-Control",
            value: "on",
          },
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin",
          },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=()",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
