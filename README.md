# PingDiff

> Know Your Connection Before You Queue

Test your ping, packet loss, and jitter to game servers without launching the game. Get personalized recommendations based on your ISP and location.

![PingDiff Screenshot](https://via.placeholder.com/800x400/1a1a2e/3b82f6?text=PingDiff)

## Features

- **Real Ping Tests** - Test actual game server IPs with ICMP ping
- **ISP Intelligence** - See how your ISP performs compared to others
- **Community Tips** - Learn from other players in your region
- **Multi-Game Support** - Starting with Overwatch 2, more games coming
- **Historical Data** - Track your connection quality over time
- **Server Recommendations** - Find the best server for your setup

## Supported Games

| Game | Status |
|------|--------|
| Overwatch 2 | Active |
| Valorant | Coming Soon |
| Counter-Strike 2 | Coming Soon |
| Apex Legends | Coming Soon |

## Quick Start

### For Users

1. **Download** the app from [pingdiff.vercel.app/download](https://pingdiff.vercel.app/download)
2. **Run** the executable (no installation needed)
3. **Select** your region (EU, NA, ASIA)
4. **Test** your connection
5. **View** results on the dashboard

### For Developers

#### Prerequisites

- Node.js 18+
- Python 3.9+
- Supabase account

#### Website Setup

```bash
cd web
npm install
cp .env.example .env.local
# Add your Supabase credentials to .env.local
npm run dev
```

#### Desktop App Setup

```bash
cd desktop
pip install -r requirements.txt
python src/main.py
```

#### Building Windows Executable

```bash
cd desktop
python build.py
# Output: dist/PingDiff.exe
```

## Project Structure

```
pingdiff/
├── web/                    # Next.js website
│   ├── src/
│   │   ├── app/           # App router pages
│   │   │   ├── api/       # API routes
│   │   │   ├── dashboard/ # Dashboard page
│   │   │   └── download/  # Download page
│   │   └── lib/           # Utilities
│   └── package.json
│
├── desktop/                # Windows desktop app
│   ├── src/
│   │   ├── main.py        # Entry point
│   │   ├── gui.py         # Tkinter GUI
│   │   ├── ping_tester.py # Ping logic
│   │   └── api_client.py  # API client
│   └── requirements.txt
│
└── supabase/              # Database
    └── migrations/        # SQL migrations
```

## Database Schema

The database is designed to be multi-game ready:

- `games` - Supported games
- `game_servers` - Server IPs by region
- `profiles` - User profiles
- `test_results` - Ping test results
- `tips` - Community tips
- `comments` - Comments on tips

## Tech Stack

- **Frontend**: Next.js 14, Tailwind CSS, Recharts
- **Backend**: Supabase (PostgreSQL)
- **Desktop**: Python, tkinter, PyInstaller
- **Hosting**: Vercel

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## Adding New Games

To add a new game:

1. Add the game to the `games` table in Supabase
2. Add server IPs to the `game_servers` table
3. Update the desktop app's `config.py` with fallback servers
4. Update the website to show the new game

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Blizzard Entertainment (Overwatch 2 is a trademark)
- The gaming community for server IP contributions

---

Made with love for gamers who hate lag.
