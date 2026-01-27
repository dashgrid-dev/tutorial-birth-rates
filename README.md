(c) 2026 by 🛸 Dashgrid.com

# Birth & Fertility Rates Germany

This repository contains a Python script that submits German birth statistics to Dashgrid dashboards via the Data Buckets API. The data is sourced from DESTATIS-GENESIS (Statistisches Bundesamt).

**Data included:**
- Annual live births by sex (1950-2024)
- Births per 1000 women by age group (1972-2024)
- Annual stillbirths (1990-2024)
- Fertility rate per woman (1972-2024)

**Code structure:**
- `src/main.py` - Main script with functions to read CSV data and submit to API
- `src/helpers.py` - Basic CSV reading utility
- `src/config.py` - API key and bucket IDs configuration
- `src/data/` - CSV data files from DESTATIS

## Requirements
- Python 3.10+ installed on your computer
- [uv](https://github.com/astral-sh/uv) package manager

### Setup
```bash
cd tutorial-birth-rates
uv sync
```

### Configuration
In `src/config.py`:

```python
API_KEY = "dk_your_api_key_here"
BUCKET_1_ID = None  # Annual Live Births By Sex
BUCKET_2_ID = None  # Births per 1000 Women
BUCKET_3_ID = None  # Stillbirths
BUCKET_4_ID = None  # Fertility Rate
```

### Run

```bash
uv run python src/main.py
```