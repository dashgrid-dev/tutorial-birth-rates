"""
    (c) 2026 by 🛸 Dashgrid.com
    Submit birth statistics data to Dashgrid Data Buckets API.

"""
import requests
from pathlib import Path
from helpers import read_csv
from config import API_KEY, BUCKET_1_ID, BUCKET_2_ID, BUCKET_3_ID, BUCKET_4_ID


# Dashgrid API base URL
API_BASE = "https://data.dashgrid.com"

# Path to CSV data files
DATA_DIR = Path(__file__).parent / "data"


def submit_chart1():
    """
    Chart 1: Annual Live Births By Sex
    Source: 1-chart-data.csv (DESTATIS 12612-0001)
    Processing: Direct mapping, no transformation
      - sk1: Male births
      - sk2: Female births
    """
    if not BUCKET_1_ID:
        print("Bucket 1 not configured")
        return

    print("Chart 1: Submitting births by sex...")

    # Step 1: Read CSV file, skip header row
    df = read_csv(DATA_DIR / "1-chart-data.csv", skip_rows=1)

    # Step 2: Build records array for API
    # Each record has a key (year) and data array with series values
    records = []
    for _, row in df.iterrows():
        records.append({
            "k": str(int(row[0])),  # Key: year as string
            "d": [
                {"sk": 1, "v": int(row[1])},  # Series 1: Male births
                {"sk": 2, "v": int(row[2])}   # Series 2: Female births
            ]
        })

    # Step 3: POST records to Dashgrid API
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
    if not BUCKET_2_ID:
        print("Bucket 2 not configured")
        return

    print("Chart 2: Submitting births per 1000 women by age group...")

    # Step 1: Read CSV file
    # This CSV is transposed: row 0 has years as columns, rows 1-35 have ages 15-49
    df = read_csv(DATA_DIR / "2-chart-data.csv")

    # Step 2: Extract years from header row
    years = [str(int(y)) for y in df.iloc[0, 1:]]

    # Step 3: Build records with averaged age groups
    # We group 35 individual ages into 7 brackets of 5 years each
    # Using mean() to preserve "per 1000 women" meaning
    records = []
    for i, year in enumerate(years):
        col = i + 1  # Column index (0 is age labels)

        # Calculate average for each 5-year age bracket
        age_15_19 = df.iloc[1:6, col].astype(float).mean()    # Rows 1-5: ages 15-19
        age_20_24 = df.iloc[6:11, col].astype(float).mean()   # Rows 6-10: ages 20-24
        age_25_29 = df.iloc[11:16, col].astype(float).mean()  # Rows 11-15: ages 25-29
        age_30_34 = df.iloc[16:21, col].astype(float).mean()  # Rows 16-20: ages 30-34
        age_35_39 = df.iloc[21:26, col].astype(float).mean()  # Rows 21-25: ages 35-39
        age_40_44 = df.iloc[26:31, col].astype(float).mean()  # Rows 26-30: ages 40-44
        age_45_plus = df.iloc[31:36, col].astype(float).mean() # Rows 31-35: ages 45-49

        records.append({
            "k": year,
            "d": [
                {"sk": 1, "v": float(round(age_15_19, 1))},    # Series 1: 15-19
                {"sk": 2, "v": float(round(age_20_24, 1))},    # Series 2: 20-24
                {"sk": 3, "v": float(round(age_25_29, 1))},    # Series 3: 25-29
                {"sk": 4, "v": float(round(age_30_34, 1))},    # Series 4: 30-34
                {"sk": 5, "v": float(round(age_35_39, 1))},    # Series 5: 35-39
                {"sk": 6, "v": float(round(age_40_44, 1))},    # Series 6: 40-44
                {"sk": 7, "v": float(round(age_45_plus, 1))}   # Series 7: 45+
            ]
        })

    # Step 4: POST records to Dashgrid API
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
      - sk1: Total stillbirths
    """
    if not BUCKET_3_ID:
        print("Bucket 3 not configured")
        return

    print("Chart 3: Submitting stillbirths...")

    # Step 1: Read CSV file
    # This CSV is transposed: row 0 has years, rows 1-16 are the 16 German states
    df = read_csv(DATA_DIR / "3-chart-data.csv")

    # Step 2: Extract years from header row
    years = [str(int(y)) for y in df.iloc[0, 1:]]

    # Step 3: Build records by summing all states for each year
    records = []
    for i, year in enumerate(years):
        col = i + 1  # Column index (0 is state names)
        total = int(df.iloc[1:17, col].astype(int).sum())  # Sum rows 1-16 (all states)
        records.append({
            "k": year,
            "d": [{"sk": 1, "v": total}]  # Series 1: Total stillbirths
        })

    # Step 4: POST records to Dashgrid API
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
    if not BUCKET_4_ID:
        print("Bucket 4 not configured")
        return

    print("Chart 4: Submitting fertility rate...")

    # Step 1: Read CSV file, skip header row
    df = read_csv(DATA_DIR / "4-chart-data.csv", skip_rows=1)

    # Step 2: Build records by averaging the two rate columns
    # The CSV has two fertility rate calculations (ages 15-44 and 15-49)
    # We average them for a single representative value
    records = []
    for _, row in df.iterrows():
        year = str(int(row[0]))
        avg_rate = (float(row[1]) + float(row[2])) / 2  # Average of both columns
        records.append({
            "k": year,
            "d": [{"sk": 1, "v": round(avg_rate, 3)}]  # Series 1: Fertility rate
        })

    # Step 3: POST records to Dashgrid API
    resp = requests.post(
        f"{API_BASE}/api/buckets/{BUCKET_4_ID}",
        json=records,
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"}
    )
    resp.raise_for_status()
    print(f"  Submitted {len(records)} records")


# Run all chart submissions
if __name__ == "__main__":
    submit_chart1()
    submit_chart2()
    submit_chart3()
    submit_chart4()
    print("Done!")
