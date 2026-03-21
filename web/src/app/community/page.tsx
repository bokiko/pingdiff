import type { Metadata } from "next";
import CommunityClient from "./CommunityClient";

export const metadata: Metadata = {
  title: "Community",
  description: "Share connection tips, compare ping results with other players, and find the best game servers for your region.",
  openGraph: {
    title: "PingDiff Community Hub",
    description: "Share connection tips, compare ping results with other players, and find the best game servers for your region.",
  },
};

export default function CommunityPage() {
  return <CommunityClient />;
}
