# CONTEXT.md

Context file for AI assistants working on PingDiff.

## ARCHITECTURE

```
pingdiff/
├── desktop/                    # Windows desktop app (Python)
│   ├── src/
│   │   ├── main.py            # Entry point
│   │   ├── gui.py             # tkinter UI (PillButton, GlowingRing, AppleToggle)
│   │   ├── ping_tester.py     # ICMP ping logic (ThreadPoolExecutor)
│   │   ├── api_client.py      # HTTP client + Settings persistence
│   │   └── config.py          # Constants (colors, regions, version)
│   ├── build.py               # PyInstaller build script
│   └── requirements.txt
│
├── web/                        # Next.js web app
│   ├── src/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── servers/route.ts    # GET /api/servers
│   │   │   │   └── results/route.ts    # POST /api/results
│   │   │   ├── dashboard/              # Community stats page
│   │   │   ├── download/               # Desktop app download
│   │   │   └── page.tsx                # Landing page
│   │   └── lib/
│   │       └── supabase.ts             # DB client + types
│   ├── package.json
│   └── .env.example
│
├── supabase/
│   └── migrations/             # SQL migrations for game servers
│
├── .gitlab-ci.yml              # CI/CD (Windows build + release)
├── CLAUDE.md                   # AI assistant instructions
└── CONTEXT.md                  # This file
```

## TECH_STACK

| Category | Technology | Purpose |
|----------|------------|---------|
| **Desktop** | Python 3.11 | Core language |
| | tkinter | GUI framework |
| | pythonping | ICMP ping library |
| | PyInstaller | Exe packaging |
| | Inno Setup | Windows installer |
| **Web** | Next.js 16 | React framework |
| | TypeScript | Type safety |
| | Tailwind CSS | Styling |
| | Zod | Schema validation |
| **Database** | Supabase | PostgreSQL hosting |
| | Row Level Security | Data protection |
| **Hosting** | Vercel | Web app hosting |
| | GitHub Releases | Desktop downloads |
| **CI/CD** | GitLab CI | Build automation |
| **VCS** | Git | Version control |
| | GitHub | Primary repo |
| | GitLab | Mirror (for CI) |

## PROJECT

**Name:** PingDiff

**Website:** www.pingdiff.com

**Description:** Free, open-source game server ping testing tool that helps gamers test ping, packet loss, and jitter to game servers before queuing. Supports 9 games across 141 servers in 8 regions.

**Key Features:**
- Real ICMP ping testing against actual game server IPs
- Multi-region comparison (EU, NA, ASIA) with ranked results
- ISP performance tracking with community data
- 100% open source, no tracking, MIT license

**Stats:**
- 10k+ tests run
- 50+ ISPs tracked
- 8 server regions

**Current Task:** None - project is stable and published

**Potential Future Tasks:**
- Add new game servers
- Improve community dashboard
- Add macOS/Linux desktop support

## STANDARDS

### Code Style

| Language | Standard |
|----------|----------|
| Python | Type hints required, use `dataclasses`, follow PEP 8 |
| TypeScript | Strict mode, Zod for validation, ESLint |
| SQL | Lowercase keywords, UUID primary keys |

### Security

- **IP validation:** Always validate IPs before ping to prevent command injection
- **Rate limiting:** 30 requests/minute on API endpoints
- **RLS:** Row Level Security on all user data tables
- **Anonymous allowed:** test_results accepts NULL user_id

### UI/UX

- **Theme:** Dark mode (zinc-950 background)
- **Components:** Apple-inspired design (PillButton, GlowingRing, AppleToggle)
- **Colors:** Defined in `desktop/src/config.py` COLORS dict

### Git

- **Commits:** Semantic style (feat:, fix:, docs:, etc.)
- **Branches:** main is production
- **Tags:** Version tags `v*` trigger CI builds
- **CI:** GitLab CI builds Windows installer on tag push

### API

- **Validation:** Zod schemas on all inputs
- **Errors:** Return structured JSON errors
- **Rate limit:** 30 req/min per IP

### Database

- **Primary keys:** UUID
- **Migrations:** SQL files in `supabase/migrations/`
- **Naming:** snake_case for tables and columns
