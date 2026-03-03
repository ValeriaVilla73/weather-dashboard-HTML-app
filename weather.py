#!/usr/bin/env python3
"""7-day weather forecast using the Open-Meteo API with a temperature chart."""

import sys
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def geocode(city: str) -> tuple[float, float, str]:
    """Return (latitude, longitude, display_name) for the given city."""
    resp = requests.get(GEOCODING_URL, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=10)
    resp.raise_for_status()
    results = resp.json().get("results")
    if not results:
        print(f"City '{city}' not found. Please try a different name.")
        sys.exit(1)
    r = results[0]
    parts = [r["name"]]
    if r.get("admin1"):
        parts.append(r["admin1"])
    if r.get("country"):
        parts.append(r["country"])
    return r["latitude"], r["longitude"], ", ".join(parts)


def fetch_forecast(lat: float, lon: float) -> dict:
    """Fetch 7-day daily temperature highs and lows."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "timezone": "auto",
        "forecast_days": 7,
        "temperature_unit": "fahrenheit",
    }
    resp = requests.get(FORECAST_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def plot_forecast(data: dict, location_name: str) -> None:
    """Render a chart of daily high/low temperatures."""
    daily = data["daily"]
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in daily["time"]]
    highs = daily["temperature_2m_max"]
    lows = daily["temperature_2m_min"]
    unit = data.get("daily_units", {}).get("temperature_2m_max", "°C")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(dates, highs, marker="o", color="#e05c1a", linewidth=2, label=f"High ({unit})")
    ax.plot(dates, lows, marker="o", color="#2196f3", linewidth=2, label=f"Low ({unit})")
    ax.fill_between(dates, lows, highs, alpha=0.15, color="#9e9e9e")

    # Annotate each point with its value
    for date, high, low in zip(dates, highs, lows):
        ax.annotate(f"{high:.0f}", (date, high), textcoords="offset points", xytext=(0, 8),
                    ha="center", fontsize=9, color="#e05c1a")
        ax.annotate(f"{low:.0f}", (date, low), textcoords="offset points", xytext=(0, -14),
                    ha="center", fontsize=9, color="#2196f3")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%b %d"))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.set_title(f"7-Day Weather Forecast — {location_name}", fontsize=14, fontweight="bold", pad=14)
    ax.set_ylabel(f"Temperature ({unit})")
    ax.legend(loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.margins(x=0.05)
    fig.tight_layout()

    # Also print a simple text summary
    print(f"\n7-Day Forecast for {location_name}\n{'─' * 42}")
    print(f"{'Date':<14} {'High':>8} {'Low':>8}")
    print(f"{'─'*14} {'─'*8} {'─'*8}")
    for date, high, low in zip(dates, highs, lows):
        print(f"{date.strftime('%a, %b %d'):<14} {high:>7.1f}{unit} {low:>7.1f}{unit}")
    print()

    output_path = "weather_forecast.png"
    fig.savefig(output_path, dpi=150)
    print(f"Chart saved to {output_path}")


def main() -> None:
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
    else:
        city = input("Enter city name: ").strip()
    if not city:
        print("No city provided.")
        sys.exit(1)

    print(f"Looking up '{city}'...")
    lat, lon, location_name = geocode(city)
    print(f"Found: {location_name} ({lat:.4f}, {lon:.4f})")
    print("Fetching 7-day forecast...")
    data = fetch_forecast(lat, lon)
    plot_forecast(data, location_name)


if __name__ == "__main__":
    main()
