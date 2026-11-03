# PPT3 VDUI

Reviewed solutions for PPT 3 (Data Visualization Unit 1).

## Files

- `ppt3_activity_solutions.py` — completed solutions for Tasks 2–4:
  - zero-baseline horizontal category price chart;
  - monthly category trends with direct end labels;
  - bubble chart encoding rating, current price, review count, and product category.
- `PPT_3/ppt3-activity-solved.ipynb` — the completed notebook version is included in the submission package when available.

## Run

Install dependencies:

```bash
python -m pip install pandas numpy matplotlib
```

Place `apple_products_pricing_2020_2026.csv` in the same directory as the script, then run:

```bash
python ppt3_activity_solutions.py
```

The supplied dataset contains 80,000 rows and 14 columns. The script validates the required fields and fails with a clear message if the CSV is missing or malformed.

## Visualization integrity

- Bar lengths use a zero baseline.
- Time-series data are aggregated to monthly means and shown with connected lines.
- Continuous values use position or bubble area; product category is encoded with color.
- Bubble sizes are scaled to the sample maximum to keep the chart legible.
