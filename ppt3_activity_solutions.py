"""PPT 3 — Data Visualization Activity: completed chart solutions.

Place apple_products_pricing_2020_2026.csv beside this file, then run:
    python ppt3_activity_solutions.py

Requires: pandas, numpy, matplotlib
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = Path(__file__).with_name("apple_products_pricing_2020_2026.csv")
REQUIRED = {
    "Date", "Platform", "Product_Category", "Current_Price_USD",
    "Rating", "Reviews_Count",
}
CATEGORY_COLORS = {
    "iPhone": "#4C72B0", "Mac": "#DD8452",
    "Watch": "#55A868", "iPad": "#C44E52",
}


def load_data(path: Path = DATA_FILE) -> pd.DataFrame:
    """Load and validate the pricing history dataset."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}. Keep the CSV beside this script."
        )
    frame = pd.read_csv(path, parse_dates=["Date"])
    missing = REQUIRED.difference(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError("Dataset contains no rows.")
    return frame


def task_2_category_bar(df: pd.DataFrame) -> pd.Series:
    """Average price by category; horizontal bars always start at zero."""
    averages = (
        df.groupby("Product_Category", observed=True)["Current_Price_USD"]
        .mean()
        .sort_values()
    )
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.barh(averages.index, averages.values, color="#4C72B0")
    ax.set_xlim(left=0)
    ax.set_xlabel("Average Current Price (USD)")
    ax.set_title("Average Current Price by Product Category")
    ax.bar_label(bars, fmt="$%.0f", padding=4)
    ax.grid(axis="x", alpha=0.2)
    ax.set_axisbelow(True)
    fig.tight_layout()
    return averages


def task_3_monthly_trend(
    df: pd.DataFrame, categories=("iPhone", "Watch", "Mac")
) -> None:
    """Plot monthly mean price with direct labels at each line's endpoint."""
    fig, ax = plt.subplots(figsize=(9, 5))
    for category in categories:
        monthly = (
            df.loc[df["Product_Category"].eq(category)]
            .set_index("Date")["Current_Price_USD"]
            .resample("MS")
            .mean()
            .dropna()
        )
        if monthly.empty:
            continue
        ax.plot(monthly.index, monthly.values, linewidth=1.8)
        ax.annotate(
            category,
            xy=(monthly.index[-1], monthly.iloc[-1]),
            xytext=(7, 0),
            textcoords="offset points",
            va="center",
            fontsize=9,
            fontweight="bold",
        )
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Current Price (USD)")
    ax.set_title("Monthly Average Price Trend by Product Category")
    ax.grid(alpha=0.2)
    ax.margins(x=0.12)
    fig.tight_layout()


def task_4_bubble_chart(df: pd.DataFrame, sample_size=2000) -> None:
    """Rating vs price; bubble area represents reviews; color represents category."""
    sample = df.sample(n=min(sample_size, len(df)), random_state=1)
    max_reviews = max(float(sample["Reviews_Count"].max()), 1.0)
    fig, ax = plt.subplots(figsize=(9, 6))
    for category, color in CATEGORY_COLORS.items():
        subset = sample.loc[sample["Product_Category"].eq(category)]
        if subset.empty:
            continue
        # Bubble area (not radius) changes continuously with review volume.
        sizes = 20 + 260 * (
            subset["Reviews_Count"].clip(lower=0) / max_reviews
        )
        ax.scatter(
            subset["Rating"], subset["Current_Price_USD"],
            s=sizes, color=color, alpha=0.45,
            edgecolor="white", linewidth=0.4, label=category,
        )
    ax.set_xlabel("Customer Rating")
    ax.set_ylabel("Current Price (USD)")
    ax.set_title("Apple Product Price vs. Rating")
    ax.legend(title="Product Category")
    ax.grid(alpha=0.18)
    fig.tight_layout()


def main() -> None:
    df = load_data()
    print(f"Loaded {len(df):,} rows.")
    print("\nAverage current price by category (USD):")
    print(task_2_category_bar(df).round(2).to_string())
    task_3_monthly_trend(df)
    task_4_bubble_chart(df)
    plt.show()


if __name__ == "__main__":
    main()
