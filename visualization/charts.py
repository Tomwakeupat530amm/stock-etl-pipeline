import os

import matplotlib

matplotlib.use("Agg")  # headless (Docker / Airflow)

import matplotlib.pyplot as plt
import seaborn as sns

from src.config import CHART_OUTPUT_DIR


def _save(fig, symbol: str, name: str) -> None:
    out_dir = os.path.join(CHART_OUTPUT_DIR, symbol)
    os.makedirs(out_dir, exist_ok=True)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, f"{name}.png"), dpi=120)
    plt.close(fig)


def create_closing_price_chart(df, symbol):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["date"], df["close_price"], color="tab:blue", linewidth=2)
    ax.set(title=f"{symbol} Closing Price", xlabel="Date", ylabel="Price ($)")
    ax.grid(True)
    _save(fig, symbol, "closing_price")


def create_volume_chart(df, symbol):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df["date"], df["volume"], color="tab:green")
    ax.set(title=f"{symbol} Daily Trading Volume", xlabel="Date", ylabel="Volume")
    ax.grid(axis="y")
    _save(fig, symbol, "volume")


def create_moving_average_chart(df, symbol):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["date"], df["close_price"], label="Close", color="tab:blue")
    ax.plot(df["date"], df["ma20"], label="20-day MA", color="tab:red", linewidth=2.5)
    ax.set(title=f"{symbol} Close vs 20-Day Moving Average", xlabel="Date", ylabel="Price ($)")
    ax.legend()
    ax.grid(True)
    _save(fig, symbol, "moving_average")


def create_returns_histogram(df, symbol):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["daily_return"].dropna(), bins=25, color="skyblue", edgecolor="black")
    ax.set(title=f"{symbol} Distribution of Daily Returns", xlabel="Daily return (%)", ylabel="Frequency")
    ax.grid(True)
    _save(fig, symbol, "returns_histogram")


def create_boxplot(df, symbol):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.boxplot(df["close_price"])
    ax.set(title=f"{symbol} Closing Price Box Plot", ylabel="Price ($)")
    ax.grid(True)
    _save(fig, symbol, "boxplot")


def create_correlation_heatmap(df, symbol):
    cols = ["open_price", "high_price", "low_price", "close_price", "volume", "daily_return"]
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df[cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title(f"{symbol} Correlation Heatmap")
    _save(fig, symbol, "correlation_heatmap")


def generate_all_charts(df, symbol):
    for fn in (
        create_closing_price_chart,
        create_volume_chart,
        create_moving_average_chart,
        create_returns_histogram,
        create_boxplot,
        create_correlation_heatmap,
    ):
        fn(df, symbol)
