import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "PingDiff - Test Your Game Server Connection",
  description: "Test your ping, packet loss, and jitter to game servers before you queue. Know your connection. Win more games.",
  keywords: ["ping test", "overwatch 2", "gaming", "latency", "packet loss", "server ping"],
  openGraph: {
    title: "PingDiff - Know Your Connection Before You Queue",
    description: "Test your ping to game servers without launching the game. Get recommendations based on your ISP.",
    type: "website",
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
