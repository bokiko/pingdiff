# PingDiff Improvement Log

## 2026-03-20 — Accessibility: ARIA labels, table semantics, and skip navigation

Comprehensive a11y pass across the dashboard, navbar, and secondary pages. The site had no named navigation landmark, no skip links on 3 of 4 pages, tables without column scope attributes, charts completely invisible to assistive technology, and stat cards that conveyed quality purely through color (WCAG 1.4.1 violation). All fixed without new dependencies.

Dashboard: skip link + main-content anchor, role="region" on stats grid, aria-label on each stat card with text description, aria-hidden on decorative icons, role="img" + aria-label on both charts, aria-label on table element, scope="col" on all th elements, time element for timestamps, aria-label on ping/loss cells so quality is communicated in text not just color.

Navbar: aria-label="Main navigation" on nav element, aria-haspopup on mobile toggle, role="menu" on mobile menu container.

Community and Download pages: both were missing skip-to-content links and main-content anchor targets entirely.

**Files changed:** `web/src/app/dashboard/page.tsx`, `web/src/components/Navbar.tsx`, `web/src/app/community/page.tsx`, `web/src/app/download/page.tsx`
**Lines:** +64 / -30

## 2026-03-19 — Performance: Memoize dashboard derived state

All derived values on the dashboard (filteredResults, avgPing, avgPacketLoss, avgJitter, regions, chartData, serverChartData) were being recomputed inline on every React render — including renders triggered by unrelated state changes like the loading flag toggling off. Wrapped each value in useMemo with the tightest possible dependency array, eliminating 5 O(n) reduce passes and 2 groupBy passes on every extraneous render. At current scale the savings are modest; at the 500-1000 result range the dashboard would hit without this change the difference is measurable. The memoized structure also makes data dependencies explicit and auditable at a glance.

**Files changed:** `web/src/app/dashboard/page.tsx`
**Lines:** +76 / -56


## 2026-03-19 — New Feature: Date range filter and CSV export for dashboard

Added two practical dashboard improvements with no new dependencies and no API changes.

Date range filter: a dropdown (Last 7 / 30 / 90 days / All time, defaulting to 30 days) applied before the existing region filter. An empty-state UI with a Clear Filters button handles the case where filters return no results.

CSV export: an Export CSV button appears in the filter toolbar whenever filtered results exist. It exports exactly the current view (date + region filters applied) as RFC 4180-compliant CSV with columns for Date, Server, Region, Avg/Min/Max Ping, Jitter, Packet Loss, ISP, Country, and City. Filename includes today's date.

Also: Refresh button moved into the filter toolbar for a consistent row; result count label added to the Recent Tests table header; header layout improved for mobile (stacks vertically below sm breakpoint).

**Files changed:** `web/src/app/dashboard/page.tsx`
**Lines:** +145 / -13

## 2026-03-18 — Security: Harden API routes and add CSP/HSTS headers

`/api/servers` was completely unprotected by rate limiting while `/api/results` already had it — an oversight that left the DB endpoint open to unbounded hammering. The rate-limit and IP-extraction logic was also duplicated inline, meaning the two routes could silently diverge over time. Additionally, `next.config.ts` was missing the two highest-impact HTTP security headers: Content Security Policy and HSTS.

Fixed by extracting a shared `rate-limit.ts` utility (named buckets, consistent IP extraction), applying rate limiting + slug validation to `/api/servers`, adding CDN caching on that endpoint, and adding CSP + HSTS to `next.config.ts`.

**Files changed:** `web/src/lib/rate-limit.ts` (new), `web/src/app/api/results/route.ts`, `web/src/app/api/servers/route.ts`, `web/next.config.ts`
**Lines:** +127 / -35


## 2026-03-18 — Code Quality: Extract shared Navbar and Footer components

The navigation bar and footer were duplicated verbatim across 4 pages (home, dashboard, community,
download), with each page managing its own mobileMenuOpen state and hardcoding its own active link
style. Extracted both into reusable components in web/src/components/.

The new Navbar uses usePathname() for automatic active-link highlighting and a single NAV_LINKS
array as the source of truth for site navigation. Any future nav change (new link, style tweak)
now requires editing one file instead of four.

**Files changed:** `web/src/components/Navbar.tsx` (new), `web/src/components/Footer.tsx` (new),
`web/src/app/page.tsx`, `web/src/app/dashboard/page.tsx`, `web/src/app/community/page.tsx`,
`web/src/app/download/page.tsx`
**Lines:** +157 / -338

## 2026-03-17 — Testing: Unit test suite for CLI and ping core logic

Added a pytest test suite covering the CLI and ping tester modules — the first tests in the project.
Tests are pure unit tests (no network calls, no subprocess invocations), so they run in milliseconds
and work offline. 68 tests across 10 test classes covering:

- `validate_ip`: valid/invalid IPv4, IPv6, hostnames, injection attempts, edge cases
- `calculate_jitter`: empty input, single value, zero jitter, constant increase, alternating, high jitter
- `get_best_server`: empty list, all timeouts, single server, lowest ping, packet loss priority, exclusion logic
- `get_connection_quality`: all 5 quality tiers and boundary values (Excellent/Good/Fair/Poor/Bad)
- `sort_results`: all 5 sort keys, timeout-last ordering, unknown key fallback
- `filter_by_max_ping`: pass-all, block-all, timeout exclusion, inclusive/exclusive boundary
- `results_to_json`: valid JSON output, field correctness, best-only, error case, empty list
- `results_to_csv`: parseable CSV, header row, best-only, empty-on-no-best, multiple rows
- Color helpers: colorize no-color mode, format_ping, format_loss
- `build_parser`: defaults, all flags, region/sort validation, type coercion

**Files changed:** `desktop/tests/__init__.py`, `desktop/tests/test_ping_tester.py`,
`desktop/tests/test_cli.py`, `desktop/pytest.ini`
**Lines:** +370 / -0

## 2026-03-18 — UI/UX: Skeleton loading screen for dashboard

The dashboard previously showed a centered spinner while fetching results from
/api/results, giving no visual indication of page structure and causing a jarring
layout shift when content arrived.

Replaced the spinner with a DashboardSkeleton component that mirrors the real
dashboard layout — four stat cards, two chart panels, and a six-row results table
— all with the existing .skeleton shimmer animation. No new dependencies. Screen
reader support via aria-busy="true" and aria-label on the skeleton root.

**Files changed:** `web/src/components/DashboardSkeleton.tsx` (new), `web/src/app/dashboard/page.tsx`
**Lines:** +123 / -4
