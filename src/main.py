"""
    (c) 2026 by 🛸 Dashgrid.com
    Submit birth statistics data to Dashgrid Data Buckets API.

"""
import requests
from pathlib import Path
from helpers import read_csv
from config import API_KEY, BUCKET_1_ID, BUCKET_2_ID, BUCKET_3_ID, BUCKET_4_ID


API_BASE = "https://api.dashgrid.io"
DATA_DIR = Path(__file__).parent / "data"


def submit_chart1():
    """
    Chart 1: Annual Live Births By Sex
    Source: 1-chart-data.csv (DESTATIS 12612-0001)
    Processing: Direct mapping, no transformation
      - sk1: Male births (absolute count)
      - sk2: Female births (absolute count)
    """
    if (not BUCKET_1_ID):
        print("Bucket 1 not configured")

    df = read_csv(DATA_DIR / "1-chart-data.csv", skip_rows=1)
    # CSV columns: Year, Male, e, Female, e, Total, e

    print("Chart 1: Submitting births by sex...")
    records = []
    for _, row in df.iterrows():
        records.append({
            # Keys must be strings
            "k": str(row[0]),
            "d": [
                {"sk": 1, "v": int(row[1])},  # Male
                {"sk": 2, "v": int(row[2])}   # Female
            ]
        })

    # POST to Dashgrid API
    resp = requests.post(
        f"{API_BASE}/api/buckets/{BUCKET_1_ID}",
        json=records,
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"}
    )
    resp.raise_for_status()
    print(f"  Submitted {len(records)} records")


def submit_chart2():
    """
    Chart 2: Births per 1000 Women by Age Group
    Source: 2-chart-data.csv (DESTATIS 12612-0008)
    Processing: Grouped 35 individual ages (15-49) into 7 age brackets (5-year), averaged
      - sk1: 15-19, sk2: 20-24, sk3: 25-29, sk4: 30-34, sk5: 35-39, sk6: 40-44, sk7: 45+
    """
    if (not BUCKET_2_ID):
        print("Bucket 2 not configured")
        return False

    print("Chart 2: Submitting births per 1000 women by age group...")
    df = read_csv(DATA_DIR / "2-chart-data.csv")
    # CSV: Row 0 has years, rows 1-35 have ages 15-49

    years = [str(int(y)) for y in df.iloc[0, 1:]]

    # 5-year age groups, averaged to keep "per 1000 women" meaning
    records = []
    for i, year in enumerate(years):
        col = i + 1
        age_15_19 = df.iloc[1:6, col].astype(float).mean()
        age_20_24 = df.iloc[6:11, col].astype(float).mean()
        age_25_29 = df.iloc[11:16, col].astype(float).mean()
        age_30_34 = df.iloc[16:21, col].astype(float).mean()
        age_35_39 = df.iloc[21:26, col].astype(float).mean()
        age_40_44 = df.iloc[26:31, col].astype(float).mean()
        age_45_plus = df.iloc[31:36, col].astype(float).mean()
        records.append({
            "k": year,
            "d": [
                {"sk": 1, "v": float(round(age_15_19, 1))},
                {"sk": 2, "v": float(round(age_20_24, 1))},
                {"sk": 3, "v": float(round(age_25_29, 1))},
                {"sk": 4, "v": float(round(age_30_34, 1))},
                {"sk": 5, "v": float(round(age_35_39, 1))},
                {"sk": 6, "v": float(round(age_40_44, 1))},
                {"sk": 7, "v": float(round(age_45_plus, 1))}
            ]
        })

    # POST to Dashgrid API
    resp = requests.post(
        f"{API_BASE}/api/buckets/{BUCKET_2_ID}",
        json=records,
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"}
    )
    resp.raise_for_status()
    print(f"  Submitted {len(records)} records")


def submit_chart3():
    """
    Chart 3: Stillbirths (sum of all states)
    Source: 3-chart-data.csv (DESTATIS BEV032)
    Processing: Summed all 16 German states into one total per year
      - sk1: Total stillbirths (absolute count)
    """
    if (not BUCKET_3_ID):
        print("Bucket 3 not configured")
        return False

    print("Chart 3: Submitting stillbirths...")
    df = read_csv(DATA_DIR / "3-chart-data.csv")
    # CSV: Row 0 is header (Bundesland;1990;1991;...), rows 1-16 are states

    years = [str(int(y)) for y in df.iloc[0, 1:]]

    records = []
    for i, year in enumerate(years):
        col = i + 1
        total = int(df.iloc[1:17, col].astype(int).sum())  # Sum all 16 states
        records.append({"k": year, "d": [{"sk": 1, "v": total}]})

    # POST to Dashgrid API
    resp = requests.post(
        f"{API_BASE}/api/buckets/{BUCKET_3_ID}",
        json=records,
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"}
    )
    resp.raise_for_status()
    print(f"  Submitted {len(records)} records")


def submit_chart4():
    """
    Chart 4: Fertility Rate
    Source: 4-chart-data.csv (DESTATIS 12612-0009)
    Processing: Averaged two rate columns (15-44 and 15-49 age ranges)
      - sk1: Average fertility rate (children per woman)
    """
    if (not BUCKET_4_ID):
        print("Bucket 4 not configured")
        return False

    print("Chart 4: Submitting fertility rate...")
    df = read_csv(DATA_DIR / "4-chart-data.csv", skip_rows=1)
    # CSV columns: Year, Age 15-45, Age 15-49

    records = []
    for _, row in df.iterrows():
        year = str(int(row[0]))
        avg_rate = (float(row[1]) + float(row[2])) / 2
        records.append({
            "k": year,
            "d": [{"sk": 1, "v": round(avg_rate, 3)}]
        })

    # POST to Dashgrid API
    resp = requests.post(
        f"{API_BASE}/api/buckets/{BUCKET_4_ID}",
        json=records,
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"}
    )
    resp.raise_for_status()
    print(f"  Submitted {len(records)} records")


if __name__ == "__main__":
    submit_chart1()
    submit_chart2()
    submit_chart3()
    submit_chart4()
    print("Done!")
