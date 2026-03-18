# PingDiff Improvement Log

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
