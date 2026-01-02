import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { SpeedInsights } from "@vercel/speed-insights/next";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "PingDiff - Test Your Game Server Connection",
    template: "%s | PingDiff",
  },
  description: "Test your ping, packet loss, and jitter to game servers before you queue. Know your connection. Win more games.",
  keywords: ["ping test", "overwatch 2", "call of duty", "warzone", "counter-strike 2", "cs2", "battlefield 6", "bf6", "gaming", "latency", "packet loss", "server ping", "connection test", "jitter"],
  authors: [{ name: "bokiko", url: "https://github.com/bokiko" }],
  creator: "bokiko",
  metadataBase: new URL("https://pingdiff.com"),
  openGraph: {
    title: "PingDiff - Know Your Connection Before You Queue",
    description: "Test your ping to game servers without launching the game. Get recommendations based on your ISP.",
    url: "https://pingdiff.com",
    siteName: "PingDiff",
    locale: "en_US",
    type: "website",
    images: [
      {
        url: "/og-image.svg",
        width: 1200,
        height: 630,
        alt: "PingDiff - Know Your Connection Before You Queue",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "PingDiff - Know Your Connection Before You Queue",
    description: "Test your ping to game servers without launching the game.",
    images: ["/og-image.svg"],
  },
  robots: {
    index: true,
    follow: true,
  },
  other: {
    "google-site-verification": "", // Add your verification code when ready
  },
};

// Structured data for the website
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "PingDiff",
  applicationCategory: "UtilityApplication",
  operatingSystem: "Windows 10, Windows 11",
  description: "Test your ping, packet loss, and jitter to game servers before you queue.",
  url: "https://pingdiff.com",
  downloadUrl: "https://pingdiff.com/download",
  softwareVersion: "1.17.1",
  author: {
    "@type": "Person",
    name: "bokiko",
    url: "https://github.com/bokiko",
  },
  offers: {
    "@type": "Offer",
    price: "0",
    priceCurrency: "USD",
  },
  aggregateRating: {
    "@type": "AggregateRating",
    ratingValue: "5",
    ratingCount: "100",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className={`${inter.className} antialiased bg-zinc-950 text-white min-h-screen`}>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
