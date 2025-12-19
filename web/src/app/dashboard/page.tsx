"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import {
  Activity,
  Download,
  Clock,
  Server,
  Wifi,
  TrendingDown,
  AlertTriangle,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

interface TestResult {
  id: string;
  ping_avg: number;
  ping_min: number;
  ping_max: number;
  jitter: number;
  packet_loss: number;
  isp: string;
  country: string;
  city: string;
  created_at: string;
  game_servers: {
    location: string;
    region: string;
  };
}

export default function DashboardPage() {
  const [results, setResults] = useState<TestResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedRegion, setSelectedRegion] = useState<string>("all");

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    try {
      const response = await fetch("/api/results?limit=100");
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      }
    } catch (error) {
      console.error("Failed to fetch results:", error);
    } finally {
      setLoading(false);
    }
  };

  // Calculate stats
  const filteredResults =
    selectedRegion === "all"
      ? results
      : results.filter((r) => r.game_servers?.region === selectedRegion);

  const avgPing =
    filteredResults.length > 0
      ? Math.round(
          filteredResults.reduce((sum, r) => sum + r.ping_avg, 0) /
            filteredResults.length
        )
      : 0;

  const avgPacketLoss =
    filteredResults.length > 0
      ? (
          filteredResults.reduce((sum, r) => sum + r.packet_loss, 0) /
          filteredResults.length
        ).toFixed(1)
      : "0";

  const avgJitter =
    filteredResults.length > 0
      ? (
          filteredResults.reduce((sum, r) => sum + (r.jitter || 0), 0) /
          filteredResults.length
        ).toFixed(1)
      : "0";

  // Get unique regions
  const regions = [
    ...new Set(results.map((r) => r.game_servers?.region).filter(Boolean)),
  ];

  // Prepare chart data
  const chartData = filteredResults.slice(0, 20).reverse().map((r, i) => ({
    name: `Test ${i + 1}`,
    ping: r.ping_avg,
    jitter: r.jitter || 0,
    loss: r.packet_loss,
  }));

  // Server comparison data
  const serverData = filteredResults.reduce((acc, r) => {
    const location = r.game_servers?.location || "Unknown";
    if (!acc[location]) {
      acc[location] = { pings: [], location };
    }
    acc[location].pings.push(r.ping_avg);
    return acc;
  }, {} as Record<string, { pings: number[]; location: string }>);

  const serverChartData = Object.values(serverData)
    .map((s) => ({
      name: s.location.split(" ")[0],
      ping: Math.round(s.pings.reduce((a, b) => a + b, 0) / s.pings.length),
    }))
    .sort((a, b) => a.ping - b.ping);

  const getQualityColor = (ping: number) => {
    if (ping < 30) return "text-green-500";
    if (ping < 60) return "text-green-400";
    if (ping < 100) return "text-yellow-500";
    if (ping < 150) return "text-orange-500";
    return "text-red-500";
  };

  const getQualityLabel = (ping: number) => {
    if (ping < 30) return "Excellent";
    if (ping < 60) return "Good";
    if (ping < 100) return "Fair";
    if (ping < 150) return "Poor";
    return "Bad";
  };

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
            <Link
              href="/dashboard"
              className="text-white font-medium transition"
            >
              Dashboard
            </Link>
            <Link
              href="/community"
              className="text-zinc-400 hover:text-white transition"
            >
              Community
            </Link>
            <Link
              href="/download"
              className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg font-medium transition"
            >
              Download
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold">Dashboard</h1>
            <p className="text-zinc-400">Your connection test results</p>
          </div>

          {/* Region Filter */}
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="bg-zinc-800 border border-zinc-700 rounded-lg px-4 py-2"
          >
            <option value="all">All Regions</option>
            {regions.map((region) => (
              <option key={region} value={region}>
                {region}
              </option>
            ))}
          </select>
        </div>

        {loading ? (
          <div className="text-center py-20">
            <div className="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-zinc-400">Loading results...</p>
          </div>
        ) : results.length === 0 ? (
          <div className="text-center py-20">
            <Server className="w-16 h-16 text-zinc-600 mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">No Results Yet</h2>
            <p className="text-zinc-400 mb-6">
              Download the app and run your first test to see results here.
            </p>
            <Link
              href="/download"
              className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-medium transition"
            >
              <Download className="w-5 h-5" />
              Download PingDiff
            </Link>
          </div>
        ) : (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Wifi className="w-5 h-5 text-blue-500" />
                  <span className="text-zinc-400 text-sm">Average Ping</span>
                </div>
                <div className={`text-3xl font-bold ${getQualityColor(avgPing)}`}>
                  {avgPing}ms
                </div>
                <div className="text-sm text-zinc-500">
                  {getQualityLabel(avgPing)}
                </div>
              </div>

              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <AlertTriangle className="w-5 h-5 text-orange-500" />
                  <span className="text-zinc-400 text-sm">Packet Loss</span>
                </div>
                <div
                  className={`text-3xl font-bold ${
                    parseFloat(avgPacketLoss) === 0
                      ? "text-green-500"
                      : "text-orange-500"
                  }`}
                >
                  {avgPacketLoss}%
                </div>
                <div className="text-sm text-zinc-500">
                  {parseFloat(avgPacketLoss) === 0 ? "No loss" : "Some loss"}
                </div>
              </div>

              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <TrendingDown className="w-5 h-5 text-purple-500" />
                  <span className="text-zinc-400 text-sm">Jitter</span>
                </div>
                <div className="text-3xl font-bold text-purple-500">
                  {avgJitter}ms
                </div>
                <div className="text-sm text-zinc-500">Variation</div>
              </div>

              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Clock className="w-5 h-5 text-green-500" />
                  <span className="text-zinc-400 text-sm">Tests Run</span>
                </div>
                <div className="text-3xl font-bold text-green-500">
                  {filteredResults.length}
                </div>
                <div className="text-sm text-zinc-500">Total tests</div>
              </div>
            </div>

            {/* Charts */}
            <div className="grid md:grid-cols-2 gap-6 mb-8">
              {/* Ping History Chart */}
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-4">Ping History</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                      <XAxis dataKey="name" stroke="#666" fontSize={12} />
                      <YAxis stroke="#666" fontSize={12} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "#1a1a1a",
                          border: "1px solid #333",
                          borderRadius: "8px",
                        }}
                      />
                      <Line
                        type="monotone"
                        dataKey="ping"
                        stroke="#3b82f6"
                        strokeWidth={2}
                        dot={{ fill: "#3b82f6", r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Server Comparison Chart */}
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-4">Server Comparison</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={serverChartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                      <XAxis dataKey="name" stroke="#666" fontSize={12} />
                      <YAxis stroke="#666" fontSize={12} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "#1a1a1a",
                          border: "1px solid #333",
                          borderRadius: "8px",
                        }}
                      />
                      <Bar dataKey="ping" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            {/* Recent Results Table */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-4">Recent Tests</h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="text-left text-zinc-400 text-sm">
                      <th className="pb-4">Server</th>
                      <th className="pb-4">Ping</th>
                      <th className="pb-4">Jitter</th>
                      <th className="pb-4">Loss</th>
                      <th className="pb-4">ISP</th>
                      <th className="pb-4">Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredResults.slice(0, 10).map((result) => (
                      <tr key={result.id} className="border-t border-zinc-800">
                        <td className="py-4">
                          <div className="font-medium">
                            {result.game_servers?.location || "Unknown"}
                          </div>
                          <div className="text-sm text-zinc-500">
                            {result.game_servers?.region}
                          </div>
                        </td>
                        <td
                          className={`py-4 font-semibold ${getQualityColor(
                            result.ping_avg
                          )}`}
                        >
                          {result.ping_avg}ms
                        </td>
                        <td className="py-4 text-zinc-400">
                          {result.jitter?.toFixed(1) || "0"}ms
                        </td>
                        <td
                          className={`py-4 ${
                            result.packet_loss === 0
                              ? "text-green-500"
                              : "text-orange-500"
                          }`}
                        >
                          {result.packet_loss}%
                        </td>
                        <td className="py-4 text-zinc-400">
                          {result.isp || "Unknown"}
                        </td>
                        <td className="py-4 text-zinc-500 text-sm">
                          {new Date(result.created_at).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
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
          </div>
        </div>
      </footer>
    </div>
  );
}
