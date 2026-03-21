import type { Metadata } from "next";
import DownloadClient from "./DownloadClient";

export const metadata: Metadata = {
  title: "Download",
  description: "Download PingDiff for Windows — free, open source desktop app to test your ping and packet loss to game servers before you queue.",
  openGraph: {
    title: "Download PingDiff for Windows",
    description: "Free, open source desktop app to test your ping and packet loss to game servers before you queue.",
  },
};

export default function DownloadPage() {
  return <DownloadClient />;
}
