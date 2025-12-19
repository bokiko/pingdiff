<div align="center">

<img src=".github/banner.svg" alt="PingDiff Banner" width="100%"/>

<br/>
<br/>

[![GitHub release](https://img.shields.io/github/v/release/bokiko/pingdiff?style=for-the-badge&logo=github&color=3b82f6)](https://github.com/bokiko/pingdiff/releases/latest)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Website](https://img.shields.io/badge/website-pingdiff.com-blue?style=for-the-badge&logo=vercel)](https://pingdiff.com)
[![Downloads](https://img.shields.io/github/downloads/bokiko/pingdiff/total?style=for-the-badge&logo=windows&color=22c55e)](https://github.com/bokiko/pingdiff/releases)

**Test your ping, packet loss, and jitter to game servers before you queue.**

[Download](https://pingdiff.com/download) • [Dashboard](https://pingdiff.com/dashboard) • [Report Bug](https://github.com/bokiko/pingdiff/issues)

</div>

---

## About

PingDiff is a lightweight desktop app that tests your connection to game servers **before** you launch the game. Know exactly which server will give you the best ping, see your ISP's performance compared to others, and get recommendations based on real player data.

### Why PingDiff?

- 🎮 **Pre-Game Testing** - Test servers without launching the game
- 📊 **Real Data** - ICMP ping tests to actual game server IPs
- 🌍 **ISP Intelligence** - See how your ISP compares to others
- 🔒 **Privacy First** - Optional anonymous data sharing
- ⚡ **Lightweight** - Under 20MB, minimal resource usage

---

## Screenshots

<div align="center">
<table>
<tr>
<td align="center"><b>Desktop App</b></td>
<td align="center"><b>Web Dashboard</b></td>
</tr>
<tr>
<td><img src="https://via.placeholder.com/400x500/1c1c1e/3b82f6?text=Desktop+App" alt="Desktop App" width="400"/></td>
<td><img src="https://via.placeholder.com/400x500/0a0a0a/3b82f6?text=Web+Dashboard" alt="Dashboard" width="400"/></td>
</tr>
</table>
</div>

---

## Quick Start

### Download & Install

1. **Download** the latest installer from [Releases](https://github.com/bokiko/pingdiff/releases/latest)
2. **Run** `PingDiff-Setup-x.x.x.exe`
3. **Launch** PingDiff from your Start Menu

### Usage

1. Select your **region** (EU, NA, ASIA, SA, ME)
2. Click **Start Test**
3. View your results and find the **recommended server**
4. Check the [dashboard](https://pingdiff.com/dashboard) for historical data

---

## Supported Games

| Game | Status | Servers |
|:-----|:------:|:-------:|
| 🎮 Overwatch 2 | ✅ Active | 13 |
| 🎯 Valorant | 🔜 Coming Soon | - |
| 💥 Counter-Strike 2 | 🔜 Coming Soon | - |
| 🚀 Apex Legends | 🔜 Coming Soon | - |

---

## Server Regions

| Region | Locations |
|:-------|:----------|
| 🇪🇺 **EU** | Amsterdam, Paris, Frankfurt |
| 🇺🇸 **NA** | Los Angeles, Chicago, New York |
| 🌏 **ASIA** | Singapore, Seoul, Tokyo, Taiwan, Sydney |
| 🇧🇷 **SA** | São Paulo |
| 🇦🇪 **ME** | Bahrain, Dubai |

---

## Tech Stack

<div align="center">

| Component | Technology |
|:----------|:-----------|
| **Website** | Next.js 16, Tailwind CSS, TypeScript |
| **Database** | Supabase (PostgreSQL) |
| **Desktop App** | Python, tkinter |
| **Installer** | Inno Setup |
| **Hosting** | Vercel |
| **CI/CD** | GitHub Actions |

</div>

---

## Development

### Prerequisites

- Node.js 18+
- Python 3.9+
- Git

### Website

```bash
# Clone the repo
git clone https://github.com/bokiko/pingdiff.git
cd pingdiff/web

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Add your Supabase credentials

# Start dev server
npm run dev
```

### Desktop App

```bash
cd pingdiff/desktop

# Install dependencies
pip install -r requirements.txt

# Run the app
python src/main.py

# Build installer (Windows only)
python build.py
```

---

## Project Structure

```
pingdiff/
├── web/                      # Next.js website
│   ├── src/app/              # App router pages
│   │   ├── api/              # API routes
│   │   ├── dashboard/        # Dashboard page
│   │   └── download/         # Download page
│   └── package.json
│
├── desktop/                  # Windows desktop app
│   ├── src/
│   │   ├── main.py           # Entry point
│   │   ├── gui.py            # UI (Apple-inspired design)
│   │   ├── ping_tester.py    # ICMP ping logic
│   │   ├── api_client.py     # API client + settings
│   │   └── config.py         # Servers & colors
│   ├── installer.iss         # Inno Setup script
│   └── requirements.txt
│
├── .github/
│   └── workflows/            # CI/CD
│
└── README.md
```

---

## Features

### Desktop App (v1.7.0)

- 🎨 **Apple-inspired UI** - Modern, clean design
- 🔄 **Auto ISP Detection** - Detects your ISP and location
- 📊 **Real-time Progress** - Circular progress indicator
- ⚙️ **Settings** - Toggle anonymous data sharing
- 📁 **Local Logs** - Stored in `%APPDATA%\PingDiff`
- 🔧 **Proper Installer** - Start Menu shortcuts, clean updates

### Web Dashboard

- 📈 **Test History** - View all your past results
- 🏆 **Best Server** - See recommended servers
- 🌐 **Community Data** - Compare with other players
- 📱 **Responsive** - Works on all devices

---

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Blizzard Entertainment (Overwatch 2 is a trademark)
- The gaming community for server IP contributions
- All contributors and testers

---

<div align="center">

**[pingdiff.com](https://pingdiff.com)**

Made with ❤️ for gamers who hate lag

<br/>

<sub>If this project helped you, consider giving it a ⭐</sub>

</div>
