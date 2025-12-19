import type { Metadata } from "next";
import { Inter } from "next/font/google";
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
  keywords: ["ping test", "overwatch 2", "gaming", "latency", "packet loss", "server ping", "connection test", "jitter"],
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
  },
  twitter: {
    card: "summary_large_image",
    title: "PingDiff - Know Your Connection Before You Queue",
    description: "Test your ping to game servers without launching the game.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} antialiased bg-zinc-950 text-white min-h-screen`}>
        {children}
      </body>
    </html>
  );
}
