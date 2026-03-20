import type { Metadata } from "next";
import DashboardClient from "./DashboardClient";

export const metadata: Metadata = {
  title: "Dashboard",
  description: "View your ping test results, packet loss trends, and server comparisons. Analyze your connection history across all game servers.",
  openGraph: {
    title: "PingDiff Dashboard — Your Connection Test Results",
    description: "View your ping test results, packet loss trends, and server comparisons.",
  },
};

export default function DashboardPage() {
  return <DashboardClient />;
}
