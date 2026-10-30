# visualization/charts.py

import os

import matplotlib.pyplot as plt
import seaborn as sns

from src.config import SYMBOL

OUTPUT_DIR = "visualization/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_closing_price_chart(df):
    """
    Creates a line chart for the closing price.

    Parameters
    ----------
    df : pandas.DataFrame
        Transformed stock dataframe.
    """

    plt.figure(figsize=(12, 6))

    plt.plot(
        df["date"],
        df["close_price"],
        color="blue",
        linewidth=2,
        marker="o",
        label=f"{SYMBOL} Closing Price"
    )

    plt.title(f"{SYMBOL} Closing Price")

    plt.xlabel("Date")

    plt.ylabel("Closing Price ($)")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/closing_price.png"
    )

    plt.close()

    print("Closing Price Chart Saved Successfully")

def create_volume_chart(df):
    """
    Creates a bar chart for daily trading volume.
    """

    plt.figure(figsize=(12,6))

    plt.bar(
        df["date"],
        df["volume"],
        color="green"
    )

    plt.title(f"{SYMBOL} Daily Trading Volume")

    plt.xlabel("Date")

    plt.ylabel("Volume")

    plt.grid(axis="y")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/volume_chart.png"
    )

    plt.close()

    print("Volume Chart Saved Successfully")

def create_moving_average_chart(df):
    """
    Creates a chart with Closing Price and 20-Day Moving Average.
    """

    plt.figure(figsize=(12,6))

    ma20 = (
        df["close_price"]
        .rolling(window=20)
        .mean()
    )

    plt.plot(
        df["date"],
        df["close_price"],
        label="Closing Price",
        color="blue"
    )

    plt.plot(
        df["date"],
        ma20,
        label="20-Day Moving Average",
        color="red",
        linewidth=3
    )

    plt.title(f"{SYMBOL} Closing Price vs 20-Day Moving Average")

    plt.xlabel("Date")

    plt.ylabel("Price ($)")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/moving_average.png"
    )

    plt.close()

    print("Moving Average Chart Saved Successfully")

def create_histogram(df):
    """
    Creates histogram of Closing Price.
    """

    plt.figure(figsize=(10,6))

    plt.hist(
        df["close_price"],
        bins=20,
        color="skyblue",
        edgecolor="black"
    )

    plt.title(f"Distribution of {SYMBOL} Closing Prices")

    plt.xlabel("Closing Price")

    plt.ylabel("Frequency")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/histogram.png"
    )

    plt.close()

    print("Histogram Saved Successfully")

def create_boxplot(df):
    """
    Creates box plot for closing prices.
    """

    plt.figure(figsize=(8,6))

    plt.boxplot(df["close_price"])

    plt.title(f"{SYMBOL} Closing Price Box Plot")

    plt.ylabel("Closing Price ($)")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/boxplot.png"
    )

    plt.close()

    print("Box Plot Saved Successfully")

def create_correlation_heatmap(df):
    """
    Creates correlation heatmap.
    """

    plt.figure(figsize=(8,6))

    correlation = df.corr(numeric_only=True)

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5
    )

    plt.title(f"{SYMBOL} Correlation Heatmap")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/correlation_heatmap.png"
    )

    plt.close()

    print("Correlation Heatmap Saved Successfully")