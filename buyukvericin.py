from pytrends.request import TrendReq
import pandas as pd
import os

pytrends = TrendReq(
    hl="tr-TR",
    tz=180,
    requests_args={
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    }
)

# Marmara Observer kapsamında kullanılacak arama terimleri
kw_list = [
    "deprem",
    "AFAD",
    "toplanma alanı",
    "deprem çantası",
    "DASK"
]

# Google Trends: Türkiye, son 12 ay
pytrends.build_payload(
    kw_list=kw_list,
    timeframe="today 12-m",
    geo="TR"
)

# İl bazlı göreli arama ilgisi
city_df = pytrends.interest_by_region(
    resolution="REGION",
    inc_low_vol=True,
    inc_geo_code=False
)

city_df = city_df.reset_index()
city_df = city_df.rename(columns={"geoName": "city"})

# Sadece Marmara Bölgesi illeri
marmara_cities = [
    "İstanbul",
    "Bursa",
    "Kocaeli",
    "Sakarya",
    "Tekirdağ",
    "Edirne",
    "Kırklareli",
    "Yalova",
    "Balıkesir",
    "Çanakkale",
    "Bilecik"
]

marmara_df = city_df[city_df["city"].isin(marmara_cities)].copy()

# Google Trends gerçek arama sayısı değildir.
# 0-100 arası normalize edilmiş göreli ilgi skorudur.
marmara_df["google_trends_awareness_score"] = (
    marmara_df["deprem"] * 0.30 +
    marmara_df["AFAD"] * 0.20 +
    marmara_df["toplanma alanı"] * 0.20 +
    marmara_df["deprem çantası"] * 0.20 +
    marmara_df["DASK"] * 0.10
)

marmara_df = marmara_df.sort_values(
    by="google_trends_awareness_score",
    ascending=False
)

output_file = "marmara_google_trends_awareness_last_12_months.csv"

marmara_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(marmara_df.to_string(index=False))
print("\nCSV kaydedildi:")
print(os.path.abspath(output_file))