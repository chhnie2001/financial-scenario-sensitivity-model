import requests
import pandas as pd
import numpy as np
from pathlib import Path

CIK = "0001158114"

HEADERS = {
    "User-Agent": "financial-scenario-sensitivity-model chhnie2001@gmail.com",
    "Accept-Encoding": "gzip, deflate",
    "Host": "data.sec.gov",
}

URL = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json"


def get_companyfacts():
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_annual_usd_facts(companyfacts, taxonomy_tag):
    try:
        facts = companyfacts["facts"]["us-gaap"][taxonomy_tag]["units"]["USD"]
    except KeyError:
        return pd.DataFrame(columns=["year", taxonomy_tag])

    rows = []
    for item in facts:
        fy = item.get("fy")
        form = item.get("form")
        val = item.get("val")

        if fy is not None and form in ("10-K", "10-K/A") and pd.notna(val):
            rows.append(
                {
                    "year": int(fy),
                    taxonomy_tag: float(val),
                    "filed": item.get("filed"),
                }
            )

    if not rows:
        return pd.DataFrame(columns=["year", taxonomy_tag])

    df = pd.DataFrame(rows)
    df = df.sort_values(["year", "filed"]).drop_duplicates(subset=["year"], keep="last")
    return df[["year", taxonomy_tag]]


def get_revenue_from_multiple_tags(companyfacts):
    candidate_tags = [
        "SalesRevenueNet",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
    ]

    frames = []
    for tag in candidate_tags:
        df = extract_annual_usd_facts(companyfacts, tag)
        if not df.empty:
            frames.append(df)
            print(f"Found revenue data for tag: {tag}")

    if not frames:
        return pd.DataFrame(columns=["year", "revenue"])

    merged = frames[0]
    for df in frames[1:]:
        merged = merged.merge(df, on="year", how="outer")

    revenue_cols = [c for c in merged.columns if c != "year"]
    merged["revenue"] = merged[revenue_cols].bfill(axis=1).iloc[:, 0]

    return merged[["year", "revenue"]]


def build_sec_financials(companyfacts):
    revenue_df = get_revenue_from_multiple_tags(companyfacts)

    gross_profit_df = extract_annual_usd_facts(companyfacts, "GrossProfit")
    gross_profit_df = gross_profit_df.rename(columns={"GrossProfit": "gross_profit"})

    net_income_df = extract_annual_usd_facts(companyfacts, "NetIncomeLoss")
    net_income_df = net_income_df.rename(columns={"NetIncomeLoss": "net_income"})

    df = revenue_df.merge(gross_profit_df, on="year", how="outer")
    df = df.merge(net_income_df, on="year", how="outer")

    for col in ["revenue", "gross_profit", "net_income"]:
        if col in df.columns:
            df[col] = df[col] / 1_000_000

    return df


def load_existing_csv(output_path):
    if output_path.exists():
        return pd.read_csv(output_path)
    return pd.DataFrame(columns=["year", "revenue", "gross_profit", "gross_margin", "net_income"])


def safe_merge(existing_df, sec_df):
    """
    Safe rules:
    1. Existing revenue is preserved unless SEC has a real non-null value.
    2. Existing gross_profit / net_income are preserved unless SEC has a real non-null value.
    3. No field is replaced by NaN from SEC.
    """
    df = pd.merge(existing_df, sec_df, on="year", how="outer", suffixes=("_old", "_sec"))

    final = pd.DataFrame()
    final["year"] = df["year"]

    for col in ["revenue", "gross_profit", "net_income"]:
        old_col = f"{col}_old"
        sec_col = f"{col}_sec"

        old_series = df[old_col] if old_col in df.columns else pd.Series(np.nan, index=df.index)
        sec_series = df[sec_col] if sec_col in df.columns else pd.Series(np.nan, index=df.index)

        # only use SEC where SEC is non-null; otherwise keep existing
        final[col] = old_series.where(sec_series.isna(), sec_series)

    final = final.sort_values("year").reset_index(drop=True)

    final["gross_margin"] = np.where(
        final["revenue"].notna() & (final["revenue"] != 0),
        (final["gross_profit"] / final["revenue"]) * 100,
        np.nan,
    )

    final = final[["year", "revenue", "gross_profit", "gross_margin", "net_income"]]

    final = final.round(
        {
            "revenue": 1,
            "gross_profit": 1,
            "gross_margin": 1,
            "net_income": 1,
        }
    )

    return final


def validate_no_destructive_overwrite(existing_df, final_df):
    """
    Prevent writing if final_df introduces MORE missing values
    in key columns than existing_df.
    """
    key_cols = ["revenue", "gross_profit", "net_income"]

    for col in key_cols:
        old_missing = existing_df[col].isna().sum() if col in existing_df.columns else 0
        new_missing = final_df[col].isna().sum() if col in final_df.columns else 0

        if new_missing > old_missing:
            raise ValueError(
                f"Refusing to overwrite file: column '{col}' would gain more missing values "
                f"({old_missing} -> {new_missing})."
            )


def main():
    output_path = Path(__file__).resolve().parent / "aaoi_financials.csv"

    existing_df = load_existing_csv(output_path)
    companyfacts = get_companyfacts()
    sec_df = build_sec_financials(companyfacts)

    final_df = safe_merge(existing_df, sec_df)

    # extra protection
    if not existing_df.empty:
        validate_no_destructive_overwrite(existing_df, final_df)

    final_df.to_csv(output_path, index=False)

    print("\nSaved file to:", output_path)
    print("\nPreview of final financials:")
    print(final_df.tail(15))


if __name__ == "__main__":
    main()