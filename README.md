(c) 2026 by 🛸 Dashgrid.com

# Dashgrid Tutorial: Birth Rates Dashboard
In this tutorial we will create a dashboard 
tracking German birth statistics using Dashgrid.

The data is taken from DESTATIS-GENESIS (Statistisches Bundesamt).
https://www-genesis.destatis.de/

The dashboard will provide the following charts
- Chart 1: Annual Live Births By Sex in Germany.
- Chart 2: Annual Live Births Per 1000 Women in Age Groups in Germany
- Chart 3: Annual Stillborn
- Chart 4: Annual Fertility Rate per Woman


## 1. Prerequisites
- Dashgrid account
- Python 3.10+ installed on yor computer
- [uv](https://github.com/astral-sh/uv) package manager
- Dashgrid account

### Setup

```bash
cd tutorial-birth-rates
uv sync
```

### Configuration

Edit `src/config.py` and set your API key and bucket IDs:

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
