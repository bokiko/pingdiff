/**
 * DashboardSkeleton — shimmer placeholders that mirror the real dashboard layout.
 *
 * Renders four stat cards, two chart panels, and a results table skeleton so the
 * page feels instantly populated while data is in-flight. Uses a CSS animation
 * defined in globals.css (shimmer keyframes) to avoid a runtime dependency.
 */

function SkeletonBlock({ className = "" }: { className?: string }) {
  return (
    <div
      className={`skeleton ${className}`}
      aria-hidden="true"
    />
  );
}

function StatCardSkeleton() {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
      {/* Icon + label row */}
      <div className="flex items-center gap-3 mb-3">
        <SkeletonBlock className="w-5 h-5 rounded-full" />
        <SkeletonBlock className="h-3 w-24" />
      </div>
      {/* Value */}
      <SkeletonBlock className="h-9 w-20 mb-2" />
      {/* Sub-label */}
      <SkeletonBlock className="h-3 w-16" />
    </div>
  );
}

function ChartPanelSkeleton() {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
      {/* Title */}
      <SkeletonBlock className="h-5 w-36 mb-5" />
      {/* Chart area — fake bar/line columns */}
      <div className="h-64 flex items-end gap-2 px-2">
        {[45, 70, 55, 85, 40, 65, 75, 50, 90, 60].map((h, i) => (
          <div
            key={i}
            className="skeleton flex-1 rounded-t"
            style={{ height: `${h}%` }}
            aria-hidden="true"
          />
        ))}
      </div>
    </div>
  );
}

function TableRowSkeleton() {
  return (
    <tr className="border-t border-zinc-800">
      <td className="py-4">
        <SkeletonBlock className="h-4 w-32 mb-1.5" />
        <SkeletonBlock className="h-3 w-16" />
      </td>
      <td className="py-4">
        <SkeletonBlock className="h-4 w-14" />
      </td>
      <td className="py-4">
        <SkeletonBlock className="h-4 w-12" />
      </td>
      <td className="py-4">
        <SkeletonBlock className="h-4 w-10" />
      </td>
      <td className="py-4">
        <SkeletonBlock className="h-4 w-24" />
      </td>
      <td className="py-4">
        <SkeletonBlock className="h-4 w-20" />
      </td>
    </tr>
  );
}

export function DashboardSkeleton() {
  return (
    <div aria-busy="true" aria-label="Loading dashboard data">
      {/* Stat Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[0, 1, 2, 3].map((i) => (
          <StatCardSkeleton key={i} />
        ))}
      </div>

      {/* Charts */}
      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <ChartPanelSkeleton />
        <ChartPanelSkeleton />
      </div>

      {/* Recent Results Table */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
        {/* Table title */}
        <SkeletonBlock className="h-5 w-32 mb-5" />
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-left">
                {["Server", "Ping", "Jitter", "Loss", "ISP", "Time"].map((col) => (
                  <th key={col} className="pb-4">
                    <SkeletonBlock className="h-3 w-14" />
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[0, 1, 2, 3, 4, 5].map((i) => (
                <TableRowSkeleton key={i} />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
