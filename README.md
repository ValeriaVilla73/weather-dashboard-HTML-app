# Weather Dashboard

A 7-day weather forecast app with two interfaces: an interactive web dashboard and a Python CLI script. Both use the [Open-Meteo](https://open-meteo.com/) API — no API key required.

## Features

- Search any city worldwide
- 7-day daily high/low temperature forecast
- Weather condition icons and descriptions (WMO weather codes)
- Precipitation and wind speed details
- Interactive temperature trend chart
- Dynamic sky themes that change based on current conditions (sunny, cloudy, rainy, snowy, stormy)
- Toggle between °F and °C

## Files

| File | Description |
|---|---|
| `weather.html` | Standalone browser app — open directly, no server needed |
| `weather.py` | CLI script — prints a forecast table and saves a chart PNG |

## How to Run

### Web app (recommended)

Just open `weather.html` in any modern browser. No installation required.

### Python CLI

**Requirements:** Python 3.10+

Install dependencies:
```bash
pip install requests matplotlib
```

Run with a city name as an argument:
```bash
python weather.py "New York"
python weather.py Tokyo
```

Or run without arguments to be prompted:
```bash
python weather.py
```

Output: a text table in the terminal and a `weather_forecast.png` chart saved to the current directory.

## Technologies

- **Open-Meteo API** — free weather forecast and geocoding API
- **Chart.js** (web) — interactive temperature trend line chart
- **matplotlib** (CLI) — static forecast chart saved as PNG
- **Vanilla HTML/CSS/JS** — no build tools or frameworks
