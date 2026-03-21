"use client";

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import {
  Download,
  Clock,
  Server,
  Wifi,
  TrendingDown,
  AlertTriangle,
  RefreshCw,
  AlertCircle,
  FileDown,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { DashboardSkeleton } from "@/components/DashboardSkeleton";
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

type DateRange = "7" | "30" | "90" | "all";

const DATE_RANGE_OPTIONS: { value: DateRange; label: string }[] = [
  { value: "7", label: "Last 7 days" },
  { value: "30", label: "Last 30 days" },
  { value: "90", label: "Last 90 days" },
  { value: "all", label: "All time" },
];

function exportToCSV(results: TestResult[]) {
  const headers = [
    "Date",
    "Server",
    "Region",
    "Avg Ping (ms)",
    "Min Ping (ms)",
    "Max Ping (ms)",
    "Jitter (ms)",
    "Packet Loss (%)",
    "ISP",
    "Country",
    "City",
  ];

  const rows = results.map((r) => [
    new Date(r.created_at).toISOString(),
    r.game_servers?.location ?? "Unknown",
    r.game_servers?.region ?? "",
    r.ping_avg,
    r.ping_min,
    r.ping_max,
    r.jitter?.toFixed(2) ?? "0",
    r.packet_loss,
    r.isp ?? "Unknown",
    r.country ?? "",
    r.city ?? "",
  ]);

  const csvContent = [headers, ...rows]
    .map((row) =>
      row
        .map((cell) => {
          const str = String(cell);
          // Wrap in quotes if contains comma, quote, or newline
          if (str.includes(",") || str.includes('"') || str.includes("\n")) {
            return `"${str.replace(/"/g, '""')}"`;
          }
          return str;
        })
        .join(",")
    )
    .join("\n");

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `pingdiff-results-${new Date().toISOString().slice(0, 10)}.csv`;
  link.click();
  URL.revokeObjectURL(url);
}

export default function DashboardClient() {
  const [results, setResults] = useState<TestResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRegion, setSelectedRegion] = useState<string>("all");
  const [dateRange, setDateRange] = useState<DateRange>("30");

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/results?limit=100");
      if (!response.ok) {
        throw new Error(`Failed to load results (${response.status})`);
      }
      const data = await response.json();
      setResults(data);
    } catch (err) {
      console.error("Failed to fetch results:", err);
      setError(err instanceof Error ? err.message : "Failed to load results. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Apply date range filter
  const applyDateFilter = useCallback(
    (data: TestResult[]): TestResult[] => {
      if (dateRange === "all") return data;
      const cutoff = new Date();
      cutoff.setDate(cutoff.getDate() - parseInt(dateRange));
      return data.filter((r) => new Date(r.created_at) >= cutoff);
    },
    [dateRange]
  );

  // Apply region filter on top of date filter
  const dateFiltered = applyDateFilter(results);
  const filteredResults =
    selectedRegion === "all"
      ? dateFiltered
      : dateFiltered.filter((r) => r.game_servers?.region === selectedRegion);

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

  // Get unique regions (from all results, not filtered)
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
      <a href="#main-content" className="skip-to-content focus-ring">
        Skip to main content
      </a>
      <Navbar />

      {/* Main Content */}
      <main id="main-content" className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold">Dashboard</h1>
            <p className="text-zinc-400">Your connection test results</p>
          </div>

          {/* Filters */}
          <div className="flex flex-wrap items-center gap-2">
            {/* Date range filter */}
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value as DateRange)}
              className="bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-sm focus-ring"
              aria-label="Filter results by date range"
            >
              {DATE_RANGE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>

            {/* Region filter */}
            <select
              id="region-filter"
              value={selectedRegion}
              onChange={(e) => setSelectedRegion(e.target.value)}
              className="bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-sm focus-ring"
              aria-label="Filter results by region"
            >
              <option value="all">All Regions</option>
              {regions.map((region) => (
                <option key={region} value={region}>
                  {region}
                </option>
              ))}
            </select>

            {/* Export CSV button */}
            {filteredResults.length > 0 && (
              <button
                onClick={() => exportToCSV(filteredResults)}
                className="inline-flex items-center gap-2 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 px-3 py-2 rounded-lg text-sm font-medium transition focus-ring"
                aria-label={`Export ${filteredResults.length} results to CSV`}
                title="Export filtered results as CSV"
              >
                <FileDown className="w-4 h-4" />
                Export CSV
              </button>
            )}

            {/* Refresh */}
            <button
              onClick={fetchResults}
              disabled={loading}
              className="inline-flex items-center gap-2 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 px-3 py-2 rounded-lg text-sm font-medium transition focus-ring disabled:opacity-50"
              aria-label="Refresh results"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
              Refresh
            </button>
          </div>
        </div>

        {loading ? (
          <DashboardSkeleton />
        ) : error ? (
          <div className="text-center py-20">
            <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">Failed to Load Results</h2>
            <p className="text-zinc-400 mb-6">{error}</p>
            <button
              onClick={fetchResults}
              className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-medium transition"
            >
              <RefreshCw className="w-5 h-5" />
              Try Again
            </button>
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
        ) : filteredResults.length === 0 ? (
          <div className="text-center py-20">
            <Clock className="w-16 h-16 text-zinc-600 mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">No Results in This Range</h2>
            <p className="text-zinc-400 mb-6">
              No tests found for the selected filters. Try a wider date range or different region.
            </p>
            <button
              onClick={() => { setDateRange("all"); setSelectedRegion("all"); }}
              className="inline-flex items-center gap-2 bg-zinc-700 hover:bg-zinc-600 px-6 py-3 rounded-lg font-medium transition"
            >
              Clear Filters
            </button>
          </div>
        ) : (
          <>
            {/* Stats Cards */}
            <div
              className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
              role="region"
              aria-label="Connection statistics summary"
            >
              <div
                className="bg-zinc-900 border border-zinc-800 rounded-xl p-6"
                aria-label={`Average ping: ${avgPing} milliseconds — ${getQualityLabel(avgPing)}`}
              >
                <div className="flex items-center gap-3 mb-2">
                  <Wifi className="w-5 h-5 text-blue-500" aria-hidden="true" />
                  <span className="text-zinc-400 text-sm">Average Ping</span>
                </div>
                <div className={`text-3xl font-bold ${getQualityColor(avgPing)}`} aria-hidden="true">
                  {avgPing}ms
                </div>
                <div className="text-sm text-zinc-500">
                  {getQualityLabel(avgPing)}
                </div>
              </div>

              <div
                className="bg-zinc-900 border border-zinc-800 rounded-xl p-6"
                aria-label={`Average packet loss: ${avgPacketLoss} percent — ${parseFloat(avgPacketLoss) === 0 ? "No loss" : "Some loss"}`}
              >
                <div className="flex items-center gap-3 mb-2">
                  <AlertTriangle className="w-5 h-5 text-orange-500" aria-hidden="true" />
                  <span className="text-zinc-400 text-sm">Packet Loss</span>
                </div>
                <div
                  className={`text-3xl font-bold ${
                    parseFloat(avgPacketLoss) === 0
                      ? "text-green-500"
                      : "text-orange-500"
                  }`}
                  aria-hidden="true"
                >
                  {avgPacketLoss}%
                </div>
                <div className="text-sm text-zinc-500">
                  {parseFloat(avgPacketLoss) === 0 ? "No loss" : "Some loss"}
                </div>
              </div>

              <div
                className="bg-zinc-900 border border-zinc-800 rounded-xl p-6"
                aria-label={`Average jitter: ${avgJitter} milliseconds`}
              >
                <div className="flex items-center gap-3 mb-2">
                  <TrendingDown className="w-5 h-5 text-purple-500" aria-hidden="true" />
                  <span className="text-zinc-400 text-sm">Jitter</span>
                </div>
                <div className="text-3xl font-bold text-purple-500" aria-hidden="true">
                  {avgJitter}ms
                </div>
                <div className="text-sm text-zinc-500">Variation</div>
              </div>

              <div
                className="bg-zinc-900 border border-zinc-800 rounded-xl p-6"
                aria-label={`Total tests run: ${filteredResults.length}`}
              >
                <div className="flex items-center gap-3 mb-2">
                  <Clock className="w-5 h-5 text-green-500" aria-hidden="true" />
                  <span className="text-zinc-400 text-sm">Tests Run</span>
                </div>
                <div className="text-3xl font-bold text-green-500" aria-hidden="true">
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
                <div className="h-64" role="img" aria-label={`Line chart showing ping history across ${chartData.length} recent tests. Latest ping: ${chartData.at(-1)?.ping ?? 0}ms`}>
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
                <div className="h-64" role="img" aria-label={`Bar chart comparing average ping across ${serverChartData.length} servers. Best server: ${serverChartData[0]?.name ?? "N/A"} at ${serverChartData[0]?.ping ?? 0}ms`}>
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
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">Recent Tests</h3>
                <span className="text-sm text-zinc-500">
                  Showing {Math.min(filteredResults.length, 10)} of {filteredResults.length}
                </span>
              </div>
              <div className="overflow-x-auto">
                <table
                  className="w-full"
                  aria-label={`Recent test results — showing ${Math.min(filteredResults.length, 10)} of ${filteredResults.length}`}
                >
                  <thead>
                    <tr className="text-left text-zinc-400 text-sm">
                      <th scope="col" className="pb-4 font-medium">Server</th>
                      <th scope="col" className="pb-4 font-medium">Ping</th>
                      <th scope="col" className="pb-4 font-medium">Jitter</th>
                      <th scope="col" className="pb-4 font-medium">Loss</th>
                      <th scope="col" className="pb-4 font-medium">ISP</th>
                      <th scope="col" className="pb-4 font-medium">Time</th>
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
                          className={`py-4 font-semibold ${getQualityColor(result.ping_avg)}`}
                          aria-label={`${result.ping_avg} milliseconds — ${getQualityLabel(result.ping_avg)}`}
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
                          aria-label={`${result.packet_loss} percent packet loss${result.packet_loss === 0 ? " — no loss" : ""}`}
                        >
                          {result.packet_loss}%
                        </td>
                        <td className="py-4 text-zinc-400">
                          {result.isp || "Unknown"}
                        </td>
                        <td className="py-4 text-zinc-500 text-sm">
                          <time dateTime={result.created_at}>
                            {new Date(result.created_at).toLocaleDateString()}
                          </time>
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

      <Footer />
    </div>
  );
}
